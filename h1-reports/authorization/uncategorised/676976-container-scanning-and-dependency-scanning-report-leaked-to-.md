# Container and Dependency Scanning Reports Leaked to Unauthorized Users via Merge Request Widget

## Metadata
- **Source:** HackerOne
- **Report:** 676976 | https://hackerone.com/reports/676976
- **Submitted:** 2019-08-19
- **Reporter:** xanbanx
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Information Disclosure, Insufficient Permission Validation
- **CVEs:** CVE-2019-15591, CVE-2017-18269, CVE-2017-16997, CVE-2018-1000001, CVE-2016-10228, CVE-2018-18520, CVE-2010-4052, CVE-2018-16869, CVE-2018-18311, CVE-2014-3488, CVE-2017-12794, CVE-2018-1000201
- **Category:** uncategorised

## Summary
GitLab's container scanning and dependency scanning reports were accessible to unauthorized users via merge request widgets despite CI pipeline access being restricted to project members only. The vulnerability allowed public project visitors to view sensitive vulnerability information (CVEs, severity levels, affected packages) that should only be visible to users with CI access permissions. This affected public projects with premium/gold features when CI pipelines were disabled for non-members.

## Attack scenario
1. Attacker creates or identifies a public GitLab project with restricted CI pipeline access (public pipelines disabled)
2. Project maintainers push code with container and dependency scanning jobs that generate vulnerability reports
3. Attacker visits the merge request page without project membership or CI access permissions
4. Merge request widget renders scanning report JSON endpoint regardless of access restrictions
5. Attacker obtains detailed vulnerability data including CVE identifiers, affected packages, severity levels, and remediation information
6. Attacker uses this information to identify exploitable vulnerabilities in the project's dependencies for targeted attacks

## Root cause
GitLab failed to enforce proper authorization checks on the container scanning and dependency scanning report endpoints. The merge request widget rendered these reports based on merge request access rather than CI pipeline access permissions. The permission model did not account for the distinction between accessing merge request data and accessing CI job artifacts/reports.

## Attacker mindset
An attacker seeking reconnaissance on public projects would appreciate this leak as it provides detailed vulnerability intelligence without authentication. For projects using premium features, this is competitive intelligence about security posture. Attackers could identify targets with known unpatched vulnerabilities, or map dependency versions across projects to find supply chain attack vectors.

## Defensive takeaways
- Always validate that accessing CI artifacts/reports requires appropriate CI pipeline viewing permissions, not just merge request access
- Separate permission models for different resource types (MR vs CI vs artifacts) must be explicitly enforced at the API/endpoint level
- Security scanning reports contain sensitive vulnerability data and should have stricter access controls than general merge request information
- Implement permission checks at multiple layers: endpoint, serialization, and response filtering
- For public projects, respect the intention of 'public pipelines disabled' by excluding all CI-derived data from public views
- Audit all API endpoints that expose CI-related data to ensure consistent permission enforcement
- Test access control with multiple permission levels: no access, merge request access only, CI access, and admin access

## Variant hunting
Check other CI/CD artifact endpoints (test reports, coverage reports, performance data) for similar permission bypasses
Review whether other premium features with sensitive outputs (SAST, DAST reports) have proper access controls
Test if CI pipeline environment variables or secrets are exposed in similar contexts
Verify job logs, artifacts, and other CI outputs respect the same pipeline visibility restrictions
Check if the vulnerability occurs in self-hosted GitLab instances or only on gitlab.com
Test whether the JSON endpoint can be accessed directly without rendering the widget

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1589
- T1592

## Notes
This is a classic authorization bypass vulnerability where different permission contexts (merge request visibility vs CI access) were not properly separated. The report demonstrates good reproduction steps with a complete proof-of-concept. The vulnerability is particularly severe because it affects premium features (container/dependency scanning) that organizations purchase specifically for security scanning, only to have results leaked to the public. The attacker requires only read access to the public project, making it trivially exploitable at scale.

## Full report
<details><summary>Expand</summary>

Hi GitLab Security team

### Summary

