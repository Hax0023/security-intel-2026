# Bypassing Content-Security-Policy via Wildcard Subdomain Whitelisting Leads to Open Redirect and Iframe XSS

## Metadata
- **Source:** HackerOne
- **Report:** 1166766 | https://hackerone.com/reports/1166766
- **Submitted:** 2021-04-16
- **Reporter:** echidonut
- **Program:** Stripo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Content-Security-Policy Bypass, Open Redirect, Cross-Site Scripting (XSS), Insecure Whitelist Configuration
- **CVEs:** None
- **Category:** web-api

## Summary
The application implemented a Content-Security-Policy to restrict iframe sources, but whitelisted the overly-broad *.firebaseapp.com domain. An attacker can deploy malicious content on Firebase Hosting (free tier) and embed an iframe pointing to their Firebase subdomain, bypassing CSP restrictions. This enables phishing attacks, open redirects, and XSS against users of my.stripo.email and viewstripo.email.

## Attack scenario
1. Attacker creates a free Firebase Hosting account and deploys malicious HTML content
2. Attacker crafts a Stripo template/message containing an iframe src pointing to their malicious firebaseapp.com subdomain
3. Victim user with sufficient browser permissions opens the template editor in my.stripo.email or viewstripo.email
4. The iframe loads successfully because *.firebaseapp.com is whitelisted in the frame-src CSP directive
5. The malicious iframe triggers a popup/redirect to a phishing domain or executes XSS payload
6. The attack affects all users who open the attacker's malicious template, particularly within the same organization

## Root cause
Overly permissive CSP whitelist using wildcard subdomains (*.firebaseapp.com) without considering that Firebase Hosting is a free, publicly accessible service where any attacker can deploy arbitrary content. The CSP policy fails to enforce strict origin restrictions and relies on the assumption that whitelisted domains are trustworthy.

## Attacker mindset
Attacker recognized that CSP whitelists often include third-party services without evaluating the security implications of user-controlled content on those services. By leveraging Firebase's free tier, the attacker bypassed the organization's security controls with minimal effort and cost, targeting users within the same platform for maximum impact.

## Defensive takeaways
- Avoid whitelisting wildcard subdomains (*.domain.com) in CSP directives; instead, whitelist specific, fully-qualified subdomains
- Regularly audit CSP policies to identify overly-permissive entries, particularly for free or user-generated-content platforms
- Implement nonce-based or hash-based CSP instead of whitelist-based approaches where possible
- Use Content-Security-Policy-Report-Only during testing to identify CSP bypasses before deploying to production
- Consider using Subresource Integrity (SRI) for third-party resources to ensure content authenticity
- For iframe sandboxing, use the sandbox attribute in addition to CSP frame-src directives to provide defense-in-depth
- Implement frame-ancestors CSP directive to prevent clickjacking and unauthorized framing
- Monitor and log CSP violations to detect exploitation attempts in real-time

## Variant hunting
Search for other applications using wildcard CSP whitelists for user-generated-content platforms (Heroku, GitHub Pages, Netlify, Vercel, Firebase Hosting, AWS Amplify). Review any CSP policies that whitelist *.cdn.provider.com or *.hosting.provider.com domains. Examine email template builders, content management systems, and drag-and-drop editors for similar CSP misconfigurations.

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1656

## Notes
The vulnerability is particularly impactful in viewstripo.email (public-facing sharing feature), which means unauthenticated users could be targeted. The attacker's ability to host arbitrary content on a whitelisted domain fundamentally undermines the CSP's security objective. The report notes this prevents users from safely editing templates without disabling JavaScript, indicating significant usability impact. The fix should involve either removing *.firebaseapp.com from the whitelist or replacing it with a strict nonce-based CSP implementation.

## Full report
<details><summary>Expand</summary>

## Summary:
`https://my.stripo.email/cabinet/#/template-editor/.....` has the ff: code to make iframes more secure:
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self';
    frame-src data: *.firebaseapp.com *.stripe.com *.google.com *.facebook.com 'self';
    style-src 'self' 'unsafe-inline' *;
    script-src 'self' 'unsafe-eval' 'unsafe-inline' *.ampproject.org googletagmanager.com *.googletagmanager.com *.amplitude.com api.vk.com *.gstatic.com *.facebook.net *.google.com *.google-analytics.com *.stripe.com *.pingdom.net *.intercom.io *.intercomcdn.com *.stripo.email *.zscalertwo.net *.zscaler.com *.zscaler.net *.pinimg.com *.getsitecontrol.com;
    img-src 'self' data: *;
    connect-src 'self' *;
    child-src blob:;
    font-src 'self' *;
    object-src 'self' *">
```

* <iframe> pointing to other domains won't work but, the whitelist in frame-src data has listed *.firebaseapp.com, a free hosting domain, leading to iframe abuse and redirects

## Steps To Reproduce:

1. Create a new message/template with HTML
2. Using nodeJS, deploy a page in firebaseapp. It's free. [Guide](https://firebase.google.com/docs/hosting/quickstart)
2. Mine is [hackerone-jm.firebaseapp.com](https://hackerone-jm.firebaseapp.com). Add the ff. line: `<iframe src="//hackerone-jm.firebaseapp.com"></iframe>` in the HTML editor
3. A browser popup will show, then redirect after

## Supporting Material/References:
{F1268265}
*Tested in Google Chrome Version 89.0.4389.128 (Official Build) (64-bit)*

## Impact

* This can be used to launch a phishing attack against users of the same organization.
*  `viewstripo.email` is also vulnerable to this making it an open redirect/xss to all users. [POC](https://viewstripo.email/6a8ceb1a-7e45-4304-a93f-0cf4c32fc3111618586929192)
* This also makes editing the message/template almost impossible without disabling javascript in your browser

*this only works assuming the user has allowed `my.stripo.email` to redirect and spawn popups.*

</details>

---
*Analysed by Claude on 2026-05-12*
