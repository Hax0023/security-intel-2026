# Denial of Service in Account Statistics Endpoint via Unrestricted Period Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 136221 | https://hackerone.com/reports/136221
- **Submitted:** 2016-05-04
- **Reporter:** apok
- **Program:** Mapbox
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Resource Exhaustion, Insufficient Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The account statistics API endpoint (mapbox.com/core/statistics/v1) lacks validation on the 'period' and 'interval' parameters, allowing authenticated users to request arbitrary time ranges that return disproportionately large response payloads. By modifying the period parameter to span extended timeframes and changing interval granularity from 'day' to 'hour', an attacker could generate excessive data (372 KB observed) potentially causing resource exhaustion and service degradation.

## Attack scenario
1. Attacker authenticates to Mapbox account or identifies a valid user account identifier
2. Attacker crafts request to statistics endpoint with manipulated 'period' parameter spanning months or years (e.g., 1451766083142,1462370883143)
3. Attacker changes 'interval' parameter from 'day' to 'hour' to multiply data granularity and response size
4. Attacker optionally sets end date to future timestamp to further increase data window
5. Endpoint processes request without validating reasonable time range limits and generates 350+ KB responses
6. Multiple requests with maximum parameters cause CPU/memory consumption and potential service unavailability for other users

## Root cause
The statistics endpoint accepts arbitrary timestamp values in the 'period' parameter without server-side validation of maximum allowed time ranges. Combined with granular 'interval' options ('hour' vs 'day'), this creates a multiplication effect on response payload sizes. No rate limiting or query complexity limits are enforced.

## Attacker mindset
Opportunistic attacker seeks to abuse poorly constrained APIs for resource consumption attacks. The attacker demonstrates responsible disclosure ethics by obtaining prior authorization from security team, limiting test scope, and providing detailed reproduction steps rather than launching full DoS.

## Defensive takeaways
- Implement maximum time range limits (e.g., 90 days) for statistics queries regardless of input
- Add server-side validation that rejects period parameters exceeding defined thresholds
- Enforce reasonable combinations of parameters (e.g., disallow 'hour' interval for periods > 30 days)
- Implement rate limiting and query complexity scoring for statistics endpoints
- Set maximum response payload sizes and truncate/paginate oversized results
- Monitor statistics endpoint for unusual access patterns (long periods, frequent requests)
- Reject future-dated end parameters in historical statistics queries
- Consider requiring explicit opt-in or additional authentication for extended data exports

## Variant hunting
Test other date-range parameters in reporting/analytics endpoints for similar issues
Check if 'metrics' and 'services' parameters have enumeration/selection limits
Attempt to combine period exploitation with other parameters to maximize response size
Test if authenticated users can request statistics for other accounts via parameter manipulation
Investigate if pagination exists but can be bypassed to retrieve all results at once
Test CSV/JSON export endpoints for similar unrestricted data dumping
Check if caching mechanisms can be exploited to amplify DoS impact

## MITRE ATT&CK
- T1190
- T1499.1
- T1499.4

## Notes
Reporter demonstrates professional responsible disclosure practices by obtaining pre-authorization from security@mapbox.com, limiting test scope to avoid production impact, and providing detailed reproduction steps. Guidelines explicitly noted DoS vulnerabilities out of scope, making pre-approval critical for this submission. Vulnerability represents classic input validation gap in query parameters where business logic constraints should restrict resource allocation. Severity moderated from high to medium due to requiring authentication and no confirmed actual service impact demonstrated.

## Full report
<details><summary>Expand</summary>

Hi Mapbox,
I know that your guidelines explicitly say that Denial of Service coinditions are not in scope and should not be attempted, but I maintained the testing between adequate parameters so as to not to create excessive load on your backend. I also sent an email to security@mapbox.com prior to submitting this report and Alex Ulsh and he or she (Sorry, can't know which since Alex is a unisex name hahaha) told me that this could be an exception.

The vulnerability relies on the https://www.mapbox.com/core/statistics/v1/apokh11/account endpoint, it seems that by modifying the "period" parameter to an arbitrary value, the amount of data returned increases probably without any limit, furthermore, if the interval is set to "hour" instead of "day", it is possible to increase the amount of data returned even further. To avoid affecting the availability of the server, I limited my testing to a small period, which still returned around 350 kb of data.

The amount of data can also be increased if the end date of the period requested is set to a point in the future.

To reproduce:
1) Create an account or login to an existing account.
2) Access this URL: https://www.mapbox.com/core/statistics/v1/apokh11/account?interval=day&period=1461766083142%2C1462370883143&metrics=countries%2Cbrowsers%2Chosts%2Cmaps%2Cversion&services=mapview%2Ctile%2Cstatic%2Cgeocode%2Cpermanentgeocode%2Cdirections%2Csurface&_=1462370883155
3) Observe that the amount of data returned is around 2.5 Kb.
4) Modify the "interval" parameter to "hour" and the "Period" parameter to, for example "1451766083142,1462370883143" 
5) Observe that the amount of data returned increased to 372 Kb. 

Not tested: If the period is long enough, the amount of time taken to answer the request will probably be increased as well.

Implication: A malicious individual could leverage this feature by asking for extended periods to cause high loads on the backend, which in turn could affect the availiability of the service.

Recommendation: Limit the period length to an amount established by the business logic, so as to mitigate the possibility of using this functionality with malicious intent.

Let me know if you require any additional tests and/or information.
Kind Regards,
Apok.

</details>

---
*Analysed by Claude on 2026-05-24*
