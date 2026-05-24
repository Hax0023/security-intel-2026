# PII Exposure via Email Confirmation Link – Email Embedded in Token & Leaked via Wayback Machine

## Metadata
- **Source:** HackerOne
- **Report:** 3210022 | https://hackerone.com/reports/3210022
- **Submitted:** 2025-06-19
- **Reporter:** mantu1738
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
An email confirmation link used by Omise (dashboard.omise.co) includes the user's email address directly embedded in a token that is visible in the URL. This token has been archived publicly by the Wayback Machine (archive.org), resulting in public exposure of personally identifiable information (PII). 

## Steps To Reproduce:
  1. Visit an archived page on Wayback Machine containing a confirmatio

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

An email confirmation link used by Omise (dashboard.omise.co) includes the user's email address directly embedded in a token that is visible in the URL. This token has been archived publicly by the Wayback Machine (archive.org), resulting in public exposure of personally identifiable information (PII). 

## Steps To Reproduce:
  1. Visit an archived page on Wayback Machine containing a confirmation URL:
  ```
https://dashboard.omise.co/users/confirm_email/BAhbCGkD5+gCVTogQWN0aXZlU3VwcG9ydDo6VGltZVdpdGhab25lWwhJdToJVGltZQ1qVh%2FA51yK3Ak6DW5hbm9fbnVtaQH7Og1uYW5vX2RlbmkGOg1zdWJtaWNybyIHJRA6CXpvbmVJIghVVEMGOgZFRkkiCFVUQwY7C1RJdTsGDWpWH8DnXIrcCTsHaQH7OwhpBjsJIgclEDsKQAlJIiFtYW50dWhhY2tlcm9uZTE3MzhAZ21haWwuY29tBjsLVA==--5d75e1da7fbede4b6285f61f758e5dbed8d62604
    ```
  2. Extract the token from the URL. Base64-decode it:
```
import base64
from urllib.parse import unquote
import re

token = "<Base64_part>"
decoded_token = base64.b64decode(unquote(token))
print(re.findall(rb"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", decoded_token))
```
  3. Observe that the token contains a full email address, e.g.,: ***big.dogs1979@gmail.com***

## Recommendations
-  Do not embed PII (email addresses) in tokens
- Disallow crawling of sensitive URLs with robots.txt
```
User-agent: *
Disallow: /users/confirm_email/
```

Note: I also tired sending by creating my own account and the url contains the email address in confirmation email.
```
https://dashboard.omise.co/users/confirm_email/BAhbCGkD5+gCVTogQWN0aXZlU3VwcG9ydDo6VGltZVdpdGhab25lWwhJdToJVGltZQ1qVh%2FA51yK3Ak6DW5hbm9fbnVtaQH7Og1uYW5vX2RlbmkGOg1zdWJtaWNybyIHJRA6CXpvbmVJIghVVEMGOgZFRkkiCFVUQwY7C1RJdTsGDWpWH8DnXIrcCTsHaQH7OwhpBjsJIgclEDsKQAlJIiFtYW50dWhhY2tlcm9uZTE3MzhAZ21haWwuY29tBjsLVA==--5d75e1da7fbede4b6285f61f758e5dbed8d62604

██████
```

  #POC
████

Thanks 
@mantu1738

## Impact

- Leaks **PII (email address)** in URL
- Publicly archived link on Wayback Machine exposes user identity
- Token is easily **Base64-decoded**
- Potential **email confirmation abuse** if token is replayable
- Risk of **user enumeration** or phishing

</details>

---
*Analysed by Claude on 2026-05-24*
