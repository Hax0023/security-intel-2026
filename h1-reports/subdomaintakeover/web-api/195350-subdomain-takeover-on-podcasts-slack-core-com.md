# Subdomain Takeover on podcasts.slack-core.com

## Metadata
- **Source:** HackerOne
- **Report:** 195350 | https://hackerone.com/reports/195350
- **Submitted:** 2017-01-02
- **Reporter:** michiel
- **Program:** Slack
- **Bounty:** $5,000
- **Severity:** medium
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** web-api

## Summary
The subdomain podcasts.slack-core.com was configured as a CNAME pointing to Feed.Press but had no corresponding account registered on the service, allowing an attacker to register the domain and serve arbitrary content. While the vulnerability exists on a secondary domain rather than Slack's root domain, it enabled full control over the subdomain's content and potential for phishing or malware distribution.

## Attack scenario
1. Attacker discovers that podcasts.slack-core.com resolves to redirect.feedpress.me via CNAME record
2. Attacker verifies that no Feed.Press account owns the custom domain registration for podcasts.slack-core.com
3. Attacker creates a Feed.Press account and registers podcasts.slack-core.com as a custom domain within their account
4. Feed.Press propagates the domain association through their systems, allowing the attacker's account to serve content
5. Attacker can now redirect traffic, host malicious content, or perform phishing attacks using the Slack subdomain
6. Attacker demonstrates proof of concept by redirecting to HackerOne homepage

## Root cause
Slack created a CNAME DNS record pointing to a third-party service (Feed.Press) but failed to maintain an active account registration or claim the domain on that service. The dangling DNS record remained after the domain was no longer in use, creating an orphaned resource that any third party could claim.

## Attacker mindset
Reconnaissance-focused: The attacker systematically enumerated subdomains under slack-core.com to understand Slack's infrastructure. Upon discovering an unused domain pointing to a third-party service, they recognized the opportunity to claim it without authorization. The approach was methodical—verify non-ownership, register the domain, and demonstrate control—showing awareness of subdomain takeover patterns and third-party service abuse vectors.

## Defensive takeaways
- Implement subdomain takeover monitoring by regularly auditing all DNS records pointing to third-party services
- Maintain active registrations or claims on all custom domains configured with external service providers
- Remove or invalidate CNAME records for domains no longer in use rather than leaving them dangling
- Establish a domain lifecycle management process that tracks which subdomains are active and who owns them
- Scan for and remediate dangling DNS records across all domains and subdomains periodically
- Use DNS validation to confirm that all CNAME targets have corresponding active configurations
- Consider using separate subdomains for third-party integrations with clear ownership documentation

## Variant hunting
Enumerate other subdomains under slack-core.com and related domains for dangling CNAME records pointing to popular hosting services (GitHub Pages, Heroku, Azure, AWS, Firebase, etc.)
Check other Slack domains (slack.com, slack-edge.com, etc.) for similar misconfigured subdomains
Investigate whether other Slack subdomains point to Feed.Press or other podcast hosting services
Look for CNAME records pointing to deprecated third-party services that may no longer validate domain ownership
Search for subdomains pointing to content delivery networks where domain claims can be usurped
Test whether other Feed.Press-based custom domains have similar unclaimed registration opportunities

## MITRE ATT&CK
- T1190
- T1584.001
- T1583.001
- T1557.002

## Notes
The researcher appropriately noted that impact is limited due to the subdomain being on slack-core.com rather than the main slack.com domain. The report demonstrates responsible disclosure by offering to release the domain from their Feed.Press account. This vulnerability type became increasingly common as organizations scaled their infrastructure and integrated with numerous third-party services without proper lifecycle management. Feed.Press' design allowing any user to claim custom domains without prior ownership verification contributed to the exploitability.

## Full report
<details><summary>Expand</summary>

I noticed `slack-core.com` is used for Slack's call infrastructure. I had never seen that domain before, so I decided to find out what else was running on it. It turned out `podcasts.slack-core.com` was pointing to a Podcast and RSS hosting service called Feed.Press. However, there was no Feed.Press account associated with `podcasts.slack-core.com`, which allowed me to register it and start serving my content from this domain. 

Note that since it is not on Slack's root domain, the impact of this vulnerability seems pretty minimal.

# Proof of Concept
Here we can see `podcasts.slack-core.com` is CNAME'd to `redirect.feedpress.me`:

```plain
michiel@msp ~ $ dig podcasts.slack-core.com                                                                                         [2.1.9]

; <<>> DiG 9.10.3-P4-Ubuntu <<>> podcasts.slack-core.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1307
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;podcasts.slack-core.com.	IN	A

;; ANSWER SECTION:
podcasts.slack-core.com. 299	IN	CNAME	redirect.feedpress.me.
redirect.feedpress.me.	3599	IN	A	5.135.16.40

;; Query time: 253 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Jan 02 14:02:07 EST 2017
;; MSG SIZE  rcvd: 103
```

By creating my own account on [Feed.Press](https://feed.press), I was able to register `podcasts.slack-core.com` as my "custom domain" under my Feed.Press account. After it propagated through Feed.Press' systems, I was able to fully control the contents served as http://podcasts.slack-core.com.

Since the domain was dormant, I decided to redirect `/` to https://hackerone.com as a proof of concept. We can see that happening using this `curl` command (note the `Location` header):

```plain
michiel@msp ~ $ curl -vv http://podcasts.slack-core.com
* Rebuilt URL to: http://podcasts.slack-core.com/
*   Trying 5.135.16.40...
* Connected to podcasts.slack-core.com (5.135.16.40) port 80 (#0)
> GET / HTTP/1.1
> Host: podcasts.slack-core.com
> User-Agent: curl/7.47.0
> Accept: */*
>
< HTTP/1.1 301 Moved Permanently
< Server: nginx
< Date: Mon, 02 Jan 2017 19:06:18 GMT
< Content-Type: text/html
< Content-Length: 178
< Location: https://hackerone.com
< X-Backend-Server: 172.16.0.53
<
<html>
<head><title>301 Moved Permanently</title></head>
<body bgcolor="white">
<center><h1>301 Moved Permanently</h1></center>
<hr><center>nginx</center>
</body>
</html>
* Connection #0 to host podcasts.slack-core.com left intact
```

# Remediation
Since the domain is not used anymore, it is recommended to remove the CNAME of `podcasts.slack-core.com` to `redirect.feedpress.me`. 

If you need me to release the domain in Feed.Press itself, let me know and I'll remove it from my account.

</details>

---
*Analysed by Claude on 2026-05-24*
