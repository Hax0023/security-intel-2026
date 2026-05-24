# Periscope android app deeplink leads to CSRF in follow action

## Metadata
- **Source:** HackerOne
- **Report:** 583987 | https://hackerone.com/reports/583987
- **Submitted:** 2019-05-18
- **Reporter:** kunal94
- **Program:** Unknown
- **Bounty:** $1,540
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Twitter Team

#Summary
This issue is mainly in the Periscope Android app against CSRF follow action using deeplink.

#Description
In normal Periscope Website, when we share a follow link like `www.pscp.tv/<user-id>/follow`, we get a response whether to follow a person or not, giving us an option, means CSRF protection is there in Periscope web application.
However, in the Periscope Android A

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

Hello Twitter Team

#Summary
This issue is mainly in the Periscope Android app against CSRF follow action using deeplink.

#Description
In normal Periscope Website, when we share a follow link like `www.pscp.tv/<user-id>/follow`, we get a response whether to follow a person or not, giving us an option, means CSRF protection is there in Periscope web application.
However, in the Periscope Android App, there are some internal deep links by which we can perform Direct CSRF in terms of the following user using internal deeplinks.

#POC

In Android Manifest XML file, internal deeplinks are described as

```html
<data android:host="user" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="user" android:pathPrefix="/" android:scheme="pscpd"/>
<data android:host="broadcast" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="broadcast" android:pathPrefix="/" android:scheme="pscpd"/>
<data android:host="channel" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="channel" android:pathPrefix="/" android:scheme="pscpd"/>
<data android:host="discover" android:pathPrefix="/" android:scheme="pscp"/>
<data android:host="discover" android:pathPrefix="/" android:scheme="pscpd"/>
```
+ It means we can use ` pscp://user/<user-id> or pscpd://user/<user-id>`
+ Now,normally if we share follow link from website, it'll be like this, `www.pscp.tv/<user-id>/follow`, further give us option to follow them or not.

+ In deeplink, we can use the same follow-link in this way - `pscp://user/user-id/follow`, Once you visit this link from the browser, you'll directly follow any person in periscope android app.

+ Here is the Final POC
```html
<!DOCTYPE html>
<html>
<a href="pscp://user/<any user-id>/follow">CSRF DEMO</a>
</html>
```
+ Visit the above POC html page from android chrome browser, click on link and you'll follow anyone directly inside Periscope android app.

#Attachment (Video)
{F492266}

+ App Info - Periscope V 1.25.5.93

Thanks
Kunal

## Impact

+ Using Periscope deeplink like pscp://user/user-id/follow, it's possible to perform Direct CSRF Follow against any user in periscope android app.

</details>

---
*Analysed by Claude on 2026-05-24*
