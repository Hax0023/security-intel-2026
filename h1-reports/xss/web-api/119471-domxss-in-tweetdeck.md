# DOM-based XSS in TweetDeck via Malicious Application Name

## Metadata
- **Source:** HackerOne
- **Report:** 119471 | https://hackerone.com/reports/119471
- **Submitted:** 2016-02-29
- **Reporter:** filedescriptor
- **Program:** Twitter/TweetDeck
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** DOM-based Cross-Site Scripting (DOM XSS), Improper Input Validation, Unsafe jQuery Usage
- **CVEs:** None
- **Category:** web-api

## Summary
TweetDeck was vulnerable to DOM-based XSS through the application source link feature. An attacker could create an application with a malicious XSS payload as the app name, and when victims clicked the app link in a tweet, the payload would execute in their browser with access to the TweetDeck domain.

## Attack scenario
1. Attacker creates a malicious Twitter application with an XSS payload (e.g., '<svg onload=alert(document.domain)>') as the application name
2. Attacker uses the malicious application to post a tweet, embedding the payload in the tweet's source metadata
3. Attacker shares the tweet or follows victims with the account to increase visibility
4. Victim opens TweetDeck and expands the malicious tweet
5. Victim clicks on the application source link (displayed as the app name)
6. The unsanitized payload executes in the victim's browser context with access to TweetDeck's domain and session data

## Root cause
The application name from tweet.source was directly passed to jQuery's $() selector without sanitization. jQuery's $() function interprets HTML/SVG strings, causing arbitrary code execution when malicious markup was provided. The lack of input validation and output encoding allowed attacker-controlled data to reach a DOM sink.

## Attacker mindset
An attacker could exploit this to steal session tokens, CSRF tokens, or user credentials from TweetDeck users. The attack requires minimal social engineering (just clicking a link) and could be scaled via viral tweets or targeted victim accounts. The ability to control application names provides plausible deniability as a legitimate application.

## Defensive takeaways
- Never pass user-controlled data directly to jQuery's $() or innerHTML without sanitization
- Use textContent or createTextNode() for displaying untrusted data instead of HTML sink methods
- Implement Content Security Policy (CSP) with strict script-src to prevent inline script execution
- Validate and sanitize all user-supplied input that appears in metadata (app names, descriptions, etc.)
- Use security-focused libraries like DOMPurify for sanitization rather than manual filtering
- Apply principle of least privilege to application creation permissions
- Implement regular security testing for DOM-based XSS vulnerabilities in JavaScript bundles

## Variant hunting
Search for other uses of .source or similar metadata fields passed to jQuery selectors or DOM manipulation methods
Review all tweet metadata rendering code (client name, link text, descriptions) for similar patterns
Check for other user-supplied data in plugin/application contexts that might reach DOM sinks
Examine other Twitter products (Twitter Web, Twitter Mobile Web) for similar architectures
Look for other jQuery $() usages with external data sources throughout TweetDeck codebase

## MITRE ATT&CK
- T1190
- T1566
- T1204

## Notes
Report notes that CSP provides some protection (blocking in non-IE browsers), but IE's CSP implementation was weaker. The vulnerability chain required user interaction but was trivially triggered through normal TweetDeck usage. The attacker's proof-of-concept used social engineering (a deceptive app name 'Click here to get followers ❤️') to increase click rates.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report a DOMXSS issue in TweetDeck.

#Details
In Tweetdeck, a tweet contains info of what client (app) the user used to sent the tweet. The render process is vulnerable to DOMXSS.

In https://ton.twimg.com/tweetdeck-web/web/dist/bundle.6f91b4e832.js, the following line is responsible for retrieving the client website:

```javascript
                case "followSourceLink":
                    TD.util.openURL($(n.getMainTweet().source).attr("href"));
                    break;
```

where ```n.getMainTweet().source``` is the client name. This name can be controlled through changing the application name (picture attached), and arbitrary characters can be inserted (including angle brackets).  Moving on, ```$()``` is a jQuery DOMXSS sink. If we inject a payload like ```<svg onload=alert(document.domain)>``` then XSS will be executed showing the executing domain.

So to sum up,
1. Attacker creates an application where the app name is a XSS payload.
2. Attacker uses the app to post a tweet, then the tweet contains a malicious info of which app the tweet is sent from
3. Victim clicks on the app info and XSS triggers.

#PoC
1. Make sure you are using latest IE (otherwise CSP kicks in)
2. Follow @attackerfoobar or search for the user on TweetDeck
3. Expand the first tweet, click "Click here to get followers ❤️" (which is a bait app name)
4. XSS executes

Video demonstration is also attached.

#Fix
Probably sanitize ```n.getMainTweet().source``` before putting it into ```$()```.

</details>

---
*Analysed by Claude on 2026-05-12*
