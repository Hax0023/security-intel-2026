# Content-Length Header Bypass Leads to Denial of Service via Large File Upload

## Metadata
- **Source:** HackerOne
- **Report:** 203388 | https://hackerone.com/reports/203388
- **Submitted:** 2017-02-04
- **Reporter:** a0xnirudh
- **Program:** Gratipay (gip.rocks)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Insufficient Input Validation, HTTP Header Spoofing, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The application validates file size restrictions by trusting the unverified Content-Length HTTP header rather than validating actual payload size. An attacker can spoof this header with a small value while uploading a large file, causing the server to read massive amounts of data into memory and process it, leading to denial of service through resource exhaustion.

## Attack scenario
1. Attacker prepares a large image file (e.g., 1GB) that exceeds the 256KB size restriction
2. Attacker intercepts the request using a proxy (Burp Suite) or crafts raw HTTP request
3. Attacker modifies the Content-Length header to a value under 256KB (e.g., 200000 bytes) while keeping actual payload large
4. Attacker forwards the request to the vulnerable endpoint (/v1.spt)
5. Server's validation passes because it checks the spoofed Content-Length header instead of actual body size
6. Server loads entire large file into memory via StringIO and Image.open(), consuming excessive resources and causing denial of service

## Root cause
The application relies solely on the untrusted Content-Length HTTP header for size validation without verifying the actual size of the request body being read. The header is set by the client and can be freely modified. Real payload size validation should occur during or after data reception, not based on client-provided headers.

## Attacker mindset
An attacker seeks to exhaust server resources by exploiting a gap between client-declared and actual data size. By deceiving the application's validation mechanism, they bypass protective controls to upload large payloads that consume memory, CPU, and I/O resources, crashing or degrading the service for legitimate users.

## Defensive takeaways
- Never trust client-provided HTTP headers (Content-Length, Content-Type, etc.) for security decisions
- Implement server-side payload size validation by reading and measuring actual request body data, not headers
- Use streaming/chunked processing with size limits rather than loading entire files into memory
- Implement rate limiting and connection timeouts to mitigate resource exhaustion attacks
- Monitor memory usage and implement circuit breakers that reject requests when resource thresholds are exceeded
- Consider using Web Application Firewalls (WAF) with payload inspection capabilities
- Validate Content-Type by inspecting actual file magic bytes/signatures, not just headers

## Variant hunting
Check other file upload endpoints for similar Content-Length-based validation
Search for other uses of request.headers['Content-Length'] in the codebase without body validation
Look for image processing operations (Image.open, resize, convert) that could be exploited with malformed files combined with header spoofing
Investigate if other streaming operations trust client headers for size enforcement
Review API endpoints that accept binary data and check if they validate actual vs declared sizes

## MITRE ATT&CK
- T1190
- T1499.4
- T1499.1

## Notes
This is a well-articulated vulnerability report that identifies a clear logic flaw. The researcher responsibly did not perform actual DoS testing but provided sufficient code analysis. The vulnerability is trivial to exploit and has high impact. The mitigation requires reading actual payload size incrementally rather than trusting headers. This pattern is common in file upload features and should be audited broadly.

## Full report
<details><summary>Expand</summary>

Hello team,

## Introduction

Since you mentioned in the rules that all libraries listed on your github repositories are in scope, I decided to take a look at http://gip.rocks

## Problem:

The application reads an image file and convert it into smaller formats, zip it and let the users to download the updated file. But the problem here is the condition check before reading the file to the variable:

File: https://github.com/gratipay/gip.rocks/blob/master/www/v1.spt

```python
if int(request.headers['Content-Length']) > 256 * 1024:
    raise Response(413)

image_type = request.headers['Content-Type']
if image_type not in ('image/png', 'image/jpeg'):
    raise Response(415)

# Load the image.
fp = StringIO(request.raw_body)
fp.seek(0)
image = Image.open(fp)

```

Here you can see that you are calculating the length of the incoming file from the `content-length` HTTP header and if it is less than `256 * 1024`, you will accept the request. But this is not a correct way to check size of the incoming file.

## POC:

1) Initiate a system wide proxy with burp suite

2) Try to send a curl request with a huge file and see the request in curl

3) The content length will be obviously greater than the max value application accepts but modify the `content-length` header to a value which is less than `256 * 1024`.

4) Forward the request and you can see that the server will read the files to a variable and if the file is large enough, this is more than enough to DOS the server.

Now since this deals with DOS, I haven't actually tried out this attack but we can easily confirm this from the source code that this can be bypassed in the way I explained above. I also tried deploying locally but I had a hard time making the software run locally and I don't have enough free time to debug what is happening.

But I think the bug is very clear from the source code itself, which is why I really didn't test it but thought to report it.

## Mitigation:

Putting your trust on HTTP headers may not be a good idea. But I am not really sure what is a solid method to find the proper length of the string in this case.

</details>

---
*Analysed by Claude on 2026-05-24*