GitLab makes the container scanning and dependency scanning information available as part of a JSON endpoint for merge requests. These reports are output of the CI job and should only be displayed if the visiting user has access to CI. However, right now GitLab displays the the container scanning and dependency scanning reports regardless of this permission, making it available to whoever has access to the merge request.

For public projects, GitLab allows to restrict CI pipelines to project members only (public pipelines disabled). However, in this case, the merge request widget still renders the scanning reports result, which is the outcome of a CI pipeline.

### Steps to reproduce

This is reproducible on gitlab.com. It requires at least a gold plan to have the container scanning and dependency scanning feature available.

1. Create a public project, restrict CI pipeline access to project members, and disable public pipelines
2. Push a  new branch and add .gitlab-ci.yml file with the following content:

```yml
test:
  script: |
    echo '{"image": "registry.gitlab.com/groulot/container-scanning-test/master:5f21de6956aee99ddb68ae49498662d9872f50ff","unapproved": ["CVE-2017-18269","CVE-2017-16997","CVE-2018-1000001","CVE-2016-10228","CVE-2018-18520","CVE-2010-4052","CVE-2018-16869","CVE-2018-18311"],"vulnerabilities": [{ "featurename": "glibc", "featureversion": "2.24-11+deb9u3", "vulnerability": "CVE-2017-18269", "namespace": "debian:9", "description": "SSE2-optimized memmove implementation problem.", "link": "https://security-tracker.debian.org/tracker/CVE-2017-18269", "severity": "Defcon1", "fixedby": "2.24-11+deb9u4"},{ "featurename": "glibc", "featureversion": "2.24-11+deb9u3", "vulnerability": "CVE-2017-16997", "namespace": "debian:9", "description": "elf/dl-load.c in the GNU C Library (aka glibc or libc6) 2.19 through 2.26 mishandles RPATH and RUNPATH containing $ORIGIN for a privileged (setuid or AT_SECURE) program, which allows local users to gain privileges via a Trojan horse library in the current working directory, related to the fillin_rpath and decompose_rpath functions. This is associated with misinterpretion of an empty RPATH/RUNPATH token as the \"./\" directory. NOTE: this configuration of RPATH/RUNPATH for a privileged program is apparently very uncommon; most likely, no such program is shipped with any common Linux distribution.", "link": "https://security-tracker.debian.org/tracker/CVE-2017-16997", "severity": "Critical", "fixedby": ""},{ "featurename": "glibc", "featureversion": "2.24-11+deb9u3", "vulnerability": "CVE-2018-1000001", "namespace": "debian:9", "description": "In glibc 2.26 and earlier there is confusion in the usage of getcwd() by realpath() which can be used to write before the destination buffer leading to a buffer underflow and potential code execution.", "link": "https://security-tracker.debian.org/tracker/CVE-2018-1000001", "severity": "High", "fixedby": ""},{ "featurename": "glibc", "featureversion": "2.24-11+deb9u3", "vulnerability": "CVE-2016-10228", "namespace": "debian:9", "description": "The iconv program in the GNU C Library (aka glibc or libc6) 2.25 and earlier, when invoked with the -c option, enters an infinite loop when processing invalid multi-byte input sequences, leading to a denial of service.", "link": "https://security-tracker.debian.org/tracker/CVE-2016-10228", "severity": "Medium", "fixedby": ""},{ "featurename": "elfutils", "featureversion": "0.168-1", "vulnerability": "CVE-2018-18520", "namespace": "debian:9", "description": "An Invalid Memory Address Dereference exists in the function elf_end in libelf in elfutils through v0.174. Although eu-size is intended to support ar files inside ar files, handle_ar in size.c closes the outer ar file before handling all inner entries. The vulnerability allows attackers to cause a denial of service (application crash) with a crafted ELF file.", "link": "https://security-tracker.debian.org/tracker/CVE-2018-18520", "severity": "Low", "fixedby": ""},{ "featurename": "glibc", "featureversion": "2.24-11+deb9u3", "vulnerability": "CVE-2010-4052", "namespace": "debian:9", "description": "Stack consumption vulnerability in the regcomp implementation in the GNU C Library (aka glibc or libc6) through 2.11.3, and 2.12.x through 2.12.2, allows context-dependent attackers to cause a denial of service (resource exhaustion) via a regular expression containing adjacent repetition operators, as demonstrated by a {10,}{10,}{10,}{10,} sequence in the proftpd.gnu.c exploit for ProFTPD.", "link": "https://security-tracker.debian.org/tracker/CVE-2010-4052", "severity": "Negligible", "fixedby": ""},{ "featurename": "nettle", "featureversion": "3.3-1", "vulnerability": "CVE-2018-16869", "namespace": "debian:9", "description": "A Bleichenbacher type side-channel based padding oracle attack was found in the way nettle handles endian conversion of RSA decrypted PKCS#1 v1.5 data. An attacker who is able to run a process on the same physical core as the victim process, could use this flaw extract plaintext or in some cases downgrade any TLS connections to a vulnerable server.", "link": "https://security-tracker.debian.org/tracker/CVE-2018-16869", "severity": "Unknown", "fixedby": ""},{ "featurename": "perl", "featureversion": "5.24.1-3+deb9u4", "vulnerability": "CVE-2018-18311", "namespace": "debian:9", "description": "Perl before 5.26.3 and 5.28.x before 5.28.1 has a buffer overflow via a crafted regular expression that triggers invalid write operations.", "link": "https://security-tracker.debian.org/tracker/CVE-2018-18311", "severity": "Unknown", "fixedby": "5.24.1-3+deb9u5"},{ "featurename": "foo", "featureversion": "1.3", "vulnerability": "CVE-2018-666", "namespace": "debian:9", "description": "Foo has a vulnerability nobody cares about and whitelist.", "link": "https://security-tracker.debian.org/tracker/CVE-2018-666", "severity": "Unknown", "fixedby": "1.4"}]}' > gl-container-scanning-report.json
    echo '{"version": "1.3","vulnerabilities": [{"category": "dependency_scanning","name": "io.netty/netty - CVE-2014-3488","message": "DoS by CPU exhaustion when using malicious SSL packets","cve": "app/pom.xml:io.netty/netty@3.9.1.Final:CVE-2014-3488","severity": "Unknown","solution": "Upgrade to the latest version","scanner": {"id": "gemnasium","name": "Gemnasium"},"location": {"file": "app/pom.xml","dependency": {"package": {"name": "io.netty/netty"},"version": "3.9.1.Final"}},"identifiers": [{"type": "gemnasium","name": "Gemnasium-d1bf36d9-9f07-46cd-9cfc-8675338ada8f","value": "d1bf36d9-9f07-46cd-9cfc-8675338ada8f","url": "https://deps.sec.gitlab.com/packages/maven/io.netty/netty/versions/3.9.1.Final/advisories"},{"type": "cve","name": "CVE-2014-3488","value": "CVE-2014-3488","url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-3488"}],"links": [{"url": "https://bugzilla.redhat.com/CVE-2014-3488"},{"url": "http://netty.io/news/2014/06/11/3.html"},{"url": "https://github.com/netty/netty/issues/2562"}],"priority": "Unknown","file": "app/pom.xml","url": "https://bugzilla.redhat.com/CVE-2014-3488","tool": "gemnasium"},{"category": "dependency_scanning","name": "Django - CVE-2017-12794","message": "Possible XSS in traceback section of technical 500 debug page","cve": "app/requirements.txt:Django@1.11.3:CVE-2017-12794","severity": "Unknown","solution": "Upgrade to latest version or apply patch.","scanner": {"id": "gemnasium","name": "Gemnasium"},"location": {"file": "app/requirements.txt","dependency": {"package": {"name": "Django"},"version": "1.11.3"}},"identifiers": [{"type": "gemnasium","name": "Gemnasium-6162a015-8635-4a15-8d7c-dc9321db366f","value": "6162a015-8635-4a15-8d7c-dc9321db366f","url": "https://deps.sec.gitlab.com/packages/pypi/Django/versions/1.11.3/advisories"},{"type": "cve","name": "CVE-2017-12794","value": "CVE-2017-12794","url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-12794"}],"links": [{"url":

</details>

---
*Analysed by Claude on 2026-05-24*
