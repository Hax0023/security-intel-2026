# OAuth access_token stealing in Phabricator

## Metadata
- **Source:** HackerOne
- **Report:** 3596 | https://hackerone.com/reports/3596
- **Submitted:** 2014-03-10
- **Reporter:** krangbuster
- **Program:** Unknown
- **Bounty:** $450
- **Severity:** unknown
- **Vuln:** Open Redirect
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi,

I found that an attacker is able to steal access_tokens of facebook users via Phabricator App (184510521580034).

when users login to phabricator, they can choose to login via Facebook (https://secure.phabricator.com/login/) attaching pic, In this case an attacker is able to exploit this behavior to steal facebook access_tokens via phabricator app.

Full Reproduce, Exploit:

1. Create

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

I found that an attacker is able to steal access_tokens of facebook users via Phabricator App (184510521580034).

when users login to phabricator, they can choose to login via Facebook (https://secure.phabricator.com/login/) attaching pic, In this case an attacker is able to exploit this behavior to steal facebook access_tokens via phabricator app.

Full Reproduce, Exploit:

1. Create a blog on phabricator https://secure.phabricator.com/phame/blog/new/
and provide a custom domain, in this case: files.nirgoldshlager.com

2. send a malicious link to the victim: https://www.facebook.com/dialog/oauth?client_id=184510521580034&response_type=token&redirect_uri=https://secure.phabricator.com/phame/live/47/ , Click Continue

when the victim will click continue, his access token will be send to my malicious server, saved in a log file under: http://files.nirgoldshlager.com

PoC Video:

https://drive.google.com/file/d/0B2-5ltUODX1LWHV6R3gxSFAwNzQ/edit?usp=sharing


</details>

---
*Analysed by Claude on 2026-05-24*
