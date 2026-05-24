# Unix Domain Socket Null Byte Injection in Ruby Socket Library

## Metadata
- **Source:** HackerOne
- **Report:** 302997 | https://hackerone.com/reports/302997
- **Submitted:** 2018-01-07
- **Reporter:** ooooooo_q
- **Program:** Ruby
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Null Byte Injection, Path Traversal, Improper Input Validation, Socket Hijacking
- **CVEs:** CVE-2018-8779
- **Category:** uncategorised

## Summary
Ruby's Unix domain socket methods (UNIXServer.open and Socket.unix) fail to properly validate null characters in socket path arguments, allowing attackers to truncate paths and connect to unintended sockets. While some methods like Socket.unix_server_loop properly reject null bytes, others inconsistently permit them, creating a security gap in socket validation.

## Attack scenario
1. Attacker identifies a Ruby application using UNIXServer.open() or Socket.unix() with user-controlled socket paths
2. Attacker crafts a malicious socket path containing a null byte (e.g., '/tmp/socket\0malicious')
3. The null byte truncates the path at the first null character, causing the socket to resolve to '/tmp/socket' instead of the intended path
4. Attacker pre-creates a socket at the truncated path ('/tmp/socket') and listens for connections
5. When the victim application attempts to connect using the crafted path, it connects to the attacker's socket instead
6. Attacker intercepts sensitive communication or injects malicious data through the hijacked socket connection

## Root cause
Inconsistent null byte validation across Ruby's Unix socket library. Lower-level socket methods (UNIXServer.open, Socket.unix) do not validate null characters in path arguments before passing them to the underlying system calls, while higher-level wrapper methods (Socket.unix_server_loop, Socket.unix_server_socket) properly validate using lstat() which rejects null bytes.

## Attacker mindset
An attacker would exploit this to perform socket hijacking attacks in multi-tenant or shared environments where socket paths may be partially user-controlled. By injecting null bytes, they can cause path truncation and redirect connections to sockets under their control, enabling man-in-the-middle attacks on inter-process communication.

## Defensive takeaways
- Always validate socket paths for null bytes before use, regardless of language or library
- Implement consistent validation across all socket creation methods in the codebase
- Use higher-level APIs that include built-in validation rather than low-level socket functions
- Never trust user-supplied paths in socket operations; sanitize and whitelist allowed paths
- Apply defense-in-depth: validate at both application and library levels
- Use static analysis to detect socket path handling with potentially untrusted input
- Consider using abstract sockets or namespace-isolated socket paths to prevent path manipulation attacks

## Variant hunting
Check other language bindings (Python socket module, Go net.Listen) for similar null byte validation gaps
Audit other file-path operations in Ruby (File.open, Dir.open) for null byte handling inconsistencies
Search for other Socket methods that may not validate paths (connect, bind operations)
Test named pipe/FIFO creation (mkfifo) for similar null byte injection vulnerabilities
Examine any custom socket wrapper libraries built on top of Ruby's socket module

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1574 - Hijack Execution Flow (Library Search Order Hijacking variant)
- T1021 - Remote Services (Local socket communication)
- T1534 - Internal Spearphishing

## Notes
The vulnerability demonstrates a classic case of inconsistent input validation within a single library. The fact that some methods (Socket.unix_server_loop) properly reject null bytes while others (UNIXServer.open) accept them suggests this was an oversight in the original implementation rather than intentional design. The impact is amplified in applications running with elevated privileges or handling sensitive IPC communication. This is a good example of why security-critical operations should have defense-in-depth validation at multiple layers.

## Full report
<details><summary>Expand</summary>

Some methods on UNIX domain socket are not checked for null characters.

```
[vagrant@localhost ~]$ ls /tmp
[vagrant@localhost ~]$ irb
irb(main):001:0> require 'socket'
=> true

irb(main):002:0> UNIXServer.open("/tmp/socket\0ruby") {|serv|
irb(main):003:1*   c = UNIXSocket.open("/tmp/socket\0sapphire")
irb(main):004:1>   s = serv.accept
irb(main):005:1>   s.write "from server"
irb(main):006:1>   c.write "from client"
irb(main):007:1>   p c.recv(20)
irb(main):008:1>   p s.recv(20)
irb(main):009:1> }
"from server"
"from client"
=> "from client"

irb(main):010:0> UNIXServer.open("/tmp/socket2") {|serv|
irb(main):011:1*   c = Socket.unix("/tmp/socket2\0emerald")
irb(main):012:1>   s = serv.accept
irb(main):013:1>   s.write "from server"
irb(main):014:1>   p c.recv(20)
irb(main):015:1> }
"from server"
=> "from server"

# safe
irb(main):016:0> Socket.unix_server_loop("/tmp/socket3\0yellow")
Traceback (most recent call last):
        5: from /home/vagrant/.rbenv/versions/2.5.0/bin/irb:11:in `<main>'
        4: from (irb):16
        3: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/socket.rb:1163:in `unix_server_loop'
        2: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/socket.rb:1108:in `unix_server_socket'
        1: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/socket.rb:1108:in `lstat'
ArgumentError (path name contains null byte)
irb(main):017:0> Socket.unix_server_socket("/tmp/socket3\0yellow")
Traceback (most recent call last):
        4: from /home/vagrant/.rbenv/versions/2.5.0/bin/irb:11:in `<main>'
        3: from (irb):17
        2: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/socket.rb:1108:in `unix_server_socket'
        1: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/socket.rb:1108:in `lstat'
ArgumentError (path name contains null byte)
```

## Impact

It may be connected to an unintended socket.

</details>

---
*Analysed by Claude on 2026-05-24*
