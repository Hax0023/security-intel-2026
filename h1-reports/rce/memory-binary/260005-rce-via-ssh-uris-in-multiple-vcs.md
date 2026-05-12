# Remote Code Execution via ssh:// URIs in Git, Mercurial, and Subversion

## Metadata
- **Source:** HackerOne
- **Report:** 260005 | https://hackerone.com/reports/260005
- **Submitted:** 2017-08-14
- **Reporter:** joernchen
- **Program:** Multiple VCS projects (Git, Mercurial, Subversion)
- **Bounty:** Donated to charity (brain aneurysm research)
- **Severity:** high
- **Vuln:** Remote Code Execution, Command Injection, Unsafe URI Handling, Improper Input Validation
- **CVEs:** CVE-2017-9800, CVE-2017-1000116, CVE-2017-1000117
- **Category:** memory-binary

## Summary
Multiple version control systems (Git, Mercurial, Subversion) improperly handle ssh:// URIs, allowing attackers to execute arbitrary commands during repository operations. The vulnerability stems from insufficient sanitization of SSH URIs passed to shell interpreters. An attacker can craft malicious repository URIs that inject shell commands executed with user privileges.

## Attack scenario
1. Attacker creates a Git/Hg/SVN repository with a specially crafted ssh:// URI containing shell metacharacters and command injection payload
2. Victim clones or checks out the malicious repository using git clone, hg clone, or svn checkout
3. The VCS client parses the ssh:// URI without proper sanitization
4. Shell metacharacters in the URI are passed unsanitized to an SSH command execution context
5. Injected shell commands execute with the victim user's privileges during the clone/checkout operation
6. Attacker achieves code execution on the victim's system

## Root cause
Version control systems failed to properly sanitize and escape SSH URIs before passing them to shell execution contexts. The applications constructed SSH commands by concatenating URI components without adequate escaping, allowing shell metacharacters and command separators to break out of intended command boundaries.

## Attacker mindset
Supply chain attack vector targeting developers. An attacker could compromise legitimate-looking repository URIs or social engineer developers into cloning malicious repositories. The attack requires user interaction (clone/checkout) but executes automatically during normal VCS workflows with no additional prompting.

## Defensive takeaways
- Never pass unsanitized user input or URI components to shell execution contexts
- Use parameterized/array-based command execution instead of string concatenation for system calls
- Implement strict URI validation and sanitization for protocol handlers (ssh, git, svn)
- Use library functions designed for URL parsing that handle escaping automatically
- Apply principle of least privilege - VCS operations should not require shell access
- Implement allowlisting for valid URI schemes and components
- Conduct security review of all code handling remote repository URIs
- Use static analysis tools to detect shell injection vulnerabilities

## Variant hunting
Search for similar issues in: Bazaar, Fossil, Perforce, Mercurial extensions, Git hosting platforms, IDE VCS integrations (VSCode, JetBrains, Visual Studio), and other tools that handle repository URIs. Look for improper handling of file://, svn+ssh://, git+ssh://, and custom protocol URIs.

## MITRE ATT&CK
- T1190
- T1059
- T1021
- T1570
- T1566

## Notes
This is a coordinated disclosure affecting three major VCS platforms simultaneously. The vulnerability required user interaction but occurred during automatic repository operations. The consistent presence across different VCS implementations suggests a shared misunderstanding about safe URI handling practices. CVE references: CVE-2017-9800, CVE-2017-1000116, CVE-2017-1000117. The CVSS score varies between sources (6.3-7.5 range depending on interpretation of attack complexity and user interaction requirements).

## Full report
<details><summary>Expand</summary>

I'd like to submit an RCE issue within Git SVN and Mercurial, the CVEs are:

*  CVE-2017-9800 (Subversion)
* CVE-2017-1000116 (Mercurial (hg))
* CVE-2017-1000117 (Git)

Further Info can be found at:

http://blog.recurity-labs.com/2017-08-10/scm-vulns

And product specific:

* https://public-inbox.org/git/xmqqh8xf482j.fsf@gitster.mtv.corp.google.com/T/#u
* http://subversion.apache.org/security/CVE-2017-9800-advisory.txt
* https://about.gitlab.com/2017/08/10/gitlab-9-dot-4-dot-4-released/

I think these issues which all are based on the same flaw could be worth
an IBB Bounty. However I'd like to point out that we at Recurity Labs
would like the bounty being donated to a charity. The to be determined
charity will be something in the field of brain aneurysm, this is due to
the fact that Felix, the founder of Recurity Labs, currently is
recovering from a brain aneurysm.


So, just let us know what you think about this.

Cheers,

joern

P.S. I took the CVSS Score from the Subversion Advisory
the Redhat advisory states a score of 6.3 (CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:L) I guess the truth is somewhere in between.

</details>

---
*Analysed by Claude on 2026-05-12*
