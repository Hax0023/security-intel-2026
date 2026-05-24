# Full Path Disclosure (FPD) via Parameter Type Confusion in updatePhrases

## Metadata
- **Source:** HackerOne
- **Report:** 9745 | https://hackerone.com/reports/9745
- **Submitted:** 2014-04-25
- **Reporter:** faisalahmed
- **Program:** localize.im
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Full Path Disclosure, Type Confusion
- **CVEs:** None
- **Category:** web-api

## Summary
An information disclosure vulnerability exists in the language editor where sending an array instead of a string value for updatePhrases parameters causes a PHP type error that reveals the server's absolute file path. The vulnerability affects the same updatePhrases functionality that was previously patched, but at a different parameter level, indicating incomplete remediation.

## Attack scenario
1. Attacker identifies the updatePhrases POST parameters used in the language translation interface
2. Attacker sends a malformed POST request with array brackets appended to parameter names (e.g., updatePhrases[edits][ID][0][])
3. The trim() function in index.php line 192 receives an array instead of expected string
4. PHP type error is generated and unhandled, causing error message to be displayed
5. Error message reveals full server path: /srv/data/web/vhosts/www.localize.im/htdocs/index.php
6. Attacker uses disclosed path information for further reconnaissance and targeted attacks

## Root cause
Insufficient input validation and type checking before passing user-supplied parameters to the trim() function. The application assumes updatePhrases parameters are strings but does not enforce or validate this constraint. Previous patch only fixed one parameter vector without addressing the underlying type validation issue.

## Attacker mindset
An attacker conducting reconnaissance would exploit type confusion to elicit error messages revealing system architecture. The attacker demonstrates methodical vulnerability hunting by re-testing the same functionality after patches, knowing that incomplete fixes often leave parallel attack vectors intact.

## Defensive takeaways
- Implement strict input validation and type enforcement on all user-supplied parameters before processing
- Use whitelist-based parameter validation rather than relying on individual parameter fixes
- Implement comprehensive error handling to prevent sensitive information leakage in error messages
- Enable custom error handlers that log detailed errors server-side while returning generic messages to clients
- Use static analysis tools to identify all instances of trim() and similar functions and verify type safety
- When patching security issues, audit the entire functionality for similar vulnerabilities rather than fixing individual parameters
- Disable PHP error display in production environments and log errors securely

## Variant hunting
Similar vulnerabilities likely exist in other functions expecting scalar parameters (explode, str_replace, strtolower, etc.). Check all POST parameters that accept updatePhrases, updateTranslations, or similar batch operations for array injection. Test other endpoints with similar phrase/translation editing functionality. Review other user input processing functions that lack explicit type validation.

## MITRE ATT&CK
- T1590.004 - Gather Victim Org Information (Identify Physical Locations)
- T1580 - Cloud Infrastructure Discovery

## Notes
This is a classic example of an incomplete security patch. The vendor fixed updatePhrases[previous][ID][0] but failed to apply the same validation to updatePhrases[edits][ID][0] and other related parameters. This suggests a systemic issue in how input validation is implemented. The vulnerability has low severity as it only discloses file paths, but it's valuable for reconnaissance preceding more severe attacks. The disclosure mentions 'LotsOfPhrases' suggesting the payload was modified for brevity, indicating there may be size/complexity factors relevant to reproduction.

## Full report
<details><summary>Expand</summary>

Hi,
found another information disclosure vulnerability/Full Path Disclosure on your application.

Proof of Concept
-------------------------
GET  : https://www.localize.im/projects/[projiect ID/languages/[Language ID]
POST CONTENT: 
`CSRFToken=TOKEN&updatePhrases[previous][yxr][0]=&updatePhrases[edits][yy4][0]=&updatePhrases[edits][yxr][0]=&updatePhrases[previous][yxq][0]=&####LotsOfPhrases######&updatePhrases[secret]=[SecredCodes]&updatePhrases[translatorID]=[ID]`

Just Add "[]" after any of those *updatePhrases[edit][ID][0]* parameter.

Note: look like my last FPD Vulnerability report. doesn't it?
but last one was at *updatePhrases[previous][ID][0]* that is fixed as you rolled out a fix for that..
i just went to check that the bug is fixed or not and found there is another parameter that is still vulnerable.

### The information from page:
> **Warning: trim() expects parameter 1 to be string, array given in /srv/data/web/vhosts/www.localize.im/htdocs/index.php on line 192**

I Also Added a Screenshot of that FPD as attachment..
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
