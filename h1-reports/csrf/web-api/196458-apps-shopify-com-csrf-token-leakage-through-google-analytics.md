# apps.shopify.com - CSRF token leakage through Google Analytics

## Metadata
- **Source:** HackerOne
- **Report:** 196458 | https://hackerone.com/reports/196458
- **Submitted:** 2017-01-07
- **Reporter:** zombiehelp54
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
#Description:
When a user tries to send a support a message to an app developer in `apps.shopify.com` , he will be asked to login and once he is logged in , he will be redirected to `apps.shopify.com/[app_id]?authenticity_token=[current_user_authenticity_token]`. 
Developers can track their app page view in `apps.shopify.com` by adding a google tracking code while editing their app.

With that sai

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
When a user tries to send a support a message to an app developer in `apps.shopify.com` , he will be asked to login and once he is logged in , he will be redirected to `apps.shopify.com/[app_id]?authenticity_token=[current_user_authenticity_token]`. 
Developers can track their app page view in `apps.shopify.com` by adding a google tracking code while editing their app.

With that said , here is how now attacker can steal someone's CSRF token and use it to submit requests on behalf of that user:
- Attacker tricks the victim to visit an HTML page that he has control over it
- The HTML page opens a new window that redirects to `https://apps.shopify.com/[attacker's_app]/support_interactions/new`
- The victim will be redirected to `https://apps.shopify.com/#login` once he is logged in , he will be redirected to `https://apps.shopify.com/[attacker's_app]?authenticity_token=[victim's_token]` 
- The attacker can now see the victim's authenticity token by checking Real-Time analytics at his google analytics dashboard
- The attacker can use the victim's CSRF token to forge HTML requests that edit the victim's app listing by issuing requests to `https://apps.shopify.com/services/shopify_applications/edit` , if the victim has a shopify application or he can use it to submit reviews,support messages ..etc


#Steps to reproduce:
1. Go to `https://app.shopify.com/services/partners/api_clients/new` to create a new application then after creating it click **Edit App Listing** and at **Google analytics code** field enter your google analytics code.
2. Go to `https://apps.shopify.com/[your_app_id]/support_interactions/new` , you'll be redirected to the login page , enter your shop domain then login.
3. After logging in you'll be redirected to `https://apps.shopify.com/img-src-x-onerror-prompt2?reveal_support=true?authenticity_token=[Your_CSRF_TOKEN]&utf8=%E2%9C%93` 
4. Now go to your google analytics dashboard `https://analytics.google.com/analytics/web/` -> **Real Time** analytics , and you'll see the whole URL with the authenticity token disclosed.

{F149974}



</details>

---
*Analysed by Claude on 2026-05-24*
