# Authenticated Cross-site Scripting in Template Name

## Metadata
- **Source:** HackerOne
- **Report:** 220903 | https://hackerone.com/reports/220903
- **Submitted:** 2017-04-14
- **Reporter:** zurke
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
###Explanation
During my research on latest WordPress I found that `$file_description`  and `$description` from `wp-admin/theme-editor.php`  are not filtering name of the template allowing attacker to do XSS attack.

```
...
		$file_description = get_file_description( $filename );

		if ( $filename !== basename( $absolute_filename ) || $file_description !== $filename ) {
			$file_description .= '<

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

###Explanation
During my research on latest WordPress I found that `$file_description`  and `$description` from `wp-admin/theme-editor.php`  are not filtering name of the template allowing attacker to do XSS attack.

```
...
		$file_description = get_file_description( $filename );

		if ( $filename !== basename( $absolute_filename ) || $file_description !== $filename ) {
			$file_description .= '<br /><span class="nonessential">(' . $filename . ')</span>';

		}

		if ( $absolute_filename === $file ) {
			$file_description = '<span class="highlight">' . $file_description . '</span>';

		}

		$previous_file_type = $file_type;
?>
		<li><a href="theme-editor.php?file=<?php echo urlencode( $filename ) ?>&amp;theme=<?php echo urlencode( $stylesheet ) ?>"><?php echo $file_description; ?></a></li>
<?php
	endforeach;
?>
```
From this code we can see that `$file_description = get_file_description( $filename );` is getting declared and later on under <li><a> tags template name is printed on the page `...<?php echo $file_description; ?></a></li>`

`$file_description` variable should be filtered before displayed to the user. For example using `htmlspecialchars()` function (example:  F175759 )

However, if victim click on the file that contain XSS payload, XSS will be executed because `$description = get_file_description( $relative_file );` is displaying name of the active file you are editing.

###Steps to replicate
1. Go to Appearance > Editor
2. Select file you want to edit (don't select files that already have name - Archives, Theme Footer for example). I used "back-compat.php" F175758
3. At the very top of the file add following comment:
```/* Template Name: <script>confirm(document.cookie);</script> */``` Like this: F175758
4. Click on Update File.
5. XSS Popup will be prompted. F175757

###Technology used: 
Google Chrome 57.0.2987.133 (64-bit) - Latest

</details>

---
*Analysed by Claude on 2026-05-24*
