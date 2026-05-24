# Default Nextcloud Server Config and iOS Nextcloud Client Leak Sharee Searches to Nextcloud Lookup Server

## Metadata
- **Source:** HackerOne
- **Report:** 1167919 | https://hackerone.com/reports/1167919
- **Submitted:** 2021-04-18
- **Reporter:** rtod
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Privacy Violation, Unintended Data Transmission, Default Insecure Configuration
- **CVEs:** CVE-2021-22912
- **Category:** uncategorised

## Summary
The iOS Nextcloud client fails to pass the lookup parameter when searching for sharees, causing all share searches to be automatically sent to the global Nextcloud lookup server by default. This leaks search queries and user sharing patterns to a third-party system without explicit user consent, whereas web and desktop clients only query the lookup server when users explicitly enable global search.

## Attack scenario
1. User installs iOS Nextcloud client and connects to their Nextcloud server instance
2. User initiates sharing a file by searching for a recipient (sharee) using the share dialog
3. iOS client makes API request to /ocs/v2.php/apps/files_sharing/api/v1/sharees but omits the lookup parameter
4. Server-side ShareesAPIController defaults lookup to true due to missing parameter
5. Search query is forwarded to the global Nextcloud lookup server (run by Nextcloud GmbH)
6. Lookup server logs the search query along with source IP, revealing sharing patterns and recipient search behavior

## Root cause
The iOS client does not explicitly set the 'lookup' parameter in sharee search API requests. The server-side ShareesAPIController treats the missing parameter as a truthy value (lookup enabled), defaulting to querying the global lookup server. This differs from web and desktop clients which implement local-first search and only query the lookup server when users explicitly opt-in.

## Attacker mindset
An attacker controlling or monitoring the Nextcloud lookup server infrastructure could profile users' sharing patterns, discover organizational relationships through recipient searches, identify sensitive collaboration targets, or correlate search queries across multiple Nextcloud instances to build intelligence on user behavior and organizational structures.

## Defensive takeaways
- Explicitly define and enforce default parameter values in API controllers rather than relying on implicit truthy/falsy behavior
- Implement privacy-by-default: local search should be exhausted before querying external services
- Ensure consistent behavior across all client implementations (web, desktop, mobile) for privacy-sensitive operations
- Add clear user-facing warnings when operations transmit data to third-party servers, with explicit opt-in requirements
- Conduct privacy impact analysis for features with distributed architecture involving third-party servers
- Document API parameters and their default behaviors explicitly in specifications
- Implement parameter validation and sanitization at API boundaries
- Consider rate-limiting or logging for lookup server queries to detect abuse patterns

## Variant hunting
Check if other Nextcloud mobile clients (Android, previously noted as vulnerable) have identical issues
Audit other API endpoints with optional 'lookup' or similar parameters for consistent default handling
Investigate if search functionality in other apps (contacts, calendar) exhibits the same behavior
Review other third-party integrations that query external Nextcloud services for default-enabled data transmission
Test if related parameters controlling external API queries have consistent implementation across clients
Examine legacy client versions to determine when this privacy regression was introduced

## MITRE ATT&CK
- T1598 - Phishing: Reconnaissance (gathering user sharing patterns)
- T1592 - Gather Victim Org Information (discovery of organizational relationships)
- T1516 - Exploit Code Execution (potential indirect via lookup server compromise)
- T1040 - Network Sniffing (passive observation of API queries)
- T1020 - Automated Exfiltration (unintended data transmission to lookup server)

## Notes
This report explicitly references a parallel vulnerability in the Android client (report 1167916), suggesting systemic issues in mobile client development practices. The vulnerability is particularly concerning because it affects multiple platforms with identical root causes. The distinction between behavior across platforms (web requiring explicit opt-in vs. mobile defaulting to global search) indicates either incomplete feature parity or platform-specific implementation gaps. The lookup server infrastructure represents a centralized privacy risk requiring careful threat modeling.

## Full report
<details><summary>Expand</summary>

In short this is the same as https://hackerone.com/reports/1167916 but then for iOS so please forgive the copy paste

On a clean Nextcloud setup the functionality "Search global and public address book for users" is enabled.
Now when searching for a sharee to share with. The lookup parameter is not passed to the server. Resulting in
https://github.com/nextcloud/server/blob/master/apps/files_sharing/lib/Controller/ShareesAPIController.php#L144
the lookup being true. So the lookup server of Nextcloud will be searched by default.

## Impact

Anybody sharing trough the android app. Leaks their sharee searches to the Nextcloud lookup server.
Now the server can can only see the origin Nextcloud server (or rather the IP of that). Still. This should not be leaked by default.

On the web and desktop there is first a local search. And only if the user explicitly presses the search globally the lookup server is queried. (to be fair this could also be more clear that it actually sends data to other systems)

</details>

---
*Analysed by Claude on 2026-05-24*
