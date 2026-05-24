# Image Upload Path Disclosure via Error Message

## Metadata
- **Source:** HackerOne
- **Report:** 158021 | https://hackerone.com/reports/158021
- **Submitted:** 2016-08-10
- **Reporter:** mefkan
- **Program:** Instacart
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Error-based Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The application discloses sensitive internal file paths when processing image uploads with unsupported formats. Error messages returned to users contain absolute server paths including timestamps and temporary directory structures. This information could aid attackers in planning further attacks by revealing server architecture and deployment details.

## Attack scenario
1. Attacker identifies image upload functionality in store list creation
2. Attacker attempts to upload a file with unsupported format (SVG instead of JPEG/PNG)
3. Application processes the file and attempts image manipulation via ImageMagick (rmagick)
4. Manipulation fails due to unsupported format, triggering error handler
5. Error handler includes full file path in JSON error response
6. Attacker receives detailed path disclosure revealing /var/app directory structure, deployment timestamps, and temporary file naming patterns

## Root cause
Error messages from image processing library (rmagick/ImageMagick) are not sanitized before returning to client. The application directly exposes exception details containing absolute file paths instead of returning generic error messages.

## Attacker mindset
Reconnaissance and information gathering. Attacker seeks to understand server architecture, directory structure, and deployment practices to identify further attack vectors or understand application behavior patterns.

## Defensive takeaways
- Implement custom error handling that sanitizes exception messages before client response
- Return generic error messages to end users (e.g., 'Invalid image format') while logging full details server-side
- Validate file formats on client-side and server-side before processing with external libraries
- Use relative paths or abstracted file references in error responses
- Implement proper exception handling to catch and transform library-specific errors
- Remove sensitive path information from all HTTP responses
- Consider using security middleware to filter sensitive patterns from responses

## Variant hunting
Test other file upload endpoints with unsupported formats (documents, videos, archives)
Attempt malformed files to trigger different error conditions
Try path traversal payloads in file names to see if paths are reflected
Test other image processing operations (resize, crop, thumbnail) for similar disclosures
Check API endpoints for similar error message handling patterns
Look for stack traces or verbose errors in other error conditions
Test with different MIME types to trigger different validation failures

## MITRE ATT&CK
- T1190
- T1592
- T1589

## Notes
This is a low-severity but legitimate information disclosure. The path reveals: (1) application deployment path structure (/var/app), (2) deployment timestamp format (20160809T225101Z), (3) temporary file storage location, (4) file naming patterns. While not directly exploitable, this information could support reconnaissance for more serious attacks. The reporter properly noted that path disclosure wasn't explicitly mentioned in the program's vulnerability policy, showing good judgment in reporting out-of-scope-seeming issues.

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
