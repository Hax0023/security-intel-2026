# Dockerized Nextcloud: Temporary config.php Read Failure Allows Anonymous Admin Account Creation

## Metadata
- **Source:** HackerOne
- **Report:** 522876 | https://hackerone.com/reports/522876
- **Submitted:** 2019-04-03
- **Reporter:** theguynamedguy86
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Improper Input Validation, Insufficient Access Control, Race Condition, Insecure Default Configuration, Missing Installation State Verification
- **CVEs:** None
- **Category:** uncategorised

## Summary
In Dockerized Nextcloud deployments with shared NFS/SMB volumes, transient failures reading config.php cause the application to incorrectly assume uninstalled state and serve the installer to anonymous users. This allows any attacker to create arbitrary admin accounts and gain full system access, even when Nextcloud is already fully installed with existing data and users.

## Attack scenario
1. Attacker monitors a target Nextcloud installation for installer availability, potentially via periodic HTTP requests to setup endpoints
2. A transient NFS/SMB connectivity issue occurs on one or more containers, causing config.php read failure during startup or runtime
3. Nextcloud incorrectly assumes uninstalled state and rewrites config.php with 'installed' = FALSE while preserving database credentials from environment variables
4. When NFS/SMB service is restored, all containers now serve the installer page due to the newer config.php timestamp indicating incomplete setup
5. Attacker accesses the installer and creates arbitrary admin credentials (username and password of choice)
6. Attacker gains full administrative access to the existing Nextcloud installation with access to all user data, files, and system settings

## Root cause
Nextcloud uses config.php file presence and readability as the sole indicator of installation state, without verifying whether database tables or existing admin users actually exist. During transient storage connectivity issues in containerized environments, failed reads cause the application to treat a fully-installed system as uninstalled, triggering installer regeneration. The installer is then exposed without validating pre-existing database state.

## Attacker mindset
An attacker targeting Nextcloud deployments would monitor for temporary service degradation windows as opportunities to access setup interfaces. By automating detection of installer availability and having credentials pre-prepared, the attacker can quickly create admin accounts before legitimate administrators notice the issue. The attack exploits the gap between actual installation state (database + users exist) and perceived state (config file unreadable).

## Defensive takeaways
- Implement database state verification before allowing installer execution: check for existence of core tables (oc_users, oc_storages, etc.) regardless of config file state
- Require explicit verification that no existing admin users exist in the database before allowing new admin account creation during setup
- Implement file locking mechanisms (fcntl, flock) to prevent partial reads of config.php during concurrent writes by multiple containers
- Add retry logic with exponential backoff for config.php reads to handle transient NFS/SMB failures without assuming uninstalled state
- Use atomic file operations (write to temporary file, then rename) when updating config.php to prevent incomplete reads
- Monitor and alert on config.php rewrites in production environments as this indicates potential compromise attempts
- Implement installer access controls: require authentication or network-level restrictions (e.g., localhost-only or IP whitelist) for setup endpoints
- Add installation state caching with secondary validation mechanisms beyond file modification time
- Consider using distributed configuration management (e.g., etcd, Consul) instead of file-based config in containerized environments
- Implement health checks that verify both filesystem connectivity AND database state before marking container as healthy

## Variant hunting
Check for similar state-detection vulnerabilities in config file deletion scenarios or permission changes (chmod 000 on config.php)
Investigate whether partial writes to other critical configuration files could trigger similar uninitialized state assumptions
Test multi-container deployments with intentional network partition scenarios to identify race conditions in configuration synchronization
Examine backup/restore workflows that might similarly reset installation state flags without validating database consistency
Search for other setup endpoints or administrative functions that might be accessible during 'uninstalled' state beyond the primary installer
Test scenarios where config.php exists but is corrupted (invalid JSON/PHP syntax) versus missing entirely
Investigate whether environment variable injection could be leveraged to set malicious database credentials when config.php is regenerated

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship (exploiting legitimate setup functionality)
- T1078 - Valid Accounts (creating unauthorized admin accounts)
- T1098 - Account Manipulation (admin account creation)
- T1548 - Abuse Elevation Control Mechanism (leveraging setup privileges)
- T1021 - Remote Service Session Initiation (accessing admin functions)
- T1529 - System Shutdown/Reboot (exploiting restart scenarios that trigger config read failures)

## Notes
This vulnerability represents a critical design flaw in how Nextcloud determines installation state in distributed environments. The reliance on a single file's readability as the source of truth for installation status is fundamentally flawed when that file is accessed over network storage with potential transient failures. The attack is particularly dangerous because it exploits normal operational conditions (temporary network issues) to create a window of vulnerability. The automatic config.php regeneration upon read failure compounds the problem by amplifying the window when the installer is available. This bug requires both a transient failure (which will eventually occur in any production NFS/SMB environment) and attacker monitoring/alertness, making it a practical threat. The fact that database credentials are preserved in the regenerated config.php means the attacker immediately gains not just application admin access but also direct database access.

## Full report
<details><summary>Expand</summary>

Consider this deployment:
- Nextcloud is already installed in a Dockerized environment.
- There are two Nextcloud containers running in the environment.
- Both containers share the same MySQL database.
- Both containers share the same data (`/var/www/html/data`) and config (`/var/www/html/config`) via NFS-mounted or SMB-mounted Docker volumes.
- All of the values Nextcloud needs to complete first-run setup (database name and credentials, admin credentials, etc) are provided to both containers via environment variables (`NEXTCLOUD_ADMIN_USER`, `NEXTCLOUD_ADMIN_PASSWORD`, `MYSQL_HOST`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`).

Now, consider that one or both of the containers encounter an issue reading `/var/www/html/config/config.php`. This could be caused by an of the following:
- Transient failure connecting to the NFS/SMB server at the time either container is launching or restarting (especially in response to a failed Liveness check).
- Timeout or other transient failure in communication with the NFS/SMB server while the container is already running.
- One container attempting to read `config.php` while the other container is writing to the file, causing an incomplete read (possibly making the file look empty).

In this situation, Nextcloud will assume that it is NOT installed (since the config seems empty). As a result, Nextcloud will launch the installer the next time ANY user requests a page from _the container that temporarily cannot read the `config.php` file_.  This causes that instance of Nextcloud to overwrite the `config.php` with a new file that has the same database credentials as the old file (populating the credentials from the environment variables), but the new config flags Nextcloud as not yet being installed (i.e. `installed` is set to `FALSE`). Some time later, assuming that NFS/SMB services have been restored to normal (e.g. the transient issue has disappeared), ALL containers will now happily serve up the Nextcloud installer to ANY user because the container that failed to read the configuration file wrote a new one with a newer timestamp that indicates Nextcloud is not installed.

From here, ANY user who stumbles upon the installer page can provide ANY username and password and end up with a new admin account with full access to the existing Nextcloud installation.

Nextcloud should NOT allow the installer to be run if ANY database tables already exist in the target database. If this is not possible, Nextcloud should at least not allow the installer to be run if any `admin` users exist in the target database.

## Impact

An attacker interested in taking over an existing installation of Nextcloud could write a script to frequently monitor that installation until such a time as that installation suffers a temporary issue reading `config.php` and starts serving up the installer. At that point, the attacker can hop over to the installation, finish the setup process, and create a username and password of their choice to gain full admin access to the entire Nextcloud installation.

With admin access, the attacker can lock out all of the existing users of the system, change system settings, and download or erase all of the files on the Nextcloud installation.

</details>

---
*Analysed by Claude on 2026-05-24*
