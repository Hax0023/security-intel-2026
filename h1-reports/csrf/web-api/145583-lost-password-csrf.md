# Lost Password CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 145583 | https://hackerone.com/reports/145583
- **Submitted:** 2016-06-17
- **Reporter:** mefkan
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I think it is something about your Wordpress version.It's not something highy risky bu it is vulnerability.

CODE:

<form name="lostpasswordform" id="lostpasswordform" action="https://nextcloud.com/wp-login.php?action=lostpassword" method="post" style="position: static; left: 0px;">
	<p>
		<label for="user_login">Username or Email<br>
		<input type="text" name="user_login" id="user_login" cla

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

I think it is something about your Wordpress version.It's not something highy risky bu it is vulnerability.

CODE:

<form name="lostpasswordform" id="lostpasswordform" action="https://nextcloud.com/wp-login.php?action=lostpassword" method="post" style="position: static; left: 0px;">
	<p>
		<label for="user_login">Username or Email<br>
		<input type="text" name="user_login" id="user_login" class="input" value="" size="20"></label>
	</p>
		<input type="hidden" name="redirect_to" value="">
	<p class="submit"><input type="submit" name="wp-submit" id="wp-submit" class="button button-primary button-large" value="Get New Password"></p>
</form>



For testing CSRF  I added the .html file to attachments.And there is a screenshot for you.


How To Fix :

Adding rp_key will be fine.

Please take a look at links below

https://wpvulndb.com/vulnerabilities/7691
https://core.trac.wordpress.org/changeset/30418

Best Regards,

</details>

---
*Analysed by Claude on 2026-05-24*
