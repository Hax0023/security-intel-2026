# XML External Entity (XXE) Injection Leading to Remote Code Execution via C-CDA XML Upload

## Metadata
- **Source:** HackerOne
- **Report:** 55431 | https://hackerone.com/reports/55431
- **Submitted:** 2015-04-08
- **Reporter:** sasi2103
- **Program:** drchrono
- **Bounty:** Unknown (Historical report from Feb 2015)
- **Severity:** Critical
- **Vuln:** XML External Entity (XXE) Injection, Arbitrary File Read, Remote Code Execution, Insecure Deserialization
- **CVEs:** None
- **Category:** web-api

## Summary
The patient management system's C-CDA XML upload feature fails to properly sanitize XML input, allowing authenticated users to inject malicious external entity declarations. This enables arbitrary file disclosure (e.g., /etc/passwd) and potentially remote code execution through entity expansion attacks or OS command injection via XXE handlers.

## Attack scenario
1. Attacker authenticates to drchrono platform with valid credentials
2. Navigates to Patients section and selects a patient record for update
3. Clicks 'Update patient (via C-CDA XML)' feature
4. Downloads legitimate C-CDA XML template from the system
5. Modifies XML to inject DOCTYPE with SYSTEM entities pointing to sensitive files (e.g., file:///etc/passwd) or command execution payloads
6. Uploads malicious XML and clicks 'Preview' to trigger XML parsing, revealing sensitive data or executing arbitrary commands

## Root cause
The application uses an XML parser with XXE processing enabled without proper input validation, schema enforcement, or DTD/entity declaration filtering. The parser directly processes user-supplied C-CDA XML files during the preview/upload workflow without disabling external entity resolution.

## Attacker mindset
An authenticated attacker recognizes that medical software typically handles standardized XML formats (C-CDA) and assumes the parser may not be properly hardened. The attacker leverages trust in XML file uploads and uses XXE as an initial foothold for data exfiltration (patient records, configuration) or escalation to RCE through wrapper protocols or expect:// handlers.

## Defensive takeaways
- Disable XXE processing in all XML parsers: set features like XMLConstants.ACCESS_EXTERNAL_DTD to empty string and XMLConstants.ACCESS_EXTERNAL_SCHEMA to empty
- Use allowlist-based XML schema validation (XSD) for C-CDA documents before parsing
- Implement strict DTD denial: reject any DOCTYPE declarations in uploaded XML or pre-process to strip them
- Validate file uploads by type, size, and content-based inspection; consider re-serializing XML through safe parsers
- Apply principle of least privilege: run XML parsing in sandboxed process with no file system or command execution access
- Log and monitor XML parsing errors and unusual entity declarations for security alerts
- Use modern, patched XML libraries; test against known XXE payloads (Billion Laughs, External Entity, Quadratic Blowup)
- Implement authentication/authorization checks before allowing file previews and limit preview scope to sanitized output

## Variant hunting
Search for other file upload endpoints accepting XML, JSON, or YAML formats (often vulnerable to XXE or deserialization)
Test SOAP-based APIs or webservices for XXE via SOAP envelope manipulation
Check for XXE via SVG, PDF, or Office document uploads (OOXML, ODF) that embed XML
Probe CSV-to-XML converters or data import features for XXE during transformation
Test XML comments, CDATA sections, and namespace declarations for XXE bypass techniques
Investigate error messages for information disclosure about file paths or parser internals during XXE exploitation
Look for blind XXE via time-based or out-of-band (OOB) DNS/HTTP exfiltration if direct output is unavailable

## MITRE ATT&CK
- T1190
- T1105
- T1041
- T1005
- T1552
- T1083

## Notes
This is a historical report from February 2015 on the drchrono medical platform. XXE in healthcare systems is particularly dangerous due to exposure of PHI (Protected Health Information) and medical records. The presence of a 'Preview' feature that renders parsed XML output makes exploitation straightforward for data exfiltration. C-CDA (Continuity of Care Document Architecture) is a standard in healthcare IT but requires careful handling. The report suggests potential RCE, likely via expect:// protocol handlers or shell metacharacter injection in XXE payloads, though the exact vector is not detailed. Recommend full security review of XML processing across all healthcare data import/export workflows.

## Full report
<details><summary>Expand</summary>

Hello security team,

I have reported this issue on Feb 6, 2015 and i'm resubmit it here again.
I was able to do XXE attack on your site and exposed the /etc/passwd file.
Scenario:
1. Login to drchrono  site.
2. Click on patients->patient
3. Click on ' Update patient (via C-CDA XML).'
4. Select the file I attached, (AXAX000001.xml), I download it from your site and added there struct for my exploit.
5. Click on 'Preview' and you'll see the content of /etc/passwd, (That can be any file on the system or any command). See xxe.png atttachement.


Best regards,
Sasi

</details>

---
*Analysed by Claude on 2026-05-12*
