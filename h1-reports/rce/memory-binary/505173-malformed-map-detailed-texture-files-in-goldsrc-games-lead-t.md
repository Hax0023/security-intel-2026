# Malformed map detailed texture files in GoldSrc games lead to Remote Code Execution

## Metadata
- **Source:** HackerOne
- **Report:** 505173 | https://hackerone.com/reports/505173
- **Submitted:** 2019-03-05
- **Reporter:** nyancat0131
- **Program:** Valve Half-Life/GoldSrc Engine (Counter-Strike)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stack Buffer Overflow, Remote Code Execution, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A stack overflow vulnerability exists in GoldSrc's detailed texture file parsing (hw.dll) when processing malformed `maps/<map_name>_detail.txt` files. Attackers can craft malicious detail texture files that are distributed via game servers using precache_generic, allowing remote code execution on connecting clients.

## Attack scenario
1. Attacker creates a malicious Counter-Strike map with a crafted `cs_mapname_detail.txt` file containing oversized texture data
2. Attacker hosts a dedicated server and uses an AMXX plugin to precache the malicious detail texture file
3. Victim client connects to the attacker's server and downloads the malicious map file via sv_downloadurl
4. Server executes client_cmd to force victims to enable detailed textures with `r_detailtextures 1`
5. Client-side hw.dll attempts to parse the malformed detail texture file and triggers stack overflow
6. Attacker's shellcode executes with victim's game privileges, achieving remote code execution

## Root cause
The detailed texture file parser in hw.dll does not properly validate input file structure or bounds-check texture name strings before copying them to a fixed-size stack buffer, allowing a stack overflow when processing malformed files.

## Attacker mindset
Server operator or malicious mapmaker distributing weaponized game content to compromise players' systems. The attack is particularly insidious as it abuses the game's built-in file distribution mechanism and client command execution features.

## Defensive takeaways
- Implement strict bounds checking and length validation for all texture file parsing operations
- Use stack canaries and ASLR to detect and prevent stack overflow exploitation
- Validate file format structure before processing (magic bytes, size headers, field lengths)
- Implement sandboxing or privilege separation for map content processing
- Add integrity checking for distributed game files (checksums/signatures)
- Disable or restrict server-side client command execution for potentially dangerous cvars
- Use safe string handling functions (strncpy with bounds checking) instead of unbounded copies
- Implement fuzzing-based testing for all file format parsers

## Variant hunting
Search for similar stack overflow patterns in texture/material file parsers across other Source engine games and modifications. Examine sprite file (`*.spr`), model (`*.mdl`), and custom content parsers for identical unsafe buffer operations. Check for precache_generic exploitation vectors in other Valve games.

## MITRE ATT&CK
- T1190
- T1499
- T1570
- T1570

## Notes
This vulnerability chain demonstrates how game distribution mechanisms can be weaponized. The workaround using sv_downloadurl bypasses the precache_generic bug, making exploitation more reliable. The attack requires client-side code execution (r_detailtextures) which can be forced server-side via client_cmd, eliminating user interaction requirements. GoldSrc engine is legacy but still used in popular titles like Counter-Strike 1.6.

## Full report
<details><summary>Expand</summary>

A crafted map detailed texture file (`maps/<map_name>_detail.txt`) can be used to exploit a stack overflow vulnerability in `hw.dll` that can lead to remote code execution.

# Reproduction
I used Counter-Strike for PoCs.

## Using a listen server
- Place attached `cs_assault_detail.txt` in `cstrike/maps` folder
- Start the game
- Open the console, type `r_detailtextures 1`
- Host a new game on `cs_assault`
- The game crashes when trying to load detailed textures

## Using a dedicated server
- Place attached `cs_assault_detail.txt` in `cstrike/maps` folder on the server
- Write an AMXX plugin that does the following:
 - Use `precache_generic` to precache `maps/cs_assault_detail.txt`
 - Use `client_cmd` to force clients to execute `r_detailtextures 1`
- Host a new server on `cs_assault`
- Open the client and connect to the server
- The client crashes when trying to load detailed textures
Note: `precache_generic` has some bug (https://github.com/ValveSoftware/halflife/issues/1551). The workaround is to setup `sv_downloadurl` for the server.

# Exploitability
Since the file can be sent from the server using `precache_generic`, and the server has the ability to slowhack clients, attackers can use this to trigger RCE on clients.

## Impact

Attackers can exploit this bug to execute arbitrary unauthorized codes on victim's computer.

</details>

---
*Analysed by Claude on 2026-05-12*
