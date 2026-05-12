# XSS via Direct Message deeplinks

## Metadata
- **Source:** HackerOne
- **Report:** 341908 | https://hackerone.com/reports/341908
- **Submitted:** 2018-04-23
- **Reporter:** 0xsobky
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - DOM, Improper Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A specially crafted payload in the 'text' parameter of Twitter's Direct Message deeplink allows injection of arbitrary HTML tags and potentially executable JavaScript code on twitter.com origin. While CSP policies currently block script execution, HTML injection enables secondary attacks such as phishing and deanonymization.

## Attack scenario
1. Attacker crafts a malicious DM deeplink URL with XSS payload encoded in the 'text' parameter
2. Attacker shares the deeplink via tweet or direct message to target users
3. Target user clicks the malicious deeplink, triggering navigation to twitter.com/messages/compose with injected payload
4. The application fails to properly sanitize the 'text' parameter value when rendering the compose form
5. Arbitrary HTML tags (including event handlers like onload) are injected into the DOM on twitter.com origin
6. While CSP blocks inline script execution, injected HTML can be leveraged for phishing, form hijacking, or deanonymization attacks

## Root cause
Insufficient input validation and output encoding of the 'text' parameter in DM deeplinks. The application does not properly sanitize URL-decoded parameter values before rendering them in the DOM, allowing HTML/tag injection despite URL encoding.

## Attacker mindset
An attacker recognizes that deeplink functionality creates a trust vector where users expect legitimacy from twitter.com URLs. By encoding payloads to bypass simple filters, they can inject HTML for phishing, credential theft, or tracking. The discovery of CSP bypassability indicates further exploitation potential.

## Defensive takeaways
- Implement strict input validation for all deeplink parameters, validating content type and format before use
- Apply proper output encoding (HTML entity encoding) when rendering any user-controlled data in DOM contexts
- Decode URL parameters safely and validate at multiple layers (URL decoding, type validation, content sanitization)
- Review CSP policies for potential bypasses and ensure they cover all script injection vectors
- Use templating engines with auto-escaping to prevent unintended HTML injection
- Test deeplink functionality with polyglot XSS payloads and HTML injection techniques during security review
- Implement Content Security Policy as defense-in-depth, not sole mitigation for injection flaws

## Variant hunting
Test other deeplink parameters (recipient_id, welcome_message_id) for similar injection vulnerabilities
Attempt polyglot payloads combining HTML, SVG, and script contexts to bypass sanitization
Investigate CSP bypass techniques using meta tags, link rel attributes, or form-based attacks
Test deeplink functionality across different Twitter clients (web, mobile, TweetDeck) for inconsistent sanitization
Probe for stored XSS if deeplinks are saved or rendered in conversation history
Test encoding variations (double encoding, Unicode escaping, CSS escapes) to evade filters
Research whether injected content persists in message previews or notifications

## MITRE ATT&CK
- T1190
- T1598
- T1583
- T1566

## Notes
Report demonstrates understanding of CSP limitations and indicates researcher was actively developing CSP bypass techniques. The use of polyglot encoding patterns (%3C%3C/%3Cx%3E) suggests sophisticated payload crafting to evade simple tag-based filters. URL was verified as exploitable. The deeplink feature creates a supply-chain trust risk where seemingly legitimate twitter.com URLs can deliver malicious content.

## Full report
<details><summary>Expand</summary>

**Description:** 
By using a specially crafted payload as the value of the text parameter in a Direct Message deeplink, a malicious user can inject arbitrary HTML tags and possibly run arbitrary JavaScript code on the "twitter.com" origin.

## Steps To Reproduce:

  1. Create a Direct Message deeplink by following the instructions on this [Twitter developer guide](https://developer.twitter.com/en/docs/direct-messages/welcome-messages/guides/deeplinking-to-welcome-message).
  2. Use the following payload as the value for the text parameter:
```
%3C%3C/%3Cx%3E/script/test000%3E%3C%3C/%3Cx%3Esvg%20onload%3Dalert%28%29%3E%3C/%3E%3Cscript%3E1%3C%5Cx%3E2
```
  3. Tweet the deeplink you created. It should look like the following:
```
https://twitter.com/messages/compose?recipient_id=988260476659404801&welcome_message_id=988274596427304964&text=%3C%3C/%3Cx%3E/script/test000%3E%3C%3C/%3Cx%3Esvg%20onload%3Dalert%28%29%3E%3C/%3E%3Cscript%3E1%3C%5Cx%3E2
```

## Impact

It seems that the deployed CSP policy currently blocks the execution of arbitrary JavaScript code, however, arbitrary HTML tags can still be injection on `twitter.com` to carry out other kinds of attacks (i.e., deanonymization attacks, phishing, etc.). While you're in the process of verifying this, I'll be working on a bypass for the CSP policy in order to execute arbitrary JavaScript.

The hacker selected the **Cross-site Scripting (XSS) - DOM** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://twitter.com/fvofo0000001444/status/988278372894740480

**Verified**
Yes



</details>

---
*Analysed by Claude on 2026-05-12*
