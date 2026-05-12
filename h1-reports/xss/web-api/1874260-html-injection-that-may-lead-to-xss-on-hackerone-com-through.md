# HTML Injection Leading to XSS in H1 Triage Wizard Chrome Extension

## Metadata
- **Source:** HackerOne
- **Report:** 1874260 | https://hackerone.com/reports/1874260
- **Submitted:** 2023-02-14
- **Reporter:** jobert
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** HTML Injection, Cross-Site Scripting (XSS), Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The H1 Triage Wizard Chrome extension contains an HTML injection vulnerability where unsanitized questionnaire responses are directly interpolated into DOM elements via innerHTML. An attacker can inject malicious HTML/JavaScript payloads through the triage questionnaire responses, which are then executed in the context of the HackerOne.com domain.

## Attack scenario
1. Attacker submits a security report to HackerOne with malicious JavaScript embedded in one of the questionnaire response fields
2. The malicious payload is stored in HackerOne's backend associated with the report
3. A user with the H1 Triage Wizard extension visits the report page with a specific URL structure
4. User right-clicks and selects 'View Triage Questionnaire (Beta)' from the context menu
5. The extension retrieves stored questionnaire responses from the backend without sanitization
6. The buildTriageQuestionnaireModal function directly injects responses using innerHTML, executing the embedded JavaScript payload

## Root cause
Unsafe use of innerHTML with unsanitized user-controlled data. The code performs string replacement on questionnaire responses without HTML entity encoding or sanitization before inserting them into the DOM. This allows arbitrary HTML and JavaScript to be injected and executed.

## Attacker mindset
An attacker would identify that triage questionnaire responses are user-controllable fields that persist in the database. By injecting script tags or event handlers into these fields, the payload executes whenever a user views the triage questionnaire through the extension, potentially stealing session tokens, exfiltrating report contents, or performing actions on behalf of the user.

## Defensive takeaways
- Never use innerHTML with user-controlled data; use textContent or createTextNode for text content
- Always HTML-encode/escape user input before inserting into DOM, or use safer APIs like innerText
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Sanitize all user-provided data on both input validation and output encoding
- Use templating engines that auto-escape by default rather than manual string replacement
- Apply principle of least privilege to Chrome extension permissions
- Implement security review processes for extension code handling sensitive data

## Variant hunting
Check other .replace() calls in the extension for similar unsafe patterns with user input
Search for other uses of innerHTML throughout the extension codebase
Audit all questionnaire fields to identify which ones accept user input
Test other context menu options and UI interactions for similar injection points
Examine how the extension handles data from other HackerOne API endpoints
Verify if the vulnerability exists in other H1 extensions or integrations

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
The vulnerability affects users who have installed the H1 Triage Wizard extension and can be exploited by any report submitter. The extension's access to HackerOne.com DOM and ability to execute scripts makes this particularly dangerous for compromising researcher sessions or stealing confidential report information. The issue demonstrates the risks of browser extensions with elevated DOM access privileges.

## Full report
<details><summary>Expand</summary>

To reproduce:

* ensure you have the H1 Triage Wizard Chrome extension enabled
* visit https://hackerone.com/reports/1622449?subject=security&/bugs=1
* right-click the report, select "View Triage Questionnaire (Beta)"
* observe an HTML payload being injected

{F2173699}

The payload is stored in █████████. The contents of this file are dynamically loaded through the Chrome extension.

The vulnerability is caused by the following code in the `triage-extension-private` repository:

```js
buildTriageQuestionnaireModal = (
  modalElement,
  triageQuestionnaireModalOptions
) => {
  let questionnaireResponses =
    triageQuestionnaireModalOptions.questionnaireResponses;
  if (questionnaireResponses) {
    modalElement.innerHTML = triageQuestionnaireHTML
      .replace("{{handle}}", triageQuestionnaireModalOptions.handle) // <-- the handle here is taken from the subject parameter (i.e. "security")
      .replace("{{1}}", questionnaireResponses[1]) // <-- the response to the questionnaire is interpolated without sanitizing it
      .replace("{{2}}", questionnaireResponses[2]) // <-- this applies to all of these
      .replace("{{3}}", questionnaireResponses[3])
// ...
```

## Impact

This vulnerability may lead to compromising confidential information or impact its integrity.

</details>

---
*Analysed by Claude on 2026-05-12*
