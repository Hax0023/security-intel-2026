# Subdomain Takeover of d02-1-ag.productioncontroller.starbucks.com via Unclaimed Azure Cloud Service

## Metadata
- **Source:** HackerOne
- **Report:** 661751 | https://hackerone.com/reports/661751
- **Submitted:** 2019-07-27
- **Reporter:** mindtrick
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Service Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker was able to claim an orphaned subdomain by creating an Azure Cloud Service matching the dangling CNAME record. The subdomain d02-1-ag.productioncontroller.starbucks.com was pointing to an unclaimed Azure service, allowing the attacker to host arbitrary content under the Starbucks domain.

## Attack scenario
1. Attacker performs DNS enumeration and discovers the subdomain d02-1-ag.productioncontroller.starbucks.com
2. DNS query reveals NXDOMAIN status with CNAME pointing to 3edbac0a-5c43-428a-b451-a5eb268f888b.cloudapp.net
3. Attacker creates a new Azure Cloud Service with the matching name to claim the orphaned CNAME
4. Attacker deploys malicious content to the Azure Cloud Service
5. Malicious content becomes accessible at the legitimate Starbucks subdomain
6. Victims access the domain believing it is legitimate Starbucks infrastructure, enabling credential theft or malware distribution

## Root cause
DNS record was not cleaned up after Azure Cloud Service was decommissioned, leaving a dangling CNAME that pointed to an unclaimed Azure resource. No mechanism existed to prevent unauthorized parties from creating a service matching the orphaned CNAME.

## Attacker mindset
Methodical reconnaissance using standard DNS tools to identify forgotten infrastructure. Exploited the trust inherent in subdomains under a legitimate domain to conduct phishing, credential harvesting, or malware distribution attacks against users who would naturally trust content hosted under starbucks.com.

## Defensive takeaways
- Implement DNS record cleanup procedures when decommissioning cloud services
- Claim dangling DNS records with permanent entries if subdomains must be retained
- Maintain an inventory of all DNS records and their associated cloud resources
- Regularly audit DNS zones for orphaned or dangling records
- Monitor for subdomain takeover attempts and implement alerting
- Use CNAME aliasing policies that prevent unauthorized resource claims
- Implement domain verification requirements at the cloud provider level
- Consider using managed DNS providers with takeover prevention features

## Variant hunting
Search for other Starbucks subdomains with NXDOMAIN status and cloud service CNAMEs; check for similar patterns across AWS (unclaimed ELB), GCP (unclaimed DNS), and other cloud providers; enumerate parent domains for forgotten infrastructure

## MITRE ATT&CK
- T1584.001 - Compromise Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598 - Phishing
- T1566 - Phishing

## Notes
The report demonstrates a common cloud security anti-pattern where DNS records outlive their infrastructure. The attacker used basic enumeration (dig) and Azure documentation to complete the takeover. The POC was responsibly disclosed. This vulnerability type affects many organizations with incomplete infrastructure lifecycle management.

## Full report
<details><summary>Expand</summary>

**Summary:**
 I was able to claim the subdomain: d02-1-ag.productioncontroller.starbucks.com using Azure Cloud Service

**Platform(s) Affected:**
Subdomain
Azure Cloud Service

## Steps To Reproduce:
1. Using dig, I was able to determine that the subdomain 'd02-1-ag.productioncontroller.starbucks.com'   was vulnerable to takeover.  The record showed status: NXDOMAIN and was pointing to the CNAME: 3edbac0a-5c43-428a-b451-a5eb268f888b.cloudapp.net.
2. Using this information, I was able to create a new Azure Cloud Service with the name '3edbac0a-5c43-428a-b451-a5eb268f888b'.  This would resolve to the CNAME record mentioned above.
3. I then crafted a website and uploaded it to the cloud service using this as a guide: https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-how-to-create-deploy-portal.
4. I was then able to view the uploaded site at http://d02-1-ag.productioncontroller.starbucks.com

## Supporting Material/References:
POC:
http://d02-1-ag.productioncontroller.starbucks.com/poc-2sKR4C.html


## How can the system be exploited with this bug?
See impact below.

## How did you come across this bug ?
Using enumeration, I was able to discover this domain and determined it was vulnerable by the DNS record data mentioned in the steps above.

## Recommendations for fix
To mitigate this issue you can:
* Remove the DNS record from the DNS zone if it is no longer needed.
* Claim the domain name in a permanent DNS record so it cannot be used elsewhere.

## Impact

This is extremely vulnerable to attacks as a malicious user could create any web page with any content and host it on the starbucks.com domain.  This would allow them to post malicious content which would be mistaken for a valid site.  They could steal cookies, bypass domain security, steal sensitive user data, etc.  Here is a nice write-up of the vulnerabilities:  https://0xpatrik.com/subdomain-takeover/

As mentioned in the write-up above the

</details>

---
*Analysed by Claude on 2026-05-24*
