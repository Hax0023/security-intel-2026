# Image Upload Path Disclosure via Error Messages

## Metadata
- **Source:** HackerOne
- **Report:** 158021 | https://hackerone.com/reports/158021
- **Submitted:** 2016-08-10
- **Reporter:** mefkan
- **Program:** Instacart
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Insufficient Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The application discloses server-side file paths in error messages when image upload validation fails. An attacker can trigger validation errors by uploading unsupported file formats (e.g., SVG) to enumerate internal directory structures and upload temporary file locations. This information could facilitate further attacks such as path traversal or local file inclusion exploitation.

## Attack scenario
1. Attacker creates a store list and attempts to upload a background image
2. Attacker crafts request with an SVG file instead of supported formats (JPEG/PNG)
3. Server processes the file and stores it in temporary directory with predictable naming
4. Image validation fails and error response is returned to client
5. Error message includes full server-side path: /var/app/[timestamp]/tmp/uploads/[random]/filename.svg
6. Attacker collects multiple error responses to map directory structure, timestamps, and upload patterns

## Root cause
Error messages return unfiltered, verbose exception details that include absolute file paths from the backend server. The application fails to sanitize error responses before sending them to clients, exposing internal infrastructure details.

## Attacker mindset
Reconnaissance and information gathering. Path disclosure enables reconnaissance of server architecture, filesystem structure, application deployment paths, and temporary file locations. This information feeds into attack planning for subsequent exploitation attempts.

## Defensive takeaways
- Implement generic error messages for client-facing responses (e.g., 'Invalid image format' instead of full path details)
- Log detailed errors server-side only; never expose absolute paths, timestamps, or internal directory structures to users
- Sanitize all error messages before serialization in API responses
- Use environment-relative or abstract path references in any necessary technical messages
- Implement centralized error handling that strips sensitive information from exceptions
- Add monitoring for repeated validation failures that may indicate reconnaissance attempts

## Variant hunting
Search for similar information disclosure in: password reset flows, file processing operations, document conversion services, media manipulation endpoints, backup restore functions, and any endpoint that processes user-supplied files and returns error details.

## MITRE ATT&CK
- T1592.004
- T1526
- T1087

## Notes
This is a classic information disclosure vulnerability with low immediate impact but significant value in attack chains. The vulnerability is trivial to trigger and requires no authentication. The disclosed path structure (with timestamp and random ID) may hint at predictable upload locations. Severity upgraded slightly if combined with path traversal or if upload directory is web-accessible.

## Full report
<details><summary>Expand</summary>

Hi,

Firstly,I couldn't see anything about Path Disclosure in your policy,so I've decided to report it.

Steps to reproduce :

1-Create a list for a store
2-Add background image from link (File has to be .svg) like aaa.com/aaa.svg
3-Then it will give an error

Let's take a look to that error

{"meta":{"code":400,"error_type":"List Error","error_message":"There was an error while updating this list","errors":["Image must be a JPEG or PNG","Image Failed to manipulate with rmagick, maybe it is not an image? Original Error: no decode delegate for this image format `/var/app/20160809T225101Z/tmp/uploads/1470789216-24489-0001-8854/full_redirect_2.svg' @ error/svg.c/ReadSVGImage/2871"]}}


As you can understand from error's Response this is the path disclosure

/var/app/20160809T225101Z/tmp/uploads/1470789216-24489-0001-8854/full_redirect_2.svg

I'm gonna add a screenshot from Request and Response for being more clear about it.

Thanks,Instacart.

</details>

---
*Analysed by Claude on 2026-05-24*
