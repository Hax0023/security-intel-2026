# SSRF in rompager-check

## Metadata
- **Source:** HackerOne
- **Report:** 374818 | https://hackerone.com/reports/374818
- **Submitted:** 2018-06-30
- **Reporter:** bb9866f3f743d6bf69b6836
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary

The script `rompager.php` does not restrict which hosts can be requested. Thereby, an attacker can send HTTP requests to localhost and other servers of the same local network segment, on port 80 and 7547. 

## Description

In `rompager.php`, the value of `CURLOPT_URL` is fully controlled:

```php
<?php
// [...]
function checkHost($ip, $port) {
	$ch = curl_init();
	curl_setopt($ch, CURL

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

## Summary

The script `rompager.php` does not restrict which hosts can be requested. Thereby, an attacker can send HTTP requests to localhost and other servers of the same local network segment, on port 80 and 7547. 

## Description

In `rompager.php`, the value of `CURLOPT_URL` is fully controlled:

```php
<?php
// [...]
function checkHost($ip, $port) {
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, "http://".$ip);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 1);
	curl_setopt($ch, CURLOPT_TIMEOUT, 1);
	curl_setopt($ch, CURLOPT_HEADER, TRUE);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
	curl_setopt($ch, CURLOPT_PORT, $port);
	$data = curl_exec($ch);
// [...]
	} else {
		$ip = $_GET['ip'];
	}
	output("<h4>Port 80</h4>\n");
	checkHost($ip, 80);
	output("<h4>Port 7547</h4>\n");
	checkHost($ip, 7547);
```

## Steps To Reproduce

  1. Access https://rompager.hboeck.de/?ip=localhost;
  1. Notice that *No RomPager found* is shown under *Port 80*.

## Impact

An attacker could force `rompager.hboeck.de` to perform HTTP requests to localhost or servers of the same local network segment.

</details>

---
*Analysed by Claude on 2026-05-24*
