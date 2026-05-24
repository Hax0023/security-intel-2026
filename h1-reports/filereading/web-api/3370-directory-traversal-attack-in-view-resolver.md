# Directory Traversal in Rails View Resolver via Wildcard URL Segments

## Metadata
- **Source:** HackerOne
- **Report:** 3370 | https://hackerone.com/reports/3370
- **Submitted:** 2014-03-06
- **Reporter:** lautis
- **Program:** Rails
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Directory Traversal, Path Traversal, Improper Input Validation
- **CVEs:** CVE-2014-0130
- **Category:** web-api

## Summary
Rails view resolver allows directory traversal attacks through wildcard URL segments, enabling attackers to read arbitrary files from the application root. The vulnerability can be exploited using both forward slashes and backslash-encoded paths, bypassing existing protection mechanisms like Rack::Protection::PathTraversal.

## Attack scenario
1. Attacker discovers a route with wildcard segment (e.g., GET /help/(*action))
2. Attacker crafts request with path traversal payload: GET /help/../../../Gemfile
3. ActionView::FileSystemResolver resolves the path using Dir.glob without proper validation
4. Sensitive file (Gemfile, database.yml, etc.) is rendered as view template
5. Attacker enhances attack by bypassing Rack::Protection using backslash encoding: GET /help/%5c../%5c../%5c../Gemfile
6. Backslashes are unescaped by resolver, allowing traversal outside view path boundaries

## Root cause
ActionView::FileSystemResolver uses Dir.glob to match view files without properly sanitizing wildcard segments for directory traversal sequences. The resolver fails to validate that resolved paths remain within intended view directories, and Rack::Protection::PathTraversal middleware (not enabled by default) uses a regex pattern that backslashes can bypass.

## Attacker mindset
An attacker would recognize that wildcard route segments represent a control flow where user input directly influences file path resolution. They would test standard traversal patterns, then progress to encoding bypasses when basic protections are detected. The goal is information disclosure of sensitive configuration files containing credentials, API keys, and source code.

## Defensive takeaways
- Enable Rack::Protection::PathTraversal middleware by default in Rails applications
- Implement strict path normalization in view resolver before glob matching (resolve symlinks, normalize separators)
- Use whitelist-based validation: verify resolved view paths are within expected view directories using realpath comparison
- Avoid using wildcard route segments; prefer explicit route definitions
- Sanitize action parameters by rejecting any containing path separators or traversal sequences
- Use File::FNM_NOESCAPE flag cautiously; prefer dedicated path validation libraries
- Apply defense-in-depth: combine path normalization, whitelisting, and middleware protection

## Variant hunting
Test other wildcard route patterns (catch-all routes with multiple segments)
Investigate Unicode normalization bypasses (NFD/NFC) for path validation
Check if symbolic link following allows escaping view paths
Test encoded variations: %2e%2e%2f, double-encoding, null bytes
Examine other file resolvers (CSS, JavaScript asset pipelines) for similar issues
Test Windows UNC paths (\\server\share) on cross-platform deployments
Analyze ERB template rendering for code execution post-traversal

## MITRE ATT&CK
- T1190
- T1083
- T1555

## Notes
This is a classic path traversal vulnerability in template engines. The bypass using backslashes is particularly noteworthy as it exploits the difference between regex-based middleware validation and glob's path semantics. The vulnerability is particularly dangerous in Rails because view files often contain sensitive information and can potentially execute Ruby code if ERB templates are rendered. The fact that wildcard routes render views even without corresponding action methods defined indicates overly permissive default behavior.

## Full report
<details><summary>Expand</summary>

There seems to be two cases that allow directory traversal when using wildcard URL segments that allow rendering view outside view paths.

For example, let say there is a route

	get '/help/(*action)’, controller: ‘help’

and a matching controller

	class HelpController < ApplicationController
	end

This renders all views that are in 'app/views/help’ (assuming default view paths) even when matching action method is not defined.

If an attacker made a request `GET /help/../../../Gemfile`, ActionView::FileSystemResolver returns Gemfile from project root as the matching view. This simple case can be prevented using Rack::Protection::PathTraversal middleware, but it is not enabled by default in Rails. Also, there could be other mechanisms that may result in rendering views that are outside view path. Not sure if that’s the expected behaviour, but this surprised me.

However, Rack::Protection::PathTraversal can be bypassed using backslashes: `GET /help/%5c../%5c../%5c../Gemfile`. The resolver uses Dir.glob, which escapes backslashes unless File::FNM_NOESCAPE flag is used. Rack::Protection::PathTraversal won’t intercept `'\../'` and the resolver treats `'\../`' as `'../'`.

Attached are fixes for the mentioned vulnerabilities with test cases.

</details>

---
*Analysed by Claude on 2026-05-24*
