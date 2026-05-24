# Open Redirect Protection Bypass in ExpressionEngine via Referer Header Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 236599 | https://hackerone.com/reports/236599
- **Submitted:** 2017-06-05
- **Reporter:** strukt
- **Program:** ExpressionEngine
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, Insufficient Input Validation, Logic Error
- **CVEs:** None
- **Category:** uncategorised

## Summary
ExpressionEngine's redirect validation mechanism uses PHP's stristr() function to verify that redirect requests originate from the same hostname by checking the Referer header. An attacker can bypass this protection by including the legitimate hostname as a substring within a malicious Referer header value (e.g., http://evil.com?http://www.example.com), causing stristr() to return TRUE and allowing unauthorized redirects to external sites.

## Attack scenario
1. Attacker identifies an ExpressionEngine instance at a target domain
2. Attacker crafts a malicious Referer header containing the target hostname as a substring: 'http://attacker.com?http://target.com'
3. Attacker sends a redirect request with URL parameter pointing to phishing/malware site and the crafted Referer header
4. The stristr() function finds the substring 'target.com' in the Referer value and returns TRUE
5. The redirect validation passes despite the request originating from attacker's domain
6. User is redirected to the attacker-controlled URL, enabling phishing, malware distribution, or credential harvesting

## Root cause
The stristr() function performs a simple substring search without context awareness. It matches the hostname anywhere within the Referer header string rather than validating that the Referer originates from the legitimate domain. The logic fails to account for query parameters or fragments that may contain the hostname as a substring.

## Attacker mindset
An attacker recognizes that substring matching is insufficient for origin validation and exploits the difference between substring containment and actual origin verification. By appending the legitimate hostname to a malicious URL via query parameters, they abuse the loose string matching to bypass referer-based CSRF protections.

## Defensive takeaways
- Use parse_url() to extract and validate the host component of the Referer header rather than substring matching
- Implement strict origin validation: compare parsed hostnames/domains directly, not raw strings
- Validate that Referer header contains the legitimate domain as the actual host, not as a substring in query parameters
- Consider implementing SameSite cookie attributes to provide defense-in-depth against CSRF attacks
- Apply whitelist-based redirect validation rather than relying solely on Referer headers
- Use security libraries or frameworks with built-in redirect protection mechanisms
- Test redirect protections with intentionally malicious Referer headers containing legitimate hostnames as substrings

## Variant hunting
Check other PHP applications using stristr()/strpos() for hostname validation in redirect/CSRF protections
Search for similar substring-based origin validation in other server-side frameworks
Investigate whether other ExpressionEngine modules or custom extensions use similar flawed redirect logic
Test variations: Referer with hostname in fragment (#), port specification, protocol confusion (http vs https)
Look for other authentication bypass mechanisms relying on Referer or Host header substring matching
Audit applications that use string.contains() or similar substring functions for security-sensitive comparisons

## MITRE ATT&CK
- T1190
- T1598
- T1598.002

## Notes
This vulnerability demonstrates the critical importance of parsing and validating HTTP headers correctly rather than using naive string matching. The Referer header is inherently unreliable for security decisions, making this a defense-in-depth failure. The PoC explicitly shows reproducibility at strukt.tk/pocs/eeredirect.html. Organizations using affected ExpressionEngine versions should upgrade immediately and audit other redirect validation logic in their codebase.

## Full report
<details><summary>Expand</summary>

Hello,

When a redirect is to be issue on an ExpressionEngine instance, a request to the following URL is made:
`http://HOST/PATH_TO_EE/index.php?URL=TARGET_URL`
Where `TARGET_URL` is replaced with the actual URL we desire to redirect to. The script `PATH_TO_EE_DIR/system/ee/legacy/libraries/Redirect.php` is the one responsible for making sure that redirects are authorized by checking the value of the Referer header against the hostname where the ExpressionEngine instance is installed. In order to do so, the following code excerpt is performed:

`if ($force_redirect == TRUE OR ( ! isset($_SERVER['HTTP_REFERER']) OR ! stristr($_SERVER['HTTP_REFERER'], $host)))`

Ignoring the very first condition because it is not relevant, and the second because it simply checks if the Referer header is not set in the request, the third condition is the actual problem here. The PHP `stristr` function is used to compare the value of the $host variable, which contains the hostname, to the value of the Referer header. The mentioned function returns TRUE iff the second parameter has been found at least once in the first string parameter, so for example if the actual hostname of the ExpressionEngine instance is http://www.example.com and the Referer header's value is http://evil.com?http://www.example.com, comparing the former and the latter would yield a TRUE return value from the `stristr` function, leaving the check flawed.

I have prepared a live example that shows the issue in action, follow the steps below to reproduce:
1- Visit http://strukt.tk/pocs/eeredirect.html
2- Enter your hostname with the `URL` GET parameter set to whatever external page you desire, the supplied URL should look like `http://HOST/PATH_TO_EE/index.php?URL=https://www.example.com`
3- Click the `Test !!` button and then click the link that will appear below the input box
4- Notice that you have been redirected directly to the supplied value of the `URL` GET parameter rather than being prompted as usual

Regards,

</details>

---
*Analysed by Claude on 2026-05-24*
