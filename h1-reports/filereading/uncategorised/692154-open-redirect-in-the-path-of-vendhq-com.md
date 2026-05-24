# Open Redirect in vendhq.com Path

## Metadata
- **Source:** HackerOne
- **Report:** 692154 | https://hackerone.com/reports/692154
- **Submitted:** 2019-09-11
- **Reporter:** zoidsec
- **Program:** Vend
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in vendhq.com that allows attackers to redirect users to arbitrary external domains by injecting a double-slash bypass (//evil.com/) into the URL path. This enables credential harvesting and malware distribution attacks by leveraging the trusted domain for phishing.

## Attack scenario
1. Attacker crafts a malicious URL: https://www.vendhq.com//attacker.com/phishing-page
2. Attacker distributes the URL via email, social media, or chat to target users
3. Victim clicks the link believing it's legitimate (trusts vendhq.com domain)
4. Browser processes the double-slash bypass and redirects to attacker.com
5. Victim lands on attacker-controlled phishing page or malware distribution site
6. Attacker harvests credentials, distributes ransomware, or performs other malicious actions

## Root cause
The redirect validation logic fails to properly sanitize or validate redirect destinations. The double-slash (//evil.com/) is interpreted as a protocol-relative URL instead of a path component, bypassing basic validation checks that may only block single-slash redirects.

## Attacker mindset
An attacker leverages the trust users place in vendhq.com's domain to conduct phishing campaigns and distribute malware with higher success rates. The bypass technique (double-slash) is simple to discover and implement, making this an easy attack vector for social engineering campaigns targeting Vend users.

## Defensive takeaways
- Implement whitelist-based redirect validation; only allow redirects to pre-approved domains
- Validate redirect URLs against a strict pattern that requires full URL parsing, not simple string matching
- Use URL parsing libraries rather than regex to properly handle protocol-relative URLs and edge cases
- Enforce absolute URL validation with explicit protocol checks (http:// or https://)
- Implement Content Security Policy (CSP) with frame-ancestors and redirect directives
- Log and monitor redirect attempts for suspicious patterns
- Educate users to verify URLs in the address bar before trusting the destination

## Variant hunting
Test triple-slash variants: ///evil.com/
Test backslash bypasses: https://www.vendhq.com\\evil.com/
Test mixed protocols: https://www.vendhq.com//http://evil.com/
Test URL encoding: https://www.vendhq.com/%2F%2Fevil.com/
Test data URIs: https://www.vendhq.com/data:text/html,<script>window.location='http://evil.com'</script>
Test javascript protocol: https://www.vendhq.com/javascript:window.location='http://evil.com'
Test relative path redirects in other endpoints/parameters
Test redirect parameters in login, logout, callback, and return_to parameters

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1598.001

## Notes
This is a straightforward open redirect vulnerability with a simple bypass technique. The impact is significant for phishing campaigns but the severity is rated medium rather than high because it requires user interaction and the vulnerability is visible in the URL. The double-slash bypass is a well-known technique in the security community. No bounce/confirmation details provided in the original report.

## Full report
<details><summary>Expand</summary>

**Summary:** 
There is an open redirection vulnerability in the path of 
```
https://www.vendhq.com/
```

**Description:**
An attacker can redirect anyone to malicious sites.

## Steps To Reproduce:

Type in this URL:

```
https://www.vendhq.com//evil.com/
```

As, you can see it redirects to that website when you inject this payload:
 ```
//evil.com/
```

evil.com was used as an example but this could be any website note, the `//` is the bypass.



## Supporting Material/References:

  * https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html

## Impact

* Attackers can serve malicious websites that steal passwords or download ransomware to their victims machine due to a redirect and there are a heap of other attack vectors.

</details>

---
*Analysed by Claude on 2026-05-24*
