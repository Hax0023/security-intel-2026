# Unrestricted file upload leads to stored xss on https://████████/

## Metadata
- **Source:** HackerOne
- **Report:** 854445 | https://hackerone.com/reports/854445
- **Submitted:** 2020-04-20
- **Reporter:** sensoyard
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**

When the user want to upload a "certificate", the web app doesn't check the content-type of the file. A user can upload any kind of file (binary,html,...)

## Step-by-step Reproduction Instructions

1. Create an account at https://██████/████████/app/registration/basic-info

2. When you are connected, click on "certification"

Upload this file as xss.html and save the modifications: 

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

**Summary:**

When the user want to upload a "certificate", the web app doesn't check the content-type of the file. A user can upload any kind of file (binary,html,...)

## Step-by-step Reproduction Instructions

1. Create an account at https://██████/████████/app/registration/basic-info

2. When you are connected, click on "certification"

Upload this file as xss.html and save the modifications: 

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Simple Test</title>
    <meta name="viewport" content="initial-scale=1.0">
    <meta charset="utf-8">
  </head>
  <body>
    <script>
	alert(document.cookie	)
	</script>
  </body>
</html>
```
3 . Go back to the "certification tab " and open the attachement in a new tab

POC :https://███/████/registration-service/files/███████.html

## Suggested Mitigation/Remediation Actions
Restrict the content-type of the uploaded files

## Impact

The unrestricted file upload vulnerability leads to stored xss.

</details>

---
*Analysed by Claude on 2026-05-24*
