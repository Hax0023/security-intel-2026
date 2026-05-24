# Subdomain Takeover on Twitter Acquisition (support.trendrr.tv)

## Metadata
- **Source:** HackerOne
- **Report:** 44578 | https://hackerone.com/reports/44578
- **Submitted:** 2015-01-21
- **Reporter:** simon90
- **Program:** Twitter/HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Third-party Service Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
A subdomain (support.trendrr.tv) belonging to a Twitter-acquired company (Trendrr) was left pointing to an unclaimed Zendesk help desk instance. The attacker could claim the Zendesk subdomain and gain full control over the support.trendrr.tv domain, enabling malicious activities. This represents a classic subdomain takeover vulnerability on an abandoned acquisition's infrastructure.

## Attack scenario
1. Attacker identifies that support.trendrr.tv is a CNAME alias pointing to trendrr.zendesk.com
2. Attacker visits support.trendrr.tv and receives Zendesk's 'No help desk configured' message with signup prompt
3. Attacker registers/claims the unconfigured Zendesk help desk instance using the signup link
4. Once claimed, attacker has full control over the trendrr.zendesk.com service and its subdomain alias
5. Attacker can now serve malicious content via support.trendrr.tv to users believing they're accessing legitimate Twitter/Trendrr support
6. Attacker could harvest credentials, distribute malware, or conduct phishing attacks leveraging the trusted domain

## Root cause
Acquisition infrastructure not properly decommissioned; Zendesk subdomain was left unclaimed and configured to respond with signup prompts, allowing external parties to claim the service. DNS CNAME record for support.trendrr.tv was not removed or updated after service shutdown.

## Attacker mindset
Reconnaissance-focused researcher identifying orphaned acquisition assets and unclaimed third-party services as attack vectors. Persistence in finding unused infrastructure that technically still resolves but lacks proper ownership controls.

## Defensive takeaways
- Conduct comprehensive DNS/subdomain audit during and after acquisitions
- Implement domain/subdomain inventory tracking with ownership validation
- Promptly remove or redirect dangling DNS records pointing to third-party services
- Configure third-party services (Zendesk, Heroku, GitHub, etc.) to prevent signup on company domains
- Monitor for unclaimed service instances responding with signup/onboarding prompts
- Establish post-acquisition infrastructure cleanup procedures within SLA
- Regularly scan for subdomain takeover vulnerabilities across entire domain portfolio

## Variant hunting
Scan all acquired company domains for unclaimed third-party service endpoints
Identify CNAME records pointing to: Zendesk, Heroku, GitHub Pages, Firebase, AWS S3, Azure Storage, etc.
Search for HTTP responses containing 'No help desk configured', 'Not configured', 'Signup', 'Claim this'
Check WHOIS registration status of subdomains with suspended/expired service instances
Monitor acquisition announcements and identify infrastructure not properly deprecated

## MITRE ATT&CK
- T1190
- T1199
- T1566

## Notes
Report demonstrates researcher's persistence across multiple vulnerability reports to same organization. Researcher references prior acceptance and fix of related Trendrr issue as credibility marker. Communication quality is notably poor with grammatical errors and unclear formatting, potentially impacting severity assessment by security team. The vulnerability is technically valid despite presentation issues. Subdomain takeover on acquired assets is particularly dangerous as users may trust the domain based on prior association with legitimate company.

## Full report
<details><summary>Expand</summary>

Hello Twitter Security Team, 

I reccomend you to read this report with the maximum attention!

This is the same isse that you ever see here: https://hackerone.com/reports/42236 and here https://hackerone.com/reports/32825.

Well ,now, the acquisition where I found this domain is: trendrr.tv..Before say something, just let me go in the deep of this report and of this domain.

Long time ago, when Twitter doesn't had his personal Bug Bounty Program on Hackerone, and have just his forms for researcher who want to report something, I reported some issues on some of your acquisitions and some got rejected (Not because the vulns where in the acq, but because the issue doesn't had a serious impact for you at their time)..  but one issue was accepted and fixed from yoru Security Team luckily, and was a issue on...TRENDRRTV!

In that time, I reported a vulenrability about renegotiation, I reccomed you to see these two screenshots below to refresh your memory:

1) http://grabilla.com/05115-39f04d06-370b-49eb-9355-b6fff4971584.html (Your first reply)

2) http://grabilla.com/05115-ad54a47d-e136-4f9f-9fc0-5ccb90737383.html (From this reply, I understood that you was going to fix that issue.)

3) http://grabilla.com/05115-0a4a4255-95ae-445f-b263-26eca02aab1d.html (Here you told me that I was going to get listed there and some months later I got the reply wich says that "You're in the HOF for year 2014" and in the same date, and two days later, I've checked the issue and the issue was fixed.

Now the point is..old time, new time, no matters. Today, I am here because I want to report this issue because is a valid bug, and it's a fruit from my hard work.

I saw that now all domain of trendrr has been shutting down except one, the onwewich I found to be vulnerable: the domain is support.trendrr.tv, that is an alias for trendrr.zendesk.com.

I visited the TRENDRR support website and it says: "No help desk at support.trendrr.tv
There is no help desk configured at this address. This means that the address is available and that you can claim it at http://www.zendesk.com/signup/"----->Here a screen wich proof that: http://grabilla.com/05115-db455e78-830e-43dd-b562-c839672cb14e.html, So once it's expire I can claim it.

And once claimed it, if you try to navigate with your browser to support.trendrr.tv  (Since this is an Alias (so is pointing out to a specific domain) for trendrr.zendesk.com as proof this screen: http://grabilla.com/05115-6d3ed6d5-494c-4c38-b0b6-3539e5161d6d.html ) you will redirect to trendrr.zendesk.com, that is my domain takeovered! :)

POC(s) of the subdomain takeover: 

1) http://grabilla.com/05115-27247cde-c11a-4dd0-a684-8d39ae5f4178.html

and

2) http://grabilla.com/05115-5e623c93-2657-4e45-a0af-4ff41593a4fc.html

Since I have complete control over the subdomain I can do whatever I want on it, be careful about that!

Ps: Even if is an acquisition and most of TRENDRR domains has been shutt-down, I except a small bounty for this, or better...I hope! =)

Please fix it as soon as possible , and let me know if you need any further information.

Regards,

Simone






</details>

---
*Analysed by Claude on 2026-05-24*
