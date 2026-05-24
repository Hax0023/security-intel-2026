# Limited Open redirection using SSO-SAML

## Metadata
- **Source:** HackerOne
- **Report:** 178345 | https://hackerone.com/reports/178345
- **Submitted:** 2016-10-27
- **Reporter:** shailesh4594
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Open Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hello,

**Endpoint:** https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true

Recently, you have patched an open redirection issue which was reported as #171398. 
I found a bypass of that patch. 

**Steps to reproduce:** 
1. Add following in comment/report : 
```https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true``` 
2. Click on link. 
3

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Hello,

**Endpoint:** https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true

Recently, you have patched an open redirection issue which was reported as #171398. 
I found a bypass of that patch. 

**Steps to reproduce:** 
1. Add following in comment/report : 
```https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true``` 
2. Click on link. 
3. You will redirected on SSO URL without going through **External Link Warning** page. 
4. Done.

PoC  : 
https://hackerone.com/users/saml/sign_in?email=teste@snapchat.com&remember_me=true (Through external warning page)
https://hackerone.com/users//saml/sign_in?email=teste@snapchat.com&remember_me=true (Without external warning page)

**Suggested Fix:** Use more stronger regular expression and filtration at this endpoint.

Best regards,
Shailesh


</details>

---
*Analysed by Claude on 2026-05-24*
