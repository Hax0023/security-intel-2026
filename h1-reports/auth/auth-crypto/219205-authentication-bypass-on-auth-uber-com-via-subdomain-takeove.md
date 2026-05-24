# Authentication bypass on auth.uber.com via subdomain takeover of saostatic.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 219205 | https://hackerone.com/reports/219205
- **Submitted:** 2017-04-07
- **Reporter:** arneswinnen
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
## Summary
This is not a standard vulnerability, but a chain of two more exotic vulnerabilities leading to a full authentication bypass of your SSO login system at auth.uber.com (via saostatic.uber.com). The root cause of this authentication bypass is two-fold:

1. Subdomain saostatic.uber.com was pointing to Amazon Cloudfront CDN, but the hostname was not registered there anymore. This allowed me

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

## Summary
This is not a standard vulnerability, but a chain of two more exotic vulnerabilities leading to a full authentication bypass of your SSO login system at auth.uber.com (via saostatic.uber.com). The root cause of this authentication bypass is two-fold:

1. Subdomain saostatic.uber.com was pointing to Amazon Cloudfront CDN, but the hostname was not registered there anymore. This allowed me to fully takeover this domain. It is now serving content of my own webserver, both over http and https (highly similar to [175070](https://hackerone.com/reports/175070) - however, I must disagree with "there are some mitigating factors (cookie scope) that make this not as bad as it might appear at first blush."). 
2. Your SSO system at auth.uber.com issues session cookies which are temporarily shared between all https://*.uber.com subdomains through its "domain=.uber.com" attribute. Although there were some countermeasures to prevent theft, the current setup still allows leakage of these high-value session cookies to the overtaken subdomain https://saostatic.uber.com in all modern browsers, leading to a full Authentication Bypass (highly similar to [172137](https://hackerone.com/reports/172137)).

## Security Impact
The security impact of the subdomain takeover is that Uber can be impersonated via this webpage. A valid SSL certificate could easily be generated for this domain via Let's Encrypt, which would make it ideal for e.g. phishing attacks. 

The security impact of the SSO system using shared session cookies for https://*.uber.com is, in combination with the subdomain takeover vulnerability, an Authentication Bypass via session hijacking. A victim must be authenticated to auth.uber.com and then visit a webpage under the attacker's control to be exploited successfully - no further interaction is required from the victim, the attack can be performed stealthily without the user noticing or being notified by Uber. The end result is that the attacker can now impersonate the victim on any of the *.uber.com which rely on auth.uber.com for authentication, such as riders.uber.com, partners.uber.com, developer.uber.com, bonjour.uber.com, etc. 

# 1. Subdomain Takeover

The subdomain "saostatic.uber.com" was (and still is) a CNAME pointing to a AWS Cloudfront CDN server (depending on your location, the latter will resolve differently):
```
# nslookup saostatic.uber.com 8.8.8.8
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
saostatic.uber.com	canonical name = d3i4yxtzktqr9n.cloudfront.net.
```
However, the hostname "saostatic.uber.com" was not claimed anymore on Cloudfront, resulting in a Cloudfront error page when visiting the subdomain before the takeover:

{F173887}

Subsequently, a new Amazon Cloudfront CDN endpoint was created and linked to an attacker-controlled origin server. For the new Cloudfront CDN endpoint, "saostatic.uber.com" was designated as hostname successfully:

{F173885}

This concluded the subdomain takeover. Visual proof can be found at http://saostatic.uber.com/subdomaintakeoverbyarneswinnen.html (unguessable filename chosen to not negatively affect Uber's reputation during takeover period) :

 {F173884}

#2. Authentication Bypass

In Uber's SSO system, auth.uber.com acts as Identity Provider and issues temporarily shared session cookies for https://*.uber.com to communicate identities to Service Providers (e.g. riders.uber.com, partners.uber.com, etc). Service Providers on their end immediately destroy the incoming temporary shared session cookies in case of erroneous (e.g. issued for other Service Provider) or successful authentication, ensuring the window for theft is small:

 {F202679}

The precious shared session cookie "_csid" can thus only be stolen between step 9 and 10, which is a very short period (automatic browser redirect). Although not impossible to exploit, a more convenient flaw was identified that allows the shared session cookie to remain alive after step 9 in the browser's cookie store in the diagram above. The issue is that, if the victim is already logged in at https://riders.uber.com (situation after last step 12 in diagram) when receiving a request containing a valid newly generated shared session cookie "_csid", it is simply ignored. Hence it stays alive in the browser until its cookie store is cleared. An attacker simply needs to directly issue another login scenario starting from step 3 in the above diagram, and end with an additional hidden request to https://saostatic.uber.com to steal the precious session cookie:

{F202676}

So now an attacker has his/her hands on the victim's "_csid" shared session cookie for https://riders.uber.com, he/she can execute the normal login flow in their own browser and replace the issued "_csid" cookie value in step 9 of the first Uber SSO Login diagram to be logged in as the victim, right? Wrong. There's another countermeasure in place, namely a variant of login cross-site request forgery protection. This is the actual updated Uber SSO Login 2 diagram:

{F202678}

The problem here are the GET param state=CSRFTOKEN and locally scoped state cookie that are added in step 3 by the Service Provider riders.uber.com and verified in step 11. Since we can't steal these values from the victim's browser, but only the "_csid" shared session cookie, this means game over, right?

No! An attacker can obtain a proper CSRFTOKEN value and accompanying state cookie value from https://riders.uber.com by starting a normal login scenario on their end (e.g. in their own browser or via a simple script). He/she can then relay the auth.uber.com URL to the victim's browser to get the "_csid" shared session cookie for these values, and inject these in his/her own browser login scenario again in step 9. In this manner, the victim effectively generates the "_csid" temporary session token for the attacker's login scenario in a separate browser, but this works flawlessly. This still allows exploitation and thus victim impersonation in the following manner (we still assume that the victim is already logged in to auth.uber.com and visits a webpage under control by the attacker, so we basically continue the flow from the above third and last diagram): 

{F202677}

# PoC

In the PoC below, the assumption is made that https://saostatic.uber.com is actually serving a valid certificate in the victim's browser, which currently is not the case (so there is currently no actual exposed risk). I figured you might not appreciate that. 

1. Open the victim's browser & browse to https://riders.uber.com . After being redirected to https://auth.uber.com , login with the victim's credentials so you end up on https://riders.uber.com trips dashboard again.
2. Open a second browser tab in the victim's browser and browse to https://saostatic.uber.com/prepareuberattack.php . Accept any certificate warnings that you may receive here - again, we're only simulating that the domain has a valid SSL certificate. Once the page has finished loading you should see a URL, "Cookie: " string and a "Set-Cookie: " strings underneath each other. This is all info gathered under the hood by the attacker's webserver that is required to login as the victim now.
3. Open the separate attacker's browser and setup an intercepting proxy tool to intercept requests and responses. Browse to the URL displayed on the prepareuberattack.php page output and intercept this request. Now copy the "Cookie: ..." string displayed on prepareuberattack.php and paste it into the request headers. 
4. The response should be a redirect to https://riders.uber.com/trips, indicating successful authentication bypass. Last but not least, copy all the "Set-Cookie: " lines from the prepareuberattack.php page output and paste them in the response before forwarding it to the browser. This ensures that the stolen cookies are properly injected in the attacker's browser. 
5. You are now logged in as the victim in the attacker's browser 

In a real attack scenario, an att

</details>

---
*Analysed by Claude on 2026-05-24*
