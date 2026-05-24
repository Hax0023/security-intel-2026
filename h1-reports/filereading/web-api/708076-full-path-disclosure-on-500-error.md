# Full Path Disclosure via Cookie Parameter Manipulation on 500 Error

## Metadata
- **Source:** HackerOne
- **Report:** 708076 | https://hackerone.com/reports/708076
- **Submitted:** 2019-10-05
- **Reporter:** rajauzairabdullah
- **Program:** HackerOne (Specific program not named in report)
- **Bounty:** Not specified in report
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A 500 error triggered by manipulating the gitHub_* cookie parameter causes the application to return verbose Python stack traces that disclose internal file paths and application structure. This information disclosure reveals sensitive details about the application's backend architecture and dependencies, including virtual environment paths and internal module locations.

## Attack scenario
1. Attacker identifies cookie parameters starting with 'gitHub_' in application requests
2. Attacker modifies the cookie value to invalid JSON or malformed base64 data
3. Application attempts to parse cookie using json.loads() on decoded value without proper error handling
4. JSON parsing fails, triggering unhandled exception
5. Server returns 500 error with full Python traceback in response
6. Attacker extracts file paths, module locations, and internal application structure from stack trace

## Root cause
Application lacks proper exception handling for cookie parsing operations. The error handling does not catch JSONDecodeError and other parsing exceptions before they propagate to the HTTP response layer, resulting in verbose stack trace disclosure in 500 error pages.

## Attacker mindset
Reconnaissance-focused adversary seeking to map application architecture and identify potential attack vectors through information disclosure. The attacker tests input validation boundaries on cookie parameters to trigger verbose error messages.

## Defensive takeaways
- Implement try-catch blocks around all user input parsing operations (JSON, base64, etc.)
- Return generic error messages to users while logging detailed errors server-side only
- Configure application to hide stack traces in production environments
- Implement proper HTTP error page templates that don't include exception details
- Validate and sanitize cookie parameters before parsing
- Use web application firewalls to filter error responses containing file paths
- Implement centralized error handling middleware

## Variant hunting
Look for similar patterns: other cookie parameters prefixed with service names (github_, google_, oauth_, etc.), form parameters passed to parsers (XML, YAML, pickle), file upload handlers with verbose errors, API endpoints that parse user-supplied serialized data without error handling, and any location where untrusted input is deserialized.

## MITRE ATT&CK
- T1592.004
- T1526
- T1087

## Notes
This is a low-severity information disclosure vulnerability. While path disclosure alone doesn't enable direct attacks, it significantly aids reconnaissance and can reveal version information about frameworks and libraries. The vulnerability demonstrates a common pattern: unhandled exceptions during input parsing leaking sensitive debugging information. The specific traceback reveals use of Pando/Aspen framework, Python 3.6, and internal file structure (/opt/python/run/venv, /bundle/4/app/www). Real impact depends on what information an attacker can extract and whether it enables further attacks.

## Full report
<details><summary>Expand</summary>

On manipulating cookie 
+ **parameter:** `gitHub_<anything>` 500 error returned with path disclosing of **Python** Files.

##Error Below:
> Traceback (most recent call last):
  File "/opt/python/run/venv/local/lib/python3.6/site-packages/state_chain.py", line 328, in loop
    new_state = function(**deps.as_kwargs)
  File "/opt/python/run/venv/local/lib/python3.6/site-packages/pando/state_chain.py", line 128, in render_response
    output = resource.render(context, state['dispatch_result'], state['accept_header'])
  File "/opt/python/run/venv/local/lib/python3.6/site-packages/aspen/http/resource.py", line 129, in render
    return self.render_for_type(available[0], context)
  File "/opt/python/run/venv/local/lib/python3.6/site-packages/aspen/simplates/simplate.py", line 140, in render_for_type
    exec(self.page_two, context)
  File "/opt/python/bundle/4/app/www/on/%platform/associate.spt", line 36, in <module>
    cookie_obj = json.loads(b64decode_s(cookie_value))
  File "/usr/lib64/python3.6/json/__init__.py", line 354, in loads
    return _default_decoder.decode(s)
  File "/usr/lib64/python3.6/json/decoder.py", line 339, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib64/python3.6/json/decoder.py", line 355, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 98 (char 97)

## Impact

Information is being disclosed about internal files.

</details>

---
*Analysed by Claude on 2026-05-24*
