# Application-level DoS on image's 'size' parameter

## Metadata
- **Source:** HackerOne
- **Report:** 247700 | https://hackerone.com/reports/247700
- **Submitted:** 2017-07-10
- **Reporter:** edoverflow
- **Program:** Gratipay
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service (DoS), Input Validation, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The 'size' parameter in the image endpoint fails to properly validate input length, allowing attackers to craft oversized requests that cause application slowdown. By repeatedly sending requests with 4094-character payloads, an attacker can exhaust server resources and degrade application performance for legitimate users.

## Attack scenario
1. Attacker identifies the vulnerable image endpoint at /<USER>/image?size=<value>
2. Attacker crafts a malicious URL with the size parameter padded to 4094 characters
3. Attacker sends this request repeatedly in a loop (10 million+ times)
4. Each request causes excessive processing or memory consumption on the server
5. Server resources become exhausted, causing slowdown for all users
6. Application becomes unavailable or severely degraded for legitimate traffic

## Root cause
The get_image_url() function contains an assertion that only checks if size is in ('original', 'large', 'small'), but the assertion operates on the parameter name alone without validating the actual request payload length. Query string parsing and subsequent processing doesn't implement length limits on the size parameter value, allowing arbitrarily long strings to be passed and processed.

## Attacker mindset
An attacker would recognize that the assertion only validates the parameter's presence/membership, not its length. They would exploit the lack of input sanitization on query string parameters to send oversized payloads that cause the application to consume excessive resources per request. By automating requests, they amplify the impact.

## Defensive takeaways
- Implement strict input validation on all user-supplied parameters, including length constraints
- Validate not just parameter names but also parameter values and their formats
- Use allowlists for expected values (was attempted here but incompletely)
- Implement rate limiting and request throttling per IP/user
- Add maximum request/parameter size limits at the web server level
- Monitor for suspicious request patterns with unusually long parameters
- Use web application firewalls (WAF) to block malformed requests
- Implement request queuing and backpressure mechanisms to gracefully handle load

## Variant hunting
Check other endpoints that parse URL parameters for similar length validation gaps
Search for other assertion-based validation that doesn't limit input size
Look for parameter handlers that perform expensive operations without length constraints
Test image endpoints in other sections of the application
Check if other file upload/processing parameters have similar issues
Review all endpoints that accept size, dimension, or format parameters

## MITRE ATT&CK
- T1499
- T1190

## Notes
The vulnerability is straightforward but impactful: while the assertion prevents invalid size values, it doesn't prevent valid values from being extremely long strings in the query parameter itself. The actual size parameter value can be padded with arbitrary data. This is an application-level DoS rather than a protocol-level attack, making it harder to detect with standard DDoS mitigation. The fix requires adding length validation: assert len(size) <= <max_length> and size in ('original', 'large', 'small').

## Full report
<details><summary>Expand</summary>

# Summary
---

The `size` parameter located on images is vulnerable to DoS. By modifying the parameter's value an attacker can cause the application to work very slowly.

# Description
---

The issue is located in the `get_image_url()` function in `gratipay/models/team/__init__.py` and can be exploited by replacing the `small` or `large` values in the following GET request: `http://<GRATIPAY INSTANCE>/<USER>/image?size=small`.

~~~python
# Images
# ======

IMAGE_SIZES = ('original', 'large', 'small')

def get_image_url(self, size):
    assert size in ('original', 'large', 'small'), size
    return '/{}/image?size={}'.format(self.slug, size)
~~~

Link: https://github.com/gratipay/gratipay.com/blob/1985e43033edd87bd16cdb46c16adbcda0bb6bc4/gratipay/models/team/__init__.py#L312-L314

# How can this issue be exploited?
---

Repeatedly sending values of 4094 characters in length will cause the DoS.

~~~python
import requests
payload = "a" * 4094
url = "http://<GRATIPAY INSTANCE>/<USER>/image?size=small" + payload

for i in range(10000000):
	requests.get(url)
~~~

</details>

---
*Analysed by Claude on 2026-05-24*
