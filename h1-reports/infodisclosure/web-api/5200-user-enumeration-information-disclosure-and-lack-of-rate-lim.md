# User Enumeration, Information Disclosure and Lack of Rate Limitation on Coinbase Request Money API

## Metadata
- **Source:** HackerOne
- **Report:** 5200 | https://hackerone.com/reports/5200
- **Submitted:** 2014-03-30
- **Reporter:** zero
- **Program:** Coinbase
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** User Enumeration, Information Disclosure, Lack of Rate Limiting, Spam/Abuse
- **CVEs:** None
- **Category:** web-api

## Summary
Coinbase's request money API endpoint lacked rate limiting, allowing attackers to send unlimited money request emails to enumerate valid user accounts and extract PII. The API disclosed whether an email belonged to a Coinbase member by displaying full names for members versus email-only for non-members in transaction history.

## Attack scenario
1. Attacker logs into Coinbase account and navigates to the request money feature
2. Attacker captures the POST request to /transactions/request_money using a proxy tool
3. Attacker modifies the request to use different email addresses and replays it without rate limit restrictions
4. Attacker sends requests to hundreds of email addresses across multiple threads simultaneously
5. Attacker checks the /transactions/ page to identify which emails are Coinbase members (displayed as full names) versus non-members (displayed as email only)
6. Attacker collects enumerated Coinbase user accounts with their full names for targeting or further attacks

## Root cause
The /transactions/request_money endpoint lacked rate limiting controls and the transaction history display logic differentiated between Coinbase members and non-members in a user-visible way, enabling both enumeration and information leakage through observable response differences.

## Attacker mindset
An attacker would recognize that the money request feature can be abused as a reconnaissance tool to identify valid Coinbase users at scale without consequences. They would leverage the lack of rate limiting and the information leakage in the UI to build a list of valid accounts with names for social engineering, credential stuffing, or targeted attacks.

## Defensive takeaways
- Implement strict rate limiting on all user-facing API endpoints, especially those involving external communications
- Ensure UI responses do not leak information about whether accounts exist based on visual differences (names vs emails)
- Normalize transaction history display to avoid disclosing membership status
- Implement CAPTCHA or additional verification for bulk request operations
- Add monitoring and alerting for suspicious patterns (multiple requests from single user in short timeframe)
- Consider implementing exponential backoff or account-level request quotas
- Log and review all API abuse patterns to identify enumeration attempts

## Variant hunting
Check other Coinbase endpoints for similar user enumeration via visual display differences (send/transfer, payments, etc.)
Test for rate limiting on password reset, login, and account recovery endpoints
Examine other financial APIs for similar enumeration through transaction history or money movement features
Look for leaked PII in API responses (names, phone numbers, addresses) when performing bulk operations
Test multi-threaded requests against other endpoints to identify missing rate limits
Check if similar user enumeration exists in notification or message features

## MITRE ATT&CK
- T1590.003 - Gather Victim Identity Information: Email Addresses
- T1598.003 - Phishing: Spearphishing Link
- T1592 - Gather Victim Account Information
- T1087 - Account Discovery
- T1038 - Data from Local System (information disclosure)

## Notes
This report demonstrates a classic security anti-pattern where information leakage combines with lack of access controls to enable account enumeration at scale. The reporter's frustration with the initial response suggests the vendor may not have fully understood the enumeration risk. The use of animated GIF proof-of-concept helped demonstrate the practical exploitation. The vulnerability is particularly severe for financial platforms where user enumeration enables social engineering and targeted attacks.

## Full report
<details><summary>Expand</summary>

NOTE: I am making this email as I think the response from Coinbase originally, via my emails to them was not correct. They had not acknowledged that this flaw allowed for user enumeration and hence I am posting the report again - in hope of a proper and well evaluated response.

The key security issue however, is that after x amount of email addresses are sent requests for money (rate limiting issue, using coinbase email for spam), the users which are members of coinbase can be differentiated between non-members.

Additionally, there is further information disclosure, as the first and last name of the coinbase users email address is also disclosed.

Hence I believe the following impacts are:

1. Unlimited money request emails, spam

2. Email Address / User enumeration on Coinbase

3. Information Disclosure of Coinbase Accounts (First and Last name)

    Steps to reproduce the issue or a proof of concept

To reproduce the vulnerability:

1. Login to Coinbase.

2. Visit https://coinbase.com/transactions

3. Click the Request Money button at the top

4. In the from field, insert a coinbase user accounts email address: e.g. ████

5. The rest of the fields can be entered in as usual

6. Click the Request Money button

7. In this stage, capture the request using a proxy, e.g. Burp Suite

