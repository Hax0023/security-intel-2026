# Uber Driver Referral SMS Flooding via Unvalidated Phone Number Input

## Metadata
- **Source:** HackerOne
- **Report:** 141339 | https://hackerone.com/reports/141339
- **Submitted:** 2016-05-27
- **Reporter:** anish2good
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Insufficient Input Validation, Lack of Rate Limiting, Lack of Phone Number Ownership Verification, SMS Bombing, Abuse of Functionality
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Uber driver referral system allows attackers to trigger repeated SMS messages to arbitrary phone numbers without validating ownership or implementing proper rate limiting. By fuzzing the /driver_invitations endpoint with the same target phone number, attackers can cause 60 SMS messages (split into 3 parts due to message length) to be sent daily to victim phone numbers, effectively enabling SMS flooding/bombing attacks.

## Attack scenario
1. Attacker identifies the POST /driver_invitations endpoint at partners.uber.com/referrals/
2. Attacker crafts malicious JSON payload with target victim's phone number in the 'mobiles' parameter
3. Attacker submits requests via fuzzing tool (OWASP ZAP) with high frequency to trigger SMS sends
4. Uber's backend sends SMS invitations without validating phone number ownership or implementing adequate rate limits
5. Victim receives 60 SMS messages daily (starting at 9:30 AM IST) on consecutive days without any way to stop them
6. Attack can be repeated against multiple phone numbers to disrupt service and damage Uber's reputation

## Root cause
The application fails to implement adequate controls: (1) No phone number ownership verification before sending SMS, (2) Insufficient rate limiting per phone number or per user/IP, (3) No CAPTCHA or challenge-response mechanism to prevent automated abuse, (4) Lack of request validation to ensure legitimate use cases only

## Attacker mindset
Malicious actor seeks to harass arbitrary users or damage Uber's brand reputation by weaponizing the referral system. The attacker exploits the absence of friction in the SMS sending flow, using automated fuzzing tools to overwhelm victims with unsolicited messages at scale with minimal effort.

## Defensive takeaways
- Implement strict rate limiting per phone number (e.g., max 1-2 SMS per day per number)
- Require phone number ownership verification (e.g., OTP confirmation) before sending referral SMS
- Add CAPTCHA/proof-of-work challenge on referral forms to prevent automated abuse
- Implement per-user/per-IP request throttling on the /driver_invitations endpoint
- Add recipient phone number validation and blacklist/feedback mechanisms
- Implement monitoring and alerts for unusual SMS sending patterns
- Require authentication and session validation for referral requests
- Implement exponential backoff or cooldown periods for repeated requests from same source
- Add audit logging for all SMS sends including source IP, user, timestamp, and recipient

## Variant hunting
Search for similar SMS/notification flooding vulnerabilities in: invitation systems (event, restaurant, delivery), password reset flows, verification code resends, notification preference endpoints, promotional SMS features, and any unauthenticated or weakly authenticated messaging functionality. Check for insufficient rate limiting on POST endpoints handling bulk communication.

## MITRE ATT&CK
- T1190
- T1584
- T1589
- T1598
- T1566

## Notes
The report demonstrates practical exploitation using OWASP ZAP fuzzing with 10,000 requests, clearly proving the vulnerability is exploitable at scale. The daily recurring nature suggests a scheduled task triggered by the initial abuse, potentially amplifying impact over time. The attacker demonstrates understanding of the 60 SMS (20 requests × 3 part messages) formula, indicating either empirical discovery or insider knowledge. This vulnerability combines elements of SMS bombing, harassment, and denial-of-service against end users.

## Full report
<details><summary>Expand</summary>

The Issue is with the design of sending SMS by the uber referrals system, and every day it's flodding my phone number with driver invitaion message 

To reproduce this scenario i have  Fuzz the below request Through OWSAP Zap I fuzzed for 10,000 requests , keep the same Phone number (I have used my number), After 20 tries uber will send message the Limit is over ,  you will recieve 60 SMS since the meessage size is more it will come in three part , 

Now the real proble will start from next and consecutive days, Every day i'm recieving 60 SMS starting at 9:30 AM IST 
------------------------------

```
POST https://partners.uber.com/driver_invitations HTTP/1.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: br
Content-Type: application/json; charset=utf-8
X-Requested-With: XMLHttpRequest
Referer: https://partners.uber.com/referrals/
Content-Length: 137
Cookie: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Connection: keep-alive
Host: partners.uber.com

{"_csrf_token":"1464319290-01-TE_leQUArIag4-5PKfW4wUkBccZdc_thW8kqNBmFFu4=","emails":[],"mobiles":["+████████"],"source":"dashboard"}
```

>>>>>>Attack Scenarion: A bad Victim can use this tool to irritate the other user (irrespective of their postion), by creating fake profiles and let's Uber take care of sending 60 SMS every day (NON STOP)  and finaly it will lead bad Impression on the UBER and 


</details>

---
*Analysed by Claude on 2026-05-24*
