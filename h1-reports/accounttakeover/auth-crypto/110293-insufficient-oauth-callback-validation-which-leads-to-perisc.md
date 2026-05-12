# Insufficient OAuth Callback Validation Leading to Periscope Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 110293 | https://hackerone.com/reports/110293
- **Submitted:** 2016-01-12
- **Reporter:** filedescriptor
- **Program:** Twitter/Periscope
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** OAuth Callback Validation Bypass, Path Traversal, Open Redirect, Account Takeover, Insufficient Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Periscope's OAuth callback validation could be bypassed by using path traversal (e.g., 'a/../home') instead of complete URIs, combined with Twitter's open redirect vulnerability in the login flow. This allowed attackers to hijack OAuth tokens and take over victim Periscope accounts without user interaction.

## Attack scenario
1. Attacker extracts Periscope's Twitter consumer key and secret through reverse engineering the mobile app
2. Attacker creates a malicious card on cards.twitter.com with fallback URL pointing to attacker-controlled site
3. Attacker crafts a path traversal callback URL (e.g., 'a/../login?redirect_after_login=https://cards.twitter.com/card_id') that bypasses callback locking
4. Attacker embeds payload in a tweet/player card that triggers when victim views timeline
5. Victim's browser automatically follows the OAuth authorization flow (via previously granted 'Login with Twitter')
6. Victim is redirected through the open redirect chain to attacker's site with OAuth token in URL fragment, completing account takeover

## Root cause
Twitter's callback locking validation assumed the callback_url parameter would be a complete URI and only checked the protocol scheme (http://, https://, etc.). The validation failed to enforce that callback_url must be a complete, well-formed URI, allowing path traversal payloads like 'a/../home' to bypass the check. Combined with an open redirect vulnerability in Twitter's login flow, this enabled OAuth token hijacking.

## Attacker mindset
An attacker recognized that OAuth callback validation mechanisms often assume well-formed inputs and fail to parse malformed paths correctly. By chaining path traversal with an existing open redirect, they discovered a 'gadget chain' to hijack OAuth flows. The attacker also leveraged implicit user trust in automatic authorization flows ('Login with Twitter') to achieve stealthy account takeover.

## Defensive takeaways
- Always validate that OAuth callback URLs are complete, well-formed URIs with proper URL parsing libraries; reject relative paths and path traversal sequences
- Implement strict whitelist validation for callback_url at the protocol + domain level, not just protocol level
- Disable automatic re-authorization for sensitive operations; require explicit user consent even if previously authorized
- Audit and eliminate open redirect vulnerabilities across all redirect parameters (redirect_after_login, etc.)
- Apply defense-in-depth: even if callback locking exists, validate callback URLs at the application level before using them
- Use proper URI parsing to prevent traversal attacks; reject URLs containing '..' or similar traversal patterns
- Consider using state parameter validation and short-lived authorization codes to limit token exposure window

## Variant hunting
Search for other OAuth implementations that validate only protocol scheme without enforcing complete URI structure
Test redirect parameters in authentication flows for path traversal bypass (redirect_uri, callback, return_url, etc.)
Enumerate open redirects across first-party domains that could chain with OAuth flows
Reverse engineer mobile apps for embedded OAuth credentials and test callback validation on those credentials
Test OAuth flows with malformed callback_url formats: relative paths, encoded traversal sequences, protocol-relative URLs
Check for automatic re-authorization features in SSO implementations that could be exploited without user interaction

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1561
- T1539
- T1550

## Notes
This report demonstrates a sophisticated attack chain combining three vulnerabilities: credentials extraction via reverse engineering, OAuth callback validation bypass via path traversal, and open redirect. The stealthiness achieved through automatic authorization and embedded payloads in cards highlights the importance of explicit user consent. The attacker's insight that callback locking assumed well-formed URI input was particularly clever. Twitter's callback locking mechanism was noted as unusually strict compared to standard OAuth implementations, yet still failed due to incomplete validation.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report an issue in the Periscope Twitter application which allows attacker to circumvent the callback locking to takeover victim's Periscope account which is connected to a Twitter account.

