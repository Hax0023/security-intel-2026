# Full Path Disclosure at ads.twitter.com via x-sendfile Header

## Metadata
- **Source:** HackerOne
- **Report:** 26825 | https://hackerone.com/reports/26825
- **Submitted:** 2014-09-03
- **Reporter:** internetwache
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** Low
- **Vuln:** Information Disclosure, Full Path Disclosure, Server Header Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The ads.twitter.com application leaks full server file paths through the x-sendfile response header when uploading campaign creative assets. This information disclosure reveals internal infrastructure details including Mesos cluster structure, executor IDs, and sandbox paths that could facilitate further attacks.

## Attack scenario
1. Attacker authenticates to ads.twitter.com and navigates to the campaign creation workflow
2. Attacker selects the 'Create new twitter-follower campaign' option and reaches the creative upload interface
3. Attacker intercepts HTTP traffic with a proxy tool during the file upload process
4. Attacker observes the response headers contain x-sendfile with full internal server paths
5. Attacker catalogs disclosed path structure including Mesos framework IDs, executor names, and sandbox locations
6. Attacker uses disclosed paths as reconnaissance for subsequent LFI, RCE, or lateral movement attacks

## Root cause
The application exposes the x-sendfile header in HTTP responses, which is meant for internal server use (nginx/Apache directive for efficient file serving). The header should be stripped or not sent to clients. This likely stems from improper header handling in the application's file serving middleware or reverse proxy configuration.

## Attacker mindset
A reconnaissance-focused attacker gathering intelligence about backend infrastructure. The disclosure of Mesos orchestration details, executor IDs, and framework structure provides valuable environmental mapping for planning infrastructure-level attacks or exploiting known vulnerabilities in specific components.

## Defensive takeaways
- Strip sensitive headers (x-sendfile, x-original-url, x-aspnet-version, etc.) at the reverse proxy/WAF layer before sending responses to clients
- Implement header filtering to remove all internal-use-only directives from client-facing responses
- Conduct regular security audits of HTTP response headers for information disclosure
- Use security headers scanning tools to detect unintended path/infrastructure leakage
- Implement defense-in-depth: even if paths are disclosed, ensure file access controls prevent actual exploitation
- Review proxy/server configurations to ensure x-sendfile is only used internally

## Variant hunting
Check other Twitter domains (twitter.com, analytics.twitter.com, business.twitter.com) for similar header leakage
Test other file upload endpoints for x-sendfile, x-original-url, and similar internal headers
Look for path disclosure in error messages, logs, or other response content beyond headers
Check for leakage of other infrastructure details (AWS ARNs, Docker container IDs, Kubernetes pod names) in responses
Test different content types and upload scenarios for inconsistent header filtering

## MITRE ATT&CK
- T1592 - Gather Victim Host Information (reconnaissance of server infrastructure)
- T1598 - Phishing for Information (identifying targets based on infrastructure disclosure)
- T1526 - Evaluate Targets (mapping internal infrastructure through disclosure)

## Notes
This is a classic information disclosure vulnerability with low direct impact but potentially valuable for attackers during reconnaissance. The Mesos/container orchestration details disclosed are particularly interesting as they suggest Twitter's internal infrastructure. The reporter correctly notes this could facilitate LFI/RCE attacks, though the vulnerability itself doesn't directly enable them. The fix is simple (header stripping) but the discovery highlights the importance of defense-in-depth. Report date (2015) predates modern DevSecOps practices and may have been fixed long ago.

## Full report
<details><summary>Expand</summary>

Hi there,

I noticed a small information disclosure (full path disclosure) on ads.twitter.com.

#Steps to reproduce

- 1. Login to ads.twitter.com
- 2. Start to create a new twitter-follower campaign
- 3. Choose to upload a new picture
- 4. Turn on your intercepting proxy
- 5. Upload a file 
- 6. You should notice a request to your log facility.

```
GET /accounts/18ce53wparq/log?v=0.9&u=https%3A%2F%2Fads.twitter.com%2Faccounts%2Fxxxx%2Fcampaigns%2Fnew_objective%2Ffollowers%3Fsource%3Dobjective_picker&rt.start=cookie&r=https%3A%2F%2Fads.twitter.com%2Faccounts%2Fxxxxx%2Fcampaigns%2Fnew&timers=&events=ads%3Afollowers%3Acreative%3A%3A%3Aenter HTTP/1.1
Host: ads.twitter.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0
Accept: image/png,image/*;q=0.8,*/*;q=0.5
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://ads.twitter.com/accounts/xxxxx/campaigns/new_objective/followers?source=objective_picker
Cookie: [COOKIES]
Connection: keep-alive
```

The response will contain something like this:

```
x-sendfile: /var/lib/mesos/slaves/201403042312-2230002186-5050-50082-705/frameworks/201104070004-0000002563-0000/executors/thermos-1409696851527-revenue_web-prod-ads-36-d76baad3-5634-4141-ab52-478be9ecab97/runs/e09cc5ea-77f8-4729-afd1-0045b2a772c5/sandbox/app/assets/images/blank.gif
```

As you can see, this discloses a full path to a resource. This information could be used in furhter attack scenarios like LFI or RCE. 

Please let me know what you think about it.

Best regards,
Sebastian

</details>

---
*Analysed by Claude on 2026-05-24*
