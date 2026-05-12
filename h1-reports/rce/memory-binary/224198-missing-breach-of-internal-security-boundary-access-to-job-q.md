# Missing/Breach of Internal Security Boundary - Access to Job Queue Results in Remote Code Execution

## Metadata
- **Source:** HackerOne
- **Report:** 224198 | https://hackerone.com/reports/224198
- **Submitted:** 2017-04-27
- **Reporter:** pruby
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Insecure Deserialization, Missing Input Validation, Broken Access Control, Unsafe Reflection
- **CVEs:** None
- **Category:** memory-binary

## Summary
GitLab's GitlabShellWorker processes arbitrary job queue entries from Redis without validation, allowing attackers to invoke any public method on shell objects through Ruby's instance_eval. An attacker with Redis access can inject malicious job queue entries to achieve remote code execution as the GitLab application user.

## Attack scenario
1. Attacker gains unauthorized access to Redis server (via network exposure, credential compromise, or other vulnerability)
2. Attacker uses Redis CLI to push malicious job entry into 'resque:gitlab:queue:gitlab_shell' queue
3. GitlabShellWorker dequeues the job without validation
4. Worker invokes arbitrary public method (instance_eval) with attacker-controlled parameters
5. Ruby's instance_eval executes injected shell commands in application context
6. Code execution occurs as GitLab application user, potentially bypassing OS-level privilege restrictions

## Root cause
GitlabShellWorker accepts and executes arbitrary method names and parameters from job queue entries without whitelisting. The worker directly invokes public methods on shell objects, and Ruby's inherited instance methods (like instance_eval) enable code execution when attacker controls both method name and parameters.

## Attacker mindset
An attacker who has compromised internal infrastructure (Redis access) seeks to escalate privileges and bypass OS-level restrictions by leveraging unsafe job queue processing to execute code as the GitLab application user rather than the Redis user.

## Defensive takeaways
- Implement strict whitelist of allowed job types and methods rather than accepting arbitrary method invocation
- Never deserialize or execute user-controlled method names from external sources including queues
- Avoid accepting arbitrary parameters to queued tasks; use database entity references instead
- Establish internal security boundaries and assume compromise of individual components (Redis, database, queue)
- Validate and sanitize all job queue entries before processing
- Restrict Redis access through network segmentation and authentication
- Monitor job queue for unexpected entries or patterns
- Use separate user contexts with minimal privileges for queue processors

## Variant hunting
Search for similar unsafe job queue handlers in: Sidekiq/Resque implementations accepting arbitrary method calls, other worker classes with reflection-based method invocation, any queue consumers using instance_eval or send() with external input, serialization patterns in message queues accepting arbitrary Ruby objects

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1021

## Notes
Researcher rated as Low net risk due to high barrier of entry (requiring Redis access), but this is a critical vulnerability in isolation. The issue demonstrates security boundary breach between application and internal queue component. Report conducted through code review and local testing, not against public GitLab instances.

## Full report
<details><summary>Expand</summary>

Test Conditions
=============

This issue was tested in GitLab Community Edition using a combination of code review (against git commit 6c65b63ca5, April 20 2017) and testing likely issues against a local deployment of Bitnami GitLab Community Edition 9.0.5-0, running on Ubuntu 14.04.5. These are running different versions of GitLab, as we were constrained by time available for deploying systems to test. This issue has not been tested against gitlab.com or other public installations.

Testing was conducted in research time provided by my employer, Insomnia Security, and was not part of a client engagement.

Issue Description
==============

The GitlabShellWorker handler for jobs from the SideKiq job queue allows arbitrary code to be executed from an enqueued job. From the Redis CLI, adding the following queue entry will result in the creation of a file /tmp/rce-demo:

    rpush 'resque:gitlab:queue:gitlab_shell' '{"class":"GitlabShellWorker","args":["instance_eval","`touch /tmp/rce-demo`"],"jid":"Zaep6UXu","enqueued_at":1493166403.21}'

This results in code execution as the GitlabShellWorker allows any public method on the shell object to be executed. All ruby objects have inherited instance methods that result in remote code execution when an attacker controls the method name and at least one parameter.

It is not necessary that GitLab execute arbitrary code from the job queue. Jobs may be whitelisted and executed only from a fixed list of tasks. Other GitLab service workers follow this more secure paradigm.

Impact
======

An attacker with the ability to add entries to any SideKiq queue may use this endpoint to execute code in the context of the GitLab application. This introduces an absolute trust relationship between the application and the queue server, which may be abused by an attacker.

While remote code execution is a critical issue, the pre-requisites for this attack imply an extremely high level of access to system internals which are known to be vulnerable to other issues and not generally exposed to external parties. As the *gain* in access is limited, and the conditions unlikely, I have rated this as having a Low net risk.

Note that access to a Redis installation implies the ability to execute code as the Redis user, as Redis itself has a high level of trust in all clients. However, this issue may be used to bypass operating system restrictions on the user role, and execute code as the GitLab application user.

Recommendations
===============

* Whitelist actions which may be invoked through the job queue.
* Avoid accepting arbitrary parameters to queued tasks. Where feasible, require that tasks act on pre-established database entities such as projects and repositories, not arbitrary filesystem paths.
* Limit trust in internal components such as message queues and database. Construct internal boundaries to limit the impact of individual components being breached.

</details>

---
*Analysed by Claude on 2026-05-12*
