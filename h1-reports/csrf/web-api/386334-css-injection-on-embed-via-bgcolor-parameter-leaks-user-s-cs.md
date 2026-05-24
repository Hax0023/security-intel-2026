# CSS Injection on /embed/ via bgcolor parameter leaks user's CSRF token and allows for XSS 

## Metadata
- **Source:** HackerOne
- **Report:** 386334 | https://hackerone.com/reports/386334
- **Submitted:** 2018-07-24
- **Reporter:** nahamsec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - DOM
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there,

There's a CSS injection here: https://chaturbate.com/embed/admin/?bgcolor=%7D*%7Bbackground:red&tour=nvfS&disable_sound=0&campaign=iNSGX 

```
  body, div#main, div.content, div.block, div.section {margin: 0px; padding: 0px;}
  body {min-width:800px;}
  div.content {width: 100%;}
  
  body {background: }*{background:red;}

```

This allows an attacker to enumerate the CSRF token. Once t

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

Hi there,

There's a CSS injection here: https://chaturbate.com/embed/admin/?bgcolor=%7D*%7Bbackground:red&tour=nvfS&disable_sound=0&campaign=iNSGX 

```
  body, div#main, div.content, div.block, div.section {margin: 0px; padding: 0px;}
  body {min-width:800px;}
  div.content {width: 100%;}
  
  body {background: }*{background:red;}

```

This allows an attacker to enumerate the CSRF token. Once the CSRF token is enumerated, we can 

#POC 
1. Go to `http://d0nut.pythonanywhere.com/demo/token_stealing/7GTt5qD1LD273WYkJyaR/reset`
2. Now go to `http://d0nut.pythonanywhere.com/demo/token_stealing/7GTt5qD1LD273WYkJyaR` and let it do it's magic :) 

{F324052}

There are numerous endpoints like `POST /choose_broadcaster_chat_color` where it returns `Content-Type: text/html; charset=utf-8` that could potentially allow a hacker to combine the two for XSS (I haven't gotten that far yet)


 **Do you mind asking your HackerOne contact to allow collaboration on your program, so I can invite another researcher that helped me exploit this fully?**

Thanks,
Ben

## Impact

#

</details>

---
*Analysed by Claude on 2026-05-24*
