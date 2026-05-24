# WordPress Unauthorized Password Reset via Compromised SERVER_NAME Variable

## Metadata
- **Source:** HackerOne
- **Report:** 226037 | https://hackerone.com/reports/226037
- **Submitted:** 2017-05-04
- **Reporter:** japz
- **Program:** Nextcloud (reported as WordPress core issue affecting Nextcloud)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Input Validation, Authentication Bypass, Password Reset Vulnerability, Host Header Injection
- **CVEs:** CVE-2017-8295
- **Category:** uncategorised

## Summary
WordPress versions up to 4.7.4 contain a vulnerability in the password reset functionality that allows attackers to intercept or generate valid password reset links without authentication by manipulating the SERVER_NAME variable. An attacker could exploit this to gain unauthorized access to victim accounts by redirecting password reset emails to attacker-controlled domains.

## Attack scenario
1. Attacker crafts a malicious request with a manipulated Host header or SERVER_NAME parameter targeting a vulnerable WordPress installation
2. The password reset function generates a password reset link using the compromised SERVER_NAME value
3. Attacker tricks a victim into requesting a password reset for their account
4. The password reset email is sent containing a link pointing to the attacker's domain instead of the legitimate site
5. Victim clicks the attacker-controlled link, revealing the password reset token
6. Attacker uses the captured token to reset the victim's password and gain account access

## Root cause
WordPress password reset functionality improperly validates or sanitizes the SERVER_NAME variable, allowing it to be influenced by Host headers or other request parameters without sufficient canonicalization checks. The reset link generation uses this unsanitized value to construct URLs in password reset emails.

## Attacker mindset
Low-effort account takeover targeting WordPress installations. Attacker recognizes that password reset mechanisms are often overlooked in security reviews and that host header manipulation is frequently under-protected. The attack requires minimal technical skill and no prior authentication.

## Defensive takeaways
- Enable UseCanonicalName or equivalent configuration to enforce static SERVER_NAME values in web server configuration
- Validate and sanitize all host/domain references before using them in security-sensitive operations like password reset links
- Implement strict whitelist validation of Host headers against configured domain values
- Use hard-coded domain values for password reset link generation rather than deriving from request headers
- Apply WordPress security patches immediately upon release
- Implement Content Security Policy headers to prevent redirect attacks
- Log and monitor unusual Host header values in password reset requests
- Consider implementing additional verification steps in password reset workflow (e.g., verification codes sent to registered email)

## Variant hunting
Hunt for similar Host header injection vulnerabilities in: (1) other authentication-related endpoints beyond password reset, (2) email notification functions that construct URLs, (3) social login providers that may use callback URLs, (4) two-factor authentication setup workflows, (5) any generated links included in transactional emails

## MITRE ATT&CK
- T1190
- T1598
- T1621
- T1556

## Notes
This appears to be CVE-2017-8295. The report is a responsible disclosure informing Nextcloud of a WordPress core vulnerability affecting their infrastructure. The reporter suggests temporary mitigation (UseCanonicalName) while waiting for official patches. This is a classic Host header injection vulnerability pattern that affects many web frameworks - the lesson applies broadly beyond WordPress.

## Full report
<details><summary>Expand</summary>

Hi Team,

Yesterday, a new 0day on wordpress core has been discovered by Dawid Golunski, so i want you guys to be aware of it to take an immediate action since nextcloud was using wordpress.

>Wordpress has a password reset feature that contains a vulnerability which
might in some cases allow attackers to get hold of the password reset link
without previous authentication. 
Such attack could lead to an attacker gaining unauthorised access to a 
victim's WordPress account.

Affected WP version is up to the latest one `4.7.4` , so while waiting for the release of the new version that will fix the issue, you may want to apply a temporary solution, enable `UseCanonicalName` to enforce static SERVER_NAME value.

You can see the full details of the issue on this URL: https://exploitbox.io/vuln/WordPress-Exploit-4-7-Unauth-Password-Reset-0day-CVE-2017-8295.html

Regards
Japz

</details>

---
*Analysed by Claude on 2026-05-24*
