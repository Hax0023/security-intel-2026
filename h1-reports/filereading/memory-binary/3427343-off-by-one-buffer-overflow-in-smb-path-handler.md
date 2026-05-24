# Off-by-One Buffer Overflow in SMB Path Handler (lib/smb.c)

## Metadata
- **Source:** HackerOne
- **Report:** 3427343 | https://hackerone.com/reports/3427343
- **Submitted:** 2025-11-15
- **Reporter:** pelioro
- **Program:** curl (libcurl)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Buffer Overflow, Off-by-One Error, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
An off-by-one buffer overflow exists in curl's SMB path handling due to an incorrect bounds check using '>' instead of '>='. A 1023-byte SMB path passes validation but causes a 1-byte overflow when the null terminator is written to the 1024-byte buffer.

## Attack scenario
1. Attacker crafts a malicious SMB URI with a 1023-character path
2. Application using libcurl with SMB support accepts the path in smb_send_open()
3. Bounds check evaluates: 1024 > 1024 = false, incorrectly allowing the path
4. strcpy() writes 1024 bytes plus null terminator (1025 total) into 1024-byte buffer
5. One byte past the buffer boundary is overwritten, corrupting adjacent stack/heap memory
6. Potential crash or information disclosure depending on adjacent memory contents

## Root cause
Logic error in bounds checking: the condition checks `byte_count > sizeof(msg.bytes)` instead of `byte_count >= sizeof(msg.bytes)`, creating a classic off-by-one vulnerability when combined with unsafe strcpy() usage.

## Attacker mindset
An attacker would target applications integrating libcurl with SMB enabled, sending specially crafted SMB paths to trigger memory corruption. While full RCE is unlikely, the attacker could exploit this for denial of service or information leakage in specific memory layouts.

## Defensive takeaways
- Always use >= instead of > for buffer boundary checks when comparing against buffer capacity
- Replace strcpy() with bounded alternatives (strncpy, memcpy with size validation)
- Implement both input validation AND safe string handling as defense-in-depth
- Use static analysis tools (ASAN, valgrind, clang-analyzer) to catch off-by-one errors
- Test edge cases: exact buffer size - 1, exact buffer size, and buffer size + 1
- Apply bounds checks consistently across all code paths handling the same buffer

## Variant hunting
Search codebase for: (1) Other strcpy/strcat calls without bounds, (2) Comparisons using > against sizeof() where >= was intended, (3) byte_count or length calculations using +1 that could overflow when checked, (4) Fixed-size arrays in network protocol handlers, (5) Similar patterns in SMB/CIFS implementations in other libraries

## MITRE ATT&CK
- T1190
- T1499

## Notes
The researcher notes exploitation is unlikely due to the single-byte overflow nature, but the bug is real and present in release builds. The vulnerability requires SMB support to be compiled in and an active SMB connection to trigger. The fix is straightforward: change the comparison operator and replace strcpy with memcpy.

## Full report
<details><summary>Expand</summary>

## Summary

Found an off-by-one buffer overflow in `lib/smb.c` when handling SMB file paths. The bounds check uses `>` instead of `>=`, allowing a path of exactly 1023 bytes to overflow the 1024-byte buffer by one byte when the null terminator is added.

## Details

**File:** lib/smb.c  
**Function:** smb_send_open()  
**Lines:** 784, 801

### The Bug

```c
struct smb_nt_create {
    // ... other fields ...
    char bytes[1024];  // fixed size buffer
} PACK;

static CURLcode smb_send_open(...) {
    struct smb_nt_create msg;
    const size_t byte_count = strlen(req->path) + 1;
    
    if(byte_count > sizeof(msg.bytes))  // Wrong: should be >=
        return CURLE_FILESIZE_EXCEEDED;
    
    // ... setup code ...
    
    strcpy(msg.bytes, req->path);  // Overflow when byte_count == 1024
}
```

### The Math

- Buffer size: 1024 bytes
- Check allows: byte_count <= 1024 (because > not >=)
- If path is 1023 bytes:
  - `strlen(req->path)` = 1023
  - `byte_count` = 1024
  - Check: `1024 > 1024` = FALSE (passes)
  - `strcpy()` writes 1024 bytes + null = **1025 bytes**
  - **Overflow by 1 byte**

## Testing

Built curl with ASan to verify:

```bash
./configure --with-openssl --enable-smb --enable-debug \
  CFLAGS="-fsanitize=address"
make
```

SMB support confirmed:
```
$ ./src/curl --version | grep smb
Protocols: ... smb smbs ...
```

Note: Couldn't trigger the crash in testing because it requires an actual SMB connection, but the bug is visible in the code.

## Fix

Two changes needed:

```diff
- if(byte_count > sizeof(msg.bytes))
+ if(byte_count >= sizeof(msg.bytes))
    return CURLE_FILESIZE_EXCEEDED;

- strcpy(msg.bytes, req->path);
+ memcpy(msg.bytes, req->path, byte_count);
```

## Notes

- Tested on curl master branch
- SMB support must be compiled in
- Bug is in release builds, not debug-only
- Manual code review, no AI used

This is a real bug that should be fixed, even though exploitation is unlikely.

## Impact

- Memory corruption (1 byte past buffer)
- Likely causes crash
- RCE unlikely (off-by-one is hard to exploit)
- Affects any app using libcurl with SMB

</details>

---
*Analysed by Claude on 2026-05-24*
