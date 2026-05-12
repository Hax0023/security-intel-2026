# Unchecked weapon ID in WeaponList message parser leads to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 513154 | https://hackerone.com/reports/513154
- **Submitted:** 2019-03-21
- **Reporter:** nyancat0131
- **Program:** Counter-Strike 1.6 (Half-Life SDK)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Buffer Overflow, Out-of-Bounds Write, Lack of Input Validation, Memory Corruption
- **CVEs:** None
- **Category:** memory-binary

## Summary
The WeaponList message parser in the Half-Life client SDK fails to validate the weapon ID parameter before using it as an array index, allowing an attacker to write arbitrary data to memory locations in the client process. By crafting a malicious WeaponList message, an attacker can overwrite the gEngfuncs function table and achieve remote code execution on connected clients.

## Attack scenario
1. Attacker sets up a malicious Counter-Strike server or performs Man-in-the-Middle (MITM) attack on game traffic
2. When a legitimate client connects and the InitHUD message is received, the attacker sends a crafted WeaponList message with an out-of-bounds weapon ID (range -128 to 127)
3. The unchecked iId value is used directly as an array index: rgWeapons[wp->iId], writing weapon structure data at arbitrary memory offsets
4. Attacker crafts the weapon structure to overwrite the gEngfuncs function pointer table, specifically the HUD_DirectorMessage function handler
5. The overwritten function pointer is redirected to a ROP gadget chain prepared by the attacker
6. When the client receives a subsequent SendCmd or director message, the compromised function pointer is invoked, executing arbitrary code with client privileges

## Root cause
The AddWeapon function performs no bounds checking on the weapon ID before using it as an array index into the rgWeapons array. The iId parameter is read directly from untrusted network data (READ_CHAR()) without validation, allowing negative or oversized indices to write beyond array boundaries and corrupt adjacent memory structures including the gEngfuncs function table.

## Attacker mindset
The attacker recognizes that game protocol messages from servers are implicitly trusted by clients without validation. By identifying the memory layout of critical structures like gEngfuncs relative to the rgWeapons array, the attacker can calculate precise offsets to achieve function pointer hijacking and ROP gadget execution.

## Defensive takeaways
- Always validate array indices before use, even when derived from 'trusted' sources like game servers
- Implement bounds checking: if (wp->iId < 0 || wp->iId >= MAX_WEAPONS) reject the message
- Never trust network-supplied data; treat all protocol messages as potentially malicious
- Use Address Space Layout Randomization (ASLR) and Data Execution Prevention (DEP) to complicate ROP gadget chains
- Consider using safer alternatives to direct memory writes (avoid array indexing with unvalidated indices)
- Implement integrity checks or signatures on critical function tables
- Apply principle of least privilege to game client processes

## Variant hunting
Search for similar patterns: (1) any array indexing with READ_CHAR() or network-supplied signed values without bounds checks, (2) direct use of network-supplied indices in other message handlers (WeaponInfo, ItemList, etc.), (3) other function tables or critical structures adjacent to unbounded arrays, (4) similar vulnerabilities in other games using the Half-Life SDK or comparable multiplayer protocols

## MITRE ATT&CK
- T1190
- T1203
- T1559
- T1021

## Notes
This vulnerability affects all clients connecting to untrusted servers. The PoC demonstrates practical exploitation using AMXX plugin to serve malicious WeaponList messages and execute arbitrary commands via function table hijacking. The vulnerability is particularly severe because it requires no user interaction beyond connecting to a malicious server.

## Full report
<details><summary>Expand</summary>

Let's look at WeaponList message parser code in the HLSDK:
``` cpp
int CHudAmmo::MsgFunc_WeaponList(const char *pszName, int iSize, void *pbuf )
{
	BEGIN_READ( pbuf, iSize );
	
	WEAPON Weapon;

	strcpy( Weapon.szName, READ_STRING() );
	Weapon.iAmmoType = (int)READ_CHAR();	
	
	Weapon.iMax1 = READ_BYTE();
	if (Weapon.iMax1 == 255)
		Weapon.iMax1 = -1;

	Weapon.iAmmo2Type = READ_CHAR();
	Weapon.iMax2 = READ_BYTE();
	if (Weapon.iMax2 == 255)
		Weapon.iMax2 = -1;

	Weapon.iSlot = READ_CHAR();
	Weapon.iSlotPos = READ_CHAR();
	Weapon.iId = READ_CHAR();
	Weapon.iFlags = READ_BYTE();
	Weapon.iClip = 0;

	gWR.AddWeapon( &Weapon );

	return 1;
}
```

And `WeaponResource::AddWeapon`:

``` cpp
void AddWeapon( WEAPON *wp ) 
{ 
		rgWeapons[ wp->iId ] = *wp;	
		LoadWeaponSprites( &rgWeapons[ wp->iId ] );
}
```
There are no boundary check, and the range of `iId` is `[-128, 128)`, so I can modify many things in the data section.

In `client.dll`, there's an object called `gEngfuncs`, it is a function table that has various functions of the engine. After some calculations on latest CS 1.6 `client.dll`, I concluded that this function table could be overwritten using the above bug.

I have attached a PoC that will pop `calc.exe` on latest CS 1.6 client when connected to malicious server. The AMXX plugin will catch `InitHUD` message, and send crafted `WeaponList` message to overwrite the address of function used in `HUD_DirectorMessage` to execute client cmds to a ROP gadget that will trigger the chain sent in the next `SendCmd` call. To overwrite that address, I used a crafted weapon sprite list (`weapon_pwn.txt`) (see `WEAPON` struct, file `cl_dll/ammo.h` in the HLSDK).

## Impact

Since it's RCE, attacker can do almost anything that don't require higher privilege (ex. compromise account, inject malware, ...)

</details>

---
*Analysed by Claude on 2026-05-11*
