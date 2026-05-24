# SSRF via potential filter bypass with too lax local domain checking

## Metadata
- **Source:** HackerOne
- **Report:** 1608039 | https://hackerone.com/reports/1608039
- **Submitted:** 2022-06-21
- **Reporter:** tomorrowisnew_
- **Program:** Unknown
- **Bounty:** $250
- **Severity:** low
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** CVE-2022-39211
- **Category:** web-api

## Summary
## Summary:
Hi.
Reviewing the code for filtering for ssrf, in `preventLocalAddress`, we can see that it calls the function `ThrowIfLocalAddress()`. It has three common checks, first, it checks if the string is `localhost`, or if it ends in `.local` or `.localhost`
```php
		// Disallow localhost and local network
		if ($host === 'localhost' || substr($host, -6) === '.local' || substr($host, -10) ==

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
Hi.
Reviewing the code for filtering for ssrf, in `preventLocalAddress`, we can see that it calls the function `ThrowIfLocalAddress()`. It has three common checks, first, it checks if the string is `localhost`, or if it ends in `.local` or `.localhost`
```php
		// Disallow localhost and local network
		if ($host === 'localhost' || substr($host, -6) === '.local' || substr($host, -10) === '.localhost') {
			$this->logger->warning("Host $host was not connected to because it violates local access rules");
			throw new LocalServerException('Host violates local access rules');
		}
```
Second check, it checks if the provided url is only a host
```php
		// Disallow hostname only
		if (substr_count($host, '.') === 0 && !(bool)filter_var($host, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
			$this->logger->warning("Host $host was not connected to because it violates local access rules");
			throw new LocalServerException('Host violates local access rules');
		}
```
Lastly, it checks if the user input is an ip, if it is, it checks if it is not in the `FILTER_FLAG_NO_PRIV_RANGE`, or `FILTER_FLAG_NO_RES_RANGE`.
These checks lack something tho.  Checks for metadata. Specifically the Alibaba metadata, and google cloud metadata.    
Other metadata like aws and digital ocean uses 169.254.169.25 which is included in the `FILTER_FLAG_NO_RES_RANGE`. Google cloud metadata tho, can be accessed with http://metadata.google.internal  which is not in any checks from above. And the alibaba metadata can be accessed with `100.100.100.200`, this ip is neither in the `FILTER_FLAG_NO_PRIV_RANGE` or `FILTER_FLAG_NO_RES_RANGE` flags, also bypassing the check. 
This make it vulnerable to ssrf when the nextcloud host is hosted with either google cloud or alibaba

## Impact

SSRF filter bypass

</details>

---
*Analysed by Claude on 2026-05-24*
