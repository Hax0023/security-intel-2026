# Improper Access Control in Nextcloud Social App Message Retrieval

## Metadata
- **Source:** HackerOne
- **Report:** 921717 | https://hackerone.com/reports/921717
- **Submitted:** 2020-07-12
- **Reporter:** sanktjodel
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Authentication, Broken Access Control, Information Disclosure, Insecure Direct Object References (IDOR)
- **CVEs:** CVE-2020-8278
- **Category:** uncategorised

## Summary
The Nextcloud Social App's displayPost function lacks authentication and authorization checks, allowing unauthenticated users to view any message including private direct messages by knowing or guessing the message token. The token is based on Unix timestamp and consists of digits only, making it feasible to brute force or predict. This enables unauthorized disclosure of sensitive user communications.

## Attack scenario
1. Attacker identifies the Nextcloud Social App endpoint pattern: /@{username}/{token}
2. Attacker obtains or observes a target username through public profiles or enumeration
3. Attacker discovers that the token is based on Unix timestamp and attempts to brute force by iterating through plausible timestamp values
4. Attacker crafts HTTP GET request with ActivityPub Accept header to the vulnerable endpoint without authentication
5. Attacker successfully retrieves private direct message content by guessing or brute forcing the token value
6. Attacker gains unauthorized access to sensitive communications between users

## Root cause
The `displayPost` function in ActivityPubController.php lacks both authentication verification and authorization checks before returning message content. The TODO comment in the source code indicates this was a known incomplete implementation. The token generation using Unix timestamp creates a predictable and enumerable identifier space, compounding the severity.

## Attacker mindset
An attacker would recognize this as a trivial IDOR vulnerability with a weak token generation scheme. They would attempt to systematically enumerate message tokens by brute forcing Unix timestamps, potentially accessing conversations at scale. The lack of rate limiting would make this attack highly feasible. Private message disclosure would be particularly valuable for social engineering or blackmail scenarios.

## Defensive takeaways
- Implement mandatory authentication checks before accessing any user-generated content, with explicit user session validation
- Add authorization layer to verify the requesting user has legitimate access to view specific messages (ownership or shared conversation membership)
- Replace predictable timestamp-based tokens with cryptographically secure random identifiers with high entropy
- Implement rate limiting and anomaly detection on message retrieval endpoints to prevent brute force attacks
- Add comprehensive audit logging for all message access attempts
- Conduct code review to identify and resolve all TODO/FIXME comments related to security controls
- Establish secure development lifecycle requiring security review before merging code with known security gaps

## Variant hunting
Search for similar patterns: (1) Other endpoints in ActivityPubController lacking auth checks, (2) Other places using timestamp-based token generation, (3) Other social/messaging features with IDOR patterns, (4) Unauthenticated access to user profile data or metadata, (5) Direct object reference vulnerabilities in file sharing or calendar apps

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1591

## Notes
The vulnerability is particularly serious because: (1) No authentication required at all, (2) Private messages are explicitly compromised, (3) Token space is small enough for brute force, (4) Developer explicitly marked as incomplete with TODO comment, (5) ActivityPub design may have security implications not properly understood by implementers. The fact that a curl request with standard headers can retrieve private messages demonstrates the severity. This is a classic case of security-by-obscurity failing due to weak token generation.

## Full report
<details><summary>Expand</summary>

The Social App (https://apps.nextcloud.com/apps/social) lacks access controls in the `displayPost` function (`/@{username}/{token}`) allowing an unauthenticated user to view any message content by knowing or guessing the message ID.

The vulnerable code is at https://github.com/nextcloud/social/blob/97fb063479d4c0ad6fccdea3774601a619f8a886/lib/Controller/ActivityPubController.php#L367.
Note the TODO comment and the lack of authentication and authorization checks.

The following is a sample curl request to access a direct (private) message (replace the host, username, and the token value):

```
curl -X 'GET' -H 'Accept: application/activity+json' 'http://{nextcloudHost}/apps/social/@{username}/{token}'|jq
```

The `token` value consists of digits only and is based on the unix time.
An attacker would have to know or guess (e.g. brute force) this message ID.

## Impact

An unauthenticated attacker can view any social message, including private (direct) messages from one user to another.
The attacker would have to know or guess the token value.

</details>

---
*Analysed by Claude on 2026-05-24*
