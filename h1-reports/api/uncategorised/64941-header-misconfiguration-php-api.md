# Header Misconfiguration - PHP API

## Metadata
- **Source:** HackerOne
- **Report:** 64941 | https://hackerone.com/reports/64941
- **Submitted:** 2015-05-30
- **Reporter:** paulos__
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hey,

Your index api page auth can easily be bypassed because it doesn't use proper auth practices in its PHP core. Here is the master code from Shopify: 

https://github.com/Shopify/shopify_php_api/blob/master/index.php

it says:

if (!isset($_SESSION['shop']) || !isset($_SESSION['token'])) header("Location: login.php");

This easily can be bypassed because the browser can decide to rec

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

Hey,

Your index api page auth can easily be bypassed because it doesn't use proper auth practices in its PHP core. Here is the master code from Shopify: 

https://github.com/Shopify/shopify_php_api/blob/master/index.php

it says:

if (!isset($_SESSION['shop']) || !isset($_SESSION['token'])) header("Location: login.php");

This easily can be bypassed because the browser can decide to receive 301/302 redirects. and since if not logged in, the code tries to decide to redirect back to the login page, and the browser can ignore it. this can create an authentication bypass and also full path disclosure.

 I have written a similar example in my blog, http://www.paulosyibelo.com/2014/08/header-based-login-bypass.html

P.S: The issue exists not only on the index.php page, but in almost every page. (ex: https://github.com/Shopify/shopify_php_api/blob/master/login.php)

The best practice I would recommend would be creating another function instead of the header one, like:

function redirect($url){
    header("Location: $url");
    exit();
}

The easiest approch is to exit(); the code after the redirection. or else, the rest of the page still renders no matter what. I hope I don't need to provide a POC as its a crystal clear bug (also with the link).

Thanks,

</details>

---
*Analysed by Claude on 2026-05-24*
