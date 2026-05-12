# Reflected XSS in Starbucks Account Redeem Page via Multiple Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 531042 | https://hackerone.com/reports/531042
- **Submitted:** 2019-04-08
- **Reporter:** zl33t
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Starbucks account creation/redemption page where the xtl_amount_type parameter is reflected without proper encoding. The vulnerability requires specific combinations of parameter values (xtl_coupon_code and xtl_amount) to bypass client-side or server-side filters, allowing arbitrary JavaScript execution.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in xtl_amount_type parameter: </script><svg/onload=alert(document.domain)>
2. Attacker discovers that payload alone does not execute due to validation/filtering
3. Attacker modifies complementary parameters (xtl_coupon_code and xtl_amount) with non-standard values to bypass filtering logic
4. Attacker sends crafted URL to victim via phishing email or social engineering
5. Victim clicks link and visits the vulnerable endpoint with modified parameters
6. Malicious JavaScript executes in victim's browser with their session context, potentially stealing cookies, session tokens, or performing unauthorized actions

## Root cause
The application implements insufficient input validation/filtering that relies on expected parameter values. When parameters deviate from expected formats, the XSS filter logic fails. The output encoding of xtl_amount_type parameter is inadequate, and the filter appears to check parameter combinations rather than properly encoding all user input regardless of other parameter states.

## Attacker mindset
The attacker demonstrated methodical testing by identifying that payloads work conditionally based on multiple parameters. This shows understanding of common filter bypass techniques and persistence in testing different parameter combinations. The approach suggests knowledge of how validation logic often fails when multiple interdependent parameters are present.

## Defensive takeaways
- Implement context-aware output encoding for all user-controlled input regardless of parameter values or combinations
- Use allowlist-based validation rather than blacklist/filter approaches for sensitive parameters
- Apply HTML entity encoding to all parameters reflected in HTML context
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Validate parameter combinations server-side with proper escaping at each step, not just at input
- Conduct comprehensive security testing that includes fuzzing parameter combinations, not just individual parameters
- Use templating engines with auto-escaping enabled
- Implement DomPurify or similar sanitization libraries if dynamic content rendering is necessary

## Variant hunting
Search for other endpoints using similar parameter naming patterns (xtl_*), check for other redemption/account creation flows, test all parameters that accept user input for similar multi-parameter bypass techniques, look for other instances where dependent parameters might bypass individual parameter validation

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link
- T1566: Phishing
- T1059: Command and Scripting Interpreter - JavaScript/Web Script

## Notes
The report quality is low with unclear technical details and grammar issues, but the core vulnerability is valid. The key insight is that validation logic checking parameter dependencies created a bypass condition. This pattern is common in applications that attempt to validate 'voucher codes' or 'redemption codes' where multiple fields must be present but validation is loose. The reporter's discovery method (changing parameters to make payload work) suggests script-based filter testing rather than deep code analysis.

## Full report
<details><summary>Expand</summary>

HI,

**Summary:** Reflected XSS 
**Description:**  the parameters are complementary to each other
**Platform(s) Affected:**  my browser firefox 52.7.3

## Steps To Reproduce:

   1. go to https://www.starbucks.com/account/create/redeem/MCP131XSR?xtl_coupon_code=1&xtl_coupon_code=81431&xtl_amount=0.0&xtl_amount_type=DOLLAR_VALUE
   1. change parameter `xtl_amount_type` to </script><svg/onload=alert()>` >note:if you  go enter this the payload not work but!!!!! you change `xtl_coupon_code` and `xtl_amount` payload will work
   1. change `xtl_coupon_code` and `xtl_amount` to any think 

   1.payload be like https://www.starbucks.com/account/create/redeem/MCP131XSR?xtl_coupon_code=1&xtl_coupon_code=hkjhkjh&xtl_amount=jhkjhj&xtl_amount_type=ayn%3C/script%3E%3Csvg/onload=alert(document%2edomain)%3E
  
## Supporting Material/References:

 {F464214}


## How can the system be exploited with this bug?
  
The attacker can execute JS code.

## How did you come across this bug ?
change `xtl_coupon_code` and `xtl_amount` payload will work
In this bug the parameters are complementary to each other

## Recommendations for fix

In this bug the parameters are complementary to each other try to retreat

## Impact

* The attacker can execute JS code.

</details>

---
*Analysed by Claude on 2026-05-12*
