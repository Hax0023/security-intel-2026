# Viral Direct Message Clickjacking via Link Truncation Leading to Google Credential Capture and Malicious Twitter App Installation

## Metadata
- **Source:** HackerOne
- **Report:** 643274 | https://hackerone.com/reports/643274
- **Submitted:** 2019-07-15
- **Reporter:** slickrockweb
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Clickjacking, Credential Theft, OAuth Hijacking, URL Truncation Information Disclosure, Social Engineering, Account Takeover, Malicious Third-Party App Authorization
- **CVEs:** None
- **Category:** uncategorised

## Summary
Attackers exploited Twitter's 38-character link truncation in direct messages to create clickjacking attacks that appeared as legitimate YouTube links. The attack chain captured Google credentials via a malicious OAuth app and subsequently hijacked Twitter accounts to install malicious follower-generation apps, creating a viral worm-like infection vector.

## Attack scenario
1. Attacker crafts extremely long URL beginning with accounts.youtube.com to deceive recipients, embedding malicious redirect chains in query parameters
2. Truncated DM appears legitimate (accounts.youtube.com/accounts/SetSI...) and is sent to victim from trusted follower account
3. Victim clicks link and is redirected through logout sequence designed to log out existing Google sessions
4. Victim is presented with malicious Google OAuth consent screen that captures credentials before redirecting to getmorefollowers.biz
5. User is redirected through freefollowers.eu and presented with one of 10+ randomized malicious Twitter OAuth apps requesting account permissions
6. Upon authorization, hijacked account automatically sends same malicious DM to all followers/open DMs, creating viral propagation and account takeover

## Root cause
Twitter's DM link truncation at 38 characters enabled URL masquerading by allowing attackers to hide malicious redirect chains behind legitimate-looking domain prefixes. Combined with lack of OAuth app vetting and insufficient DM security controls, this created a cascade vulnerability enabling credential theft and account compromise at scale.

## Attacker mindset
Sophisticated attack demonstrating understanding of multiple OAuth flows, URL manipulation, and social engineering psychology. The viral propagation mechanism (hijacked accounts automatically spreading to followers) shows deliberate design for scale and evasion. Monetization through both follower services and account takeover suggests organized criminal enterprise.

## Defensive takeaways
- Implement full URL display or expanded link preview in DMs before user clicks, not truncation
- Add URL domain verification warnings for OAuth flows originating from unexpected sources
- Enforce stricter OAuth app review process, especially for apps requesting direct message or follower access
- Detect and rate-limit accounts performing mass DM sends (automated viral propagation detection)
- Implement re-authentication requirements for sensitive actions like authorizing third-party apps
- Add email notifications when new OAuth apps are authorized on an account
- Implement cross-site request forgery (CSRF) protections for OAuth callback flows
- Monitor for patterns of account credentials being used from unexpected geographic locations or IPs

## Variant hunting
Search for other truncation vulnerabilities in messaging platforms (Telegram, WhatsApp, Instagram DMs, etc.)
Hunt for similar OAuth redirect chain attacks using malicious Google/Facebook apps as intermediaries
Monitor for other follower-farming services that may employ same viral infection mechanism
Identify other services vulnerable to URL masquerading through truncation (search results, chat apps, email clients)
Search for exploitation of nested URL encoding to obscure redirect destinations
Hunt for similar worm-like propagation patterns in social media exploits (self-replicating via DMs)

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1187 - Forced Authentication
- T1056.004 - Phishing for Information: Spearphishing Link
- T1589.001 - Gather Victim Identity Information: Credentials
- T1111 - Multi-Factor Authentication Interception
- T1528 - Steal Application Access Token
- T1650 - Acquire Infrastructure: Virtual Private Server
- T1583.006 - Acquire Infrastructure: Web Services
- T1583.001 - Acquire Infrastructure: Domains
- T1204.001 - User Execution: Malicious Link
- T1539 - Steal Web Session Cookie

