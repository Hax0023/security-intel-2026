# Unprivileged Stored XSS via wp_targeted_link_rel Attribute Injection

## Metadata
- **Source:** HackerOne
- **Report:** 509930 | https://hackerone.com/reports/509930
- **Submitted:** 2019-03-14
- **Reporter:** simonscannell
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Attribute Injection, Input Validation Bypass
- **CVEs:** CVE-2019-16773
- **Category:** web-api

## Summary
The wp_targeted_link_rel() function in WordPress improperly parses HTML attributes using regex that ignores attribute boundaries, allowing attackers to inject event handlers through malformed rel attributes. By placing a rel attribute inside another attribute's value and omitting delimiters, attackers can break attribute boundaries and inject arbitrary event handlers that bypass sanitization filters.

## Attack scenario
1. Attacker creates a user account on a BuddyPress forum or WordPress site
2. Attacker edits their user profile/bio and injects payload: <a href="#" title=" target='abc' rel= onmouseover=alert(/XSS/) ">PoC</a>
3. The wp_targeted_link_rel() filter processes the link and detects the unquoted rel=abc attribute
4. Filter adds quotes around rel value, breaking the outer title attribute: rel="abc" creates an extra quote character
5. The injected onmouseover event handler becomes valid HTML outside the title attribute
6. When site visitors view the attacker's profile and hover over the link, the JavaScript executes in their browser context

## Root cause
The wp_targeted_link_rel() function uses a simplistic regex pattern (|rel\s*=([^\s]*)|i) that matches rel attributes without considering their position within the attribute string or proper HTML parsing. When a rel attribute is found without delimiters, the function defaults to adding double quotes. The str_replace() operation then injects these quotes into the original attribute string without re-validating the HTML structure, breaking attribute boundaries when the rel attribute is embedded within another attribute's value.

## Attacker mindset
An unprivileged user seeking to escalate impact through profile-based payload injection. The attacker recognizes that user descriptions are often displayed without strict sanitization and that the vulnerable filter runs before content security filters. By crafting a malicious user bio, the attacker achieves persistent stored XSS affecting all site visitors who view the profile, potentially enabling account compromise or worm-like propagation.

## Defensive takeaways
- Use proper HTML parsing libraries (DOMDocument) instead of regex for attribute manipulation
- Parse attributes before modifying them, not after insertion back into HTML
- Ensure sanitization filters execute before output-modifying filters like wp_targeted_link_rel()
- Apply consistent sanitization order across all content types (user bios should follow same kses filter ordering as posts)
- Validate HTML structure integrity after attribute modifications
- Consider using established utility functions like parse_shortcode_atts() for safe attribute parsing
- Implement attribute-level escaping rather than string-level replacements

## Variant hunting
Search for other WordPress filters or plugins that: (1) use regex to parse HTML attributes without proper boundary checking, (2) apply filters before kses sanitization, (3) perform str_replace on matched attributes without re-parsing, (4) handle user-controlled content in profile fields, bios, or custom post types. Check BuddyPress extensions, forum plugins, and user profile plugins for similar attribute injection vulnerabilities.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link
- T1566: Phishing
- T1204: User Execution
- T1547: Boot or Logon Autostart Execution

## Notes
This vulnerability is particularly impactful because: (1) it requires no special privileges, (2) it affects stored content viewed by multiple users, (3) it can be made wormable by injecting the same payload into other users' profiles through XSS, (4) BuddyPress displays user bios prominently, (5) the filter order difference between user descriptions and other content types makes this a logic error rather than simple oversight. The researcher demonstrated excellent vulnerability analysis by tracing the filter execution order and identifying why user descriptions are uniquely vulnerable compared to post content.

## Full report
<details><summary>Expand</summary>

The user description is vulnerable to a Stored XSS via an attribute injection. At fault is the `wp_targeted_link_rel()` filter that parses attributes regardless of their position.

```
function wp_targeted_link_rel( $text ) {
	// Don't run (more expensive) regex if no links with targets.
	if ( stripos( $text, 'target' ) !== false && stripos( $text, '<a ' ) !== false ) {
		$text = preg_replace_callback( '|<a\s([^>]*target\s*=[^>]*)>|i', 'wp_targeted_link_rel_callback', $text );
	}
```

