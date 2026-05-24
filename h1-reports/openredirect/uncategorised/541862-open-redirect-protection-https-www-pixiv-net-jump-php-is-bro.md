# Open Redirect Protection Bypass in Pixiv Novels via jumpuri Markup

## Metadata
- **Source:** HackerOne
- **Report:** 541862 | https://hackerone.com/reports/541862
- **Submitted:** 2019-04-18
- **Reporter:** katsuragicsl
- **Program:** Pixiv
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Inconsistent Security Implementation, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Pixiv implemented open redirect protection for illustrations using a jump.php redirect handler, but this protection was not consistently applied to novels. Users could embed malicious external URLs in novel content using the [[jumpuri:]] markup syntax that would redirect users while displaying a different URL in the preview.

## Attack scenario
1. Attacker creates a novel on Pixiv with legitimate-looking content
2. Attacker uses the [[jumpuri:display_url > actual_url]] markup to embed a malicious redirect (e.g., [[jumpuri:https://pixiv.net/ > https://attacker-phishing-site.com]])
3. The preview shows the benign display URL (https://pixiv.net/) to appear legitimate
4. Victims click the link in the published novel, trusting it based on the displayed URL
5. The actual redirect target (attacker's phishing site) is executed instead of the displayed URL
6. Attacker can harvest credentials or deliver malware via the phishing destination

## Root cause
The open redirect protection mechanism using jump.php was implemented inconsistently across different content types. While illustrations properly convert external URLs to jump.php redirects, the novel rendering engine failed to apply the same protection when processing the [[jumpuri:]] markup syntax. This suggests separate code paths for rendering illustrations versus novels without unified URL validation.

## Attacker mindset
An attacker would recognize that Pixiv has security awareness (jump.php protection exists) but exploit the inconsistent implementation as a gap. This is an ideal attack vector because: (1) the preview masks the actual destination, (2) users trust content on legitimate platforms, (3) novels allow freeform markup that isn't sanitized identically to other content types, and (4) the attack can be scaled across multiple novels.

## Defensive takeaways
- Implement centralized URL validation and redirect handling - avoid duplicate security logic across content types
- Apply security transformations at the data layer rather than presentation layer to prevent bypasses
- Audit all markup syntax parsers ([[jumpuri:]], etc.) for consistent handling of URLs
- Use allowlists for redirect destinations rather than trying to detect malicious URLs
- Implement consistent content sanitization for all user-submitted content regardless of format
- Add automated tests that verify security mechanisms work across all content types and markup patterns
- Consider removing direct URL embedding capabilities in favor of content moderation and curated links

## Variant hunting
Test other markup syntaxes in novels for similar bypasses ([[jump:]], [[link:]], etc.)
Check if illustrations allow alternative markup that bypasses jump.php conversion
Test novel content in other Pixiv features (galleries, series, collections) for inconsistent redirect handling
Examine other user-controlled content fields (bios, descriptions, comments) for similar markup processing
Test URL encoding variations and alternative schemes (javascript:, data:, etc.) in jumpuri markup
Check if the jump.php handler itself has validation bypasses that could complement this vulnerability

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1557.002 - Adversary-in-the-Middle: ARP Cache Poisoning (if redirecting to credential harvesting)
- T1598 - Phishing (social engineering via trusted platform)

## Notes
This vulnerability demonstrates a common security anti-pattern: implementing controls in multiple places without centralized enforcement. The fact that the jump.php protection was visible in novel previews suggests the developers knew about the security requirement but failed to enforce it in the actual rendering logic. The markup-based nature of the [[jumpuri:]] syntax suggests this may be a custom templating system vulnerable to incomplete security implementation. The report quality is high with clear reproduction steps and evidence of the issue.

## Full report
<details><summary>Expand</summary>

## Summary:

I found that pixiv has a open redirect protection, any external link in illustration is converted to `https://www.pixiv.net/jump.php?<link provided by user>`. For example `https://i3mx4usociis8twimpcu2ty0erkh86.burpcollaborator.net/abc` in `https://www.pixiv.net/member_illust.php?mode=medium&illust_id=74148892` is converted to `https://www.pixiv.net/jump.php?https%3A%2F%2Fi3mx4usociis8twimpcu2ty0erkh86.burpcollaborator.net%2Fabc`. See the attachment "illust.png".

However, that is not true for novels. Links in novel is shown to be converted to `jump.php` link in preview (see attachment "preview.png") but they actually aren't. See `https://www.pixiv.net/novel/show.php?id=109971051` and "novel.png" for an example. 

Since the "jump.php" protection mechanism is working for illusts and the preview of novels, I think lacking this protection for novels is not an intended behavior.

## Steps To Reproduce:

  1. Add a novel
  2. Choose "Add URL" and edit the content to something like `[[jumpuri:https://pixiv.net/ > https://i3mx4usociis8twimpcu2ty0erkh86.burpcollaborator.net/abc]]`
  3. Save
  4. You will see a link in the novel which reads `https://pixiv.net/` but actually it is `https://i3mx4usociis8twimpcu2ty0erkh86.burpcollaborator.net/abc`. See `https://www.pixiv.net/novel/show.php?id=10997105` for your reference.

## Impact

Faking users to the wrong site

</details>

---
*Analysed by Claude on 2026-05-24*
