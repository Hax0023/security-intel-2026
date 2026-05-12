# IE 11 Self-XSS on Jira Integration Preview Base Link

## Metadata
- **Source:** HackerOne
- **Report:** 212721 | https://hackerone.com/reports/212721
- **Submitted:** 2017-03-12
- **Reporter:** ziot
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Cross-Site Scripting (Self-XSS), URL Validation Bypass, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
A Self-XSS vulnerability exists in the Jira Integration configuration page where malicious JavaScript URLs can be injected via the Base URL field. The vulnerability exploits a URL validation bypass using javascript:// protocol that returns a javascript: data URI in the preview response, which executes when clicked in IE 11 where CSP restrictions are not enforced.

## Attack scenario
1. Attacker with admin access to a HackerOne program navigates to Integrations > Jira configuration page
2. Attacker enters a crafted payload (javascript://alert(document.domain);%2f%2f@) in the Base URL input field
3. Attacker submits the form, triggering an AJAX request to /jira_integrations/preview endpoint
4. Server-side validation fails to properly sanitize the javascript:// protocol and returns a response containing a javascript: URI
5. The malicious URL is inserted into an <a href> element and rendered as clickable 'Test escalation URL' link
6. When a user clicks the link in IE 11 (which lacks CSP script-src protection), JavaScript executes in the context of hackerone.com

## Root cause
The backend preview endpoint (/jira_integrations/preview) does not properly validate the Base URL parameter before incorporating it into the generated escalation URL. The validation allows javascript:// protocol bypass, which gets normalized to javascript: in the response. The frontend then directly renders this URL in an href attribute without additional sanitization, and IE 11's lack of CSP enforcement allows script execution.

## Attacker mindset
The researcher identified a URL validation weakness by fuzzing protocol handlers and discovering that javascript:// bypasses the intended restrictions. They recognized that while the preview endpoint has weak validation, the actual save endpoint may have stronger controls. They analyzed the attack surface, threat model mitigations (CSP, CSRF protection, self-XSS nature), and browser-specific vulnerabilities to provide context for severity assessment.

## Defensive takeaways
- Implement strict URL validation using allowlist approach for protocols (http, https only) rather than blocklist/blacklist
- Normalize and validate URLs after decoding to prevent protocol confusion attacks (javascript://, data:, etc.)
- Sanitize all user-controlled data before inserting into href attributes; use URL parsing libraries that reject non-http protocols
- Apply consistent validation rules across preview and save endpoints to prevent inconsistencies that enable bypass
- Ensure Content Security Policy is properly configured and enforced across all supported browsers, not just modern ones
- Implement output encoding for URLs in href context to prevent protocol injection
- Consider using HTMLElement.href property validation instead of string concatenation for URL handling

## Variant hunting
Test other protocol handlers (data:, vbscript:, file:, about:) to identify similar bypass opportunities
Check if similar patterns exist in other integration configuration pages (GitHub, GitLab, Azure, etc.)
Probe whether the actual PUT/save endpoint has identical validation weakness allowing stored XSS
Investigate if CSRF protections can be bypassed through XMLHttpRequest or form submissions
Test whether other user-controlled fields (issue_type, summary, description) have similar injection points
Check for URL validation bypass using variations like javascript%3A, %20javascript:, or mixed-case variants
Examine whether the vulnerability extends to other browsers with CSP support but particular rendering quirks

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a well-documented self-XSS that the researcher appropriately contextualized regarding its limitations. The report demonstrates good security maturity by explaining why it's not a higher severity issue despite the XSS execution: (1) Self-XSS nature requires user interaction, (2) payload is visibly displayed before execution, (3) preview endpoint validation differs from save endpoint, (4) CSRF protection limits attack scope, (5) CSP mitigates in most browsers. The browser-specific nature (IE 11 only) and the researcher's transparent analysis of mitigations shows understanding of practical security impact versus theoretical vulnerability severity.

## Full report
<details><summary>Expand</summary>

I wasn't sure if you would accept this report due to it being Self-XSS, but I figured it might be useful information because it breaks one of the flows used to validate URLs.

Steps
====================

1. Launch IE 11
2. Log into a HackerOne account that has admin on a program.
3. Go to the Automation -> Integrations -> Jira page, e.g.
 * https://hackerone.com/buer_haus/integrations
 * -> https://hackerone.com/buer_haus/integrations/jira/edit
4. Set the Base URL input to the following:
 * `javascript://alert(document.domain);%2f%2f@`
{F168165}
5. Fill in the rest of the required inputs with any data.
6. After the AJAX request is sent to Preview, you'll have generated a `Test escalation URL` link under Section 2 Test Integration.
{F168164}
7. Click the `Test escalation URL` link.
8. ---> You executed a JavaScript alert in a new window displaying the context as hackerone.com
{F168166}


Info
====================

There's a Cross-Site Scripting vulnerability on the program Configure JIRA Integration page. When the user puts a URL into the Base URL input, it sends an AJAX request to `/jira_integrations/preview` and returns with a JSON response containing a URL in `example_escalation_url`. This JSON value gets placed into an <a href> element on the page. It's possible to break the URL validation in a way that it returns with a JavaScript data URI so that it executes JavaScript when a user clicks on the link.

This is relatively low impact because of the following:
 * The JavaScript link text is shown in a preview right above the URL. It's pretty obvious it's a JavaScript link at that point.
 * It breaks the URL validation on the POST preview and not on the actual PUT request to save the URL to the integration page. Maybe there's a way around this, but I couldn't find a way. This makes it a Self-XSS and not Stored.
 * Even if you could get it Stored, it's protected by CSRF so you can't attack other programs. You would have to invite people to your program or attack other users already in your program.
 * The HackerOne CSP rules prevent script-src at `self`. That means this will only execute in browsers that don't support CSP such as IE 11.

Request/Response
====================
URL https://hackerone.com/buer_haus/jira_integrations/preview
POST 
```
pid=123&issue_type=1&base_url=javascript://alert(1)%3B@&summary={{title}}&description={{details_truncated}}+{{1+1}}+#{1+1}&labels=HackerOne&assignee=&custom=test=1
```

Response:
```
{"preview":{"example_escalation_url":"javascript:alert(1);@/secure/CreateIssueDetails!init.jspa?assignee=\u0026description=%7B%7Bdetails_truncated%7D%7D+%7B%7B1+1%7D%7D+%23%7B1+1%7D\u0026issuetype=1\u0026labels=HackerOne\u0026pid=123\u0026summary=%7B%7Btitle%7D%7D\u0026test=1"}}
```

Source
====================
```<a href="javascript:alert(document.domain);%2f%2f@/secure/CreateIssueDetails!init.jspa?assignee=&amp;description=%7B%7Bdetails_truncated%7D%7D+%7B%7B1%2B1%7D%7D+%23%7B1%2B1%7D&amp;issuetype=1&amp;labels=HackerOne&amp;pid=123&amp;summary=%7B%7Btitle%7D%7D&amp;test=1" target="_blank"><!-- react-text: 82 -->Test escalation URL<!-- /react-text --><!-- react-text: 83 --> <!-- /react-text --><i class="icon-external-link"></i></a>```

</details>

---
*Analysed by Claude on 2026-05-12*
