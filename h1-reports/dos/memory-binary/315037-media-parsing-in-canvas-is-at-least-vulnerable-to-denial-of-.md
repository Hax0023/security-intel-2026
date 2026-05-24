# Multiple Denial of Service Vulnerabilities in node-canvas Media Parsing (PNG, JPG, GIF)

## Metadata
- **Source:** HackerOne
- **Report:** 315037 | https://hackerone.com/reports/315037
- **Submitted:** 2018-02-11
- **Reporter:** webtonull
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Buffer Overflow, Out-of-Bounds Read, Memory Corruption, Denial of Service
- **CVEs:** CVE-2020-8215
- **Category:** memory-binary

## Summary
Multiple vulnerabilities in node-canvas (v1.6.9) image parsing library allow attackers to trigger segmentation faults and crash Node.js processes through maliciously crafted PNG, JPG, and GIF images. The vulnerabilities include classic buffer overflows and out-of-bounds memory reads that could potentially be exploited for code execution.

## Attack scenario
1. Attacker identifies a web service using node-canvas or dependent packages like ascii-art for image processing
2. Attacker crafts malicious image files (PNG, JPG, or GIF) using fuzzing techniques to trigger memory corruption
3. Attacker uploads or provides the crafted image to the vulnerable service through standard image input mechanisms
4. Service passes the image to canvas library for processing without validation
5. Canvas library attempts to parse the malformed image, triggering buffer overflow or out-of-bounds read
6. Node.js process segfaults, causing denial of service and service downtime

## Root cause
Unsafe memory operations in Cairo-backed Canvas implementation's image parsing routines for multiple formats. The underlying image parsing libraries (likely libpng, libjpeg, libgif) are called without sufficient bounds checking, allowing crafted images to read or write beyond allocated memory regions.

## Attacker mindset
Reconnaissance-focused: Identify popular Node.js packages and their usage patterns. Automation-minded: Use AFL fuzzing to systematically discover memory corruption bugs. Opportunistic: Target high-volume libraries with millions of downloads to maximize impact potential.

## Defensive takeaways
- Implement strict image validation and size limits before processing user-supplied media
- Use sandboxed image processing in separate processes with resource limits and crash isolation
- Keep canvas and underlying image libraries (Cairo, libpng, libjpeg, libgif) updated to patched versions
- Validate image file headers and format compliance before parsing
- Implement monitoring for process crashes and unusual memory behavior
- Consider using alternative, more mature image processing solutions with better security records
- Apply principle of least privilege to image processing services

## Variant hunting
Search for similar buffer overflow patterns in other Node.js image libraries (Jimp, Sharp, ImageMagick bindings). Test video processing libraries (ffmpeg bindings) and document parsing (pdf2image) with malformed files. Fuzz SVG, WebP, and TIFF parsers in canvas and related packages.

## MITRE ATT&CK
- T1190
- T1499
- T1499.004

## Notes
The report mentions !exploitable analysis suggesting potential RCE, but the primary confirmed impact is DoS through segmentation faults. The vulnerabilities were discovered through systematic fuzzing with AFL, demonstrating the effectiveness of fuzzing for finding memory safety issues in media parsers. The high download statistics (~1.5M annually in 2017) indicate widespread potential impact.

## Full report
<details><summary>Expand</summary>

There is at least a DoS vulnerability in canvas.
It segfaults node.js which leads to a Denial of Service, but according to !exploitable it could possibly be worse

## Module

**canvas**

node-canvas is a Cairo backed Canvas implementation for NodeJS.

https://www.npmjs.com/package/canvas

version: 1.6.9

Stats
2,207 downloads in the last day
42,354 downloads in the last week
194,214 downloads in the last month

~1,587,298 estimated downloads per year (2017) 

## Description

The vulnerabilities were found with fuzzing with afl. PNG, JPG and GIF parsing are all vulnerable.
The vulnerabilities can be exploited if user provided images are passed through the libraries. One example of a package using canvas, is ascci-art which generates ascii from an image. 

One of the bugs appear to be a classic buffer overflow (PNG), while for some of the other bugs it appears to try to read memory it should not have access to.

## Steps To Reproduce:

Provided with this report is a set of images triggering the vulnerabilities. These can be tested with ascii-art which uses canvas:
`ascii-art image /full/path/to/test/image`

## Supporting Material/References:

- Ubuntu 16.04 64-bit
- nodejs v9.5.0
- npm v5.6.0

## Impact

Denial of service - take down a service running on node.js, if that service can be tricked into parsing a user-supplied image
Possibly worse if !exploitable is right, and these vulnerabilities can be used to inject shell code.

</details>

---
*Analysed by Claude on 2026-05-24*
