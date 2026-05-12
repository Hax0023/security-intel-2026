# Panorama UI XSS leads to Remote Code Execution via Kick/Disconnect Message

## Metadata
- **Source:** HackerOne
- **Report:** 631956 | https://hackerone.com/reports/631956
- **Submitted:** 2019-06-29
- **Reporter:** shayhelman
- **Program:** Counter-Strike: Global Offensive (Valve)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Cross-Site Scripting (XSS), Remote Code Execution (RCE), Improper Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
CS:GO's Panorama UI framework contains an XSS vulnerability in kick/disconnect message handlers due to unsafe HTML parsing with html="true" attribute enabled. Attackers can inject malicious JavaScript payloads via the KickClient() SourceMod function to achieve arbitrary code execution on victim machines, including executing system commands through SteamOverlayAPI.

## Attack scenario
1. Attacker sets up a CS:GO dedicated server with a malicious SourceMod plugin using KickClient() function
2. Attacker crafts XSS payload using <a onmouseover> tag with JavaScript code: <a onmouseover='javascript:SteamOverlayAPI.OpenExternalBrowserURL(...)'>message</a>
3. Victim joins the attacker's server (either through deception or direct invitation)
4. Server executes KickClient() with malicious payload, triggering the disconnect popup UI
5. Victim's mouse hovers over the disconnect message, triggering the onmouseover event
6. JavaScript executes with arbitrary capabilities, potentially launching calc.exe or other system commands via file:// protocol

## Root cause
The popup_generic.xml Panorama layout file has html="true" enabled on Label elements that process unsanitized user input from server kick/disconnect messages. The Panorama framework parses these messages as raw HTML/JavaScript without proper input validation or output encoding, allowing injection of arbitrary HTML tags and event handlers.

## Attacker mindset
An attacker would recognize that game servers are trusted environments with privileged code execution contexts. By compromising server-side message delivery mechanisms (SourceMod plugins), they can force clients to render and interact with malicious content. The low interaction requirement (simple mouse hover) maximizes exploitation probability. The use of SteamOverlayAPI provides direct system command execution without additional privilege escalation.

## Defensive takeaways
- Disable html="true" attribute in Panorama UI files unless absolutely necessary; use text content instead
- Implement strict input validation and sanitization on all server-to-client messages, especially those displayed in UI popups
- Use allowlisted HTML tags and event handlers rather than blocking dangerous ones; prefer text-only rendering for untrusted content
- Apply output encoding/escaping to neutralize HTML metacharacters in user-controlled strings
- Restrict SteamOverlayAPI capabilities to prevent execution of arbitrary system commands via file:// protocol handlers
- Implement Content Security Policy (CSP) equivalents in Panorama framework to prevent inline script execution
- Audit all Panorama layout files for html="true" usage and reduce attack surface by requiring server trust validation

## Variant hunting
Search for other Panorama layout files with html="true" enabled that process user input from chat, lobby messages, friend requests, or server communications. Investigate other Valve games using Panorama (Dota 2, Artifact, Half-Life: Alyx) for similar XSS vulnerabilities. Look for additional event handlers beyond onmouseover that require minimal user interaction (onload, onfocus). Research other SteamAPI or overlay functions callable from JavaScript context that could lead to system compromise.

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1566
- T1204

## Notes
This vulnerability is particularly severe because it bridges the gap between web-based XSS and native code execution through SteamOverlayAPI integration. The attack requires no user awareness of security risks - a simple mouse hover triggers exploitation. The writeup references similar vulnerability #470520, suggesting Valve had prior knowledge of Panorama XSS issues. The SourceMod KickClient() function's lack of character limits compared to sm_kick command demonstrates how plugin systems can increase attack surface. The file:// protocol handler in SteamOverlayAPI is dangerous and should be restricted or sandboxed.

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
