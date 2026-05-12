# Stored XSS in Search via Class Attribute Abuse to Impersonate Login Interface

## Metadata
- **Source:** HackerOne
- **Report:** 351376 | https://hackerone.com/reports/351376
- **Submitted:** 2018-05-14
- **Reporter:** kiyell
- **Program:** Reverb.com
- **Bounty:** Undisclosed
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), HTML Injection, Stored XSS, Phishing
- **CVEs:** None
- **Category:** web-api

## Summary
The search functionality fails to properly sanitize HTML tags and class attributes, allowing attackers to inject arbitrary HTML that renders with legitimate Reverb.com CSS classes. An attacker can craft a search query containing HTML elements styled with authentic Reverb classes to create a convincing fake login dialog overlaying page content, enabling phishing attacks against users.

## Attack scenario
1. Attacker crafts malicious search query containing HTML markup with legitimate Reverb CSS classes (e.g., 'fancybox-opened', 'dialog', 'button--orange')
2. Attacker shares crafted URL via email, social media, or other channels to potential victims
3. Victim clicks link and is taken to Reverb.com search results page
4. Injected HTML renders with authentic Reverb styling, displaying convincing fake login overlay claiming account is locked
5. Victim enters credentials or clicks phishing link believing they're performing legitimate account recovery
6. Attacker captures credentials or redirects victim to credential harvesting site

## Root cause
Insufficient input validation and output encoding in search functionality. The application fails to sanitize HTML tags and specifically does not prevent use of class attributes that map to existing CSS styles. No content security policy or strict HTML filtering prevents arbitrary tag injection.

## Attacker mindset
Attacker recognizes that legitimate-looking UI elements are more effective for phishing than obviously malicious content. By leveraging existing CSS classes, they bypass typical defenses that might filter dangerous attributes while maintaining visual authenticity. This requires minimal technical sophistication but high effectiveness.

## Defensive takeaways
- Implement strict input validation on all user-controlled search parameters; whitelist only safe characters
- Use HTML entity encoding (not just tag stripping) for all user input in search queries before output
- Implement Content Security Policy (CSP) headers to restrict inline styles and script execution
- Apply output encoding appropriate to context (HTML context requires HTML entity encoding)
- Sanitize HTML using proven libraries (e.g., DOMPurify, OWASP HTML Sanitizer) that strip both tags and attributes
- Disable or heavily restrict the class attribute in user-controlled input contexts
- Implement server-side rendering validation to ensure output matches expected safe formats
- Use templating engines that auto-escape by default rather than manual concatenation
- Conduct security testing specifically for CSS-based UI spoofing attacks

## Variant hunting
Test other user input fields (product names, descriptions, comments) for similar class attribute injection
Attempt to inject other HTML elements with styling attributes (style=, data-* attributes)
Try injecting classes that trigger modal overlays or redirect functionality
Test whether SVG or other XML-based markup can bypass filters
Attempt to inject legitimate Reverb CSS class names for other UI components (payment forms, admin panels)
Check if attribute values can be manipulated through encoding bypasses (unicode, HTML entities in attributes)
Test if JavaScript event handlers can be injected via attributes like onclick disguised with legitimate classes

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1187

## Notes
This is a follow-up to report #349684 showing that while initial XSS filtering may block obvious payloads, insufficient sanitization of attributes allows sophisticated UI spoofing. The attacker's creativity comment and phishing focus indicate this could enable large-scale credential theft campaigns. The PoC demonstrates that legitimate CSS framework classes can be weaponized. Given Reverb's marketplace nature with financial transactions, this poses significant risk to user account compromise and fraud.

## Full report
<details><summary>Expand</summary>

This is an expansion of #349684 which was flagged as a duplicate. In that bug report I explained that several HTML tags end up rendering when entered into the main search. I've since found out that the class attribute of multiple types of tags can be modified to create a realistic imitation of core functionality on the Reverb website.

Example: <a href="http://badwebsite.com"><span class="btn button button--orange button--wide">XSS</a></span>

In the following PoC, I used tags such as <span>, <div>, <a>, and <li> in combinations with the "class" attribute to create a prominent login box (which fades out all content underneath it) that explains that their account has been locked and to click a link in order to unlock it.


Please forgive me if this is still considered a low risk and just "Informative"

PoC: https://sandbox.reverb.com/marketplace?query=%3Cspan%20class%3D%22fotorama--fullscreen%20fancybox-mobile%20fancybox-type-html%20fancybox-opened%22%20%3E%3Cdiv%20class%3D%22fancybox-skin%22%3E%3Cdiv%20class%3D%22fancybox-inner%22%3E%3Cdiv%20class%3D%22%20registration%20tabbable%20dialog%20signup-login-container%20mlr-auto%22%3E%3Cul%20class%3D%22nav-tabs%20fluid-row%22%3E%3Cli%20class%3D%22col-6%22%3E%3Ca%20class%3D%22%22%20href%3D%22%23registration-form%22%3ECreate%20Account%3Ca%3E%3C%2Fli%3E%3Cli%20class%3D%22col-6%22%3E%3Ca%20class%3D%22active%22%20href%3D%22%23login-form%22%3ESign%20in%3Ca%3E%3C%2Fli%3E%3C%2Ful%3E%3Cdiv%20class%3D%22tab-content%20pt-1%22%3E%20%20%3Ch4%20class%3D%22session-form__header%22%3ELog%20In%20to%20Reverb%3C%2Fh4%3E%3Ch1%3EYour%20account%20has%20been%20disabled%3C%2Fh1%3E%3Cbr%3E%20%3Ccode%3EDue%20to%20multiple%20unsuccessful%20attempts%20to%20login%20to%20your%20account.%20Your%20account%20has%20been%20locked%20for%20your%20protection.%20Please%20click%20below%20to%20unlock%20it%3C%2Fcode%3E%3Cbr%3E%3Cbr%3E%3Cbr%3E%20%3Ca%20href%3D%22http%3A%2F%2Fbadwebsite.com%22%3E%3Cspan%20class%3D%22btn%20button%20button--orange%20button--wide%22%3EUnlock%3C%2Fa%3E%20%3Cp%20class%3D%22center%20small%20mt-1%22%3EForgot%20your%20password%3F%20%3Ca%20href%3D%22http%3A%2F%2Fbadwebsite.com%22%3EReset%20it%3C%2Fa%3E%20%3C%2Fp%3E%20%3Chr%20class%3D%22class%3D%22mtb-1%22%3E%20%3Ca%20class%3D%22session-form__facebook-link%22%20href%3D%22http%3A%2F%2Fbadwebsite.com%22%3E%3Cspan%20class%3D%22fa%20fa-facebook%22%3E%3C%2Fspan%3E%20Log%20In%20with%20Facebook%3C%2Fa%3E%3Cbr%3E%20%3C%2Fdiv%3E%3C%2Fspan%3E%3C%2Fspan%3E%3Cbr%3E

## Impact

A malicious user with more creativity than me could likely duplicate the appearance of other core pieces of the Reverb.com website in order to phish for user account information.

</details>

---
*Analysed by Claude on 2026-05-12*
