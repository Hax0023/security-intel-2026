# Abuse of Api that causes spamming users and possible DOS due to missing rate limit

## Metadata
- **Source:** HackerOne
- **Report:** 223557 | https://hackerone.com/reports/223557
- **Submitted:** 2017-04-24
- **Reporter:** khalidamin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** api
- **CVEs:** None
- **Category:** uncategorised

## Summary
##Summary:
In your sub-domain: http://demo.weblate.org , another endpoint doesn't have any rate limit on it to prevent spamming you by posting a lot of questions.

##Description:
Spamming and Possible DOS is being possible due to missing rate limit on this endpoint.

**Request**
POST /accounts/email/ HTTP/1.1
Host: demo.weblate.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20

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

##Summary:
In your sub-domain: http://demo.weblate.org , another endpoint doesn't have any rate limit on it to prevent spamming you by posting a lot of questions.

##Description:
Spamming and Possible DOS is being possible due to missing rate limit on this endpoint.

**Request**
POST /accounts/email/ HTTP/1.1
Host: demo.weblate.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://demo.weblate.org/
Cookie: XXX
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 126

csrfmiddlewaretoken=&email=victim_email&content=



</details>

---
*Analysed by Claude on 2026-05-24*
