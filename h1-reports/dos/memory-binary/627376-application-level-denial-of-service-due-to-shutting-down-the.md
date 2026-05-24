# Application Level Denial of Service via Path Traversal Bypass in http-live-simulator

## Metadata
- **Source:** HackerOne
- **Report:** 627376 | https://hackerone.com/reports/627376
- **Submitted:** 2019-06-24
- **Reporter:** 3la2kb
- **Program:** http-live-simulator (npm package v1.0.7)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Path Traversal, Input Validation Flaw, Improper Error Handling
- **CVEs:** None
- **Category:** memory-binary

## Summary
The http-live-simulator module crashes when processing crafted URLs containing path traversal sequences that result in an empty pathname after sanitization. The vulnerable code attempts to read an empty pathname as a file, causing undefined data to be written to the response, triggering a server crash.

## Attack scenario
1. Attacker identifies the http-live-simulator module running on localhost:8080
2. Attacker crafts malicious URL with path traversal: curl --path-as-is http://localhost:8080/../?a
3. URL parser extracts pathname component, which initially contains /../
4. Sanitization loop removes /../ sequences, leaving pathname as empty string
5. Empty pathname bypasses the default file routing logic that would normally handle /
6. Application attempts fs.readFile() on project directory instead of a file, returning undefined
7. Calling res.write(undefined) causes type error and server crash

## Root cause
The path traversal fix introduced in the previous patch uses simple string replacement (pathname.replace('/../','')) which reduces /../ to empty string. The code then fails to handle the edge case where pathname becomes empty, and doesn't validate that abspath points to a file before attempting to read it. Additionally, no error handling exists for fs.readFile() operations.

## Attacker mindset
An attacker seeks to disrupt service availability. Upon discovering the module, they notice it has path traversal protections but recognize the sanitization is incomplete. By crafting a minimal payload that reduces the pathname to empty, they can reliably crash the server with a single request, achieving denial of service with minimal effort.

## Defensive takeaways
- Never rely solely on string replacement for path sanitization; use proper path resolution functions like path.normalize() and path.resolve()
- Validate that sanitized paths are non-empty before processing
- Always verify file existence and type (file vs directory) before attempting file operations
- Implement comprehensive error handling around I/O operations to prevent unhandled exceptions from crashing the process
- Add input validation to reject requests with suspicious path patterns before processing
- Use allowlists for accessible paths rather than blacklist-based filtering
- Test edge cases including empty strings, null values, and boundary conditions when implementing security fixes

## Variant hunting
Test other path traversal patterns: /.../?a, /./?a, ///..///?a to find additional bypass methods
Try exploiting similar empty pathname conditions in other URL parsing scenarios (POST requests, different query string formats)
Look for other npm packages using similar pathname sanitization patterns and test for identical vulnerabilities
Test if pathname can be set to null or other falsy values that might bypass existence checks
Attempt double encoding or other encoding bypasses: /%2e%2e%2f
Test with very long path sequences to see if replacement logic creates unexpected results

## MITRE ATT&CK
- T1190
- T1499.4

## Notes
This vulnerability demonstrates the danger of patching security issues with incomplete fixes. The original report (411405) was patched but the fix created a new attack surface. The application lacks proper error handling - res.write(undefined) should be caught and handled gracefully. The root issue stems from improper input validation on URL pathname combined with insufficient error handling in file read operations.

## Full report
<details><summary>Expand</summary>

## Module
**module name:** http-live-simulator
**version:** 1.0.7
**npm page:** https://www.npmjs.com/package/http-live-simulator

## Description
I've found a way to crash the server due to the way it parses URL 

## Steps To Reproduce:
1- Install the module : `npm install -g http-live-simulator`
2- Run the server : `http-live`
3- Attempt to crash the server by this command `curl --path-as-is http://localhost:8080/../?a`

## Explanation :
the reason for this issue is the fix for my previous [report](https://hackerone.com/reports/411405)
which is :
```javascript
	var pathname = url.parse(req.url, true).pathname;
	while(pathname.indexOf("/../") != -1) {
		pathname = pathname.replace("/../",""); //fix for path traversal bug
	}
```
so now if we pass ` http://localhost:8080/../?a` as the url the `pathname` becomes empty
which will cause skipping this condition :
```javascript
		if (pathname == "/") {
			for(var i=0;i<defaults.length;i++) {
				if (fs.existsSync(process.cwd() + '/' + defaults[i])) {
					pathname = '/' + defaults[i];
					break;
				}
			}
			if (pathname == '/') {
				return404(res, pathname);
				console.log(pathname);
				return;
			}
		}
```
with this in mind now we can proceed to the buggy snippet :
```javascript
		abspath = process.cwd() + pathname;
		console.log('REQUEST: ', req.method, pathname);

		if (fs.existsSync(abspath)) {
			console.log("in condition");
			fs.readFile(abspath, function(err, data) {
				console.log("in condition1");
				var ext = pathname.slice(pathname.indexOf("."));
				var mtype = getMimeType(ext);
				res.writeHead(200, {'Content-Type': mtype});
				console.log(abspath, data);
				res.write(data);
				res.end();
			});
		}
``` 
here `abspath` becomes `<project_dir>` which cannot be read by `readFile` because it's a directory not a file causing the value of `data` to be `undefined` which will cause an error when trying to `res.write(data);` as `res.write()` function expects its parameter to be a string or buffer but it's `undefined` in this case.

## Fix :
append a `/` to `pathname` if it becomes empty after sanitizing

## Impact

Denial of service due to shutting down the server

</details>

---
*Analysed by Claude on 2026-05-24*
