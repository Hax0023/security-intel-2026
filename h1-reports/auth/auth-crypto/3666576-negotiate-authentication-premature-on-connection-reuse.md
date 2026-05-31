# Negotiate Authentication Premature on Connection Reuse

## Metadata
- **Source:** HackerOne
- **Report:** 3666576 | https://hackerone.com/reports/3666576
- **Submitted:** 2026-04-11
- **Reporter:** sdainard
- **Program:** curl
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Credential Leakage, Improper State Management, Information Disclosure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Curl 8.19.0+ inappropriately sends Negotiate/SPNEGO authentication headers on reused keep-alive connections where authentication was already completed. A state synchronization bug introduced in commit ab650379a8 causes fresh empty auth contexts to be created during connection reuse, triggering premature credential transmission. This affects all platforms and can lead to credential leakage through unnecessary Authorization header transmission.

## Attack scenario
1. Attacker establishes first HTTP request to target server using curl with Negotiate authentication enabled
2. Server completes Negotiate/SPNEGO authentication and connection remains open via keep-alive
3. Attacker makes second request to different resource on same connection
4. Due to metadata context being cleared while connection state persists, curl creates fresh empty auth context
5. Curl incorrectly treats new request as new auth attempt and sends Authorization header with Kerberos token
6. Token is transmitted unnecessarily, exposing credentials to network monitoring or MITM attacks

## Root cause
Commit ab650379a8 relocated Negotiate auth context from persistent storage to on-demand metadata storage. During connection reuse, metadata is cleared while connection-level state (`conn->http_negotiate_state = GSS_AUTHSUCC`) persists. When `Curl_auth_nego_get()` is called on reused connection, it creates fresh empty context, breaking synchronization and causing code to treat reused connection as new authentication attempt.

## Attacker mindset
Network eavesdropper seeking to capture Kerberos tickets/tokens from HTTP connections. Attacker leverages connection reuse patterns in curl clients to capture authentication credentials unnecessarily transmitted on second requests, bypassing normal HTTP authentication flow semantics.

## Defensive takeaways
- Implement strict synchronization between connection state machines and authentication context storage - validate consistency across reuse boundaries
- Add explicit auth state validation in connection matching logic before reusing keep-alive connections
- Create comprehensive test coverage for authentication state during connection reuse scenarios, including multi-request sequences
- Implement audit logging for unnecessary credential transmission on authenticated connections
- Consider adding authentication context lifecycle checks at connection pooling layer
- Review all credential-bearing auth schemes (SPNEGO, NTLM, Kerberos) for similar state management issues

## Variant hunting
Check for similar state synchronization issues in other authentication mechanisms (NTLM, OAuth, Digest, Mutual TLS). Review connection pooling logic in other HTTP clients (libcurl bindings, curl clones). Verify that connection state machines properly validate auth context across reuse boundaries. Examine scenarios where metadata storage is cleared but persistent connection state remains.

## MITRE ATT&CK
- T1187 - Forced Authentication
- T1040 - Traffic Sniffing
- T1556 - Modify Authentication Process

## Notes
Report identifies three coordinated issues: (1) test server masking bug preventing test failures visibility; (2) connection reuse regression in ConnectionExists() missing auth state validation; (3) this Negotiate auth credential leakage. Reporter responsibly held Issues #1 and #2 for coordinated disclosure to prevent premature vulnerability exposure. Tests 2077, 2078 fail but were previously masked. Affects curl 8.19.0 and later (released December 2025). All platforms vulnerable. Reporter used AI tools for code analysis verification and documentation, but vulnerability discovery and root cause analysis were manual.

## Full report
<details><summary>Expand</summary>

## Summary:

Curl 8.19.0+ inappropriately sends Negotiate authentication headers on reused keep-alive connections where authentication was already completed. Commit ab650379a8 (June 2025) moved negotiate auth context to on-demand metadata storage, but during connection reuse the metadata gets cleared while the connection-level state (`conn->http_negotiate_state = GSS_AUTHSUCC`) persists. When `Curl_auth_nego_get()` is called on the reused connection, it creates a fresh empty context, causing the code to treat it as a new auth attempt and inappropriately send auth headers containing credentials/tokens. This affects all Negotiate/SPNEGO (Kerberos) authentication with keep-alive connections.

