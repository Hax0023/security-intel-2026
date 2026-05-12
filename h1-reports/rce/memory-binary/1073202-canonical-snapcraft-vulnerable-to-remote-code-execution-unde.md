# Canonical Snapcraft Remote Code Execution via Library Inclusion from Current Working Directory

## Metadata
- **Source:** HackerOne
- **Report:** 1073202 | https://hackerone.com/reports/1073202
- **Submitted:** 2021-01-07
- **Reporter:** itszn
- **Program:** Canonical Snapcraft
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Arbitrary Code Execution, Library Hijacking, LD_LIBRARY_PATH Manipulation, Insecure Script Generation, Privilege Escalation
- **CVEs:** CVE-2020-27348
- **Category:** memory-binary

## Summary
Snapcraft before 4.4.4 generates wrapper scripts with empty LD_LIBRARY_PATH variables, which are treated as current working directory by the dynamic linker. An attacker can place malicious libraries (e.g., libc.so.6) in any directory where a snap application is executed, achieving remote code execution. The vulnerability affects nearly all snap-packaged applications until they are rebuilt with the patched snapcraft version.

## Attack scenario
1. Attacker creates a directory structure (e.g., cloned git repository) and places a malicious libc.so.6 library with embedded payload code in it
2. Attacker also creates subdirectories matching LD search paths (e.g., tls/) to ensure library discovery across different architectures
3. Victim downloads/clones the attacker-controlled directory and executes a snap-packaged application from within it (e.g., running 'chromium' command)
4. The snap application's wrapper script runs with empty LD_LIBRARY_PATH, causing the dynamic linker to treat current working directory as a library search path
5. Malicious libc.so.6 is loaded and executed with user privileges inside the snap container, executing the payload code
6. Attacker leverages X11 permissions (commonly granted to GUI applications) to escape the snap container and gain full system access as the current user

## Root cause
Snapcraft's script generator incorrectly creates wrapper scripts with empty LD_LIBRARY_PATH variables instead of properly sanitized or absolute paths. Per POSIX behavior, empty path components in LD_LIBRARY_PATH are interpreted as the current working directory, enabling arbitrary library loading from the execution context.

## Attacker mindset
An attacker seeking low-friction code execution against Ubuntu users would recognize that snap-packaged applications are increasingly prevalent (Chromium, Docker, etc.). By understanding LD behavior quirks, the attacker could craft innocuous-looking directories (movie folders, code repos) containing malicious libraries, socially engineering users to execute snap applications within these directories. The container escape via X11 demonstrates sophisticated knowledge of snap confinement mechanisms.

## Defensive takeaways
- Always explicitly set LD_LIBRARY_PATH to absolute, non-empty values in dynamically-generated wrapper scripts; never allow empty components
- For packaging systems, validate generated scripts for shell variable expansion vulnerabilities and library path sanitization before release
- Implement application-level safeguards: snap confinement should restrict LD_LIBRARY_PATH modification and validate library paths at runtime
- Require application rebuilds when packaging infrastructure vulnerabilities are discovered; establish automated rebuild/re-release pipelines
- Review and restrict X11 plug grants in snap definitions; X11 access should require explicit user consent and be documented as high-risk
- Implement code signing and integrity verification for snap packages to detect tampering
- Monitor LD-related environment variables and warn users when executing applications from untrusted directories
- Educate users about risks of running applications from downloaded/cloned repositories without vetting contents

## Variant hunting
Similar issues in other containerization/packaging systems (Flatpak, AppImage, Docker) that auto-generate wrapper scripts with environment variables
Other LD_* variables (LD_PRELOAD, LD_AUDIT) that might be similarly vulnerable to empty-component expansion
Build systems (CMake, Autotools, setuptools) that generate runner scripts and may have identical empty-variable bugs
Systemd unit file generation that sets library paths for service execution
Native extension builders (pip, npm-native modules) that create wrapper scripts for binary execution
Snap confinement escape vectors via other plugs (audio, camera, network sockets) beyond X11

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1574.001 Hijack Execution Flow: DLL Search Order Hijacking (Linux equivalent)
- T1547.001 Boot or Logon Autostart Execution
- T1036.005 Masquerading: Match Legitimate Name or Location
- T1218 System Binary Proxy Execution
- T1548.004 Abuse Elevation Control Mechanism: Elevated Execution with Prompt
- T1563 Steal Application Access Token

