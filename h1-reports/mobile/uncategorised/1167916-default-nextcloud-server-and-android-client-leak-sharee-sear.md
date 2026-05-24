# Default Nextcloud Server and Android Client leak sharee searches to Nextcloud lookup server

## Metadata
- **Source:** HackerOne
- **Report:** 1167916 | https://hackerone.com/reports/1167916
- **Submitted:** 2021-04-18
- **Reporter:** rtod
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Unintended Data Transmission, Privacy Violation
- **CVEs:** CVE-2021-22905
- **Category:** uncategorised

## Summary
The Nextcloud Android client leaks user sharee searches to the Nextcloud lookup server by default due to missing lookup parameter validation, while web and desktop clients require explicit user action. This unintended data transmission exposes search queries to external systems without user consent or awareness.

## Attack scenario
1. Attacker or researcher sets up Nextcloud server with default settings where 'Search global and public address book for users' is enabled
2. User opens Nextcloud Android app and attempts to share a file with another user
3. User begins typing a search query in the sharee search field to find a recipient
4. Android app automatically sends the search query to the Nextcloud lookup server without the lookup parameter being set
5. Lookup server receives and logs the search query along with the origin Nextcloud server IP address
6. Attacker with access to lookup server logs gains visibility into what users are searching for and which servers are using the app

## Root cause
The ShareesAPIController.php in the server-side API endpoint defaults the 'lookup' parameter to true when it is not explicitly passed. The Android client fails to send this parameter in its request, causing unintended queries to the external lookup server. The web and desktop clients implement client-side logic to only query the lookup server on explicit user action, but the Android client lacks this protective behavior.

## Attacker mindset
An attacker with access to the Nextcloud lookup server infrastructure, or a network eavesdropper, could monitor sharee search patterns to perform user profiling, enumerate organizational structures through search query analysis, or identify which Nextcloud instances are actively being used. The attacker benefits from default behavior that was likely unintended and inconsistent across client implementations.

## Defensive takeaways
- Implement explicit opt-in for lookup server queries rather than default-to-enabled behavior
- Enforce consistent behavior across all client implementations (web, desktop, mobile) for privacy-sensitive operations
- Add clear user-facing notifications when data will be transmitted to external servers
- Require explicit lookup parameter in API requests rather than defaulting it server-side
- Conduct security review of default settings for data transmission to external systems
- Implement client-side validation to prevent unintended external API calls
- Add logging and monitoring for unexpected lookup server queries to detect similar issues

## Variant hunting
Check if other Nextcloud API endpoints have similar default parameter behaviors that leak data
Review all mobile client implementations for similar patterns of missing privacy controls present in desktop clients
Audit other sharee/contact search functionality across all Nextcloud apps for inconsistent privacy controls
Test other external service integrations in Nextcloud for unintended default data transmission
Investigate whether other parameters intended to control external API calls are being ignored by clients

## MITRE ATT&CK
- T1041
- T1020
- T1592
- T1087

## Notes
This is a privacy and data leakage issue rather than a traditional security vulnerability. The inconsistency between client implementations suggests this was unintended behavior. The lookup server was reportedly down at time of report, limiting real-world exposure. The reporter explicitly notes that even web/desktop clients could be more transparent about when they query external systems. This highlights the importance of secure-by-default principles and consistent privacy behavior across platform implementations.

## Full report
<details><summary>Expand</summary>

On a clean Nextcloud setup the functionality "Search global and public address book for users" is enabled.

Now when searching for a sharee to share with. The lookup parameter is not passed to the server. Resulting in
https://github.com/nextcloud/server/blob/master/apps/files_sharing/lib/Controller/ShareesAPIController.php#L144

the lookup being true. So the lookup server of Nextcloud will be searched by default.
It seems that the lookup server is down now. But this seems to be an error I assume?

## Impact

Anybody sharing trough the android app. Leaks their sharee searches to the Nextcloud lookup server.
Now the server can can only see the origin Nextcloud server (or rather the IP of that). Still. This should not be leaked by default.

On the web and desktop there is first a local search. And only if the user explicitly presses the search globally the lookup server is queried. (to be fair this could also be more clear that it actually sends data to other systems)

</details>

---
*Analysed by Claude on 2026-05-24*
