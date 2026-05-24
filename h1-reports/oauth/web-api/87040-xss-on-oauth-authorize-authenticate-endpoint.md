# XSS on OAuth authorize/authenticate endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 87040 | https://hackerone.com/reports/87040
- **Submitted:** 2015-09-02
- **Reporter:** filedescriptor
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
I would like to report an issue where certain endpoints on twitter.com and api.twitter.com is vulnerable to XSS.

##Detail
The redirection page after authorization/authentication does not sanitize the *oauth_callback* parameter.

##PoC
1. Go to http://innerht.ml/pocs/twitter-oauth-xss (Please use IE or something that hasn't implemented CSP)
2. Click on Authorize app
3. Alert pops up


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

Hi,
I would like to report an issue where certain endpoints on twitter.com and api.twitter.com is vulnerable to XSS.

##Detail
The redirection page after authorization/authentication does not sanitize the *oauth_callback* parameter.

##PoC
1. Go to http://innerht.ml/pocs/twitter-oauth-xss (Please use IE or something that hasn't implemented CSP)
2. Click on Authorize app
3. Alert pops up

Note: it also affects api.twitter.com as they both have the same endpoints

##Repo step
1. Obtain the request token (https://api.twitter.com/oauth/request_token) where parameter *oauth_callback* contains HTML like ```javascript%3A%2F%2F"><script>alert(document.domain)</script>```
2. Redirect the victim to the authorize/authenticate page with the token

</details>

---
*Analysed by Claude on 2026-05-24*
