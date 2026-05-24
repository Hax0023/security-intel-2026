# CSRF in all API endpoints when authenticated using HTTP Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 195156 | https://hackerone.com/reports/195156
- **Submitted:** 2017-01-01
- **Reporter:** zombiehelp54
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
#Description:
**Short:**
I have found a CSRF vulnerability in all API endpoints `/admin/[any_api_endpoint]/` if the current user has authenticated using HTTP authentication.

**Details:**
When a user generates API credentials for a private application in his shop he will be given API key and password that he can use to access his shop resources, moreover shopify provides an HTTP authentication URL

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

#Description:
**Short:**
I have found a CSRF vulnerability in all API endpoints `/admin/[any_api_endpoint]/` if the current user has authenticated using HTTP authentication.

**Details:**
When a user generates API credentials for a private application in his shop he will be given API key and password that he can use to access his shop resources, moreover shopify provides an HTTP authentication URL to the user as an example URL.
{F148606}

If the user is authenticated through HTTP authentication , the browser will automatically send the credentials in the `Authroization` header with each request so the user will still be authenticated without need to submit the username and password each time.

I have found that if a user has authenticated through HTTP authentication (opened the example URL that shopify provided him when he created the private application) , all the API endpoints will be vulnerable to CSRF.
#Steps to reproduce: 
1. Login to your shopify account 
2. Create a private application then open the authentication example URL in a new browser.
3. for testing , submit the following form through the browser in which you opened the example link: 

```
<form action="https://[shop].myshopify.com/admin/products.json" method=post>
<input name="product[title]" value="API CSRF TEST">
<input name="product[vendor]" value="test">
<input name="product[body_html]" value="<h1>API CSRF TEST [Can be stored XSS for admins]</h1>">
 <input name="product[product_type]" value="test">
<input type=submit>
</form>
```
4- Go to `[shop].myshopify.com/admin/products` and you'll see the product.

All the API endpoints are vulnerable , even the endpoints that only accept (PUT , PATCH or DELETE) , you can submit requests with these methods using `_method` parameter. 
#What is the problem here?
The vulnerability exists because API endpoints accept data submitted with `content-type: application/x-www-form-urlencoded` without any validation for the authenticity token if the user is authenticated through HTTP authentication. 
#Impact:
Through this vulnerability an attacker can do malicious actions through the victim's session which includes: creating a webhook that pings the attacker's server for all events happening on the victim's shop, fulfilling orders  , creating a transaction ,editing themes ..etc (All possible actions done through the API).


Thanks and happy new year :)

</details>

---
*Analysed by Claude on 2026-05-24*
