# Several XSS affecting Zomato.com and developers.zomato.com

## Metadata
- **Source:** HackerOne
- **Report:** 114631 | https://hackerone.com/reports/114631
- **Submitted:** 2016-02-04
- **Reporter:** harrymg
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there, I have found several XSS in Zomato.com and developers.zomato.com

A. Steps to reproduce:
1. Go to zomato.com
2. Look for any restaurant
3. Click "Write review" and enter the payload as your review
                                             (<img src=x onerror=alert(document.domain)>)
4. Click "Publish review" . XSS pop up

B. Now in developers.zomato.com:
1. Go to developers.zomato.com

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

Hi there, I have found several XSS in Zomato.com and developers.zomato.com

A. Steps to reproduce:
1. Go to zomato.com
2. Look for any restaurant
3. Click "Write review" and enter the payload as your review
                                             (<img src=x onerror=alert(document.domain)>)
4. Click "Publish review" . XSS pop up

B. Now in developers.zomato.com:
1. Go to developers.zomato.com
2. Go to "widgets" tab
3. Look for "Restaurant Search" widget and click "Add Widget"
4. Now a window will open (restaurant search), on the left side, you will see "Search for restaurant, cuisine or a dish" now, enter the payload   (<img src=x onerror=alert(document.domain)>) in the seachbar, XSS popup.

C. developers.zomato.com (II)
1. Go to developers.zomato.com
2. Go to "widgets" tab
3. Look for "Foodie Index Widget"
4. Click "add widget"
5. In the longitude and latitude, enter the XSS payload
 (<img class="emoji" alt="😯" src="x" /><svg onload=prompt(document.domain)>). 
6. XSS popup

I hope you fix this since this are affecting several zomato users.
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
