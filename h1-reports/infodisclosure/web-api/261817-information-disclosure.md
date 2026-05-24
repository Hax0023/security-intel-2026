# Information Disclosure via Publicly Accessible JavaScript File Containing Private Data

## Metadata
- **Source:** HackerOne
- **Report:** 261817 | https://hackerone.com/reports/261817
- **Submitted:** 2017-08-20
- **Reporter:** cuso4
- **Program:** Legal Robot
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Hardcoded Credentials/PII
- **CVEs:** None
- **Category:** web-api

## Summary
A publicly accessible JavaScript file contained sensitive internal information including private cryptographic hashes, employee names, email addresses, and third-party software details. The file was served directly from the application's web root without any access controls or obfuscation, allowing any unauthenticated user to retrieve this data.

## Attack scenario
1. Attacker discovers the application domain and enumerates common asset paths
2. Attacker identifies a JavaScript file with a non-standard naming pattern (hash filename)
3. Attacker retrieves the JavaScript file via HTTP GET request without authentication
4. Attacker parses the file content and discovers hardcoded PII (names, email addresses)
5. Attacker identifies cryptographic hashes and third-party software information
6. Attacker uses discovered credentials/emails for social engineering, account compromise, or correlates with breached databases

## Root cause
Sensitive data (PII, hashes, internal configuration) was embedded directly in a client-side JavaScript file that was publicly served without access controls. The file was likely generated during build/deployment without proper secrets management or data sanitization.

## Attacker mindset
Reconnaissance and information gathering. The attacker likely discovered this through automated scanning or manual exploration of web application assets, recognizing that JavaScript files often contain exploitable hardcoded data, credentials, or system information.

## Defensive takeaways
- Never hardcode sensitive data (PII, hashes, credentials) in client-side code
- Implement strict secrets management and environment-based configuration separation
- Sanitize build artifacts before deployment; audit all client-side code for sensitive information
- Use obfuscation, minification, and source map removal in production builds
- Implement Content Security Policy (CSP) headers to limit script exposure
- Conduct regular scanning of public-facing assets for exposed credentials and PII
- Use automated tooling (SAST, dependency scanning) to detect hardcoded secrets before deployment
- Implement proper access controls and authentication for sensitive assets

## Variant hunting
Search for other JavaScript files with similar hash-based naming patterns in the application
Enumerate common paths (.js, .min.js, /assets/, /static/, /dist/) for similar exposed files
Check git repositories and public source control for accidentally committed secrets
Scan compiled/minified files for Base64-encoded or obfuscated sensitive data
Look for environment variables, API keys, or authentication tokens in build artifacts
Check source maps (.js.map files) which often contain unminified source code with sensitive data

## MITRE ATT&CK
- T1526 - Gather Victim Identity Information
- T1592 - Gather Victim Identity Information
- T1589 - Gather Victim Identity Information (Email Addresses)
- T1598 - Phishing for Information
- T1598.004 - Spearphishing Link
- T1598.003 - Spearphishing Link
- T1040 - Network Sniffing

## Notes
The report quality is poor with minimal technical detail, but the vulnerability is clear and high-impact. The exposure of PII (names, emails) creates direct social engineering risks. The unknown hashes and third-party software details could enable supply chain attacks or targeted reconnaissance. The file naming pattern (hash-based) suggests this may be a compiled/bundled asset from a build system, indicating a systemic secrets management failure in the deployment pipeline rather than isolated hardcoding.

## Full report
<details><summary>Expand</summary>

team,
I believe that it might be dislose some internal information .it's should not be there.


URL:
 https://app.legalrobot.com/89e4d4e5f94c29cff9fb29556730107fadae85ff.js


WHAT I GOT :

there are private hashes (i don't know from where they belongs ).

efdea4cdb677750a420fee807eacf21eb9898ae79b9768766e4faa04a2d4a34","4211ab0694635168e997b0ead2a93daeced1f4a04a95c0f6cfb199f69e56eb77"],["2b4ea0a797a443d293ef5cff444f4979f06acfebd7e86d277475656138385b6c","85e89bc037945d93b343083b5a1c86131a01f60c50269763b570c854e5c09b7a"],["352bbf4a4cdd12564f93fa332ce333301d9ad40271f8107181340aef25be59d5","321eb4075348f534d59c18259dda3e1f4a1b3b2e71b1039c67bd3d8bcf81998c"],


PRIVATE NAME AND EMAIL :

{name:"ccuilla",email:"ccuilla@gmail.com"}
Name:"rdickert",email:"robert.dickert@gmail.com

and two or three more ...


MOSTLY INTERNAL THIRD PARTY SOFTWARE INFORMATION ,WHICH SHOULD NOT BE THERE.

-REGARDS



</details>

---
*Analysed by Claude on 2026-05-24*
