# Blind Stored XSS in Shopify Internal Parquet Viewer

## Metadata
- **Source:** HackerOne
- **Report:** 1103298 | https://hackerone.com/reports/1103298
- **Submitted:** 2021-02-14
- **Reporter:** testingforbugs
- **Program:** Shopify
- **Bounty:** Unknown (redacted in report)
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Blind XSS, Improper Input Validation, Unsafe HTML Rendering
- **CVEs:** None
- **Category:** web-api

## Summary
A blind stored XSS vulnerability was discovered in Shopify's internal Parquet Viewer tool, where malicious payloads could be injected and executed when the file was processed by employees. The vulnerability allowed arbitrary JavaScript execution in the context of an internal analysis tool, potentially leading to credential theft or unauthorized access.

## Attack scenario
1. Attacker identifies that Parquet files processed by Shopify's internal Parquet Viewer tool do not properly sanitize data
2. Attacker crafts a malicious Parquet file containing XSS payload in a field that will be rendered as HTML (likely in 'Sample Data' section)
3. Attacker uploads or provides the malicious Parquet file through an entry point (unknown, possibly file upload functionality or data pipeline)
4. File is stored and later accessed by a Shopify employee through the Parquet Viewer interface
5. When employee opens the tool and navigates to 'Sample Data' section, the stored XSS payload executes in their browser context
6. Attacker's payload captures employee credentials, session tokens, or performs actions on behalf of the employee within internal systems

## Root cause
The Parquet Viewer application fails to properly sanitize or encode data extracted from Parquet files before rendering it as HTML. The application likely uses innerHTML or equivalent unsafe DOM manipulation when displaying sample data, allowing embedded scripts to execute.

## Attacker mindset
The reporter demonstrates sophisticated understanding of blind XSS techniques, including the ability to identify execution via IP/User-Agent logging and knowledge of internal Shopify infrastructure (GCS paths, employee names). This suggests either internal reconnaissance or previous knowledge of target systems. The redacted sensitive information indicates responsible disclosure awareness.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) for all internal tools to prevent inline script execution
- Always encode/escape user-controlled data before rendering to DOM; use textContent instead of innerHTML
- Apply input validation and sanitization at file parsing layer for all data sources
- Implement output encoding specific to HTML context for all rendered data
- Add security review process for internal tools with same rigor as customer-facing applications
- Monitor for blind XSS via DNS/HTTP callbacks; implement detection in internal tool infrastructure
- Use security headers (X-Content-Type-Options, X-Frame-Options) on internal tool pages
- Implement DOM-based XSS protection libraries for safe HTML rendering

## Variant hunting
Test other Shopify internal data visualization/analysis tools for similar vulnerabilities
Examine other file format viewers (CSV, JSON, XML viewers) for identical sanitization gaps
Check if other data processing pipelines render unvalidated data from external sources
Look for blind XSS in internal reporting tools that aggregate user-submitted data
Test file upload functionality across internal tools for stored XSS in metadata/content
Examine sample data preview functionality in other analytical/diagnostic tools

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
Report contains significant redactions of sensitive information including employee names, IP addresses, and internal GCS paths. This demonstrates responsible disclosure but limits technical analysis. The 'file://' URL scheme indicates local HTML file generation, suggesting the viewer generates temporary HTML from Parquet data. The fact that payload execution was confirmed via employee User-Agent logging shows attacker sophisticated tracking methodology. Unknown entry point is concerning - could indicate vulnerability in data pipeline ingestion rather than direct user upload.

## Full report
<details><summary>Expand</summary>

##Summary:
Hey, hope you are doing well, I have found that one of my blind xss payload fired in one of your internal tool `Parquet viewer` on 14th feb 11:23 PM IST

I don’t know the entry point were I put my bXSS payload, But this is fired in one of your employee ( `[██████` ) computer.

##Details:
I am attaching all the details here.

* Vulnerable Page URL
`file://localhost/private/var/folders/4m/pdc_bjcj17dcxbtlllqqq81w0000gp/T/parquet-viewer-6296239398097329598.html`

* User IP Address
`█████████`

* User-Agent
`Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36`

You can see the name of Shopify employee `████████` at `gs://starscream-adhoc/user/███/shop_dimension/part-00039-4039dc30-6a7a-4108-838d-fb1daec9a216-c000.snappy.parquet`
* ███████

* Open the dom.html and go o the `Sample Data` ███████
████

## Impact

████

Kind Regards
Aman

</details>

---
*Analysed by Claude on 2026-05-12*
