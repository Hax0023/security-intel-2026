# WAF Bypass via Non-Standard ASCII Characters Enabling Reflected XSS on 404 Pages

## Metadata
- **Source:** HackerOne
- **Report:** 716761 | https://hackerone.com/reports/716761
- **Submitted:** 2019-10-17
- **Reporter:** laszaro
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (Reflected), WAF Bypass, Encoding Bypass, Input Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A WAF filter designed to block reflected XSS on 404 pages can be bypassed by injecting non-standard ASCII characters (hex values %80-%FF) between encoded quote characters and payload data. This allows attackers to execute arbitrary JavaScript in the context of the victim's browser, enabling credential theft and unauthorized actions on behalf of authenticated users.

## Attack scenario
1. Attacker identifies that a previous XSS vulnerability on Starbucks 404 pages was partially patched with encoding-based WAF rules
2. Attacker tests various non-standard ASCII character encodings to determine which bypass the WAF
3. Attacker discovers that hex values in the range %80-%FF are not filtered, while %00-%7F are properly blocked
4. Attacker crafts payload embedding non-ASCII character (e.g., %80) between double-encoded quotes (%2522) and XSS payload containing accesskey and onclick handlers
5. Attacker sends crafted URL to victim via phishing email or social engineering
6. Victim clicks link and JavaScript executes, stealing session cookies or performing unauthorized account actions

## Root cause
The WAF implementation uses a blocklist approach that only filters standard ASCII characters (hex %00-%7F) in URL-encoded payloads. The filter does not account for non-standard ASCII and extended ASCII characters (%80-%FF) that can be processed by the application, creating a gap in encoding validation. The application appears to decode these multi-byte sequences without proper sanitization of the resulting characters.

## Attacker mindset
Security researcher identifies incomplete fix of prior vulnerability and systematically tests alternative encoding methods to discover gaps in WAF logic. Demonstrates that simple range-based filtering is insufficient without understanding character encoding boundaries and double-encoding attack vectors.

## Defensive takeaways
- Use whitelist-based input validation rather than blocklists for security-critical filters
- Understand and properly handle multi-byte character encodings (UTF-8, ISO-8859-1, etc.) in security controls
- Implement canonicalization before validation: decode all encodings and normalize input to known safe format
- Test WAF bypass techniques including double-encoding, mixed encoding types, and non-standard character ranges
- Apply output encoding (HTML entity encoding) at point of use in 404 error pages, not just input filtering
- Use established XSS protection libraries rather than custom WAF rules
- Perform comprehensive testing across all character ranges (0x00-0xFF) when implementing filtering rules
- Consider using Content-Security-Policy headers as defense-in-depth against reflected XSS

## Variant hunting
Test other character encoding boundaries: UTF-16, UTF-32, unicode escapes (%uXXXX), HTML entities, combinations of URL + HTML encoding; test whether other HTML special characters (<, >, etc.) can bypass using similar non-ASCII injection; probe whether the WAF inconsistency exists on other Starbucks domains beyond .com.br; check if similar patterns work with other event handlers (onerror, onload, etc.); test Null byte injection (%00) combinations with non-ASCII; verify if the exception values (%81, %8d, %8f, %90, %9d) have exploitable characteristics

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
This is a follow-up to report 629745 demonstrating incomplete vulnerability remediation. The researcher methodically identified the exact character range boundaries of the WAF bypass (all values >0x7F work except specific exceptions), indicating the fix addressed only 7-bit ASCII filtering. The accesskey+onclick technique leverages Firefox's accesskey feature as execution trigger, showing understanding of browser-specific XSS vectors. The 404 page context is particularly dangerous as it may be less scrutinized by developers than normal application pages. Report demonstrates importance of comprehensive security testing after patches rather than assuming fixes are complete.

## Full report
<details><summary>Expand</summary>

**Summary:** Report [629745](https://hackerone.com/reports/629745) not properly resolved: "Many Starbucks websites are vulnerable to cross-site scripting on 404 pages because double quotes lack sanitizing in hidden input tags, which leads to JavaScript execution".

**Description:**
Report 629745 caught my attention, so I began testing the WAF to see if I could find any other issues. After a while I found out that the previously reported issue was not properly resolved as I was able to bypass the double encoding filter.

The original payload on the report was something like this:
```
https://www.starbucks.com.br/testing%2522%2520accesskey='x'%2520onclick='confirm%601%60'
```
and it got resolved. But you can bypass the filter with this:
```
https://www.starbucks.com.br/testing%2522%80%2520accesskey='x'%2520onclick='confirm%601%60'
```
Notice the `%80` between `%2522` and `%2520`. In fact, you can replace the `%80` with any hex value __beyond `%7f`__  and the payload still works (there's a couple of exceptions throwing "Bad Request" errors:  `%81`, `%8d`, `%8f`, `%90`, and `%9d`), but values in the range `%00-%7f` get properly filtered out (throwing custom "Server Error" pages and 404 pages, 301 and 302 redirect pages, and default 400 Bad Request errors, depending on the value)

So, this payload works:
```
https://www.starbucks.com.br/testing%2522%FF%2520accesskey='x'%2520onclick='confirm%601%60'
```
but this one doesn't:
```
https://www.starbucks.com.br/testing%2522%7F%2520accesskey='x'%2520onclick='confirm%601%60'
```

There is a similar behaviour if you put the double-hex digit first.
This payload breaks the filter:
```
https://www.starbucks.com.br/testing%80%2522%2520accesskey='x'%2520onclick='confirm%601%60'
```
but this one doesn't:
```
https://www.starbucks.com.br/testing%7F%2522%2520accesskey='x'%2520onclick='confirm%601%60'
```

**Platform(s) Affected:** Firefox 69.0.3

## Steps To Reproduce:

  1. Visit this link on Firefox: 

```
https://www.starbucks.com.br/testing%2522%80%2520accesskey='x'%2520onclick='confirm%601%60'
```

  2. Press CONTROL+ALT+X on Mac, or ALT+SHIFT+X on Windows

## Recommendations for fix
The range of hex values `%80-%FF` is breaking the WAF filter, those values need to be filtered out just like the range `%00-%7F` is being filtered out.

## Impact

As the original report said:
"JavaScript is against Starbucks users on multiple critical domains. JavaScript execution results in information theft and an attacker can perform unwanted actions on a victim's behalf".

</details>

---
*Analysed by Claude on 2026-05-12*
