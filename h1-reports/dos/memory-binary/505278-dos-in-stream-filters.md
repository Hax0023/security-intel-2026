# Denial of Service in PHP Stream Filters - Endless Loop in convert.iconv Filter

## Metadata
- **Source:** HackerOne
- **Report:** 505278 | https://hackerone.com/reports/505278
- **Submitted:** 2019-03-05
- **Reporter:** meitis
- **Program:** PHP
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Infinite Loop, Resource Exhaustion
- **CVEs:** CVE-2018-10546
- **Category:** memory-binary

## Summary
A maliciously crafted stream filter operation using convert.iconv with specific character encoding parameters causes PHP to enter an infinite loop, consuming CPU resources until the process is terminated. This can be triggered with minimal code and no special privileges, allowing attackers to exhaust server resources.

## Attack scenario
1. Attacker identifies PHP application that processes user-controlled data through stream filters
2. Attacker crafts input or exploits file upload functionality to trigger stream_filter_append with convert.iconv.iso-10646/utf8//IGNORE parameters
3. PHP process enters infinite loop during stream_get_contents() operation on filtered stream
4. CPU utilization spikes to 100% for affected process
5. If multiple processes are available, attacker repeats attack to exhaust all PHP-FPM workers or available processes
6. Server becomes unresponsive to legitimate requests due to resource exhaustion

## Root cause
The convert.iconv stream filter implementation contains a logic error in character conversion handling that fails to properly advance the stream position or handle conversion state, causing the filter to repeatedly process the same data without termination.

## Attacker mindset
Exploit a simple, reproducible denial of service vector that requires minimal code and knowledge. Target the stream filter functionality which may be used in file processing, image handling, or data transformation operations. Aim to crash or exhaust resources of vulnerable PHP applications with minimal effort.

## Defensive takeaways
- Validate and sanitize filter parameters when accepting user-controlled stream filter specifications
- Implement resource limits and timeouts for stream operations to prevent infinite loops
- Avoid using convert.iconv filters with untrusted encoding parameters; prefer tested alternatives like mb_convert_encoding()
- Monitor for CPU spikes and implement rate limiting on stream processing operations
- Use PHP stream filters only on trusted input streams; isolate untrusted data processing
- Keep PHP and stream extension libraries updated to receive security patches
- Consider disabling unnecessary stream filter wrappers in php.ini if not required

## Variant hunting
Search for other stream filter combinations (convert.quoted-printable, convert.base64, etc.) with unusual encoding parameters that may trigger similar infinite loops. Test chained filters with edge case character sequences. Investigate other iconv wrapper usage patterns in PHP extensions.

## MITRE ATT&CK
- T1499.4
- T1190

## Notes
This vulnerability is particularly dangerous because it requires only a few lines of PHP code and no authentication. Applications processing file uploads or handling text transformations through stream filters are at risk. The issue appears to be in the underlying iconv implementation or its PHP wrapper. Related to PHP bug report #76249.

## Full report
<details><summary>Expand</summary>

see bug report
https://bugs.php.net/bug.php?id=76249

as simple as
<?php
$fh = fopen('php://memory', 'rw');
fwrite($fh, "abc");
rewind($fh);
stream_filter_append($fh, 'convert.iconv.iso-10646/utf8//IGNORE', STREAM_FILTER_READ, []);
echo stream_get_contents($fh);

=> one process running in an endless loop

## Impact

DOS, process ends up in an endless loop, CPU (or available php processes or both) of affected system get easily exhausted

</details>

---
*Analysed by Claude on 2026-05-24*