## Notes
CVE-2020-27348 assigned. The researcher responsibly disclosed to Ubuntu Security Team before public submission and waited one month post-fix to allow user updates before detailed writeup. Critical insight: empty LD_LIBRARY_PATH components treated as CWD is POSIX-standard behavior, making this a design/implementation flaw rather than a dynamic linker quirk. Many popular snaps (Chromium, Docker) remained vulnerable post-fix pending rebuilds, creating a window of continued exposure. The X11 escape demonstrates that snap confinement is not absolute security boundary for GUI applications. Researcher included functional POC proving exploitability.

## Full report
<details><summary>Expand</summary>

Preface: I apologize for previously submitting this bug to hacker1 before it was fully addressed by the Ubuntu Security Team

I have reported this issue to the Ubuntu Security team and it has been fixed:
CVE-2020-27348
Bug link: https://bugs.launchpad.net/snapcraft/+bug/1901572
Ubuntu Security Team Disclosure: https://discourse.ubuntu.com/t/usn-4661-1-snapcraft-vulnerability/19640
Commit fixing the issue in snapcraft: https://github.com/snapcore/snapcraft/commit/a0ceca9d531a34c979251030ed67b5fa2abfdd9a

I waited an month before submitting this report (which has additional non-public exploitation details) to allow users to update. See **Example Attack Scenarios** for ways this bug could have been used.

## Background:
Snapcraft is a Ubuntu project which allows applications to be bundled in containers, installed easily by users, and allow automatic updates of individual packages. Snapcraft is becoming more and more the main way to install packages on Ubuntu systems (including server). For example installing Chromium on Ubuntu 20+ will now install the Snapcraft package instead of the normal apt package. Many users/servers may be using snapcraft installed packages without knowing it. Additionlly Ubuntu recommends installing packages using Snapcraft and even prompts users when they try to run non-installed applications:

```
itszn@ubuntu:~$ docker

Command 'docker' not found, but can be installed with:

sudo snap install docker
...

See 'snap info docker' for additional versions.
```

# Bug Description:
Snapcraft before 4.4.4 is vulnerable to library inclusion from the current working directory. This allowed attackers to gain remote code execution in almost **any application** that was installed with snapcraft, when run in an attacker controlled directory. This could be as simple as running an application in a cloned git repository.

The bug is due to incorrect bash script generation when creating confined snap packages. Snapcraft will generate wrapper scripts to run the application, but accidently uses empty variables to define the `LD_LIBRARY_PATH` for the application. Due to a quirk with LD, empty path entries are treated as current working directory. This means that any libraries (for example libc.so.6) in the current working directory will be loaded into the snap application when run. (Additionally LD will search several subdirectories including `tls`).

A malicious library could easily be crafted to run arbitrary remote code when a snap application is run. This code will run inside the snap container so it will initially be somewhat restricted and can only access any files in the users home directory (excluding dotfiles). However due to many apps also including X11 permissions, it is fairly trivial to escape the container using X11 commands. This would give an attacker full access to the system as the current user.

