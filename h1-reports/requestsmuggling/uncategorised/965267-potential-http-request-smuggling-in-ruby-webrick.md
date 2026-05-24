# HTTP Request Smuggling in WEBrick via Improper Transfer-Encoding Validation

## Metadata
- **Source:** HackerOne
- **Report:** 965267 | https://hackerone.com/reports/965267
- **Submitted:** 2020-08-23
- **Reporter:** piao
- **Program:** Ruby on Rails / WEBrick
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Improper Input Validation, CWE-444: Inconsistent Interpretation of HTTP Requests
- **CVEs:** None
- **Category:** uncategorised

## Summary
WEBrick's read_body function uses a loose regex pattern (/chunked/io) to validate the Transfer-Encoding header, allowing attackers to bypass validation with malformed headers like 'Transfer-Encoding: AAAchunkedBBB'. This enables HTTP request smuggling attacks where subsequent requests can be misinterpreted, potentially poisoning caches or bypassing security controls.

## Attack scenario
1. Attacker crafts an HTTP request with Transfer-Encoding header containing 'chunked' as a substring within other characters (e.g., 'AAAchunkedBBB')
2. WEBrick's regex /chunked/io matches the substring and treats the request as chunked-encoded despite malformed syntax
3. The server parses the request body using chunked decoding logic on improperly formatted data
4. A second legitimate request is sent immediately after, which gets misaligned due to incorrect body size calculation
5. The second request's headers/body are interpreted as part of the first request or vice versa
6. Attacker gains ability to poison backend responses, bypass authentication, or perform cache poisoning

## Root cause
The validation logic uses a case statement with regex pattern matching (/chunked/io) that performs substring matching rather than strict header value validation. RFC 7230 requires exact 'chunked' value with proper syntax, but the code accepts any string containing 'chunked' as a substring.

## Attacker mindset
An attacker seeking to exploit request smuggling would recognize that loose header validation creates ambiguity in how proxies and backends parse requests. By crafting malformed Transfer-Encoding headers, they can desynchronize request boundaries and exploit the difference in parsing logic between WEBrick and upstream/downstream servers.

## Defensive takeaways
- Implement strict header validation using exact matching (==) or comprehensive parsing against RFC 7230 specifications
- Use whitelist-based validation for Transfer-Encoding values: only accept 'chunked' in isolation, reject headers with extraneous characters
- Validate that Transfer-Encoding header conforms to proper syntax (no padding, exact casing handling)
- Implement request smuggling detection: alert on conflicting Content-Length and Transfer-Encoding headers
- Normalize and validate all HTTP headers before processing request bodies
- Add security tests specifically for malformed Transfer-Encoding values (prefixed/suffixed text)
- Consider using a vetted HTTP parsing library rather than custom regex-based validation

## Variant hunting
Test other headers with substring matching vulnerabilities: Content-Encoding, Accept-Encoding
Search for similar regex patterns in form /keyword/io without anchors (^$) or proper validation
Check for case-insensitive matching vulnerabilities in other protocol headers
Probe Transfer-Encoding variations: 'chunked ' (trailing space), ' chunked', 'Chunked', 'CHUNKED'
Investigate if other methods also use loose regex for parsing critical headers

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1036: Masquerading
- T1040: Traffic Redirection

## Notes
This is a classic request smuggling vulnerability stemming from insufficient input validation. The fix requires replacing the regex case statement with strict validation against RFC specifications. WEBrick should normalize and reject any Transfer-Encoding value that doesn't exactly match 'chunked' (case-insensitive per RFC). The vulnerability is particularly dangerous in architectures where WEBrick sits behind reverse proxies, as desynchronization can lead to cache poisoning or request routing attacks.

## Full report
<details><summary>Expand</summary>

function read_body in file /lib/webrick/httprequest.rb use  expression ```/chunked/io``` to decide ```transfer-encoding``` whether or not.
that is not rigorous. When using webrick as a http server, a attacker may use  a ```Transfer-Encoding: AAAchunkedBBB``` header to fake a legal header. than can make a HTTP Request Smuggling attack.
```
def read_body(socket, block)
      return unless socket
      if tc = self['transfer-encoding']
        case tc
        when /chunked/io then read_chunked(socket, block)
        else raise HTTPStatus::NotImplemented, "Transfer-Encoding: #{tc}."
        end
      elsif self['content-length'] || @remaining_size
        @remaining_size ||= self['content-length'].to_i
        while @remaining_size > 0
          sz = [@buffer_size, @remaining_size].min
          break unless buf = read_data(socket, sz)
          @remaining_size -= buf.bytesize
          block.call(buf)
        end
        if @remaining_size > 0 && @socket.eof?
          raise HTTPStatus::BadRequest, "invalid body size."
        end
      elsif BODY_CONTAINABLE_METHODS.member?(@request_method)
        raise HTTPStatus::LengthRequired
      end
      return @body
    end
```

## Impact

It is possible to smuggle the request and disrupt the user experience.

</details>

---
*Analysed by Claude on 2026-05-24*
