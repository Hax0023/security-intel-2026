# Impact of Using the PHP Function "phpinfo()" on System Security - PHP info page disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 1822665 | https://hackerone.com/reports/1822665
- **Submitted:** 2023-01-04
- **Reporter:** carpc
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
phpinfo() is a debug functionality that prints out detailed information on both the system and the PHP configuration.
This function can reveal sensitive information such as the exact PHP version, operating system and its version, internal IP addresses, server environment variables, and loaded PHP extensions and their configurations. An attacker can use this information to research know

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

## Summary:
phpinfo() is a debug functionality that prints out detailed information on both the system and the PHP configuration.
This function can reveal sensitive information such as the exact PHP version, operating system and its version, internal IP addresses, server environment variables, and loaded PHP extensions and their configurations. An attacker can use this information to research known vulnerabilities for the system and potentially exploit other vulnerabilities.

## Steps To Reproduce:

  1. Access the address https://rewardsforjustice.net/phpinfo.php 


##Remediation Guidance
To remediate this issue, you should remove the phpinfo() function from your code, or ensure that it is only accessible to trusted individuals. Additionally, you should ensure that your server environment variables are not accessible to unauthorized users.

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * "Secure Configuration Guide for PHP" by the National Institute of Standards and Technology (NIST): https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-42.pdf
* "PHP Security Best Practices" by the Open Web Application Security Project (OWASP): https://www.owasp.org/index.php/PHP_Security_Best_Practices
* "PHP Configuration and Hardening" by the SANS Institute: https://www.sans.edu/security-resources/policies/general/docs/php-configuration-hardening

## Impact

This information can help an attacker gain more information on the system. After gaining detailed information, the attacker can research known vulnerabilities for that system under review. The attacker can also use this information during the exploitation of other vulnerabilities.

</details>

---
*Analysed by Claude on 2026-05-24*
