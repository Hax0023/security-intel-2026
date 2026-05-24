# Path Traversal in Shopify App Proxy

## Metadata
- **Source:** HackerOne
- **Report:** 869888 | https://hackerone.com/reports/869888
- **Submitted:** 2020-05-10
- **Reporter:** ngalog
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Shopify's App Proxy feature fails to properly sanitize path traversal sequences (../) in user-supplied URLs, allowing unauthenticated attackers to bypass intended path restrictions and access files/endpoints on the OAuth app's hosting server that should be protected. An attacker can traverse beyond the configured proxy path to reach arbitrary locations on the backend server by injecting ../ sequences into the request path.

## Attack scenario
1. Attacker discovers a Shopify store with an installed OAuth app that uses the App Proxy feature
2. App Proxy is configured with a restricted path like /proxy pointing to https://attacker-app.com/proxy
3. Attacker crafts a malicious request to /apps/ss/b.php/../../ to traverse up directory levels
4. Shopify's proxy server fails to normalize or strip the ../ sequences before forwarding the request
5. Request is proxied to the backend server without path sanitization, reaching unintended endpoints
6. Attacker gains access to sensitive files or functionality outside the intended /proxy directory scope

## Root cause
Shopify's App Proxy implementation does not properly validate or normalize user-supplied path parameters. The proxy forwards requests with path traversal sequences intact without stripping or validating them, allowing directory traversal attacks to bypass path restrictions.

## Attacker mindset
An attacker targeting this vulnerability would recognize that proxy services are common attack surfaces due to URL manipulation opportunities. By testing standard path traversal payloads (../) against the proxy endpoint, they can identify that input sanitization is missing and escalate from the restricted proxy path to arbitrary server access. This is a low-effort, high-impact vulnerability requiring only URL manipulation.

## Defensive takeaways
- Implement strict path canonicalization - resolve all ../, ./, and encoded variants to absolute paths before processing
- Validate that resolved paths remain within the intended proxy scope using whitelist/allowlist validation
- Reject requests containing path traversal sequences rather than attempting to strip them
- Normalize URLs at the earliest point of entry and reject any requests that change after normalization
- Use URL parsing libraries that handle edge cases and encoded traversal attempts
- Implement server-side path validation independent of client input
- Add request logging and monitoring for suspicious path patterns
- Apply the principle of least privilege to backend service access from proxy layer

## Variant hunting
Similar path traversal vulnerabilities likely exist in: (1) other Shopify proxy/webhook handling features that forward external requests, (2) custom domain proxying with user-controlled path segments, (3) API gateway or reverse proxy implementations that fail to normalize paths, (4) file serving or static content proxy endpoints, (5) custom app hosting platforms with similar request forwarding patterns

## MITRE ATT&CK
- T1190
- T1083
- T1566

## Notes
The report demonstrates a practical exploitation by showing that traversal sequences allow access to the root directory of the backend server (evidenced by Dropbox domain verification meta tag response). This indicates the vulnerability has significant impact as it completely bypasses the intended path restriction model of App Proxy. The vulnerability is pre-authentication, affecting any store with the vulnerable app installed.

## Full report
<details><summary>Expand</summary>

Hi,

I found app proxy is vulnerable to path traversal, the attacker scenario is from anonymous user to oauth app owner.

## Description
In app proxy function, it is possible proxy request to shopify custom domain request to oauth app store defined host, and because shopify didn't escape the `../`, it allows anyone to escape the path and reach unintended location.

## Steps to reproduce
- Since setting up and explaining how to setup app proxy would be so trouble, I'll go straight to the point.
- The app proxy for my oauth app is set to  `https://████████/proxy`, path and subpath is `apps/ss`
- My store `█████` has installed it
- If you go https://███████/apps/ss/test, you should see `hi im ron`, which matches `https://██████████/proxy/test`
- In theory, you can't use this proxy to see what's hosting in `https://████████/` since I have added `/proxy` in the path
- However with this path traversal, it is possible now

Copy and paste this to the burp repeater and hit Send

```
GET /apps/ss/b.php/../../?shop=a&Shop=asd HTTP/1.1
Host: ███████
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1


```

response is 

```
	<head>
<meta name=dropbox-domain-verification content=4yyz8tdqnx1e />
</head>


<body>hi</body>


```

Which matches response at `https://█████/`

## Impact

Able to perform path traversal on oauth app as anonymous user

</details>

---
*Analysed by Claude on 2026-05-24*
