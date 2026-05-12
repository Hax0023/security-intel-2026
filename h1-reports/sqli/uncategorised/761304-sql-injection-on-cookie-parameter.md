# SQL Injection on Cookie Parameter (lang)

## Metadata
- **Source:** HackerOne
- **Report:** 761304 | https://hackerone.com/reports/761304
- **Submitted:** 2019-12-18
- **Reporter:** w31rd0
- **Program:** MTN Yemen
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** SQL Injection, Cookie-based SQL Injection, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The 'lang' cookie parameter in the search endpoint is vulnerable to SQL injection, allowing attackers to manipulate SQL queries through improperly sanitized cookie input. The vulnerability was confirmed by injecting single quotes that produced SQL syntax errors, demonstrating the application directly concatenates user input into SQL statements without proper parameterization.

## Attack scenario
1. Attacker identifies the vulnerable 'lang' cookie parameter in GET /index.php/search/default endpoint
2. Attacker injects a single quote (') in the lang cookie value to trigger SQL syntax error
3. Application returns SQL error message confirming the injection point and query structure
4. Attacker injects a second quote to balance the SQL statement and remove error messages
5. Attacker can now craft UNION-based or time-based blind SQL injection payloads to extract data
6. Attacker exfiltrates sensitive database information such as user credentials, personal data, or other confidential records

## Root cause
The application fails to use prepared statements or parameterized queries when processing the 'lang' cookie parameter. Instead, it directly concatenates the unsanitized cookie value into the SQL query string, allowing attackers to break out of the intended query context and execute arbitrary SQL commands.

## Attacker mindset
The researcher demonstrates responsible disclosure by identifying the vulnerability but explicitly stating they did not attempt data exfiltration. However, an attacker would recognize this as a critical flaw allowing complete database compromise, potentially accessing customer data, authentication credentials, and business-sensitive information. The cookie-based vector is particularly attractive as it may bypass traditional input validation focused on URL parameters.

## Defensive takeaways
- Always use prepared statements or parameterized queries for all database interactions, regardless of input source (URL, cookies, headers, body)
- Implement strict input validation on all cookie parameters with whitelist-based validation (e.g., lang parameter should only accept specific language codes)
- Disable database error messages in production environments to prevent information disclosure about query structure
- Apply Web Application Firewall (WAF) rules to detect and block SQL injection patterns in cookies
- Conduct regular security code reviews focusing on all data sources (parameters, cookies, headers), not just obvious input vectors
- Implement least-privilege database accounts with minimal required permissions to limit damage from SQLi exploitation
- Use ORM frameworks that enforce parameterization by default

## Variant hunting
Search for other cookie parameters that may be used in SQL queries (user preferences, tracking IDs, authentication tokens). Examine similar applications in the same organization that may use identical vulnerable code patterns. Test other endpoints that accept cookies and perform database operations. Look for other parameters vulnerable to similar injection attacks (HTTP headers, referer, user-agent) that may be logged to database.

## MITRE ATT&CK
- T1190
- T1526
- T1110

## Notes
The researcher responsibly requested permission before further exploitation. The vulnerability is confirmed through error-based SQL injection (single quote causing syntax error, double quote balancing the statement). The 'lang' parameter is a common vector as developers often assume cookies are trusted input. This demonstrates the importance of treating ALL input sources as untrusted. The vulnerability affects mtn.com.ye (MTN Yemen's main website), suggesting potential access to customer data and business systems.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello team. It seams one of the parameters in the cookies is vulnerable to SQL injection. Below requests has the lang parameter in cookies. If you inject one quote mark like '. You get SQL error with the syntax. By injecting a second you have the error removed.
I did not attempt to exfiltrate data as this is obvious indication of SQLi.

```
GET /index.php/search/default?t=1&x=0&y=0 HTTP/1.1
Host: mtn.com.ye
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=86ce3d04baa357ffcacf5d013679b696; lang=en'; _ga=GA1.3.1859249834.1576704214; _gid=GA1.3.1031541111.1576704214; _gat=1; _gat_UA-44336198-10=1
Upgrade-Insecure-Requests: 1
```

I would like to ask for permission for further exploiting this issue.

## Impact

Web application is vulnerable to SQL injection, allowing access to data

</details>

---
*Analysed by Claude on 2026-05-11*
