# Adobe Flash Player Regular Expression UAF Remote Code Execution Vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 139879 | https://hackerone.com/reports/139879
- **Submitted:** 2016-05-19
- **Reporter:** bee13oy
- **Program:** Adobe Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Use-After-Free (UAF), Remote Code Execution (RCE), Memory Corruption
- **CVEs:** CVE-2016-4121
- **Category:** memory-binary

## Summary
A use-after-free vulnerability exists in the PCRE regex engine bundled with Adobe Flash Player that allows remote code execution. The vulnerability affects Flash Player versions 11.5.502.135 through 20.0.0.286 and can be exploited through malicious regular expression patterns to achieve arbitrary code execution.

## Attack scenario
1. Attacker crafts a malicious Flash (.swf) file or web page containing weaponized ActionScript code with a specially crafted regular expression pattern
2. Victim visits the malicious webpage or opens the crafted Flash file in a vulnerable Flash Player version (11.5.502.135 - 20.0.0.286)
3. The crafted regex pattern triggers the UAF vulnerability in the PCRE engine during regex compilation or matching operations
4. Memory corruption occurs due to accessing freed memory, allowing attacker to overwrite adjacent heap structures
5. Attacker leverages the heap overflow to achieve arbitrary code execution with the privileges of the Flash Player process
6. Attacker gains remote code execution on the victim's system, potentially installing malware or exfiltrating data

## Root cause
The PCRE regex engine version bundled with Adobe Flash Player contains a use-after-free vulnerability where memory is freed prematurely during regex pattern processing, but the freed memory pointer is subsequently dereferenced without validation, allowing exploitation via specially crafted regex patterns.

## Attacker mindset
Target widespread Flash Player installations for drive-by exploitation. Leverage UAF vulnerability for heap manipulation and RCE without user interaction beyond visiting a webpage. Focus on high-value targets by embedding exploit in targeted watering hole attacks or ad networks.

## Defensive takeaways
- Immediately patch Adobe Flash Player to versions after 20.0.0.286 or disable Flash in browsers entirely
- Implement strict Content Security Policy (CSP) headers to restrict script execution and sandboxing
- Deploy memory protection mechanisms such as Address Space Layout Randomization (ASLR) and Data Execution Prevention (DEP)
- Monitor for suspicious regex compilation patterns or unusual memory allocation behaviors in Flash processes
- Use allowlist-based Flash content policies - only allow Flash from trusted sources
- Implement browser-level sandboxing to isolate Flash Player processes from system resources
- Maintain security awareness training on avoiding malicious content and untrusted websites

## Variant hunting
Search for other PCRE engine implementations in legacy Adobe products (Reader, AIR). Investigate regex handling in other Flash-based multimedia players. Review PCRE versions for similar UAF patterns in memory management during pattern compilation/matching. Check for similar vulnerabilities in other regex engines (PCRE2, Oniguruma, RE2) when used in web plugins.

## MITRE ATT&CK
- T1190
- T1203
- T1055
- T1547

## Notes
Reported directly to Adobe and assigned CVE-2016-4121. Exploit proof-of-concept demonstrated calculator popup on affected versions. This vulnerability highlights the critical security risks of deprecated Flash Player and the importance of retiring legacy plugin technologies. The UAF in PCRE is a classic memory corruption vector exploitable through user-controllable regex patterns.

## Full report
<details><summary>Expand</summary>

I. Summary
There's a UAF Vulnerability in the PCRE engine version used in Flash that could lead to Remote Code Execution.

II. Affected 
Adobe Flash Player 11.5.502.135 ~ 20.0.0.286

III. Reference
Identified as CVE-2016-4121, and reported to Adobe  directly.
https://helpx.adobe.com/security/products/flash-player/apsb16-15.html

Original report with an exploit demo which will pop up a calculator works well on fp_11.5.502.135 ~ fp_18.0.0.209 shows how to achieve Remote Code Execution.

IV. Credit
bee13oy of CloverSec Labs

</details>

---
*Analysed by Claude on 2026-05-12*
