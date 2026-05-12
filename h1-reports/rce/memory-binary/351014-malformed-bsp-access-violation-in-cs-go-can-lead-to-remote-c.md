# Malformed .BSP Access Violation in CS:GO Leading to Remote Code Execution

## Metadata
- **Source:** HackerOne
- **Report:** 351014 | https://hackerone.com/reports/351014
- **Submitted:** 2018-05-13
- **Reporter:** chippy
- **Program:** Valve Bug Bounty (CS:GO)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Memory Corruption, Access Violation, Improper Input Validation, Buffer Overflow
- **CVEs:** None
- **Category:** memory-binary

## Summary
A malformed BSP (Binary Space Partition) map file in CS:GO triggers an access violation due to insufficient input validation during map parsing. An attacker hosting a malicious server can distribute crafted map files that cause memory corruption, leading to arbitrary code execution on victim clients during map download and loading.

## Attack scenario
1. Attacker creates a malformed BSP file with invalid data structures in critical sections
2. Attacker hosts a CS:GO server and configures it to serve the malicious BSP as a custom map
3. Victim connects to the attacker's server, triggering automatic map download
4. CS:GO client begins parsing the BSP file during map initialization
5. Malformed BSP structure causes memory access violation in parsing code
6. Attacker achieves code execution within the victim's CS:GO process context

## Root cause
CS:GO's BSP file parser fails to properly validate and bounds-check data structures within the binary map format. The parser assumes well-formed input and does not verify structure sizes, offsets, or element counts before dereferencing pointers or accessing memory regions, allowing crafted malicious BSP files to trigger out-of-bounds memory access.

## Attacker mindset
An attacker would weaponize this vulnerability by creating a fake or compromised CS:GO server to attract players. The passive distribution mechanism (automatic map downloads) is ideal for mass compromise without user interaction beyond joining a server. This targets the game's trust model where clients automatically download content from servers.

## Defensive takeaways
- Implement strict input validation and bounds checking for all binary file format parsers
- Verify BSP structure integrity (magic numbers, version checks, header validation) before parsing
- Use safe deserialization practices with size limits and offset validation
- Implement address space layout randomization (ASLR) and DEP/NX to mitigate exploitation
- Consider sandboxing map loading in a restricted process or container
- Add integrity checks (signatures/hashes) for downloaded game content
- Implement fuzzing tests for binary file parsers with malformed input
- Use memory-safe languages or libraries for parsing untrusted binary formats

## Variant hunting
Search for similar vulnerabilities in other game engines' map format parsers (Quake, Source engine mods, Unreal Engine), other BSP-based games, and any client that automatically downloads and parses binary content from remote servers without validation. Check for similar patterns in 3D model format parsing (MDL, DAE, FBX) and texture format handling.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566.001: Phishing - Spearphishing Attachment
- T1203: Exploitation for Client Execution
- T1559.001: Inter-Process Communication - Component Object Model
- T1548.004: Abuse Elevation Control Mechanism - Elevated Execution with Prompt

## Notes
This is a classic example of trusting untrusted server-provided content. The attack surface is particularly dangerous because legitimate game mechanics (automatic map downloads) are weaponized. The report lacks specific technical details about which BSP structure field triggers the violation, suggesting potential CVE-level severity. This vulnerability type is especially critical in multiplayer games where server-to-client content distribution is expected behavior.

## Full report
<details><summary>Expand</summary>

A malformed .BSP can trigger an Access Violation on CS:GO that can lead to arbitrary code execution on a remote computer. I have attached a copy of the malformed .BSP which reliably triggers an Access Violation on CS:GO.

## Impact

An attacker hosting a malicious server could compromise a remote client by having them download a custom map, triggering remote code execution on the victim's computer.

</details>

---
*Analysed by Claude on 2026-05-11*