## Affected version

- __Vulnerable__: curl 8.19.0 and later (released December 2025)
- __Last safe version__: < curl 8.19.0
- __Platform__: All platforms (Linux, Windows, macOS, etc.)
- __Breaking commit__: ab650379a8 "vauth: move auth structs to conn meta data" (June 9, 2025)
- __Tests failing__: test 2077, 2078 (masked by separate test server bug - see note below)

## Steps To Reproduce:

1. Build curl 8.19.0 or later with Negotiate/SPNEGO auth support enabled
2. Configure a server requiring Negotiate authentication with keep-alive connections enabled
3. Make first request with Negotiate auth: `curl --negotiate -u : http://server/resource1`
4. On same connection (keep-alive), make second request: `curl --negotiate -u : http://server/resource2`
5. __Expected__: Second request should NOT send Authorization header (auth already done)
6. __Actual__: Second request inappropriately sends "Authorization: Negotiate" header with credentials
7. Alternatively, run curl test suite: `make test` and observe tests 2077, 2078 fail

__Note__: Test failures are currently masked by a separate test server bug in `tests/server/sws.c` (line 2387: `req->connmon = FALSE;`) that prevents proper disconnect logging. This test server issue does not affect the security vulnerability itself, only its visibility in the test suite. Please see summary below.

## Technical Details:

Root cause in `lib/vauth/negotiate.c` - `Curl_auth_nego_get()` creates fresh empty context when metadata lookup fails on reused connections, breaking synchronization with `conn->http_negotiate_state`.  
Detailed analysis and proposed fix available in my  investigation notes.

## Discovery Timeline

a. While applying a CVE patch to curl 8.17.0, test 338 failed, revealing **Issue #2** (connection reuse regression in `lib/url.c`).
b. Investigating curl 8.19.0 revealed **Issue #2** was still present but tests were passing - this exposed **Issue #1** (test server masking the actual bug).
c. Before submitting Issues #1 and #2, performed additional verification to check for other potentially masked tests.
d. This verification revealed **Issue #3** (this report) - the Negotiate auth credential leakage on connection reuse. Now reporting Issue #3 while holding Issues #1 and #2 to prevent premature disclosure that could compromise security investigation.

## Related Issues Found During Investigation

**Issue #1 - Test Server Masking Bug:**
- **File**: `tests/server/sws.c`, line 2387
- **Problem**: Line `req->connmon = FALSE;` disables connection monitoring after first disconnect, preventing subsequent `[DISCONNECT]` markers with `--next` flag
- **Impact**: Masks real connection reuse bugs by making tests appear to pass when they should fail
- **Status**: Fix prepared, holding for coordinated disclosure with Issue #3

**Issue #2 - Connection Reuse Regression:**
- **File**: `lib/url.c`, function `ConnectionExists()`
- **Problem**: Missing Negotiate auth state validation in connection matching logic - connections incorrectly reused when auth states don't match
- **Impact**: Security vulnerability allowing connection reuse with mismatched authentication state
- **Status**: Pull request prepared with fix, holding for coordinated disclosure with Issue #3

Detailed analysis and patches available for both issues.

## AI Usage Disclosure

AI tools were used for code analysis verification, documentation formatting, and report preparation. Vulnerability discovery, root cause analysis, and technical investigation were performed through manual code review and testing.

## Impact

## Summary:

This vulnerability causes inappropriate disclosure of Negotiate authentication credentials on reused HTTP connections. When a curl client reuses a keep-alive connection where Negotiate/SPNEGO authentication was already completed, it incorrectly sends new Authorization headers containing Kerberos tickets/tokens. This can lead to:

1. __Credential leakage__: Authentication tokens sent when not required, potentially exposing them to network monitoring or man-in-the-middle attacks
2. __Cross-resource authentication bypass__: In connection reuse scenarios where connections are repurposed (though rare), auth credentials could be sent to unintended endpoints
3. __Protocol violations__: Violates HTTP authentication state machine by re-authenticating on connections where auth was already successful
4. __Enterprise security impact__: Particularly severe in corporate environments using Kerberos/Active Directory where Negotiate auth is the primary authentication mechanism

</details>

---
*Analysed by Claude on 2026-05-31*
