# Server-Side Request Forgery (SSRF) on List Image Upload

## Metadata
- **Source:** HackerOne
- **Report:** 158016 | https://hackerone.com/reports/158016
- **Submitted:** 2016-08-09
- **Reporter:** eboda
- **Program:** Instacart
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Insufficient Input Validation, Lack of URL Scheme Whitelisting
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Instacart API endpoint for updating list images accepts arbitrary URLs in the `list[remote_image_url]` parameter without proper validation, allowing attackers to make the server perform requests to internal services. An attacker can probe internal network services and potentially interact with localhost ports, as demonstrated by successfully triggering a connection attempt to the SSH service on 127.0.0.1:21.

## Attack scenario
1. Attacker creates or obtains access to a list within Instacart
2. Attacker sends POST request to /api/v2/lists/[LIST_ID] with malicious remote_image_url parameter pointing to internal service (e.g., http://127.0.0.1:21, http://169.254.169.254/latest/meta-data, http://internal.service.local:8080)
3. Server performs HTTP request to the attacker-supplied URL without validation
4. Attacker receives error message or response indicating server successfully connected to the internal endpoint
5. Attacker enumerates internal services, ports, and metadata endpoints to gather sensitive information
6. Attacker potentially interacts with internal APIs, cloud metadata services, or administrative interfaces

## Root cause
The application fails to validate and sanitize the `remote_image_url` parameter before using it in a server-side HTTP request. There is no whitelist of allowed domains, no validation of URL schemes, and no restriction preventing connections to private IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) or cloud metadata endpoints.

## Attacker mindset
An attacker would recognize this as an opportunity to probe the internal network architecture without direct access, discover running services on localhost and internal networks, extract sensitive information from cloud metadata services, or potentially compromise internal systems by chaining with other vulnerabilities in internal services.

## Defensive takeaways
- Implement strict URL validation and sanitization on all user-supplied URLs before making server-side requests
- Maintain a whitelist of allowed domains or URL patterns rather than using blacklists
- Explicitly block requests to private IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, ::1, fc00::/7)
- Block requests to cloud metadata services (169.254.169.254, 169.254.170.2, etc.)
- Use only secure URL schemes (HTTPS whitelist) and reject http://, file://, ftp://, and other schemes
- Implement network-level egress filtering to prevent internal connections from application servers
- Use a dedicated image proxy service with strict configuration rather than direct URL fetching
- Log and alert on suspicious URL access attempts for security monitoring
- Implement timeouts and size limits on remote image downloads to prevent denial of service

## Variant hunting
Search for other endpoints accepting remote URLs (user avatars, profile images, banner images, document uploads)
Test other image update endpoints with SSRF payloads (list_image, item_image, recipe_image)
Check for variations in parameter names (image_url, imageUrl, image_source, remote_url)
Test alternative HTTP schemes and bypasses (http://@127.0.0.1, http://0.0.0.0, http://localhost, 127.0.1)
Attempt to access cloud metadata endpoints (AWS, GCP, Azure) if service is cloud-hosted
Test with URL encoding bypasses (%2e%2e, hex encoding of localhost)
Check if the vulnerability exists in image fetching for other user-generated content features

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1046 - Network Service Discovery
- T1040 - Network Sniffing
- T1589 - Gather Victim Identity Information
- T1526 - Cloud Service Discovery

## Notes
The error message disclosure is particularly dangerous as it reveals internal service details (SSH version, Ubuntu version). The vulnerability is straightforward to exploit and requires minimal authentication (just list access). This is a classic SSRF vulnerability that could be chained with internal service vulnerabilities or used for reconnaissance of the internal network topology and services.

## Full report
<details><summary>Expand</summary>

Summary
----------

There is a Server-side request forgery when updating the image for a list.

Steps to reproduce
-----------------

1. Create a list and change its image. That will send a POST request to https://beta.instacart.com/api/v2/lists/[LIST_ID] with the following parameters:

    ```
list[remote_image_url]=https://example.com/yourimage.jpg
```

2. Change the  url to http://127.0.0.1:21 and you will get as response:

    ```{json}
{
	"meta":
	{
		"code": 400,
		"error_type": "List Error",
		"error_message": "There was an error while updating this list",
		"errors": ["Image could not download file: wrong status line: \"SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.3\""]
	}
}
```
    Which shows that it tried to connect to the SSH port on localhost.  


</details>

---
*Analysed by Claude on 2026-05-24*
