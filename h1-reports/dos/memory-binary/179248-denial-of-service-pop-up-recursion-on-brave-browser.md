# Denial of Service via Recursive Pop-up Dialog Prompts in Brave Browser

## Metadata
- **Source:** HackerOne
- **Report:** 179248 | https://hackerone.com/reports/179248
- **Submitted:** 2016-11-01
- **Reporter:** sahiltikoo
- **Program:** Brave Browser
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Resource Exhaustion, Uncontrolled Dialog Generation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Brave Browser on Linux is vulnerable to a denial of service attack through recursive pop-up dialogs that freeze the browser window. An attacker can send a malicious HTML file containing self-perpetuating dialog.alert() or window.open() calls that consume system resources, making the browser unresponsive and requiring process termination.

## Attack scenario
1. Attacker crafts HTML file containing recursive pop-up code (likely window.alert() in a loop or location.reload() triggering dialogs)
2. Attacker distributes the HTML file via email, social media, or hosts it on a web server
3. Victim opens the HTML file or visits the attacker's website in Brave Browser
4. Browser begins spawning unlimited dialog prompts in rapid succession
5. Browser window becomes frozen and unresponsive; user cannot interact with UI controls
6. Victim is forced to terminate the browser process via system commands (kill -9 on Linux, Task Manager on Windows)

## Root cause
Brave Browser lacks rate limiting or user confirmation mechanisms for recursive dialog prompts. Unlike Chrome which implements a 'Prevent this page from creating additional dialogs' checkbox after multiple prompts, Brave allows unlimited consecutive dialog generation without restriction. The mishandling of dialog event handlers and location.reload() combinations allows exponential resource consumption.

## Attacker mindset
Low-effort malicious activity targeting browser DoS. Attacker exploits known browser weaknesses that persist across implementations. Goal is user frustration and system resource exhaustion rather than data theft, demonstrating platform-specific vulnerability gaps.

## Defensive takeaways
- Implement dialog prompt rate limiting with automatic suppression after N consecutive dialogs within a time window
- Add 'Prevent this page from creating additional dialogs' checkbox after first/second dialog prompt
- Set maximum concurrent dialog limit per page context
- Implement timeout mechanism for dialog stacks to prevent indefinite dialog chains
- Monitor dialog generation frequency and implement exponential backoff
- Add browser settings to globally disable or sandbox dialog prompts for untrusted origins
- Provide keyboard shortcut (beyond Ctrl+W) to force-close problematic tabs

## Variant hunting
Test recursive window.open() chains with varying popup parameters
Test window.alert()/confirm()/prompt() loops with async callbacks
Test combination of location.reload() + dialog generation
Test setTimeout/setInterval triggering dialogs repeatedly
Test onbeforeunload event handlers creating dialog loops
Test interaction with page unload handlers and dialog queues
Test dialog generation from iframes and child windows
Test promise-based async dialog chains

## MITRE ATT&CK
- T1499
- T1499.004

## Notes
This is a known class of vulnerability previously patched in Chrome and Safari, but Brave (derivative of Chromium) failed to properly implement the same safeguards. The vulnerability demonstrates importance of tracking upstream security fixes across browser forks. Linux platform specificity suggests possible timing or resource handling differences. PoC included hosted on tiks.host-ed.me. Report filed against Brave Browser version 0.11.6.

## Full report
<details><summary>Expand</summary>



## Summary:

Basically I have found a denial of service attack on brave browser in Linux platform.In this bug when we open the __html file or visiting (www.tiks.host-ed.me)__ then click on __pop up dos.html__ ,(which contains a recurring pop up code),the Pop up freezes the entire browser window except for minimize button  and on maximizing it hangs, we can't close any tabs neither using (Ctrl+w) to close current tab that is causing recursion. This is a known issue and in past has been already addressed in browsers such as _Google Chrome_, however Brave Browser is still affected by the issue.And in _safari browser_ Pop up's come after some time delays that allows user to stop the running process by clicking on (X) in URL.

##Attack Scenario :-

This can be exploited by an attacker just by sending this __html file or visiting (www.tiks.host-ed.me)__ to victim through email or any other source and when victim will open the html file in his/her Brave browser their window will freeze and they would need to kill the process in Linux(kill -9 pid) or (End Task) in windows. So to avoid such misuse of the issue some patches must be made. 

>The vulnerability occurred due to mishandling of location.reload function, as it keeps reloading the >document, however the issue more likely is present inside of not limiting the pop ups or simply offering no >way to ignore further prompts. 


## Products affected:
 
_Brave browser(0.11.6) on Linux platform_

## Steps To Reproduce:

1.) Got o www.tiks.host-ed.me then click on __pop up dos.html__ file or You can open the html code i have attached below on brave browser.
2.) You will see pop up like :-

{F131446}

And while in Google chrome this effect is limited by offering a checkbox to prevent the current document from creating additional dialogs. Like as shown below :-

{F131451}





## Supporting Material/References:

I have attached POC images and html code that you will require in resolving the above issue.

Thanks
sahiltikoo


</details>

---
*Analysed by Claude on 2026-05-24*
