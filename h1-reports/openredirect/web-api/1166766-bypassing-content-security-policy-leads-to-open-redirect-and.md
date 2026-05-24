# Bypassing Content-Security-Policy via Whitelisted Firebase Domain Leading to Open Redirect and Iframe XSS

## Metadata
- **Source:** HackerOne
- **Report:** 1166766 | https://hackerone.com/reports/1166766
- **Submitted:** 2021-04-16
- **Reporter:** echidonut
- **Program:** Stripo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Content Security Policy Bypass, Open Redirect, Iframe Injection, Subdomain Takeover Risk, XSS via Iframe
- **CVEs:** None
- **Category:** web-api

## Summary
Stripo's Content-Security-Policy whitelists *.firebaseapp.com in the frame-src directive, allowing attackers to host malicious iframes on Firebase's free hosting. An attacker can inject iframes pointing to attacker-controlled Firebase domains, bypassing CSP restrictions and enabling open redirects and XSS attacks against users.

## Attack scenario
1. Attacker creates a Firebase project and deploys a malicious page containing redirect logic or XSS payloads
2. Attacker injects HTML containing <iframe src='//attacker.firebaseapp.com'></iframe> into a Stripo template/message editor
3. Due to CSP whitelisting *.firebaseapp.com in frame-src, the iframe loads successfully despite CSP restrictions
4. When the template is viewed or shared, the iframe triggers a browser popup and redirects users to phishing sites or executes XSS
5. Users of the same organization are targeted via the shared template links on viewstripo.email
6. Editing templates becomes difficult as popups and redirects disrupt the user experience

## Root cause
Overly permissive CSP whitelisting of *.firebaseapp.com, a free public hosting service, in the frame-src directive. This allows any attacker to register a Firebase project and host malicious content that bypasses CSP protections. The policy lacked verification that whitelisted domains were actually trusted partners.

## Attacker mindset
An attacker recognizes that free hosting platforms like Firebase are publicly available, allowing anyone to register subdomains. By identifying these in CSP whitelists, they can abuse the trusted domain exception to inject malicious iframes without being blocked. This is a low-effort attack requiring minimal technical skill.

## Defensive takeaways
- Never whitelist entire domain wildcards (*.domain.com) for shared/free hosting services in CSP policies
- Use explicit subdomain whitelisting only for verified, controlled infrastructure owned by the organization
- Implement stricter frame-src policies; consider using 'self' only and requiring explicit same-origin frames
- Regularly audit CSP whitelists to identify overly permissive entries, especially public hosting domains
- Use CSP report-only mode to monitor violations before enforcing strict policies
- Consider implementing additional iframe sandboxing attributes (sandbox attribute) independent of CSP
- Require administrative verification for any third-party domain whitelisting

## Variant hunting
Search for other commonly whitelisted free hosting/CDN services in CSP policies: *.github.io, *.netlify.app, *.vercel.app, *.surge.sh, *.now.sh, *.heroku.com, *.replit.com. Look for wildcard entries in frame-src, child-src, and default-src directives. Check if organizations whitelist public S3 buckets (*.s3.amazonaws.com) or other user-controlled cloud storage.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1659 - Content Injection
- T1204.001 - Social Engineering (User Execution)

## Notes
The vulnerability demonstrates a critical flaw in CSP design: whitelisting entire domains of shared/free hosting platforms negates the security benefit of CSP. The attacker has no need for account takeover or XSS on legitimate Firebase projects—they simply create their own. The PoC on viewstripo.email shows the issue affects public template sharing, amplifying impact. The researcher notes this disrupts normal editing workflows, indicating high usability impact alongside security concerns.

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
*Analysed by Claude on 2026-05-24*
