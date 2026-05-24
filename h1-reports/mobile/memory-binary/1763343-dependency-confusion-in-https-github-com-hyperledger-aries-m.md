# Dependency Confusion in Hyperledger Aries Mobile Agent React Native

## Metadata
- **Source:** HackerOne
- **Report:** 1763343 | https://hackerone.com/reports/1763343
- **Submitted:** 2022-11-05
- **Reporter:** r3drush
- **Program:** Hyperledger
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Dependency Confusion, Supply Chain Attack, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Hyperledger Aries Mobile Agent React Native application depends on an internal package 'aries-bifold' that is not published to the public npm registry. An attacker could register a malicious package with the same name on npm and achieve remote code execution on all systems installing the agent. This is a classic dependency confusion vulnerability exploiting the npm package resolution order.

## Attack scenario
1. Attacker identifies that aries-mobile-agent-react-native depends on 'aries-bifold' package via package.json analysis
2. Attacker verifies that 'aries-bifold' is not published on public npm registry but only exists in private/internal repositories
3. Attacker registers and publishes a malicious package named 'aries-bifold' on public npm with a higher version number
4. When a developer or CI/CD pipeline installs aries-mobile-agent-react-native, npm resolves 'aries-bifold' to the malicious public package instead of the intended private one
5. The malicious package executes arbitrary code during npm install phase (via install scripts or postinstall hooks)
6. Attacker gains remote code execution on the target system with the privileges of the installing user

## Root cause
The package.json references an internal/private dependency 'aries-bifold' without proper namespace protection or private registry configuration. The npm package resolution algorithm prioritizes public registry packages, and no mechanisms (such as npm scoping, .npmrc configuration, or package-lock.json pinning) prevent installation of a malicious public package with the same name.

## Attacker mindset
An attacker seeking supply chain compromise would recognize that widely-used open-source projects often have undeclared private dependencies. By finding packages referenced in package.json but absent from public registries, the attacker can perform a low-effort, high-impact attack targeting all downstream consumers without needing to compromise the original project's infrastructure.

## Defensive takeaways
- Use npm namespace scoping (@organization/package-name) for all internal/private dependencies to prevent name collisions
- Configure .npmrc with 'scope:registry' settings to route scoped packages to private registries
- Commit package-lock.json and yarn.lock files to version control to lock exact dependency versions and prevent resolution to unintended packages
- Audit package.json for any dependencies not present in public registries and ensure they are properly configured for private/internal resolution
- Implement dependency verification in CI/CD pipelines (e.g., npm audit, SBOM generation, signature verification)
- Use private npm registry proxies or mirrors that can detect and block dependency confusion attempts
- Monitor npm registry for malicious packages matching internal dependency names

## Variant hunting
Similar patterns exist in any project using unpublished internal packages without proper namespace protection. Search package.json files in large organizations for package references that don't appear in public npm registry. Look for projects using monorepos without scoping. Check for organizations that publish some packages publicly but reference others privately without scoped names.

## MITRE ATT&CK
- T1195.001
- T1199
- T1566.004
- T1592

## Notes
The researcher responsibly limited their proof-of-concept by not actually uploading the malicious package, demonstrating good faith. This vulnerability is particularly dangerous because it affects the software supply chain at the point of installation, affecting all downstream users automatically. The fix is straightforward but requires coordination across development and package management processes.

## Full report
<details><summary>Expand</summary>

Hi,
I found dependency confusion vulnerability in your aries mobile agent. 

The agent is installed through npm which then download thepublic packages required by the application. Those dependencies are defined through the package.json file. I found that your agent depends on the package "aries-bifold" that is not currently present in the public repository; an attacker could upload its malicious package and then gain remote code execution on every target installing the agent.
I limited my research on finding the missing package without uploading the "malicious" package on npm because https://github.com/hyperledger/aries-mobile-agent-react-native is not in scope (but is not out-of-scope either), but the methods to exploit this vulnerability are well documented here:
1) https://dhiyaneshgeek.github.io/web/security/2021/09/04/dependency-confusion/

More about this vulnerability from the researcher who discovered it:
2) https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610

Cheers,
r3drush

## Impact

Remote code execution to clients installing the agent

</details>

---
*Analysed by Claude on 2026-05-24*