# Fix
Snapcraft [fixed](https://github.com/snapcore/snapcraft/commit/a0ceca9d531a34c979251030ed67b5fa2abfdd9a) the issue in the script generator by including a check for empty string. However for the fix to be applied, application authors must "refresh" their app, regenerating the vulnerable files. This means that **many applications are still vulnerable** (ie chromium and docker) until re-generated correctly.

# POC
Attached is both the POC archive which should still work against chromium. Additionally is a script that generates the malicious `libc.so.6`

```
itszn@ubuntu:~$ tar xfvz snap-escape
itszn@ubuntu:~$ cd snap-escape
itszn@ubuntu:snap-escape$ ls
total 8
-rw-rw-r-- 1 itszn itszn    0 Oct 25 11:04 amazing-movie.mp4
-rw-rw-r-- 1 itszn itszn    0 Oct 25 11:28 cool-page.html
-rw-rw-r-- 1 itszn itszn 2193 Oct 25 11:45 README.txt
drwxrwxr-x 3 itszn itszn 4096 Oct 25 11:28 tls
itszn@ubuntu:snap-escape$ chromium
Got code execution running as itszn inside snap container!

We can read/write any non-hidden (non-dot) file in
+ echo 'Hello from snap code exec' > /home/itszn/pwned
+ cat /home/itszn/pwned
Hello from snap code exec

However we are still restricted by the container

We cannot access dotfiles
+ echo 'echo PWNED' >> /home/itszn/.bashrc
./tls/s: 20: ./tls/s: cannot create /home/itszn/.bashrc: Permission denied

Or other non-home files
+ cat /etc/issue
cat: /etc/issue: Permission denied

Luckily, this snap has the x11 plug
We can use this escape the container!
Starting container escape...



Escape Success!

We are now running code outside of snap container, we now have full privs of itszn

For example we now can read /etc/issue:
+ cat /etc/issue
Ubuntu 18.04.4 LTS \n \l


Or modify dotfiles
+ echo 'echo PWNED' >> /home/itszn/.bashrc
+ tail -n 1 /home/itszn/.bashrc
echo PWNED

Full escape and code execution~!
```

## Impact

In many situations, an attacker could gain full access to a user's system running as the current user. The following are example attack scenarios demonstrating how an attacker could abuse this bug against users.

# Example Attack Scenarios:
## Scenario 1: VLC
- Attacker creates a malicious archive containing a video file. Like before the malicious library is hidden in a `tls` directory to prevent suspicion (potentially even disguised as subtitle information)
- The target user wants to view the video file and downloads the archive. They extract the archive and find the video file:

```
itszn@ubuntu:~$ tar xfvz movie.tar.gz && cd movie
itszn@ubuntu:movie$ ls
total 8
-rw-rw-r-- 1 itszn itszn    0 Oct 25 11:04 amazing-movie.mp4
-rw-rw-r-- 1 itszn itszn 2193 Oct 25 11:45 README.txt
drwxrwxr-x 3 itszn itszn 4096 Oct 25 11:28 tls
drwxrwxr-x 3 itszn itszn 4096 Oct 25 11:29 tls_subtitles
```
- The user now runs VLC, which they installed using snapcraft (VLC is one of the top Snapcraft apps according to the Snap store).

```
itszn@ubuntu:movie$ vlc ./amazing-movie.mp4
```
- At this point the attacker has achived coded exction in the VLC container. The attacker can use the X11 plug to trivially escape this container.
- The attacker now has full access to the system as the user

## Scenario 2: Chromium
- Attacker adds malicious library into a github reposity. The library is hidden in a `tls` directory in the repo (making it harder to be noticed by the target user). 
- Target user clones the git repo and opens the html file with chromium (which since Ubuntu 20 is always installed as a Snapcraft package):

```
itszn@ubuntu:~$ git clone git@github.com:example/example-site.git && cd example-site
itszn@ubuntu:example-site$ ls
total 8
-rw-rw-r-- 1 itszn itszn    0 Oct 27 14:31 some_page.html
drwxrwxr-x 3 itszn itszn 4096 Oct 25 11:29 css
drwxrwxr-x 3 itszn itszn 4096 Oct 25 11:29 js
drwxrwxr-x 3 itszn itszn 4096 Oct 25 11:28 tls
itszn@ubuntu:example-site$ chromium ./some_page.html
```

- Normally to compromise a user from a webpage both a browser exploit and a sandbox escape are required. However as the malicious library is injected before any sandboxing is applied, the attacker **does not need to escape the Chromium Sandbox**. The attacker now has remote code execution in the chromium container. Additionally this works even if the user already has chromium open (normally it would just tell the other chromium to load the page).
- As before, the attacker can use the X11 plug to trivially escape this container.
- The attacker now has full access to the system as the user

**NOTE**: From my testing, Chromium is **still** vulnerable as they need to manually refresh their snap packages to apply the fix.

## Scenario 3: Docker
- Attacker adds malicious library into a github reposity. The library is hidden in a `tls` directory in the repo (making it harder to be noticed by the target user). 
- Target user clones the git repo, inspects the Dockerfile, and then builds the docker image. (NOTE: The dockerfile is non malicious. Under normal operation, there would be no risk. The user additionally can validate that the image would normally not attach any files or volumes).

```
itszn@ubuntu:~$ git clone git@github.com:example/example-app.gi

</details>

---
*Analysed by Claude on 2026-05-12*
