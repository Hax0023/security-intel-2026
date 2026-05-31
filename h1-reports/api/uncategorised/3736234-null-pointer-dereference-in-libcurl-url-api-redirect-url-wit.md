# NULL pointer dereference in libcurl URL API redirect_url() with CURLU_DEFAULT_SCHEME

## Metadata
- **Source:** HackerOne
- **Report:** 3736234 | https://hackerone.com/reports/3736234
- **Submitted:** 2026-05-14
- **Reporter:** mulan_dh
- **Program:** curl/libcurl
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** NULL pointer dereference, Denial of Service, Memory safety
- **CVEs:** None
- **Category:** uncategorised

## Summary
A NULL pointer dereference exists in libcurl's URL API when curl_url_set() handles a relative URL with CURLU_DEFAULT_SCHEME on a CURLU handle lacking a stored scheme. The redirect_url() function in lib/urlapi.c dereferences u->scheme before null validation, causing a SIGSEGV crash.

## Attack scenario
1. Attacker creates a CURLU handle and sets host and path without explicitly setting a scheme
2. Attacker calls curl_url_set() with a relative URL and CURLU_DEFAULT_SCHEME flag
3. The URL API uses a default scheme internally but does not persist it in u->scheme
4. redirect_url() is invoked and immediately dereferences u->scheme via strlen()
5. NULL pointer dereference occurs, triggering SIGSEGV and crashing the process
6. Attacker achieves denial of service against the vulnerable application

## Root cause
The redirect_url() function assumes u->scheme is non-NULL and calls strlen(u->scheme) before performing NULL checks. Meanwhile, urlget_url() can use DEFAULT_SCHEME internally without persisting it to u->scheme when CURLU_DEFAULT_SCHEME flag is set, creating a state where the handle lacks a stored scheme but redirect_url() expects one.

## Attacker mindset
An attacker targeting libcurl-based applications seeks to trigger a crash via remote input. By understanding the URL API's two-phase scheme handling (internal default vs. persistent storage), the attacker crafts a specific sequence of CURLU operations to reach the vulnerable code path with untrusted relative URLs, achieving DoS.

## Defensive takeaways
- Always validate pointer non-nullability before dereferencing, even in paths that seem internally consistent
- Synchronize internal state representations with persistent object state; avoid using temporary values that differ from stored values
- Add explicit NULL checks for all pointer dereferences immediately before use, not relying on earlier conditional branches
- For API functions that support default values via flags, ensure defaults are either always persisted or never assumed to exist later
- Implement fuzz testing on URL API with various flag combinations and incomplete CURLU handle states
- Use static analysis tools to detect potential NULL dereferences and enforce invariant checking

## Variant hunting
Search for similar patterns in libcurl's URL handling: other functions that reference u->scheme, u->host, u->port without null checks; flag-based default value mechanisms that diverge from persistent state; relative URL processing in other parts of urlapi.c; similar defensive gaps in other URL parsing libraries (cURL clones, browser engines, web frameworks).

## MITRE ATT&CK
- T1190
- T1499

## Notes
The vulnerability requires a specific sequence of API calls and is most impactful against applications that build CURLU handles incrementally with partial information and process remote or untrusted URLs. The fix is straightforward (add NULL check), but the root cause reflects a deeper architectural issue where temporary and persistent state diverge. Dan Fandrich from curl security team was involved in the disclosure.

## Full report
<details><summary>Expand</summary>

## Summary A NULL pointer dereference appears to exist in libcurl's URL API path when `curl_url_set()` handles a relative URL together with `CURLU_DEFAULT_SCHEME` on a `CURLU` handle that has host/path information but no stored `u->scheme`. The issue is in `lib/urlapi.c` inside `redirect_url()`, where `u->scheme` is used in `strlen(u->scheme)` before the function checks whether the relevant inputs are valid. If the URL handle reaches this path without a stored scheme, the process can crash with SIGSEGV. Dan Fandrich from the curl security list asked me to submit this report on HackerOne for tracking. This is the same issue previously emailed to `security@curl.se`. ## Affected version - Source reviewed: curl master / 8.21.0-DEV area, `lib/urlapi.c`, `redirect_url()` - The original report stated reproduction against libcurl 8.14.1 and the current development source path. - Local reproduction environment used libcurl URL API semantics around `CURLU_DEFAULT_SCHEME`. ## Technical details In `redirect_url()`, `u->scheme` is dereferenced before a safe NULL check: ```c const char *protsep = base + strlen(u->scheme) + 3; DEBUGASSERT(base && relurl && u); if(!base)   return CURLUE_MALFORMED_INPUT; ``` The problematic path is possible because `urlget_url()` can use `DEFAULT_SCHEME` locally when `CURLU_DEFAULT_SCHEME` is supplied, without necessarily storing a scheme in `u->scheme`: ```c if(u->scheme)   scheme = u->scheme; else if(flags & CURLU_DEFAULT_SCHEME)   scheme = DEFAULT_SCHEME; else   return CURLUE_NO_SCHEME; ``` This means URL generation can succeed using a default scheme string, while the underlying `CURLU` object can still have `u->scheme == NULL`. Later, `redirect_url()` assumes `u->scheme` is non-NULL and calls `strlen(u->scheme)`. ## Steps to reproduce The following minimal PoC constructs a `CURLU` handle with host and path, but no explicit scheme, then sets a relative URL using `CURLU_DEFAULT_SCHEME`: ```c #include <stdio.h> #include <curl/curl.h> int main(void) {     CURLU *u = curl_url();     CURLUcode rc;     if(!u)         return 2;     curl_url_set(u, CURLUPART_HOST, "example.com", 0);     curl_url_set(u, CURLUPART_PATH, "/original", 0);     rc = curl_url_set(u, CURLUPART_URL, "/newpath", CURLU_DEFAULT_SCHEME);     printf("Return code: %d\n", rc);     curl_url_cleanup(u);     return 0; } ``` Compile and run: ```bash gcc -o curl-url-default-scheme-poc poc.c -lcurl ./curl-url-default-scheme-poc ``` Expected safe behavior: libcurl should return a `CURLUcode` error such as `CURLUE_MALFORMED_INPUT` or otherwise normalize/store the default scheme safely. Observed vulnerable behavior in the original test: process crash / segmentation fault from dereferencing `u->scheme` in `redirect_url()`. ## Suggested fix Add a `u->scheme` validation before using it in `redirect_url()`, or ensure the default scheme used by `urlget_url()` is persisted in the `CURLU` object before `redirect_url()` is called. Example defensive check: ```c if(!base || !u || !u->scheme)   return CURLUE_MALFORMED_INPUT; const char *protsep = base + strlen(u->scheme) + 3; ```

## Impact

## Impact A process using libcurl's URL API can be crashed by reaching this URL parsing path with attacker-controlled or otherwise untrusted relative URL input. The direct security impact is denial of service against applications that: - Build a `CURLU` handle in stages, setting host/path without an explicit scheme - Accept or process relative URLs - Use `CURLU_DEFAULT_SCHEME` for convenience or redirect-style normalization If such input is remotely controllable in an application, an attacker may be able to terminate the process by triggering the NULL pointer dereference. I do not claim code execution; this is a crash/availability issue.

</details>

---
*Analysed by Claude on 2026-05-31*
