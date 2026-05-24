# Unauthorized Access to Argo Dashboard

## Metadata
- **Source:** HackerOne
- **Report:** 2247231 | https://hackerone.com/reports/2247231
- **Submitted:** 2023-11-09
- **Reporter:** devdevrl
- **Program:** Undisclosed (Redacted)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Authentication, Broken Authorization, Insufficient Access Controls
- **CVEs:** None
- **Category:** uncategorised

## Summary
An Argo Workflows dashboard is exposed without proper authentication controls, allowing unauthenticated users to access and manipulate workflows. Attackers can view, delete, and modify workflows as well as manipulate sensors, potentially leading to data disclosure and operational disruption.

## Attack scenario
1. Attacker discovers the exposed Argo dashboard subdomain through reconnaissance or public disclosure
2. Attacker navigates to the dashboard URL without providing any credentials
3. Attacker gains access to the workflows management interface due to missing authentication
4. Attacker views sensitive workflow definitions, logs, and configuration data
5. Attacker modifies or deletes existing workflows to disrupt operations
6. Attacker manipulates sensor configurations to trigger malicious workflow executions

## Root cause
The Argo Workflows dashboard was deployed without implementing authentication mechanisms or access controls. The application lacks proper identity verification before granting access to administrative functions.

## Attacker mindset
An attacker would recognize this as a quick win for gathering intelligence on the organization's CI/CD pipelines and automation workflows. The ability to modify workflows presents opportunities for supply chain attacks, data exfiltration, or infrastructure sabotage without requiring valid credentials.

## Defensive takeaways
- Implement authentication (OAuth2, OIDC, or SAML) on all Argo dashboard endpoints
- Deploy reverse proxy authentication (e.g., Nginx auth_request) in front of Argo
- Apply network segmentation to restrict Argo dashboard access to authorized networks only
- Enable RBAC (Role-Based Access Control) within Argo for fine-grained permissions
- Implement audit logging for all workflow modifications and sensor changes
- Conduct regular security reviews of exposed management interfaces
- Use web application firewalls to detect and block unauthorized access attempts

## Variant hunting
Look for other Argo deployments with similar exposure patterns. Check for other exposed Kubernetes management dashboards (Kubernetes Dashboard, Rancher). Investigate if other microservices in the organization use similar authentication patterns or if they were deployed with default/missing security configurations.

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1087
- T1526
- T1021

## Notes
The writeup is relatively brief and lacks technical depth. The redactions prevent full assessment but indicate a legitimate exposure. The reporter correctly identifies this as a chain vulnerability (information disclosure + operational impact). The 'low' severity self-assessment appears conservative given the ability to modify/delete workflows, which could have significant business impact.

## Full report
<details><summary>Expand</summary>

##Summary 
Hi team i hope you are well t is a pleasure to work in your program. I will begin to present the vulnerability that I found it: Unauthorized access to Argo dashboard 

After conducting an in-depth analysis, I have identified a security concern within the Argo deployment to which I have access. Specifically, I can manipulate workflows, including deletion and addition, as well as modify sensors. While the immediate impact is assessed as low, it is important to acknowledge that this vulnerability could potentially lead to unauthorized access and compromise sensitive data in future deployments. Urgent attention and corrective measures are advised to mitigate this risk and ensure the security of the system.

##Steps

 Vulnerable subdomain :

```
1. https://████/
```

###Example POC:  https://█████/

███
███████
███████

## Impact

Leads to information disclosure

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Go to the webisite below:
https://████████/workflows

## Suggested Mitigation/Remediation Actions
Block access to dashboard



</details>

---
*Analysed by Claude on 2026-05-24*
