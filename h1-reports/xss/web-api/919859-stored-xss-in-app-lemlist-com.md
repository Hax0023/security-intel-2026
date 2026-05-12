# Stored XSS in app.lemlist.com Campaign Buddies Feature

## Metadata
- **Source:** HackerOne
- **Report:** 919859 | https://hackerone.com/reports/919859
- **Submitted:** 2020-07-09
- **Reporter:** omarelfarsaoui
- **Program:** Lemlist
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Buddies-to-Be feature of Lemlist's campaign management interface where user-supplied input is not properly sanitized before storage and rendering. An attacker can inject arbitrary JavaScript code that will execute in the browsers of any user viewing the affected campaign, enabling session hijacking and cookie theft.

## Attack scenario
1. Attacker logs into their Lemlist account and creates or edits an existing campaign
2. Attacker navigates to the 'Buddies-to-Be' tab and clicks 'Add one' to create a new buddy entry
3. Attacker injects malicious SVG payload `/><svg src=x onload=confirm(document.domain);>` into the input field
4. Attacker fills in required fields (Icebreaker, companyName) and clicks create
5. Malicious payload is stored in the database without sanitization
6. When any user (victim) views this campaign, the stored XSS payload executes in their browser, allowing cookie theft or session hijacking

## Root cause
The application fails to properly validate and encode user input in the Buddies-to-Be feature before storing it in the database and rendering it in the DOM. The payload breaks out of the intended context and injects executable JavaScript.

## Attacker mindset
An attacker would recognize that campaign management features often handle user-controlled data with minimal validation. By injecting malicious markup into fields meant for text data, they can achieve persistent code execution affecting all users who interact with the campaign, making this a high-impact vector for credential theft and account compromise.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, whitelisting expected characters and formats
- Apply proper output encoding/escaping appropriate to the context (HTML entity encoding for HTML content)
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize and validate data on both client and server-side
- Implement context-aware templating engines that auto-escape by default
- Conduct security code review of all user input handling in campaign management features
- Deploy automated security testing to catch XSS vulnerabilities early

## Variant hunting
Test other campaign management features (sequences, email templates, contact fields) for similar XSS
Check if other fields in Buddies-to-Be feature are vulnerable (Icebreaker, companyName)
Investigate profile fields, team member invitations, and workspace settings for stored XSS
Test DOM-based XSS vectors in dynamic features that load campaign data
Examine API endpoints for reflected XSS in campaign data responses

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1528

## Notes
This is a classic stored XSS vulnerability with clear business impact - attackers could compromise multiple user sessions through a single malicious campaign entry. The proof-of-concept demonstrates successful payload execution using SVG and event handler injection to bypass basic filters. Cookie theft indicates session hijacking was the primary concern, but the vulnerability could enable credential harvesting, malware distribution, or lateral movement within connected systems.

## Full report
<details><summary>Expand</summary>

Hi there,
I found a stored xss [app.lemlist.com](https://app.lemlist.com/).

## Steps To Reproduce:

  1. go to https://app.lemlist.com/.
  1. create or edit **campaigns**.
  1. visit tab **Buddies-to-Be**.
  1. click **Add one** on the right Top.
  1. Fill in the input 
  1. add `/><svg src=x onload=confirm(document.domain);>` ** Icebreaker** and **companyName**
  1. click create .
              
## POC
{F901411}

## Impact

Stealing cookies

</details>

---
*Analysed by Claude on 2026-05-12*
