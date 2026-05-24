# Instant Open Redirect in GitLab Web IDE Live Preview via Unsandboxed CodeSandbox iframe

## Metadata
- **Source:** HackerOne
- **Report:** 437142 | https://hackerone.com/reports/437142
- **Submitted:** 2018-11-08
- **Reporter:** chaosbolt
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, Insufficient Iframe Sandboxing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
GitLab's Web IDE embeds CodeSandbox previews in an unsandboxed iframe, allowing malicious JavaScript code to redirect the top-level window to arbitrary URLs via window.open(..., '_top'). An attacker can craft a project with malicious code that redirects users away from GitLab when they preview the code, potentially facilitating phishing or malware distribution.

## Attack scenario
1. Attacker creates a public GitLab project with innocent-looking Vue.js project files
2. Attacker includes malicious index.js containing window.open('https://evil.com', '_top') to redirect on load
3. Victim opens the project in GitLab's Web IDE and clicks 'Preview'
4. CodeSandbox iframe loads and executes the JavaScript without sandbox restrictions
5. Victim's browser is redirected to attacker's phishing site or malware distribution server
6. Attacker can now harvest credentials or deliver malware under false pretenses

## Root cause
The iframe embedding CodeSandbox in GitLab's Web IDE lacks the 'sandbox' attribute, which would restrict iframe capabilities. Without sandboxing, untrusted code executing within the iframe has full access to the window object and can manipulate the top-level browsing context.

## Attacker mindset
An attacker seeking to compromise GitLab users recognizes that developers actively browse and test code in IDEs. By embedding redirect payloads in seemingly legitimate projects, they can deceive users into visiting malicious sites. The attack requires minimal effort—just two files in a public repo—yet has broad reach since anyone previewing the code is vulnerable.

## Defensive takeaways
- Always sandbox third-party iframes using the 'sandbox' attribute with minimal required permissions (e.g., allow-scripts but not allow-top-navigation)
- Implement Content Security Policy (CSP) headers to restrict navigation and script execution contexts
- Use 'allow-top-navigation-by-user-activation' sparingly, only allowing user-triggered navigation, not programmatic redirects
- Regularly audit iframe embeddings in web applications for proper isolation
- Consider using 'allow-same-origin' cautiously; often unnecessary if proper header policies are in place
- Educate developers on iframe security risks and sandbox attribute best practices

## Variant hunting
Check for other embedded iframes (code playgrounds, preview renderers, documentation viewers) that may lack sandboxing
Test if similar preview features in other GitLab products (snippets, wikis, documentation) have the same vulnerability
Investigate whether other IDEs or code collaboration platforms embedding external services have proper sandbox controls
Look for programmatic navigations using window.location, window.parent.location, or similar in user-controlled iframes
Examine if sandbox restrictions can be bypassed via frame-busting techniques or other DOM manipulation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (delivery vector for follow-up attacks)
- T1598 - Phishing for Information (credential harvesting at redirect destination)
- T1105 - Ingress Tool Transfer (potential payload delivery)

## Notes
This is a straightforward but impactful vulnerability affecting all users of GitLab's Web IDE. The fix is simple and standard web security practice. The report demonstrates good security research methodology by providing clear reproduction steps and a concrete fix. The vulnerability has been publicly disclosed, suggesting either vendor remediation or intentional publication for awareness.

## Full report
<details><summary>Expand</summary>

Hello Gitlab team! Asset is my own gitlab installation for Ubuntu.

The issue I want to report is lack of sandbox attribute in iframe pointing to codesandbox. This results content inside iframe redirect top level window on load.

How to reproduce:

1. create index.js with following content:
```
window.open("https://evil.com","_top");
```
2.  create package.json with following content:
```
{
  "main": "index.js",
  "dependencies": {
    "vue": "latest"
  }
}
```
3. open file in Web IDE and load preview

How to fix:

1. add sandbox attribute with needed permissions (for example, you need allow-scripts for sure) on codesandbox iframe.

## Impact

Open redirect on web ide preview load.

</details>

---
*Analysed by Claude on 2026-05-24*
