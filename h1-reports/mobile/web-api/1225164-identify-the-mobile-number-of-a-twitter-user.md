# Information Disclosure - Mobile Number Enumeration via Differential Error Response Analysis

## Metadata
- **Source:** HackerOne
- **Report:** 1225164 | https://hackerone.com/reports/1225164
- **Submitted:** 2021-06-12
- **Reporter:** aymen_mansour
- **Program:** Twitter (HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Information Disclosure, Timing/Response-based Enumeration, Insufficient Rate Limiting, Flawed SMS Verification Logic
- **CVEs:** None
- **Category:** web-api

## Summary
A vulnerability in Twitter's SMS-based account recovery mechanism allows attackers to enumerate and identify the complete mobile number of any user by analyzing differential error messages. By repeatedly triggering SMS code requests and observing rate-limit messages, an attacker can distinguish the victim's actual number from decoys through brute-force enumeration combined with country-specific phone number formatting.

## Attack scenario
1. Attacker identifies target Twitter username and determines victim's country of origin
2. Attacker accesses Twitter's password reset/SMS verification endpoint with the target username
3. Attacker repeatedly requests SMS codes to trigger rate-limiting on the actual registered number
4. Attacker observes that the legitimate number returns 'exceeded attempts' message while fake numbers return 'code will be sent' message
5. Attacker uses country-specific phone number ranges and operator codes to brute-force the partial number format (e.g., 26-27 prefix for specific region)
6. Attacker enumerates remaining digits (10,000 combinations) and identifies the victim's complete mobile number by matching the rate-limit response pattern

## Root cause
Twitter's SMS verification system failed to implement proper controls: (1) Insufficient rate limiting across different phone numbers, (2) Differential error messages that leak information about which numbers are account-associated, (3) No protection against enumeration attacks on the account recovery endpoint, (4) Lack of constant-time responses or response obfuscation

## Attacker mindset
An attacker seeks to enumerate PII (personally identifiable information) to support further attacks such as SIM swapping, social engineering, account takeover, or harassment. The systematic approach using country-specific formatting and operator codes demonstrates careful reconnaissance and optimization of the brute-force attack surface.

## Defensive takeaways
- Implement aggressive rate limiting per IP/session across all SMS request endpoints, not per phone number
- Return identical error messages regardless of whether a number is associated with an account
- Add delays and randomization to response times to prevent timing-based enumeration
- Implement CAPTCHA or similar challenges after N failed attempts at the endpoint level
- Log and alert on suspicious enumeration patterns (multiple similar number requests)
- Use account verification tokens instead of rate-limit state that persists across attempts
- Monitor for brute-force patterns targeting phone number ranges with specific prefixes
- Implement per-account limits on password recovery attempts, not just per-number limits

## Variant hunting
Similar enumeration attacks on email-based password recovery flows that leak account existence
Phone number enumeration on two-factor authentication setup endpoints
Differential responses in account linking/unlinking features that accept phone numbers
Username enumeration combined with phone number association during onboarding
Response time analysis on SMS delivery endpoints to infer phone number validity
Enumeration of associated email addresses through similar differential response patterns
Account recovery endpoints on other platforms (Instagram, Telegram, WhatsApp) with SMS verification

## MITRE ATT&CK
- T1589 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information
- T1598 - Phishing for Information
- T1040 - Network Sniffing (related to SMS interception post-enumeration)
- T1110 - Brute Force
- T1016 - System Network Configuration Discovery

## Notes
The writeup demonstrates sophisticated attack methodology combining enumeration, rate-limit abuse, and probabilistic analysis. The attacker's use of country-specific operator codes to reduce search space from billions to thousands shows practical optimization. The core weakness is Twitter's failure to implement constant-time, uniform responses on security-critical endpoints. This is a critical privacy issue as phone numbers are sensitive PII often used as secondary identifiers. The vulnerability likely affected all users and required no authentication, making it highly exploitable at scale.

## Full report
<details><summary>Expand</summary>

**Summary:** 
By exploiting this security vulnerability we can detect the mobile number of a twitter user.


**Description:**
This security vulnerability is of type "Information disclosure" it allows to exploit Flawed behavior of the twitter system to obtain distinct responses when different error states occur.
This security vulnerability allows to identify the mobile number of a twitter user from its USER_NAME.

## Steps To Reproduce:

We explain how to get the mobile number which is (██████████) from the following twitter user "███"==> USER_NAME = ████

1.access the following url: "████" and enter user name "██████" and click search. (see screenshot "1.PNG")
2. At this step twitter  displays the last 2 digits of mobile number through this message "text a code to the phone number ending in 15", the last two digits are 15, click on next.(see screenshot "2.PNG")
3. repeat step number 2 several times, i.e. repeat asking to receive the code several times until you get the following message: "You've exceeded the number of attempts. Please try again later."(see screenshot "3.PNG")
4.Now twitter  block sends it sms code to the number associated with the victim's twitter  account which ends with two digits 15

====> twitter  block sends it again sms for the correct victim mobile number, ie "████████" but it does not block it sends sms to any other different mobile number at ███ (the probability that twitter block sends an sms to mobile number different to █████████ which ends in 15 and has the following format &&&&&&15 at the time of launching the attack is 0.000001% ) so we can use the "Forgot Password" feature and ask to receive an sms on all the following format numbers &&&&&&15 and the attempt which returns the following message: "You've exceeded the number of attempts. Please try again later."is an attempt associated with the victim mobile number.

==> an attempt to receive an SMS code at the mobile number of the following format: &&&&&&15 may return 3 different messages:
1st message : Number not associated with a twitter  account
2nd message : "You'll recive a code to verify here so you can reset your accont password." ==> this is not the victim mobile number .(see screenshot "7.PNG" and "8.PNG" )
3rd message: "You've exceeded the number of attempts. Please try again later". ==> this is the victim mobile number (see screenshot "4.PNG" and "5.PNG" and "6.PNG"  )


5. to identify the mobile number we will access this url "████████" and try to request sms code on all the mobile numbers that end by 15 which follows this format &&&&&&15 that is to say make a brute force on all the number which ends in 15, therefore the request which tries to recive sms code associating with the correct victim number account will display the following message: "You've exceeded the number of attempts. Please try again later" on the other side any other request that is not associated with victim's correct mobile number will display the following message: "You'll recive a code to verify here so you can reset your accont password." or a number not associated with a twitter account.


===>we can deduce the number of victim's digit according to the user's country or we can easily deduce it, the victim's country is "██████" so the format of its number is as follows: &&&&&&15, To accelerate the brute force and decipher the correct digits more quickly associated with this number &&&&&&15 we will use the following information:
the mobile number for the ████ region begins with the following operator phone code: (26-27) (56-57)
, so we are now going to brute force on this number range:
26&&&&15 ... 27 &&&&15
56&&&&15 ... 57&&&&15

we have 10 ^ 4 = 10000 mobile number to test each time to identify the correct victim mobile number, we eliminate the numbers that are not associated with a twitter account then determine which number blocked by twitter from receiving sms that returns the message next: "You've exceeded the number of attempts. Please try again later" , this is the victim mobile number.

## Impact: [add why this issue matters]
This issue has a critical impact on user privacy

## Impact

Attacker has a critical impact on the confidentiality  of the twitter user

</details>

---
*Analysed by Claude on 2026-05-24*
