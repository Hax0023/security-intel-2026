# Stored XSS in Private Messages on m.ok.ru Mobile

## Metadata
- **Source:** HackerOne
- **Report:** 302253 | https://hackerone.com/reports/302253
- **Submitted:** 2018-01-03
- **Reporter:** circuit
- **Program:** Odnoklassniki (OK.ru)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored XSS, Improper Input Sanitization, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the private messaging system of m.ok.ru's mobile version where user input containing HTML/JavaScript is not properly sanitized before rendering. An attacker can inject malicious scripts through the 'Contact Seller' messaging feature in marketplace listings, causing arbitrary JavaScript execution in victims' browsers.

## Attack scenario
1. Attacker creates a marketplace listing in an OK.ru group with a crafted product name or description containing XSS payload like '><img src="x" onerror="alert()">'
2. Attacker clicks 'Contact Seller' button to initiate a private message conversation
3. The XSS payload is stored in the messaging system without proper sanitization
4. When the recipient or any user views the conversation/message thread, the malicious script executes in their browser
5. Attacker can steal session cookies, perform actions on behalf of the victim, or redirect to phishing sites
6. The vulnerability persists as the payload remains stored on the server

## Root cause
The `discus_dialogs_topic` div element displays user-controlled input without HTML entity encoding or Content Security Policy protection. The application fails to escape angle brackets and special characters before rendering them in the DOM.

## Attacker mindset
An attacker operating a marketplace seller account would identify the messaging feature as an entry point. They recognize that the 'Contact Seller' functionality likely passes unsanitized user input directly to the database and frontend, enabling persistent XSS that affects all message viewers.

## Defensive takeaways
- Implement strict input validation and HTML entity encoding (HTML escape) for all user-generated content before rendering
- Use templating engines with auto-escaping enabled by default (e.g., Jinja2, Handlebars with escaping)
- Deploy Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize output using proven libraries (e.g., DOMPurify, OWASP Java HTML Sanitizer)
- Perform security code review focusing on message/comment rendering logic
- Implement automated XSS detection in testing pipelines with payload lists

## Variant hunting
Check other messaging features (group chats, comments, reviews) for similar sanitization failures
Test product titles, descriptions, and seller profiles for XSS injection points
Review other user-generated content rendering areas (posts, wall, notifications)
Attempt SVG-based XSS vectors and event handler variations
Test reflected XSS in search parameters combined with stored XSS in messages

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability is demonstrated with a simple alert() PoC but could be escalated to account takeover via session theft or credential harvesting. The marketplace context increases likelihood of user interaction. The report includes screenshot evidence (referenced attachments F251208-F251216) demonstrating the full exploitation chain. Written in Russian, suggesting the researcher is from CIS region.

## Full report
<details><summary>Expand</summary>

Приветствую.

Нашел багу в личных сообщениях в мобильной версии
{F251208}

Что нужно, чтоб заюзать:

1. Переходим в группу https://m.ok.ru/group/54904397693159/market
2. Ищем товар единственный на страничке
{F251213}
3. Переходим на него и нажимаем на кнопку "Связаться с продавцом" (https://m.ok.ru/group/54904397693159/market)
{F251215}
4. Видим алерт.
{F251216}


Нет фильтрации служебных символов тут -
<div class="discus_dialogs_topic emphased tx-ellip">"&gt;<img src="x" onerror="alert()"></div>

## Impact

XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
