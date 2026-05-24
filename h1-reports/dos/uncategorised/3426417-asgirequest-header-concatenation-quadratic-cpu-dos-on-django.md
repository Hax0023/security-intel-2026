# ASGIRequest Header Concatenation Quadratic CPU DoS on Django

## Metadata
- **Source:** HackerOne
- **Report:** 3426417 | https://hackerone.com/reports/3426417
- **Submitted:** 2025-11-14
- **Reporter:** sy2n0
- **Program:** Django
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Algorithmic Complexity, Resource Exhaustion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Django's ASGIRequest handler performs quadratic string concatenation when processing repeated HTTP headers, allowing attackers to exhaust worker CPU with a single request containing thousands of duplicate headers. The vulnerability exists in the META dictionary construction loop where each repeated header value is concatenated using immutable string operations, causing Θ(n²) computational complexity for n repeated headers.

## Attack scenario
1. Attacker opens an HTTP/2 connection to a Django ASGI deployment (gunicorn+uvicorn, Daphne, etc.)
2. Attacker crafts a GET request with a single cookie or other header repeated 8,000-16,000 times with small individual values (<128 bytes)
3. ASGIRequest.__init__() enters the header processing loop and begins concatenating each repeated header value using string concatenation
4. Each concatenation operation copies the entire accumulated string due to Python's immutable string semantics, consuming exponential CPU cycles
5. Request initialization consumes several hundred milliseconds to multiple seconds of CPU before reaching any view code
6. Attacker repeats the attack on parallel connections to saturate all available worker processes and deny service to legitimate users

## Root cause
The ASGIRequest constructor iterates over ASGI scope headers and uses the pattern `value = existing + "," + new` for repeated headers. Python strings are immutable, so each concatenation operation allocates new memory and copies the entire accumulated string. The code lacks upper bounds on repeated headers and buffering mechanisms, resulting in Θ(n²) complexity where n is the number of repeated headers.

## Attacker mindset
An attacker recognizes that HTTP/2 and HTTP/3 allow legal header repetition and exploits Django's naive string concatenation approach. The attack is trivial to execute (single connection, small payload), stays within Django's documented limits (URLs/headers <8KB, body <2.5MB), bypasses authentication, and doesn't require special configuration. The attacker can efficiently saturate worker pools by keeping multiple connections alive.

## Defensive takeaways
- Avoid string concatenation in loops; use list collection with join() after loop completion
- Implement per-request limits on repeated headers or total header count
- Use algorithmic complexity analysis during code review, especially for request parsing paths
- Monitor CPU utilization and request processing times to detect algorithmic DoS attacks
- Consider streaming/buffering mechanisms for header processing rather than accumulating in memory
- Validate header field names and counts early in request processing pipeline
- Test performance with adversarial input patterns (repeated headers, large counts) during security review

## Variant hunting
Similar quadratic concatenation patterns in query string parsing or cookie handling
WSGI request handlers (django.core.handlers.wsgi) for identical vulnerabilities
Other frameworks' ASGI/HTTP implementations using naive string concatenation for multi-valued headers
Request body parsing with repeated form field concatenation
Middleware that reconstructs or processes headers sequentially
WebSocket upgrade header handling with repeated headers
Reverse proxy header forwarding that concatenates repeated headers

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
The vulnerability affects all Django versions with ASGI support. Individual header values remain small (~128B), so the attack avoids triggering size-based limits while header repetition count (8K-16K) causes algorithmic complexity explosion. The PoC demonstrates clear quadratic growth: 2K headers (15ms) → 4K headers (67ms) → 8K headers (233ms) → 16K headers (1.1s). HTTP/2 framing makes header repetition natural since it sends individual name-value pairs. Remediation involves collecting values in lists and joining only after iteration completes, reducing complexity to Θ(n log n) at worst. This is a classic algorithmic DoS vulnerability exploitable without authentication or special permissions.

## Full report
<details><summary>Expand</summary>

# ASGIRequest header concatenation quadratic CPU DoS

**Reporter:** Jiyong Yang / BAEKSEOK University 
**Target:** Django (current `main`, affects all versions with ASGI support)  
**Type:** Denial of Service (CPU exhaustion)

## Summary
`django.core.handlers.asgi.ASGIRequest` builds the `META` dictionary by iterating over the ASGI `scope["headers"]` array. Whenever the same header name appears multiple times (which is legal in HTTP/2 and HTTP/3), the code concatenates the previous value and the new chunk via `value = existing + "," + new`. Because Python strings are immutable, each concatenation copies the entire accumulated value. If an attacker repeats a header `n` times, the loop performs `1 + 2 + … + n = Θ(n²)` bytes of copying before the request even reaches view code. A single request with a few thousand duplicated headers therefore ties up the worker CPU and creates a denial-of-service condition on any Django ASGI deployment.

