# Authorization Header Leak in ssrf_filter via Cross-Host Redirect

## Metadata
- **Source:** HackerOne
- **Report:** 3642600 | https://hackerone.com/reports/3642600
- **Submitted:** 2026-04-01
- **Reporter:** argareksapatii
- **Program:** ssrf_filter (Open Source)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Credential Exposure, Improper Header Handling, Cross-Origin Information Disclosure, Insecure Redirect and Forward
- **CVEs:** None
- **Category:** web-api

## Summary
ssrf_filter fails to strip sensitive Authorization headers when following HTTP redirects to different hosts, allowing attackers to steal credentials via redirect-based header forwarding. An attacker controlling a redirect target can capture bearer tokens and replay them against protected APIs to gain unauthorized access.

## Attack scenario
1. Attacker identifies an application using ssrf_filter with bearer token authentication
2. Attacker crafts a URL pointing to their controlled server that returns a 302/301 redirect to a different attacker-controlled collection endpoint
3. Application calls ssrf_filter.get() with Authorization header containing valid bearer token
4. ssrf_filter follows redirect and reconstructs request by reapplying original headers including Authorization
5. Attacker's collection endpoint receives and logs the Authorization header value
6. Attacker replays stolen bearer token against the target API's protected endpoints to access private data

## Root cause
The ssrf_filter redirect handling logic reuses the original request options when following redirects without differentiating between same-host and cross-host targets. The code path rebuilds redirected requests by reapplying caller-supplied sensitive state (headers, body, request_proc) indiscriminately to all redirect destinations, violating the HTTP security principle that sensitive headers should only be sent to the original origin.

## Attacker mindset
An attacker exploiting this vulnerability seeks to harvest authentication credentials through redirect manipulation. The attack is particularly attractive because it requires minimal effort (controlling one server and generating a redirect) to capture reusable tokens that grant full API access. The attacker likely targets applications with valuable protected data accessible via bearer token authentication.

## Defensive takeaways
- Strip sensitive headers (Authorization, Cookie, Proxy-Authorization) when following cross-origin redirects
- Implement strict origin checking: compare original request host with redirect target host before reapplying headers
- Avoid reusing request options directly for redirected requests; rebuild only safe, non-sensitive components
- Log and alert on cross-origin redirects as these may indicate SSRF attack chains or credential leaks
- Consider implementing redirect limits and validating that redirect targets match expected origins
- Document redirect handling behavior clearly for library consumers and default to secure-by-default practices
- Include security tests for cross-origin redirect scenarios in CI/CD pipelines

## Variant hunting
Search for similar patterns in other HTTP client libraries and SSRF filters that follow redirects: check for header reuse in urllib3, requests, httpx, httpclient implementations; audit custom HTTP clients in SSRF mitigation layers; look for redirect handling in API gateways and proxies that may have identical flaws; examine Java HttpClient, Go http.Client, and Python urllib redirect implementations for the same credential leakage pattern.

## MITRE ATT&CK
- T1190
- T1598
- T1557
- T1040
- T1550

## Notes
This is a well-documented vulnerability with a functional PoC demonstrating end-to-end exploitation. The attacker successfully captured a bearer token and replayed it for unauthorized access, meeting the threshold for High severity. The vulnerability affects a widely-used open-source SSRF mitigation library, creating potential supply-chain impact. The fix should differentiate redirect behavior by origin and strip sensitive headers on cross-host redirects while optionally allowing same-host redirect header forwarding.

## Full report
<details><summary>Expand</summary>

## Summary:

`ssrf_filter` follows redirects by rebuilding each redirected request from the original request options. When a redirect crosses to a different host, it still reapplies caller-supplied sensitive state such as the `Authorization` header.

As a result, an attacker-controlled redirect target can receive credentials that were intended only for the original request origin.

I verified impact with a local proof of concept. A bearer token attached to the initial request was forwarded to a different host, captured there, and then successfully replayed against a separate protected API endpoint, which returned private data. This demonstrates credential theft followed by unauthorized access, not just passive header disclosure.

## Steps To Reproduce:

1. Clone the repository and enter the project root:

   ```bash
   git clone https://github.com/arkadiyt/ssrf_filter
   cd ssrf_filter
   ```

2. Run the attached bearer-token replay PoC:

   ```bash
   ruby artifacts/ssrf_filter_redirect_leak_2026-04-01/01_bearer_token_replay.rb
   ```

3. The PoC starts three local servers:
   - redirector.test, which returns a 302 redirect to collector.test
   - collector.test, which records the inbound Authorization header
   - api.test, which exposes /private and only returns data when the correct bearer token is presented

4. Observe that SsrfFilter.get(...) follows the redirect and forwards the original Authorization header to collector.test.

5. Observe that the stolen token is then replayed to api.test/private and succeeds.

Expected output:
```
[:fetch_response, "200", "stolen"]
[:stolen_token, "Bearer service-token-123"]
[:replay_response, "200", "private-data"]
```

Interpretation:
- Authorization is forwarded across an origin change.
- The leaked bearer token is reusable.
- Reuse of the stolen token grants access to protected data.

Note: for local-only reproduction, the PoC temporarily allows loopback addresses so the entire harness can run on one machine. That adjustment is only for the lab setup and is not part of the vulnerability itself. The issue is the forwarding of sensitive credentials across cross-host redirects.

## Supporting Material/References:

* Evidence bundle: ssrf_filter/artifacts/ssrf_filter_redirect_leak_2026-04-01.zip
* Bearer token replay PoC: ssrf_filter/artifacts/ssrf_filter_redirect_leak_2026-04-01/01_bearer_token_replay.rb
* Evidence outputs: ssrf_filter/artifacts/ssrf_filter_redirect_leak_2026-04-01/evidence_outputs.md
* Draft report: ssrf_filter/artifacts/ssrf_filter_redirect_leak_2026-04-01/report_draft.md
* Relevant code path: ssrf_filter/lib/ssrf_filter/ssrf_filter.rb
  - redirect loop reuses the original request options
  - redirected requests reapply headers/body/request_proc
  - redirects are not differentiated between same-host and cross-host targets

</details>

---
*Analysed by Claude on 2026-05-24*