8. If done correctly, the request should look like the following:

    POST /transactions/request_money HTTP/1.1
    Host: coinbase.com
    User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0
    Accept: */*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    X-CSRF-Token: QXdn0YJf9N7wsbI9QQcyDowBqsaEI6bUB8COSqLh2sI=
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    X-Requested-With: XMLHttpRequest
    Referer: https://coinbase.com/transactions
    Content-Length: 213
    Cookie: _coinbase_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTdlMWRiNTQ1ZGY0ZWQxMjA2N2E2OWEyM2U2NzBmNGJjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXJRY0owUWsrSlYrb0hUZDlQM3AwZ0R2cUlqeVlWOTVmUCtSMHVqUUdYckU9BjsARg%3D%3D--b3a84dd08d3654246378c244c2d25b83efaace5b; df=f1e650f064a5d9637c5b4710e49593a2; _coinbase=BAh7C0kiEWxhc3RfdXNlcl9pZAY6BkVGVToaTW9wZWQ6OkJTT046Ok9iamVjdElkIhFTDzZ2yroQA7EAAlFJIhBfY3NyZl90b2tlbgY7AEZJIjFRWGRuMFlKZjlON3dzYkk5UVFjeURvd0Jxc2FFSTZiVUI4Q09TcUxoMnNJPQY7AEZJIg9zZXNzaW9uX2lkBjsARkkiJTExZDMzZmU0N2E1YWJiNDVhNTA4MWY1ZTc5MWVjNTZjBjsAVEkiFGxhc3RfcmVxdWVzdF9hdAY7AEZsKwf0PQ9TSSISc2Vzc2lvbl90b2tlbgY7AEYiRTVhY2Q0NGFmNDFmODFjMTliMGUwODYwOGMyN2RjNTgxN2RkOTlhY2IyMTQ2OWI1MDEyN2M2ZmRlNTU1NGU5OGRJIhJidXR0b25fcGFyYW1zBjsARkM6LUFjdGl2ZVN1cHBvcnQ6Okhhc2hXaXRoSW5kaWZmZXJlbnRBY2Nlc3N7CUkiCWNvZGUGOwBUSSIlOTE0YWM0Yjk1NDA3YTExODZiNjg1NDEzYWViNjc3N2IGOwBUSSINcmVmZXJyZXIGOwBUSSIRY29pbmJhc2UuY29tBjsAVEkiCXV0ZjgGOwBUSSII4pyTBjsAVEkiF2F1dGhlbnRpY2l0eV90b2tlbgY7AFRJIjFRWGRuMFlKZjlON3dzYkk5UVFjeURvd0Jxc2FFSTZiVUI4Q09TcUxoMnNJPQY7AFQ%3D--c083b1c8e179ed6cfaa0f4b0d28b591b7d446247; request_method=GET; _cb_cookie_test=true; wcsid=raGNP96CtPB3NiHR1T41E5Z2IEgpD2FC; hblid=6yunfgNtaUi6mcv91T41E5V2IEtCA0K0; _oklv=1393507811571%2CraGNP96CtPB3NiHR1T41E5Z2IEgpD2FC; olfsk=olfsk42341207274371073; _ok=8678-140-10-4291; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1393505916467%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; __cfduid=d1e5585dec9616cee843e28044a6324451393507051048; return_to=; __ssid=d1bedf38-8c4d-4ad6-837e-de61ac0ff777; 914ac4b95407a1186b685413aeb6777b=530f3b68467d61cc1100033a
    Connection: keep-alive
    Pragma: no-cache
    Cache-Control: no-cache

    utf8=%E2%9C%93&authenticity_token=QXdn0YJf9N7wsbI9QQcyDowBqsaEI6bUB8COSqLh2sI%3D&transaction%5Bfrom%5D=place_email_here&transaction%5Bamount%5D=0.001&transaction_amount_converted=0.59&transaction%5Bnotes%5D=Test

9. This request can now be replayed unlimited times, with unlimited email addresses inputted. Coinbase does not limit the rate of POST requests to /transactions/request_money
10. After x number of requests are sent to /transactions/request_money, visit /transactions/
11. It can be identified that those who are NOT members of Coinbase, show up as email addresses only, whereas those WHO ARE members of Coinbase, show up as Full Names. --> Email Address / User Account enumeration
12. Furthermore, the coinbase members whose emails are identified, have their full names disclosed to the attacker. Information Leakage

I have attached a GIF showing this entire process. I attempted 80 email addresses, 5 threads simultaneously via Burp Suite Intruder. Either download the GIF attached in this email, or visit http://uppix.net/0XKQ4v.gif.

Thanks for your time,

██████████

</details>

---
*Analysed by Claude on 2026-05-24*
