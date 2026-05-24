# Admin Panel Takeover via Authentication Bypass and URL Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 428757 | https://hackerone.com/reports/428757
- **Submitted:** 2018-10-25
- **Reporter:** bigchonk
- **Program:** HackerOne (Report #428757)
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Authorization Bypass, URL Parameter Manipulation, Sensitive Information Disclosure, Path Traversal (attempted)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can bypass authentication and gain unauthorized admin panel access by manipulating URL parameters and the x-urlpath parameter in a JSP-based ITSM application. Once authenticated as admin, the attacker can view sensitive PII including DOD IDs, emails, names, modify tickets, alter user information, and change permissions.

## Attack scenario
1. Attacker navigates to the target application URL with a crafted x-app parameter pointing to 'itsm' and x-urlpath pointing to login.jsp
2. Attacker modifies the x-urlpath parameter to traverse directories (e.g., ../../../../../../../../passwd) to bypass the login mechanism
3. When initial path traversal fails, attacker clicks login which unexpectedly grants full admin panel access
4. Attacker navigates to Applications > Quick Links > AR System Report Console to access the database
5. Attacker runs reports from the console to extract sensitive PII data (DOD IDs, emails, names, phone numbers)
6. Attacker modifies tickets, user information, and permissions across the system without restriction

## Root cause
The application fails to properly validate and sanitize the x-urlpath parameter before processing it. The authentication check appears to be context-dependent and can be bypassed through specific URL parameter combinations. The x-redir parameter chain does not properly enforce authentication gates.

## Attacker mindset
An opportunistic attacker exploiting a simple URL manipulation vulnerability discovered through parameter fuzzing. The attacker realized that authentication could be completely bypassed through parameter manipulation, providing unrestricted access to sensitive government/military data (DOD IDs indicate US Department of Defense systems).

## Defensive takeaways
- Implement server-side session validation on every request, not just initial login
- Use allowlists for URL path parameters rather than blacklists or character filtering
- Enforce authentication checks at the routing/framework level before business logic executes
- Sanitize and validate all URL parameters, especially x-urlpath, x-app, and x-redir
- Implement proper access control checks independent of URL parameters
- Use security frameworks that enforce authentication gates transparently
- Implement audit logging for all admin panel access and data queries
- Regular security testing of parameter combinations and authentication bypass techniques

## Variant hunting
Test other x-* parameters for similar bypass patterns (x-app, x-redir, x-action)
Attempt path traversal on other JSP endpoints beyond login.jsp
Try URL encoding variations of the bypass payload
Test authentication bypass on other BMC Remedy AR System installations
Fuzz parameters with null bytes, double encoding, and unicode variations
Attempt to access other protected resources directly via URL manipulation

## MITRE ATT&CK
- T1190
- T1566
- T1021
- T1078
- T1087
- T1041
- T1552

## Notes
This report involves a US Department of Defense system (indicated by DOD ID references), making it a critical infrastructure security issue. The vulnerability affects multiple attack vectors: authentication bypass, authorization bypass, and sensitive data exposure. The simplicity of the exploit (URL parameter manipulation) suggests this is a fundamental authentication architecture flaw rather than an edge case. The application appears to be BMC Remedy AR System (ITSM) based on the URL structure and component names.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

**Summary:** [add summary of the vulnerability]
I'm able to take over the admin panel, allowing me to viewing the entire ticket database's PII (DOD ID, email, name by changing the URL and bypassing authentication
**Description:** [add more details about this vulnerability]

## Steps To Reproduce:
1: Go to
████████?x-app=itsm&x-urlpath=/arsys/shared/login.jsp&x-redir=%2Farsys%2Fforms%2Fedgelb-itsm-ar%2FRKM%253AKnowledgeArticleManager%2FDisplay%2BView%2F%3Feid%3DKBA000000024701%26cacheid%3Ddf8e1567

2: Change URL to 
█████?x-app=itsm&x-urlpath=../../../../../../../../passwd
3) 
LFI fails, click login
4) Enjoy full admin panel access

5 (Leak PII)
In the left hand corner, applications -> quick links -> AR system report console
Bottom left, click run


## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)
Proof of PII:
██████████

Proof of admin panel:
█████████

## Impact

I can steal users DOD IDs, pretty much anything I want because I'm the websites admin
Change tickets
Change user info
Change permission
Steal PII

</details>

---
*Analysed by Claude on 2026-05-24*
