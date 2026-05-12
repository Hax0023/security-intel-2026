# Reflected/Stored XSS on duckduckgo.com via Urban Dictionary Integration

## Metadata
- **Source:** HackerOne
- **Report:** 1110229 | https://hackerone.com/reports/1110229
- **Submitted:** 2021-02-24
- **Reporter:** monke
- **Program:** DuckDuckGo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Stored XSS, HTML Injection, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected/stored XSS vulnerability was discovered on DuckDuckGo's search results page when searching for content from Urban Dictionary. When a specially crafted payload containing HTML/JavaScript was indexed on Urban Dictionary and subsequently rendered in DuckDuckGo's search results, it executed arbitrary JavaScript in the context of the main DuckDuckGo domain. The vulnerability could be triggered both by performing the search directly or by visiting a malicious URL with the payload in the query parameter.

## Attack scenario
1. Attacker injects malicious JavaScript payload into Urban Dictionary (a third-party site indexed by DuckDuckGo)
2. DuckDuckGo crawls and indexes the content from Urban Dictionary containing the XSS payload
3. Attacker crafts a malicious DuckDuckGo search URL containing the payload (e.g., urban dictionary search with HTML injection)
4. Victim clicks the malicious DuckDuckGo URL or performs the search in DuckDuckGo's search bar
5. DuckDuckGo's search results page renders the indexed content without proper HTML encoding/sanitization
6. Arbitrary JavaScript executes in the victim's browser within the DuckDuckGo domain context, enabling session hijacking, credential theft, or malware distribution

## Root cause
DuckDuckGo failed to properly sanitize or HTML-encode content from indexed third-party websites (Urban Dictionary) before rendering it in search results. The search results page rendered user-controlled content from search parameters and indexed pages without sufficient output encoding, allowing HTML injection and XSS exploitation.

## Attacker mindset
An opportunistic attacker discovered that DuckDuckGo's search results rendering mechanism does not properly encode HTML entities from indexed content. By injecting payloads into commonly indexed websites, attackers can achieve persistent XSS on DuckDuckGo itself, affecting all users who view those search results. The attacker recognized the high-impact nature of compromising a major search engine's domain.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) headers to restrict inline script execution and limit script sources
- Apply HTML entity encoding to all user-controlled and third-party content before rendering in HTML context
- Use templating engines with auto-escaping enabled (e.g., Jinja2, Handlebars) rather than manual string concatenation
- Implement output encoding specific to context (HTML encoding, JavaScript encoding, URL encoding, CSS encoding)
- Sanitize rich HTML content using allowlist-based libraries (DOMPurify, html-sanitizer) if HTML rendering is necessary
- Validate and sanitize search parameters on both client and server side
- Implement subresource integrity (SRI) for any external scripts
- Regularly audit third-party content integration points for proper encoding
- Use security headers: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- Implement automated XSS detection in security testing pipeline

## Variant hunting
Look for similar issues in other search engines' result rendering, auto-complete suggestions, 'Did you mean' features, and knowledge panel integrations. Check Wikipedia integration, instant answers, or other data sources that DuckDuckGo indexes. Investigate whether the vulnerability exists in cached/archived version links, image search results, or news aggregation features.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Search Engine Poisoning variant
- T1204 - User Execution - Malicious Link
- T1566 - Phishing - Spearphishing Link

## Notes
The report demonstrates a critical supply chain security issue where compromising an upstream indexed source (Urban Dictionary) can cascade into attacks on the downstream search engine (DuckDuckGo). The dual nature as both reflected and stored XSS increases severity - reflected via URL parameters, stored via indexed content. The use of image tag with malformed src (img src=x<) is a common XSS filter evasion technique. Report lacks explicit bounty amount, but the vulnerability's severity and impact on a major search engine suggests significant compensation was likely awarded.

## Full report
<details><summary>Expand</summary>

Hi DuckDuckGo,

While browsing normally (since I use DuckDuckGo on a daily basis), I discovered an interesting stored XSS on the duckduckgo main search engine. A payload that somebody had left on urbandictionary.com had triggered a HTML injection, and a stored XSS as a result. 

**Steps to Reproduce**
1. Search the following in the searchbar of DuckDuckGo: `urban dictionary "><img src=x<`
2. A payload left by someone else will render itself and fire in the main DuckDuckGo page.
3. It is also possible to visit the page via the DuckDuckGo URL as [such](https://duckduckgo.com/?q=urban+dictionary+%22%3E%3Cimg+src%3Dx%3C&t=ffab&atb=v1-1&ia=web) and the XSS will trigger.

**POC**
- The page itself renders HTML. The payload fires.
- {F1207848}
- {F1207849}

## Impact

There are several impacts here.
- Firstly, the DuckDuckGo URL serves as a payload, because simply visiting the page with the right search parameter triggers the XSS, although the search parameters themselves do not directly trigger it. 
- Secondly, the XSS is stored in the search results, so this can be considered to be Stored XSS.
- It is possible to execute any Javascript via the main DuckDuckGo page.

If you have any questions or require clarification, I am happy to help.
Cheers,
PMOC

</details>

---
*Analysed by Claude on 2026-05-12*
