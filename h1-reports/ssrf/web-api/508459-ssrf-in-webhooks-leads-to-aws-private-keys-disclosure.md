# SSRF in webhooks leads to AWS private keys disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 508459 | https://hackerone.com/reports/508459
- **Submitted:** 2019-03-12
- **Reporter:** honoki
- **Program:** Omise
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Server-Side Request Forgery (SSRF), Insufficient Redirect Validation, Metadata Service Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
Omise's webhook implementation fails to properly validate HTTP 303 redirects, allowing attackers to make arbitrary HTTP requests from the application server. An attacker can exploit this to access AWS EC2 instance metadata and retrieve sensitive AWS credentials and private keys.

## Attack scenario
1. Attacker registers a webhook endpoint in Omise dashboard pointing to attacker-controlled server
2. Attacker hosts a PHP script that issues HTTP 303 redirect to AWS metadata service (169.254.169.254)
3. Attacker triggers an API call in Omise that generates a webhook event
4. Omise application server makes HTTP request to attacker's webhook URL
5. Server follows 303 redirect (which was not properly validated) to AWS metadata endpoint
6. Attacker reads AWS credentials and private keys from webhook delivery logs in dashboard

## Root cause
The webhook implementation applies insufficient validation to HTTP redirect responses. While the application appears to block most redirects, HTTP 303 (See Other) status codes are followed without validation, creating a bypass mechanism. Additionally, the application fails to block requests to internal/private IP ranges like 169.254.169.254 (AWS metadata service).

## Attacker mindset
The attacker recognized that defensive measures were likely in place against redirects but discovered a specific HTTP status code bypass. The attacker then pivoted to target AWS metadata endpoints, which are a well-known source of sensitive credentials in cloud environments. The attacker likely performed reconnaissance on HTTP status codes to find which ones would bypass restrictions.

## Defensive takeaways
- Implement strict whitelist validation for all redirect targets, blocking all 3xx redirects or only allowing same-origin redirects
- Block requests to private IP ranges including 169.254.169.254 (AWS metadata), 127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
- Use network segmentation to prevent application servers from accessing metadata services
- Implement Allow-lists for webhook endpoints rather than block-lists
- Log and monitor all HTTP requests made by webhooks for suspicious patterns
- Rotate all AWS credentials immediately after discovering SSRF vulnerabilities
- Review cloud provider access logs to detect past exploitation attempts
- Use IAM roles with minimal required permissions (principle of least privilege)
- Consider using webhook signature validation to ensure only trusted sources are processed

## Variant hunting
Test other HTTP redirect status codes (301, 302, 307, 308) to identify which are followed
Attempt to access other cloud metadata services (GCP, Azure, OpenStack) via similar redirects
Test requests to internal services on non-metadata ports (e.g., 8080, 3000, 5432)
Examine webhook implementations in other payment processors and SaaS platforms for similar patterns
Check if webhook implementations in other Omise features (callbacks, notifications) have same vulnerability
Test for SSRF via URL encoding, Unicode encoding, or other bypass techniques in redirect locations

## MITRE ATT&CK
- T1190
- T1552.005
- T1526
- T1570

## Notes
This is a critical vulnerability combining SSRF with cloud credential exposure. The 303 redirect bypass is particularly notable as a defensive evasion technique. The vulnerability demonstrates why cloud applications must actively block metadata service access at the application layer, not just rely on network controls. The attacker's ability to view webhook responses in the dashboard allowed direct credential theft without needing separate data exfiltration channels.

## Full report
<details><summary>Expand</summary>

## Vulnerability Summary

Omise makes use of Amazon AWS as their application environment. Due to a vulnerability in the way webhooks are implemented, an attacker can make arbitrary HTTP/HTTPS requests from the application server and read their responses. This is known as a server-side request forgery (SSRF) vulnerability.

This vulnerability leads to access to Omise's Amazon EC2 instance with the user role `aws-opsworks-ec2-role`, including AWS private keys.

## Description

The vulnerability exists in the way webhooks follow redirects. In general, it appears that redirects are not followed, but a HTTP 303 See Other status code allows an attacker to bypass this restriction.

By pointing my webhook URL to a server that issues a 303 redirect, I am able to redirect and read the responses of arbitrary HTTP/HTTPS requests from the application server. E.g. the following PHP script results in a successful request that is followed by the server:

`<?php header('Location: http://<arbitrary-location>', TRUE, 303); ?>`

As a result, it is possible to request a number of things, including AWS credentials on the metadata server located at `http://169.254.169.254/latest/meta-data/iam/security-credentials/aws-opsworks-ec2-role`

## Steps to reproduce

* Host the following payload on `https://<your-attacker-server>/redir.php`:

````
<?php header('Location: http://169.254.169.254/latest/meta-data/iam/security-credentials/aws-opsworks-ec2-role', TRUE, 303); ?>
````
* Point your webhook endpoint on https://dashboard.omise.co/test/webhooks/edit to `https://<your-attacker-server>/redir.php`
* Make a random call to the API, e.g. adding a user;
* View the "Recent Deliveries" of the webhook calls on https://dashboard.omise.co/test/webhooks
* Note the `200 OK` status code indicating a successful redirect
* Click the event to view the response body of the AWS metadata

## Recommendation

I recommend to ensure all input provided to the endpoint is validated. In this case, ensure that 303 redirects are not followed either.

I also recommend resetting all AWS access tokens. In addition, I recommend reviewing the Amazon access logs to investigate if this vulnerbility has been exploited in the past.

## Attachments

* **20190312_AWS-SSRF-303-redirect-2.png** - Screenshot showing the output of the AWS credentials obtained through the SSRF vulnerability.
* **20190312_AWS-SSRF-303-redirect.png** - Screenshot showing the output of the AWS index of metadata.

## Impact

By exploiting this vulnerability, an unauthorized attacker could gain access to the AWS environment of Omise. Note that the SSRF vulnerability could be abused in a variety of ways, not just limited to obtaining AWS credentials. For example, to enumerate and access services and web applications running on the internal network.

</details>

---
*Analysed by Claude on 2026-05-11*
