# Stored XSS in SupportFlow Admin Ticket Table

## Metadata
- **Source:** HackerOne
- **Report:** 145091 | https://hackerone.com/reports/145091
- **Submitted:** 2016-06-16
- **Reporter:** whitehatter
- **Program:** SupportFlow
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Missing Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
SupportFlow contains a stored XSS vulnerability in the admin ticket listing page where ticket messages are rendered without proper escaping. An attacker can inject malicious JavaScript through ticket creation that executes when administrators view the ticket table at /wp-admin/edit.php?post_type=sf_ticket.

## Attack scenario
1. Attacker creates a support ticket with XSS payload in the message field (e.g., <script>alert('XSS');</script>)
2. Payload is stored in the WordPress database without sanitization
3. Administrator navigates to SupportFlow admin panel and views All Tickets table
4. Malicious script executes in the administrator's browser context with admin privileges
5. Attacker can steal admin session cookies, perform admin actions, or inject backdoors
6. Attack persists until ticket is deleted, affecting all admins who view the ticket list

## Root cause
The SupportFlow admin class fails to escape output when rendering ticket messages in the admin table. Line 1175 of class-supportflow-admin.php directly outputs user-controlled ticket data without using WordPress escaping functions (esc_html, esc_attr, wp_kses_post).

## Attacker mindset
Low-effort, high-impact attack requiring only ticket submission capability. Attacker recognizes that admin interfaces often receive less scrutiny than user-facing pages and that stored XSS affecting administrators is particularly valuable for privilege escalation and lateral movement.

## Defensive takeaways
- Always escape output context-appropriately: use esc_html() for HTML content, esc_attr() for attributes, wp_kses_post() for rich HTML
- Apply output escaping at the point of rendering, not at storage
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Sanitize all user inputs on storage with sanitize_text_field() or equivalent
- Audit admin interfaces specifically for XSS as they are high-value targets
- Use WordPress security functions consistently across all output locations
- Implement automated security scanning to detect unescaped output in templates

## Variant hunting
Search for other locations in SupportFlow where ticket data, messages, or user-submitted content is displayed in admin interfaces without escaping. Check email subject lines, customer names, ticket titles, and custom metadata fields. Review other post types and custom admin tables for similar patterns.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a classic WordPress plugin vulnerability pattern. The fix is straightforward: wrap the output variable with appropriate escaping function. Similar vulnerabilities are common in poorly-audited WordPress plugins where developers use direct variable interpolation instead of WordPress escaping functions.

## Full report
<details><summary>Expand</summary>

SupportFlow containers a stored XSS vulnerability in how it generates the admin table of tickets at _SupportFlow -> All Tickets_ (`/wp-admin/edit.php?post_type=sf_ticket`).

Any ticket can be created with an XSS payload like this:

```
<script>alert('XSS');</script>
```

When an admin goes to view the table of tickets, XSS is triggered, because the value is never escaped here:

https://github.com/SupportFlow/supportflow/blob/71a6053848c523f7b50b61a1f3770013badc76c0/classes/class-supportflow-admin.php#L1175

I've attached a screenshot demonstrating the XSS payload - please let me know if there are any questions.

</details>

---
*Analysed by Claude on 2026-05-24*
