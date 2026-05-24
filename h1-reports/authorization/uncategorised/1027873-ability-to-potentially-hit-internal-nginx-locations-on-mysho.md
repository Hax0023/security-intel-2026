# X-Accel-Redirect Header Exploitation via App Proxy to Access Internal NGINX Locations

## Metadata
- **Source:** HackerOne
- **Report:** 1027873 | https://hackerone.com/reports/1027873
- **Submitted:** 2020-11-06
- **Reporter:** imgnotfound
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Header Injection, Improper Input Validation, Insecure Proxy Configuration
- **CVEs:** None
- **Category:** uncategorised

## Summary
Shopify's NGINX reverse proxy configuration fails to ignore the X-Accel-Redirect header returned by App Proxy backends, allowing attackers to perform internal redirects to arbitrary NGINX locations. An attacker controlling an App Proxy backend can inject X-Accel-Redirect headers to redirect requests to internal services that should not be directly accessible.

## Attack scenario
1. Attacker creates a malicious external service or compromises an existing App Proxy endpoint
2. Attacker configures the service to return responses with X-Accel-Redirect headers pointing to internal NGINX locations (e.g., /internal/admin, /private-service/flag)
3. Attacker directs victims or makes requests through a legitimate App Proxy endpoint configured to proxy to their malicious service
4. NGINX processes the X-Accel-Redirect header and performs internal redirection to the attacker-specified location
5. The internal location is accessed with the victim's context/permissions, potentially exposing sensitive data or functionality
6. Attacker exfiltrates information from internal services that should be isolated from public access

## Root cause
The NGINX configuration does not explicitly ignore the X-Accel-Redirect response header from upstream App Proxy services. NGINX by default processes this header for internal redirects, enabling attackers to leverage untrusted upstream responses to access internal locations that should only be accessible within NGINX's internal routing logic.

## Attacker mindset
An attacker would seek to leverage the App Proxy feature—a legitimate but potentially dangerous mechanism—to gain unauthorized access to internal services. The discovery exploits the trust boundary between NGINX and upstream services; if an upstream service can be controlled or influenced, it becomes a pivot point to internal resources. The attacker recognizes that internal NGINX locations often contain sensitive functionality or data that should never be directly accessible to external requests.

## Defensive takeaways
- Always explicitly disable untrusted response headers at proxy boundaries using proxy_ignore_headers directives for headers like X-Accel-Redirect, X-Accel-Expires, X-Accel-Limit-Rate, X-Accel-Buffering
- Implement strict validation and allowlisting of upstream service responses, especially for any headers that can influence routing or redirects
- Segregate internal and external NGINX location definitions; never expose internal locations to untrusted upstream services
- Apply the principle of least privilege: configure App Proxy endpoints with minimal necessary permissions and restrict them to specific, safe paths
- Regularly audit NGINX configurations for insecure proxy settings and test reverse proxy configurations for header injection vulnerabilities
- Monitor and log X-Accel-Redirect header usage; alert on unexpected internal location redirects from user-facing proxies
- Document and enforce a security policy regarding which headers should be honored from which upstream services

## Variant hunting
Test for X-Accel-Expires, X-Accel-Buffering, X-Accel-Charset, and other X-Accel-* headers that may have similar exploitation potential
Check for similar header injection vulnerabilities in other reverse proxy technologies (HAProxy, Envoy, cloud CDNs) that support internal redirects
Investigate whether other Shopify proxy features (API proxies, webhook proxies) have similar misconfigurations
Probe for time-of-check-time-of-use (TOCTOU) vulnerabilities in NGINX location matching that could bypass internal restrictions
Test whether X-Accel-Redirect can be chained with other response headers (Location, Refresh) for amplified impact
Enumerate other cloud platforms' reverse proxy configurations for similar internal redirect mechanisms left unprotected

## MITRE ATT&CK
- T1190
- T1557
- T1021
- T1552
- T1039

## Notes
The researcher demonstrated proof-of-concept by successfully redirecting to /collections/all but was unable to find actual sensitive internal locations during testing. This does not diminish the severity—it indicates either good operational security on Shopify's part (no sensitive internal locations exposed to NGINX internal redirects) or that the researcher's fuzzing was insufficient. The vulnerability is configuration-based and exploitable if any internal NGINX locations exist. The fix is straightforward and already documented in NGINX documentation, suggesting this was a configuration oversight rather than a fundamental platform issue. App Proxies are inherently risky as they create a user-controlled upstream service; defense-in-depth measures are essential.

## Full report
<details><summary>Expand</summary>

By making use of the [Shopify App Proxy](https://shopify.dev/tutorials/display-data-on-an-online-store-with-an-application-proxy-app-extension) and the [**X-Accel** feature of NGINX](https://www.nginx.com/resources/wiki/start/topics/examples/x-accel/), it is possible to hit any configured `internal` NGINX location as your current configuration is not ignoring the `X-Accel-Redirect` header response from an upstream service. 

The way it works is that NGINX allows internal redirection to a location determined by that header returned from a backend - in our case being the configured **App Proxy** backend controlled by the attacker.

For example, the following request would ends up hitting `http://private-service/flag`
{F1067100}

However, I did some very basic fuzzing and wasn't able to hit anything but still reporting and will let you guys assess the risk.

## Steps to reproduce
### Create a service that return a X-Accel-Redirect header
First step, is to create a server that is returning a response with the `X-Accel-Redirect` header.
1. Open [mocky.io](https://designer.mocky.io/design)
2. Within the **HTTP Headers** section, enter:
```
{
	"X-Accel-Redirect": "/collections/all"
}
```
3. Scroll down and click **Generate my HTTP response** and copy the **Mock URL**

Otherwise, you can simply use https://run.mocky.io/v3/d7cdfcbc-6994-4f3b-a323-fe8377535507 which is already configured per above steps

### Setup the App Proxy
1. Within Shopify Partners, create a new private application and install it on your shop
1. From that application setup, go to **Extensions > Online Store** and setup an **App proxy**
1. From that **App proxy** configuration, set the following values:
	1. Subpath prefix: `a`
	1. Subpath `apps`
	1. Proxy URL `https://run.mocky.io/v3/d7cdfcbc-6994-4f3b-a323-fe8377535507` or enter your own mock URL 
1. Within your browser, open your `https://{shop}.myshopify.com/a/apps` by taking care of replacing the `{shop}` placeholder with your actual shop name on which you installed the application

As a result, you are being proxied your current shop `/collections/all` page proving that your current NGINX configuration follows the `X-Accel-Redirect` directive. 

## Mitigation
To mitigate this issue, a `proxy_ignore_headers X-Accel-Redirect` directive should be set in your NGINX configuration as described in the [NGINX documentation](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_ignore_headers)

## Impact

As mentioned, I wasn't actually able to hit any of your internal routes but that could only mean that my URL fuzzing wasn't good enough or that you actually do not have any configured internal routes on that proxy.

</details>

---
*Analysed by Claude on 2026-05-24*