#Detail
In the mobile Periscope app, the *consumer_key* and *consumer_secret* for Twitter application are directly embedded into the app in order to facilitate the OAuth process. The key and secret are protected by obfuscation but it can be recovered by reverse engineering. 

For reference this is the key and secret for Periscope:
```
CONSUMER_KEY: █████████
CONSUMER_SECRET: ███
```

In fact, the leakage of the key and secret pair is *not* a major security concern as Twitter provides the "Callback Locking" protection to prevent the *callback_url* to be overwritten during the Request Token phase.

Periscope *does* employ callback locking. However, the locking for Periscope is kind of special compared to normal applications (I guess this is only for Twitter's official applications). In short, it checks whether the protocol for *callback_url* can be used to leak the OAuth token to third parties. For example, ```https://```, ```http://```, ```ftp://``` are forbidden, while ```twittersdk://``` and ```whatever://``` are allowed. The check is sufficient by itself. However, the check is under the assumption that the *callback_url* provided is a complete URI. In addition, it is discovered that it is possible to **use only the path** for *callback_url* and pass the test (e.g. a/../home is valid), and that allows the path to be traversed. Now, if an attacker can find an open redirector on Twitter, he/she can use that as *callback_url* to redirect victim with the OAuth token to attacker's control site.

The attack flow would look like this:

1. Attacker uses the consumer key & secret to generate a request token
2. Victim authorizes the Periscope app for the request token
3. Victim is redirected to the open redirector with path traversal (e.g. /redirect?url=http://attacker.com#&oauth_token=...)
4. Victim then lands on attacker controlled site with the token (http://attacker.com#&oauth_token=)
5. Now the attacker gains the OAuth token from victim. He/she can use it to to exchange for *access_token* and logins victim's Periscope account.

(By the way, the URL fragment in step 3 is a common technique to preserve tokens during HTTP redirect which I really like)

And without surprise, such open redirect bug does exist. 
In the login page (https://twitter.com/login?redirect_after_login=), the *redirect_after_login* parameter can be specified to redirect users if they have logged in. There's a check in place which rejects any URL which is not belong to a Twitter subdomain (i.e. whitelist \*.twitter.com). However, for Twitter ads one can make a generation card and set the fallback URL to any destination, and the URL for the card happens to be a Twitter subdomain (cards.twitter.com). So after all, attackers can first setup a generation card to redirect to attacker's controlled site, and use the card URL as *redirect_after_login*.

The redirection flow:

1. callback_url = a/../../login?redirect_after_login=https://cards.twitter.com/card_id
2. https://cards.twitter.com/card_id
3. https://attacker.com

BAM BAM BAM

Now, Periscope has enabled "Login with Twitter", that means the user will automacially authorize the app for authentication if he/she has done that once before, attacker can abuse that to make the whole attack **stealthy and without user interaction**.

#PoC
1. Prepare an Periscope account which is connected to a Twitter account, and make sure you have logged in Twitter as that account
2. Go to https://twitter.com/attackerfoobar/status/686936815945789440
3. Wait for a moment
4. Your Periscope account will then be renamed as "Pwn3d"

In this PoC I embedded the payload in a player card to achieve maximum stealthiness, so that whenever the tweet arrives to victim's timeline the attack automatically triggers. You can also check out the standalone PoC here: https://innerht.ml/pocs/periscope-oauth-callback-hijack

Video demonstration: https://vimeo.com/151530694 (password: xauth)

#Fix
Since the open redirect bug is more like a feature and may be many of them out there, I would suggest to improve the validation on the callback locking. For example, only allow the *callback_url* to be a complete URL should do the job.

</details>

---
*Analysed by Claude on 2026-05-11*
