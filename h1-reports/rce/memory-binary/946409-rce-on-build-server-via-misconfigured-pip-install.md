# RCE on Yelp Build Server via Typosquatting Unclaimed PyPI Package

## Metadata
- **Source:** HackerOne
- **Report:** 946409 | https://hackerone.com/reports/946409
- **Submitted:** 2020-07-29
- **Reporter:** alexbirsan
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Dependency Confusion, Typosquatting, Arbitrary Code Execution, Supply Chain Attack, Misconfigured Package Manager
- **CVEs:** None
- **Category:** memory-binary

## Summary
A misconfiguration in Yelp's build infrastructure caused the system to fetch the internal package 'yelp-cgeom' from the public PyPI registry instead of an internal registry. The researcher claimed the unclaimed package name on PyPI and demonstrated arbitrary code execution on a Yelp build server (Jenkins) via malicious setup.py during package installation.

## Attack scenario
1. Attacker identifies internal Yelp package name 'yelp-cgeom' through public information disclosure or reconnaissance
2. Attacker verifies the package is unclaimed on the public PyPI registry
3. Attacker uploads malicious Python package with same name to PyPI containing backdoored setup.py script
4. Yelp build server attempts to install 'yelp-cgeom' due to misconfigured package manager settings
5. Misconfiguration causes system to resolve dependency to public PyPI instead of internal registry
6. setup.py executes automatically during pip install, granting attacker code execution as Jenkins user on build server

## Root cause
Build infrastructure misconfiguration directing pip to resolve packages from public PyPI registry instead of internal registry, combined with use of internal package names that were unclaimed on public PyPI, enabling dependency confusion attacks.

## Attacker mindset
Supply chain attacker targeting development/build infrastructure. Methodology demonstrates careful reconnaissance, responsible vulnerability disclosure, and focus on high-impact targets. Attacker assumes internal packages may be unclaimed publicly and uses proof-of-concept to validate vulnerability rather than launching destructive attack.

## Defensive takeaways
- Implement explicit package index configuration (e.g., .pypirc, pip.conf, requirements.txt with index URLs) to prevent public registry fallback
- Use private package registry with authentication and require internal packages to be explicitly registered/reserved
- Implement network-level controls to restrict outbound connections to approved registries only
- Monitor and audit all pip/package manager installations, especially during CI/CD pipeline execution
- Pre-claim or reserve all internal package names on public registries to prevent typosquatting
- Implement package signature verification and checksum validation
- Use dependency lock files with pinned versions and hashes
- Implement least-privilege access for CI/CD service accounts and build servers
- Regular security audits of dependency resolution configurations across all build infrastructure

## Variant hunting
Similar misconfigurations likely present in other organizations using private package registries. Search for: (1) npm/Node.js packages with similar dependency confusion in npm public registry, (2) Maven/Java packages on Maven Central, (3) Ruby gems on rubygems.org, (4) Go modules on pkg.go.dev, (5) NuGet packages, (6) PyPI packages from other enterprises. Organizations with monorepos or internal naming conventions are high-risk targets.

## MITRE ATT&CK
- T1195.001 - Supply Chain Compromise: Compromise Software Dependencies
- T1195.003 - Supply Chain Compromise: Compromise Software Supply Chain
- T1566 - Phishing: General phishing techniques applied to package management
- T1190 - Exploit Public-Facing Application (build server exposure)
- T1072 - Software Deployment Tools (abuse of pip/package manager)

## Notes
This is a well-executed, responsible disclosure of a critical supply chain vulnerability. The researcher demonstrated genuine RCE capability without causing harm, adhering to HackerOne program policies. The vulnerability class (dependency confusion) became widely recognized after similar findings in major tech companies. The misconfiguration suggests inadequate environment separation between internal and public package infrastructure. Jenkins installation with internet access to public registries is a significant risk factor in this scenario.

## Full report
<details><summary>Expand</summary>

The following Python library has been installed on at least one Yelp owned build server directly from the public PyPI registry.

* https://pypi.org/project/yelp-cgeom/

This package should normally be downloaded from the internal Yelp registry, but a misconfiguration appears to have caused it to be downloaded from `pypi.org` instead.

This package name was previously unclaimed on PyPI. In order to detect such misconfigurations, I have uploaded my own code under the `yelp-cgeom` name.

Whenever `yelp-cgeom` is installed, my `setup.py` script is executed on the machine where it is downloaded. The script sends a callback to my server containing:

* the originating IP
* the machine's hostname
* the current working directory

To avoid breaching the program policy, no further actions are taken.

# Vulnerable machine

At `Wed jul 29 2020 04:27:23 GMT`, and again 20 seconds later, I have received the following callback:

* originating IP: `54.71.19.248`
* hostname: `10-81-21-60-uswest2bdevc.uswest2-devc.yelpcorp.com`
* home directory: `/nail/home/jenkins`
* directory: `/ephemeral/tmpdir/pip-install-o6jnSv/yelp-cgeom`

This indicates that my preinstall script was executed on the server above.

## Impact

If this package had been claimed by an attacker, this would have led to arbitrary code execution on the affected server, as well as allowing the attacker to add backdoors inside the affected project(s) during the build process.

</details>

---
*Analysed by Claude on 2026-05-11*
