# Html Injection and Possible XSS via MathML

## Metadata
- **Source:** HackerOne
- **Report:** 502926 | https://hackerone.com/reports/502926
- **Submitted:** 2019-02-27
- **Reporter:** z41b1337_
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
I would like to report HTML Injection and possible cross site scripting (XSS) vulnerability using the MathML on Firefox.
Account title of field is vulnerable to Html Injection which can lead an attacker to store javascript using the MathML in Firefox.
Modern Firefox versions allow usage of inline MathML. While other user agents don't support the href attribute for MathML elements (yet), Firefo

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
I would like to report HTML Injection and possible cross site scripting (XSS) vulnerability using the MathML on Firefox.
Account title of field is vulnerable to Html Injection which can lead an attacker to store javascript using the MathML in Firefox.
Modern Firefox versions allow usage of inline MathML. While other user agents don't support the href attribute for MathML elements (yet), Firefox does and thereby enables passive JavaScript execution. Note that supporting href for MathML elements is a feature - introduced with MathML 3. The same effect can be observed by using xlink:href. The statusline action further enables obfuscation of the actual link target - and in this example hides the JavaScript URI.

Step to reproduce
1- Login to your mopub account.
2- Go to account settings.
3- Click on Edit user settings.
4- Add this payload in Title field 

<math href="javascript:alert(1)">CLICKME</math>

<math>
<!-- up to FF 13 -->
<maction actiontype="statusline#http://google.com" xlink:href="javascript:alert(2)">CLICKME</maction>

<!-- FF 14+ -->
<maction actiontype="statusline" xlink:href="javascript:alert(3)">CLICKME<mtext>http://http://google.com</mtext></maction>
</math>

5- Click on Submit Button.
6- HTML link will be stored in account Title.
7- Click on that html link and XSS will be executed in Firefox.

POC
Please see the images in the attachment.

## Impact

The vulnerability allow a malicious user to inject html tags and execute Javascript  which could lead to steal user's session

</details>

---
*Analysed by Claude on 2026-05-24*