```85:103:django/django/core/handlers/asgi.py
        for name, value in self.scope.get("headers", []):
            name = name.decode("latin1")
            if name == "content-length":
                corrected_name = "CONTENT_LENGTH"
            elif name == "content-type":
                corrected_name = "CONTENT_TYPE"
            else:
                corrected_name = "HTTP_%s" % name.upper().replace("-", "_")
            value = value.decode("latin1")
            if corrected_name == "HTTP_COOKIE":
                value = value.rstrip("; ")
                if "HTTP_COOKIE" in self.META:
                    value = self.META[corrected_name] + "; " + value
            elif corrected_name in self.META:
                value = self.META[corrected_name] + "," + value
            self.META[corrected_name] = value
```

## Impact
- One HTTP/2 request that repeats a short header 8,000–16,000 times consumes several hundred milliseconds to multiple seconds of CPU just to build the request object. No body payload is required.
- Attackers can open a handful of parallel connections and keep ASGI workers (uvicorn + gunicorn, Daphne, etc.) saturated, preventing legitimate traffic from being served.
- The attack stays within Django's documented limits (URLs/headers < 8 KB, body < 2.5 MB) and requires no special configuration changes, so it satisfies the Django security policy.

## Proof of Concept
The following script imports Django from the repository, constructs `ASGIRequest` objects with varying header counts, and measures how long `__init__()` spends concatenating:

```python
import sys, time
from io import BytesIO

sys.path.insert(0, "/django-poc")
sys.path.insert(0, "/django-poc/django")
import asgiref.sync

class ThreadSensitiveContext:
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc, tb): return False

asgiref.sync.ThreadSensitiveContext = ThreadSensitiveContext

from django.conf import settings
if not settings.configured:
    settings.configure(DEBUG=False, SECRET_KEY="x", ROOT_URLCONF=__name__,
                       ALLOWED_HOSTS=["*"], USE_TZ=True)

import django
django.setup()
from django.core.handlers.asgi import ASGIRequest

def bench(n, header_len=128):
    scope = {
        "type": "http",
        "scheme": "http",
        "path": "/",
        "method": "GET",
        "headers": [(b"cookie", b"a=1" * (header_len // 4)) for _ in range(n)],
        "query_string": b"",
    }
    start = time.perf_counter()
    ASGIRequest(scope, BytesIO(b""))
    return time.perf_counter() - start

for n in (2_000, 4_000, 8_000, 16_000):
    print(f"{n} headers -> {bench(n):.6f}s")
```

Example output on my M3 system:

```
2000 headers -> 0.015708s
4000 headers -> 0.066771s
8000 headers -> 0.233624s
16000 headers -> 1.131225s
```

Doubling the header count quadruples the runtime, clearly showing the Θ(n²) growth. All requests used zero body bytes and only ~2 MB of total header data, so they comply with Django's policy limits.

## Attack Scenario
1. Open an HTTP/2 connection to the Django ASGI deployment (gunicorn+uvicorn, Daphne, etc.).
2. Send a GET request with one cookie (or any header) duplicated thousands of times, keeping individual header values small (<128 B) and leaving the body empty.
3. `ASGIRequest` concatenates each copy into `META`, burning CPU before middleware or views run.
4. Repeat on a few concurrent connections to keep all worker processes busy and deny service to legitimate users.

## Root Cause
The request constructor stores repeated headers as a single comma-delimited string by copying the full accumulated value at every iteration. Because Python strings are immutable, each `existing + "," + value` operation reallocates and copies the entire string. There is no upper bound on repeated headers and no streaming/buffering mechanism, so the loop performs Θ(n²) work for Θ(n) input.

## Remediation Ideas
1. Collect repeated headers in lists (e.g., `defaultdict(list)`) and only call `",".join(values)` after the loop, reducing the complexity to O(n).
2. For cookies, use `"; ".join(...)` with the same approach instead of repeated string concatenation.
3. Optionally enforce a sane maximum repetition count per header name to fail fast on absurd inputs.

## Policy Fit
- Inputs remain within Django's published limits (body under 2.5 MB, headers under 8 KB per entry).
- Attack works against default ASGI deployments with no custom settings.
- Impact is a classic CPU exhaustion DoS, explicitly listed as in-scope for Django's security program.

## Timeline
- 2025-11-14: Issue discovered and locally benchmarked.

</details>

---
*Analysed by Claude on 2026-05-24*
