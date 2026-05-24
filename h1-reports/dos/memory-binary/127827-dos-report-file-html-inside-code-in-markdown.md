# DOS Report - FILE html inside <code> in markdown

## Metadata
- **Source:** HackerOne
- **Report:** 127827 | https://hackerone.com/reports/127827
- **Submitted:** 2016-04-02
- **Reporter:** pisarenko
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service (DOS), File Handling Vulnerability, Markdown Processing Flaw
- **CVEs:** None
- **Category:** memory-binary

## Summary
A malicious file embedded within markdown code blocks can render reports unopenable, causing denial of service. By crafting specific HTML content wrapped in markdown code tags, an attacker can crash or hang the report viewing functionality. The vulnerability impacts report accessibility and could be exploited to sabotage vulnerability disclosures.

## Attack scenario
1. Attacker receives an invite to report to a program on HackerOne
2. Attacker creates a new vulnerability report with carefully crafted HTML content
3. Attacker embeds the malicious content within markdown code blocks using backticks
4. Attacker includes file attachments (F82764, F82765) with specially formatted content
5. When the report creator or other users attempt to open the report, the markdown renderer processes the code block
6. The malicious HTML/file content causes the report page to become unresponsive or crash (DOS)

## Root cause
HackerOne's markdown parser does not properly sanitize or validate file content and HTML within code blocks, allowing specially crafted content to cause rendering issues or application crashes when processed.

## Attacker mindset
Disrupt collaboration by making reports inaccessible to intended recipients; sabotage vulnerability disclosure process; create chaos in communication channels; potentially extort or coerce organizations by making critical reports unavailable.

## Defensive takeaways
- Implement strict input validation for file uploads and markdown content
- Sandbox markdown rendering in separate processes with resource limits
- Add file type and content whitelisting for attachments
- Implement timeout mechanisms for report rendering
- Use HTML entity encoding and sanitization libraries (DOMPurify, Bleach)
- Test markdown parser with adversarial inputs and fuzzing
- Implement rate limiting on report creation
- Add monitoring for rendering failures and timeouts

## Variant hunting
Test other code fence formats (triple backticks, tildes) with malicious content
Attempt SVG/XML bomb payloads within code blocks
Try deeply nested markdown structures to cause parser stack overflow
Test with other file types (PDF, images) containing malicious metadata
Attempt billion laughs attack in XML-based code blocks
Test regex-based markdown processing with ReDoS (Regular Expression DOS) patterns
Try Unicode edge cases and control characters in code blocks

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1561: Disk Wipe
- T1499: Endpoint Denial of Service

## Notes
Report quality is poor with unclear POC instructions and incomplete details. File references (F82764, F82765, F82766) are not available in the text. Severity assessment assumes DOS impact on report accessibility. The vulnerability appears to be in HackerOne's markdown rendering engine when processing file attachments within code blocks. Actual impact depends on whether the DOS is temporary (page hang) or persistent (report permanently unopenable).

## Full report
<details><summary>Expand</summary>

LOOK rezult
https://hackerone.com/reports/127809

{F82764}

POC

Copy in {F82766} TXT file (all) and create a new review 
I warn you , if you do this , then the report cannot open .

You can create a report , attach files and replace my files F82764 and F82765 , paste in the contents of the report and create it

Why is it a security bug ?
I answer , if I get an invite to report to someone , I may make it available to all


P.S EXAMPLE html inside <code> in markdown

` {F82766} `


Thanks PISARENKO


</details>

---
*Analysed by Claude on 2026-05-24*
