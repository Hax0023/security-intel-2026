# Stored XSS via Question Title in Share to Twitter Button on Quora Embed Widget

## Metadata
- **Source:** HackerOne
- **Report:** 258876 | https://hackerone.com/reports/258876
- **Submitted:** 2017-08-11
- **Reporter:** stefanovettorazzi
- **Program:** Quora
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The embed_iframe widget at quora.com/widgets/embed_iframe fails to properly sanitize question titles containing quote characters, allowing attackers to inject JavaScript code into the href attribute of the 'Share to Twitter' button. When a user clicks the Share to Twitter button for a question with a crafted title containing quotes and JavaScript, the injected code executes in their browser.

## Attack scenario
1. Attacker creates a question on Quora with a title containing malicious JavaScript payload wrapped in quotes (e.g., 'Question "-alert(document.domain)-"?')
2. Attacker answers their own question to generate a valid embed_iframe URL for the answer
3. Attacker shares the embed_iframe widget URL (containing path to the malicious answer) with victims via social engineering or publishes it on a website
4. Victim visits the embed_iframe widget and clicks the 'Share' button to reveal sharing options
5. Victim clicks 'Share to Twitter' button, which has malicious JavaScript in its href attribute
6. JavaScript payload executes in victim's browser with their privileges, potentially stealing session tokens, credentials, or performing actions as the victim

## Root cause
The server-side code generates the 'Share to Twitter' button with an href attribute containing unsanitized user input from the question title. The href uses javascript: protocol with the question title concatenated into the Twitter intent URL without proper HTML entity encoding or quote escaping. When the question title contains double quotes, it breaks out of the href string context and injects arbitrary JavaScript.

## Attacker mindset
An attacker would recognize that user-generated content (question titles) are reflected in an iframe widget without proper sanitization. They would test for XSS by using quote characters to escape the href attribute context, allowing JavaScript injection. The stored nature of the vulnerability (persisted in the question title) makes it particularly attractive for widespread exploitation.

## Defensive takeaways
- Always HTML-encode user-controlled data before inserting into HTML attributes, especially special characters like quotes, less-than, and greater-than signs
- Use proper HTML templating libraries that automatically escape output based on context (attribute vs text node vs JavaScript context)
- Validate and sanitize user input server-side, not just client-side, for question titles and other user-generated content
- Avoid using javascript: protocol in href attributes; use proper event handlers (onclick) with URL-encoded parameters instead
- Implement Content Security Policy (CSP) headers to mitigate the impact of XSS vulnerabilities
- Use Security headers like X-XSS-Protection and X-Content-Type-Options
- Perform security code review specifically for widget/embed functionality which may be served across different contexts
- Test iframe widgets with payloads containing special characters, quotes, and JavaScript to identify encoding gaps

## Variant hunting
Test other Quora endpoints for similar href/src attribute injection patterns where user content is reflected without encoding
Check if other embed endpoints (not just embed_iframe) have similar vulnerabilities
Test if answer text, author names, or other metadata fields have similar encoding issues in share buttons
Look for other URLs with 'path' parameters that might reflect unsanitized question/answer data
Check if the vulnerability exists in other languages/subdomains (language.quora.com variants)
Test Share to Facebook, LinkedIn, and other social sharing buttons for similar patterns
Investigate if the vulnerability can be chained with CSRF to force authenticated users to share malicious content
Check if the payload can be delivered via URL parameters instead of just question titles

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (delivery mechanism)
- T1204 - User Execution (requires click)
- T1005 - Data from Local System (potential data exfiltration via XSS)

## Notes
This is a stored XSS vulnerability with medium-to-high impact because it requires user interaction (clicking Share to Twitter) but affects any user who visits the embed widget. The vulnerability is particularly concerning for embed widgets since they are often embedded in third-party sites, potentially affecting users who never directly visit quora.com. The attack surface is broad since any question with a crafted title can be leveraged. The payload `"-alert(document.domain)-"` demonstrates proof of concept by breaking out of the href attribute context. Similar vulnerabilities may exist in other social sharing integrations.

## Full report
<details><summary>Expand</summary>

**Summary:**
The endpoint at `https://{language}.quora.com/widgets/embed_iframe?path={path_to_answer_in_same_language}` shows the answer you specify in _path_ (like `/Question/answer/User`) in a format useful to embed.
There is one button _Share_ that when clicked shows another button _Share to Twitter_. The `href` attribute of this last button is of the format `javascript: window.open(&quot;https://twitter.com/intent/tweet?text=Answer on @Quora by @User to Question? http://qr.ae/nnnn&quot;, &quot;Share Answer to Twitter&quot;, &quot;width=600, height=250&quot;)`.
The problem is that you can create a question with `"` (quotes) and inject Javascript code that is going to be executed when the user clicks _Share to Twitter_.

**Description (Include Impact):**
It requires user interaction, but it works.

### Steps To Reproduce

1. Go to https://www.quora.com/
2. Click on _Ask Question_ 
3. Enter a valid question which includes `"-alert(document.domain)-"` somewhere. I entered `Question ignore "-alert(document.domain)-"?` and it was accepted as valid
4. Now you may be in the page of the question you just asked
5. Click on _Answer_
6. Enter anything
7. Click on _Submit_
8. Copy the path from the address bar. Mine was `/Question-ignore-alert-document-domain/answer/Cuenta-Para-Probar`
9. Go to `https://www.quora.com/widgets/embed_iframe?path={path_from_last_step}`. Mine is https://www.quora.com/widgets/embed_iframe?path=/Question-ignore-alert-document-domain/answer/Cuenta-Para-Probar
10. Click on _Share_
11. Click on _Share to Twitter_
12. `alert(document.domain)` is executed

### Optional: Your Environment (Browser version, Device, app version, os version etc)

 * It is not browser dependent. Anyway, I tested it on Firefox, Chrome and Safari for Mac.

### Optional: Supporting Material/References (Screenshots)

 * I don't think is necessary, but let me know if you need something else.

</details>

---
*Analysed by Claude on 2026-05-12*
