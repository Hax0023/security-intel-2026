# Chained Open Redirects and Ideographic Full Stop Bypass Twitter's Link Blocking

## Metadata
- **Source:** HackerOne
- **Report:** 1032610 | https://hackerone.com/reports/1032610
- **Submitted:** 2020-11-12
- **Reporter:** jub0bs
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Open Redirect, Unicode Encoding Bypass, Access Control Bypass, Security Filter Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can bypass Twitter's domain deny list by chaining two open redirects (twitter.com and analytics.twitter.com) combined with replacing ASCII periods with Ideographic Full Stop Unicode characters. This allows posting links to blocked domains like ddosecrets.com that would normally be rejected by Twitter's link validation system.

## Attack scenario
1. Attacker identifies target blocked domain (e.g., ddosecrets.com) on Twitter's deny list
2. Attacker crafts malicious URL by replacing ASCII periods with Ideographic Full Stop (%E3%80%82) to evade string matching validation
3. Attacker chains the URL through analytics.twitter.com redirect endpoint with 'rd' parameter containing the disguised malicious URL
4. Attacker wraps the analytics.twitter.com redirect in twitter.com/login redirect_after_login parameter for additional obfuscation
5. Attacker posts the final chained redirect URL in a tweet, passing Twitter's backend link validation
6. When users click the link, they are redirected through twitter.com → analytics.twitter.com → blocked domain without interstitial warning

## Root cause
Twitter's link validation system has multiple implementation flaws: (1) insufficient validation of redirect chains through trusted Twitter subdomains, (2) failure to normalize Unicode characters (specifically Ideographic Full Stop) that are semantically equivalent to ASCII periods before validation, (3) lack of recursive validation of redirect targets, and (4) trust in analytics.twitter.com and login endpoints as safe redirect vectors without proper constraint on redirect destinations.

## Attacker mindset
Sophisticated attacker seeking to distribute links to politically sensitive or malicious content (ddosecrets.com) while evading Twitter's safety controls. The attacker demonstrates deep knowledge of URL encoding, Unicode semantics, and Twitter's architecture to find creative bypass techniques. Motivation likely involves circumventing content moderation and distributing sensitive/harmful content at scale.

## Defensive takeaways
- Implement Unicode normalization (NFKC/NFKD) on all URLs and domain names before applying validation rules
- Maintain allow-list approach for redirect endpoints rather than allowing arbitrary redirects from trusted domains
- Apply recursive validation to redirect chain destinations, not just initial URL
- Implement strict domain validation that checks the actual resolved domain, not string representations
- Use URL parsing libraries that handle edge cases and Unicode variants correctly
- Add interstitial warning pages for redirects leaving Twitter domain, even from trusted internal endpoints
- Audit analytics and authentication endpoints for open redirect vulnerabilities
- Implement Content Security Policy to restrict redirect destinations
- Perform security testing with Unicode variants and encoding bypasses

## Variant hunting
Test other Unicode characters that may be normalized to ASCII period (U+002E): Fullwidth Full Stop (U+FF0E), One Dot Leader (U+2024), Hyphenation Point (U+2010)
Chain multiple redirect endpoints together (3+ hops) to further obfuscate redirect path
Test alternative redirect parameters on analytics.twitter.com and other Twitter subdomains
Attempt to bypass using percent-encoding at different nesting levels
Test double-encoding and alternative encoding schemes (UTF-7, UTF-16)
Look for other Twitter endpoints with open redirects (ads.twitter.com, business.twitter.com, etc.)
Test redirect chains through third-party services with trust relationships to Twitter
Attempt case variation in domain names combined with Unicode substitution

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1192
- T1203
- T1204.001

## Notes
This vulnerability is particularly severe because: (1) it exploits Twitter's own infrastructure to bypass safety measures, (2) the crafted URLs appear to originate from twitter.com domain increasing click likelihood, (3) it defeats the specific mechanism Twitter uses to protect against malicious links, (4) it demonstrates the complexity of Unicode-safe security validation, and (5) it could be used to distribute malware, phishing, or politically sensitive content at massive scale through an influential platform.

## Full report
<details><summary>Expand</summary>

**Summary:** A chain of two open redirects (on `analytics.twitter.com` and `twitter.com`), coupled with the use of an Ideographic Full Stop allows an attacker to defeat [Twitter's approach to blocking links](https://help.twitter.com/en/safety-and-security/phishing-spam-and-malware-links).

**Description:** Twitter maintains a deny list of domain names and prevents users from tweeting (direct or indirect) links to those domains. Most notably perhaps, Twitter recently added (tsk tsk...) `ddosecrets.com` to that deny list. The link validation performed by the backend is a black box (not documented anywhere public, as far as I know). However, I have found a way to defeat it. By combining the following two open (one internal, one external) redirects,

* `https://twitter.com/login?redirect_after_login=ONLY_TWITTER_SUBDOMAINS_ALLOWED_URL`
* `https://analytics.twitter.com/daa/0/daa_optout_actions?action_id=4&rd=ARBITRARY_URL%3F` (note the URL-encoded question mark at the end)

and using an [Ideographic Full Stop](https://unicode-table.com/en/3002/) in place of the ASCII period in the malicious target URL, it's possible to craft a URL that redirects to the forbidden domain name but that Twitter allows users to post in tweets.

## Steps To Reproduce:

  1. Choose the target URL; let's take `https://ddosecrets.com` as an example.
  2. Replace all occurrences of the ASCII period by the URL-encoded version of the [Ideographic Full Stop](https://unicode-table.com/en/3002/), i.e. `%E3%80%82`: `https://ddosecrets%E3%80%82com`.
  3. URL-encode the result of step 2: `https%3A%2F%2Fddosecrets%25E3%2580%2582com`.
  4.  Append the result of step 3 to `https://analytics.twitter.com/daa/0/daa_optout_actions?action_id=4&rd=` and append `%3F` to the result: `https://analytics.twitter.com/daa/0/daa_optout_actions?action_id=4&rd=https%3A%2F%2Fddosecrets%25E3%2580%2582com%3F`.
  5. URL-encode the result of step 4: `https%3A%2F%2Fanalytics.twitter.com%2Fdaa%2F0%2Fdaa_optout_actions%3Faction_id%3D4%26rd%3Dhttps%253A%252F%252Fddosecrets%2525E3%252580%252582com%253F`.
  6. Append the result of step 5 to `https://twitter.com/login?redirect_after_login=`: `https://twitter.com/login?redirect_after_login=https%3A%2F%2Fanalytics.twitter.com%2Fdaa%2F0%2Fdaa_optout_actions%3Faction_id%3D4%26rd%3Dhttps%253A%252F%252Fddosecrets%2525E3%252580%252582com%253F`.
  7. Log in to Twitter and tweet the URL resulting from step 6. Posting the tweet will succeed (but it shouldn't, if link validation were effective).
  8. Click the malicious link in the tweet you just posted; you'll get redirected to the forbidden domain without being shown any Twitter interstitial page.

(If you're not logged in to Twitter when you click the malicious link, you'll get prompted to log in, but you will still get redirected to the forbidden domain afterwards.)

## Supporting Material/References:

See attached proof-of-concept video.

## Impact

Attackers can defeat [Twitter's approach to blocking links](https://help.twitter.com/en/safety-and-security/phishing-spam-and-malware-links) and post arbitrary unsafe links (starting with `https://twitter.com`, which really compounds the problem) in tweets.

</details>

---
*Analysed by Claude on 2026-05-24*
