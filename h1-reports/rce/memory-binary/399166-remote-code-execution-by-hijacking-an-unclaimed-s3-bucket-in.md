# Remote Code Execution via Hijacked Unclaimed S3 Bucket in Rocket.Chat Installation Script

## Metadata
- **Source:** HackerOne
- **Report:** 399166 | https://hackerone.com/reports/399166
- **Submitted:** 2018-08-24
- **Reporter:** edoverflow
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Arbitrary Code Execution, Supply Chain Attack, Insecure Direct Object References, Resource Hijacking
- **CVEs:** None
- **Category:** memory-binary

## Summary
Rocket.Chat's install.sh script downloads a tarball from an unclaimed S3 bucket (s3://rocketchatbuild/) without any integrity verification. An attacker can register the unclaimed bucket and serve malicious code that gets automatically executed during installation. This represents a critical supply chain vulnerability affecting all users running the installation script.

## Attack scenario
1. Attacker discovers the install.sh script references https://s3.amazonaws.com/rocketchatbuild/rocket.chat-develop.tgz
2. Attacker verifies the S3 bucket does not exist (NoSuchBucket error) and is unclaimed
3. Attacker creates an AWS S3 bucket with the same name (rocketchatbuild)
4. Attacker uploads a malicious rocket.chat-develop.tgz file containing arbitrary code
5. When a user runs install.sh, curl downloads the attacker's malicious tarball
6. The tar command extracts the malicious archive and code executes with user privileges

## Root cause
The installation script downloads executable code from an external source without: (1) verifying bucket ownership/authenticity, (2) validating file integrity via cryptographic signatures or checksums, (3) using a reserved/protected S3 bucket name, or (4) implementing DNS-based bucket locking mechanisms.

## Attacker mindset
An attacker recognizes that installation scripts are inherently trusted by users and that S3 bucket names are globally unique but not reserved until claimed. By exploiting this window of opportunity, they can inject malicious code into the software supply chain at installation time, affecting all users who run the script before the developers claim the bucket.

## Defensive takeaways
- Always cryptographically sign release artifacts and verify signatures before execution
- Use AWS bucket ownership verification mechanisms or reserved bucket naming conventions
- Implement integrity checks (SHA-256 hashes, GPG signatures) for all downloaded artifacts in installation scripts
- Host installation artifacts on owned/controlled infrastructure or claim S3 buckets immediately
- Pin S3 bucket ownership with proper IAM policies and bucket ACLs
- Consider using package managers or software repositories with built-in verification (apt, yum, npm, etc.)
- Implement code signing and verify installation scripts themselves
- Monitor for typosquatting or bucket hijacking of project-related S3 buckets

## Variant hunting
Search for other installation/deployment scripts referencing unclaimed S3 buckets
Audit docker-compose.yml, setup.py, and package.json files for similar patterns
Check for hardcoded URLs downloading binaries/artifacts from AWS S3 without verification
Review CI/CD pipelines for unverified artifact downloads
Scan for wget/curl commands in shell scripts downloading from infrastructure the project doesn't own

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1195 - Supply Chain Compromise
- T1195.002 - Supply Chain Compromise: Compromised Software Supply Chain
- T1195.003 - Supply Chain Compromise: Compromised Code Repository
- T1566 - Phishing
- T1204 - User Execution of Malicious File
- T1059.004 - Command and Scripting Interpreter: Unix Shell

## Notes
This is an exemplary supply chain attack with minimal complexity. The researcher responsibly disclosed the vulnerability and demonstrated proof-of-concept without causing harm. The vulnerability is particularly severe because installation scripts execute with elevated privileges and are inherently trusted. AWS S3 bucket squatting has become a known attack vector (similar to domain squatting). Resolution requires immediate bucket registration and long-term implementation of artifact verification mechanisms.

## Full report
<details><summary>Expand</summary>

Hi team,

When I downloaded the latest release of Rocket.Chat to test the fix for my previous report I spotted an `install.sh` script. Inside that installation script I noticed [the following line](https://github.com/RocketChat/Rocket.Chat/blob/develop/install.sh#L14):

```diff
#!/bin/bash
set -x
set -euvo pipefail
IFS=$'\n\t'

ROOTPATH=/var/www/rocket.chat
PM2FILE=pm2.json
if [ "$1" == "development" ]; then
  ROOTPATH=/var/www/rocket.chat.dev
  PM2FILE=pm2.dev.json
fi

cd $ROOTPATH
+ curl -fSL "https://s3.amazonaws.com/rocketchatbuild/rocket.chat-develop.tgz" -o rocket.chat.tgz
tar zxf rocket.chat.tgz  &&  rm rocket.chat.tgz
cd $ROOTPATH/bundle/programs/server
npm install
pm2 startOrRestart $ROOTPATH/current/$PM2FILE
```

So I decided to see if I could access the contents of that S3 bucket. To my surprise, I got the following error message:

```
$ aws s3 ls s3://rocketchatbuild

An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist
```

That is when I realised that you were requesting a file from an unclaimed S3 bucket. I created a bucket with that name and I am currently serving my own `rocket.chat-develop.tgz` file that your script now fetches. The script then executes my code on any user's machine. **Please note that I do not want to cause any harm to Rocket.Chat users so all I did was upload a text file with my username in it and will happily remove the file as soon as you have seen this report.**

```
~ λ curl -fSL "https://s3.amazonaws.com/rocketchatbuild/rocket.chat-develop.tgz" -o rocket.chat.tgz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--   100   179  100   179    0     0    250      0 --:--:-- --:--:-- --:--:--   250
~ λ tar -xvzf rocket.chat.tgz 
frogs-find-bugs/
frogs-find-bugs/hehehe
~ λ cat frogs-find-bugs/hehehe 
EdOverflow :D
```

Please let me know how you would like to proceed with this report and I will try my best to help you out wherever I can.

\- Ed

## Impact

An adversary or, at the very least, I can execute arbitrary code whenever someone runs `install.sh`.

</details>

---
*Analysed by Claude on 2026-05-12*