## Notes
This attack demonstrates sophisticated understanding of OAuth flows, URL manipulation, and social engineering. The 38-character truncation was a direct platform design flaw that enabled domain spoofing. The viral propagation mechanism (automated DM sending from hijacked accounts) created exponential infection rate. Report includes actual malicious URLs (redacted) and links to compromised domains. The attack chain involved at least 3-4 redirect hops through attacker-controlled infrastructure, making it difficult to trace to original source. Attack likely profitable through follower service monetization and potential account credential sales.

## Full report
<details><summary>Expand</summary>

**Summary:** [Viral Direct Message Clickjacking via link truncation leading to capture of both Google credentials & installation of malicious 3rd party Twitter App]

**Description:** [Because very long links in direct messages are truncated after 38 characters the malicious actors were able to provide a malicious link in a direct message that appeared as though it was to an authenticated YouTube video and caused a clickjacking scenario to occur. The link caused any users that were already logged into a Google account to be first logged out and then asked to log back in. A malicious Google app captured the account credentials and then redirected the user to the website getmorefollowers.biz (embedded in the initial link query string) which in turn redirected the user to freefollowers.eu domain. This executed a PHP script and /or a javascript which in turn redirected the user to one of at least 10 different randomized malicious 3rd party Twitter apps (see attached file redirect-sequence-from-start.png for the initial redirect sequence). Depending on whether the user was already logged into their Twitter account, the authentication process was potentially done for the user and/or the user only needed to click on the authenticate button. These apps all did essentially the same thing. They generated a couple of followers to the account but also hijacked the account into sending this same malicious link as a Direct message to everyone that it was able to in that account (open DMs and reciprocal follows). Thus creating the virality of the infection and starting the sequence all over again on hundreds of new victims.

Users that weren't already logged into Google were redirected directly to getmorefollowers.biz and then to freefollowers.eu and then to the malicious Twitter app and sent to one of at least 10 different randomized Oauth screens and encouraged to connect to a 3rd party Twitter app that would supposedly provide you free followers (also provided a paid service to increase your followers).

Here is an example "FULL" link we received from a malicious account that we were investigating named @█████████

ONLY FOR YOU Eric JN Ellason {{ https://accounts.youtube.com/accounts/SetSID?89085489=████████&ilo=1&89085489=████&ils=a4cc1b7ed445598f16cef403bb3b0311&ilc=0&Bi06UejC9N=89085489&continue=https%3A%2F%2Fgoogle.com%2Faccounts%2FLogout%3Fcontinue%3Dhttps%253A%252F%252Fappengine.google.com%252F_ah%252Flogout%253Fcontinue%253Dhttps%25253A%25252F%25252Fwww.google.com%25252Furl%25253Fsa%25253Dt%252526rct%25253Dj%252526q%25253D%252526esrc%25253Ds%252526frm%25253D1%252526source%25253Dweb%252526cd%25253D1%252526cad%25253Drja%252526ved%25253D0CDAQFjAA%252526url%25253Dhttp%2525253A%2525252F%2525252Fwww.getmorefollowers.biz%2525252F%252526ei%25253D3meWUs3fGMun0wWr94CoAg%252526usg%25253DAFQjCNFg9bZvpiCSGCVgdaryfriEHS-XEA%252526sig2%25253D8hAat-jqQCQ0Ciz9ywCbEw%252526bvm%25253Dbv.57155469%25252Cd.bGQ&Bi06UejC9N=43992 … }} message id: 92439


What gets displaying and hotlinked in the Direct Message is this:

ONLY FOR YOU Eric JN Ellason { accounts.youtube.com/accounts/SetSI... } message id: 92439

Screenshot attachment (new-DM-infections.png) shows 9 new links sent out as DMs to new victims from another infected account we posted to Twitter.


Here is an older example that we found:

https://accounts.youtube.com/accounts/SetSID?ssdc=1&sidt=ALWU2csbcs9naItQW2g9gJSaN3QCEtSXNR%2F%2FgHRk%2B%2FacQ5RRlR6qkFXVNv1zNoCD4xCsw2zAU7XtQ5nTcoTWLokEO16qm2KqD8dQsKvLJQghxcRG%2BxRGeHymPAwEAWWWIfVpIHIdWWSR7QDaDg%2Fds4CPnpJeHPzg24hAeNHRjj%2BfZUhZClhvopoA9yPv13%2BIKm5QBlCZHinUlFsz%2FffGJEFmLuu4%2Bo5EaQv3xRhD8gTfWKp5uo22CeMXz8K5UH7F5l6RPVND4eX5CO7wRAq7vl6RbM2UoK07CpD9LSIbZV%2FC4%2F9zRx7a1weMOZ1JjtH9I9zUPi2eJdnbPjoplfXQ1WOQtVVCmgmVk2XSZDSPov%2F2hrU6bCT5xdLVGCSkImSRb8bIqtFxN7uXSsAht%2BiRpCk8IlZEvCRrbPk8bDe6hLanwCsKv0sRPHb4IWJkKAAiz6ID8e%2FwV83zvzNXwvz%2FyT4hJ2%2BD%2BVVatg%3D%3D&continue=https%3A%2F%2Fwww.google.com%2Fintl%2Fen%2Fimages%2Flogos%2Faccounts_logo.png&dbus=PK.2
]

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

 1. [Direct message is sent from a reciprocal follow within your account. Presumably can happen to accounts with Open DMs. The direct message, because of link truncation appears to be a Youtube video. Message in general looks like this.  ONLY FOR YOU Eric JN Ellason { accounts.youtube.com/accounts/SetSI... } message id: 92439 ]
 2. [The User who receives this direct message from someone they follow, clicks on the embedded link (in some cases from very trusted sources who have themselves been infected).]
 3. [The link sequence first attempts to log the user out of any Google accounts or apps they are currently logged into. And then asks them to relog back into their Google account, capturing their Google account credentials. Presumably there is a malicious Google app that they have created which in turn continues the sequence and currently eventually sends them to the website www.getmorefollowers.biz . Other domains have been used and will likely be swapped out in the future. We provide a list of 7 domains we believe have been used in this campaign.]
 4. [getmorefollowers.biz currently redirects the user to www.freefollower.eu and specifically this URL www.freefollower.eu/redirect.php. The user will generally be unaware of this redirect and will only see the final Twitter authentication screen to authenticate a 3rd party Twitter app. We were able to short circuit the redirect chain and use just the URL www.freefollower.eu/redirect.php from different VPN locations and with a virgin state browser to identify most of the different malicious 3rd party apps. It appears they randomize sending the user to 1 of at least 10 different 3rd party apps. We document them below in the "Additional Materials" section]
 5. [For users not logged into any Google accounts, they get directly sent to the website www.getmorefollowers.biz and step 4 above continues the sequence ]
 6. [Since the user is presumably already logged into their Twitter account they then get an authentication screen asking them to authenticate the app. It is also possible via malicious javascripts that this process of clicking on the authentication button is completed for them in the background making the user completely unaware of much of this sequence.]
 7. [If the user is not logged into their Twitter account and has javascript disabled I believe the sequence does stop at the freefollower.eu website. Here you can click on the "Signin with Twitter" button to log into your Twitter account and then authenticate this app to have access to your account. Of course this sequence really only happens with security professionals looking into and short circuiting the redirect sequences]

## Impact: [The attacker in this situation has already been able to create a viral attack vector in addition to harvesting thousands of Google account credentials and installing their malicious 3rd party Twitter app on thousands of accounts. Please note this report is also being submitted to the Google Bug Bounty program because part of the attack sequence occurs on their infrastructure.

Once one account is breached that account in turn sends out the malicious link via the authenticated 3rd party Twitter app (we identify the set of randomized apps above) to everyone in their trusted set of reciprocal follows (since the link is sent only via direct message). This greatly increases the trust factor and likely hood a significant number of people that receive this link will click and follow the malicious sequence and continue the viral infection sequence. At the same time the hackers can have their malicious 3rd party Twitter app authenticated within thousands of accounts. Through RiskIQ we were already able to verify that thousands of Twitter accounts within the past month had been breached and infected via this Clickjacking attack. We are attaching a document showing about 1000 accounts that fell victim to this attack (s

</details>

---
*Analysed by Claude on 2026-05-24*