It essentially just parses the attribute string of all `<a>` tags and passes them to the preg replace callback.

```
function wp_targeted_link_rel_callback( $matches ) {
	$link_html = $matches[1];
	$rel_match = array();
...
// Value with delimiters, spaces around are optional.
	$attr_regex = '|rel\s*=\s*?(\\\\{0,1}["\'])(.*?)\\1|i';
	preg_match( $attr_regex, $link_html, $rel_match );

	if ( empty( $rel_match[0] ) ) {
		// No delimiters, try with a single value and spaces, because `rel =  va"lue` is totally fine...
		$attr_regex = '|rel\s*=(\s*)([^\s]*)|i';
		preg_match( $attr_regex, $link_html, $rel_match );
	}
```

As can be seen it then uses a regex to parse the `rel` attribute, its value and its delimeter from the string.

If the rel attribute is found, the following happens:

```

	if ( ! empty( $rel_match[0] ) ) {
		$parts     = preg_split( '|\s+|', strtolower( $rel_match[2] ) );
		$parts     = array_map( 'esc_attr', $parts );
		$needed    = explode( ' ', $rel );
		$parts     = array_unique( array_merge( $parts, $needed ) );
		$delimiter = trim( $rel_match[1] ) ? $rel_match[1] : '"';
		$rel       = 'rel=' . $delimiter . trim( implode( ' ', $parts ) ) . $delimiter;
		$link_html = str_replace( $rel_match[0], $rel, $link_html );
```

As you can see the value of the `rel` attribute is splitted by whitespaces and each part is then escaped. The targeted `rel` value is then added to the alread existing ones and put back together.

Most importantly, are the following line:

```
		$delimiter = trim( $rel_match[1] ) ? $rel_match[1] : '"';
		$rel       = 'rel=' . $delimiter . trim( implode( ' ', $parts ) ) . $delimiter;
		$link_html = str_replace( $rel_match[0], $rel, $link_html );
```
if the delimeter is empty (e.g. when `rel=abc` has no quotes), the delimer becomes  `"`. The original rel attribute is then replaced with the new one. 

This is a problem since the following payload:

`<a title="  target='xyz'  rel=abc ">PoC</a>`

would turn into

`<a title=" target='xyz' rel="abc" ">PoC</a>` Note that an additional `"` has been injected and the title attribute has been escaped.

This is because the regex to match the rel attribute ignores the position of the `rel` attribute within the attribute string. The above payload shows how the rel attribute is placed within a double quoted attribute. Since no delimeter is set, the delimer becomes a double quote and when the rel attribute is inserted back into the string, the double quote is injected.

I recommend using something like `parse_shortcode_atts()` as in `wp_rel_nofollow()` to prevent this from happening.

By abusing the attribute injection, it is easily possible to create a Stored XSS payload. 

Tge `wp_targeted_link_rel()` filter is not only called on the user description, however, this is where it becomes exploitable. This is because this vulnerable filter is added before the `kses` filters are added, which means that the injected attribute would be caught by `wp_post_kses()`. The user description is the only exception where the kses filters are called before `wp_targeted_link_rel()` is called.

`<a href="#" title=" target='abc' rel= onmouseover=alert(/XSS/) ">This is a PoC for a Stored XSS</a>`


## Proof of Concept

The following will demonstrate how a normal forum user can achieve stored XSS on their profile page in BuddyPress
████████

1. This works if the Bio of forum users is displayed in their profile page. Log in as an administrator and go to Appearence -> Customize and then BuddyPress Nouveu -> Member front page and make sure that displaying the user bio is enabled

2. Create a normal forum user account
3. Login and edit your profile. Paste 
`<a href="#" title=" target='abc' rel= onmouseover=alert(/XSS/) ">This is a PoC for a Stored XSS</a>` as your user description
4. visit your profil and hover over the link.

## Impact

The Impact of this can vary from site to site. I have shown how this can be exploited in BuddyPress as a mere, normal forum user. Since you can also inject a style attribute and make the link span over the entire page, one can turn this into a wormable Stored XSS in BuddyPress.

Basically every plugin or forum is affected that displays the user description.

</details>

---
*Analysed by Claude on 2026-05-12*
