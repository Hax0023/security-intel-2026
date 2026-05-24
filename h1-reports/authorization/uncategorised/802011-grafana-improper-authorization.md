# Grafana Improper Authorization - Datasource Configured with Admin Credentials

## Metadata
- **Source:** HackerOne
- **Report:** 802011 | https://hackerone.com/reports/802011
- **Submitted:** 2020-02-21
- **Reporter:** lazydog
- **Program:** Kubernetes (test-infra)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Improper Authorization, Privilege Escalation, Configuration Error, Credential Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Grafana datasource for InfluxDB was misconfigured to use an admin user account instead of a read-only user, allowing authenticated Grafana users to escalate privileges and execute arbitrary InfluxDB commands through the datasource proxy. This could lead to complete compromise of the InfluxDB instance including data destruction.

## Attack scenario
1. Attacker identifies Grafana instance at velodrome.k8s.io with datasource proxy endpoint exposed
2. Attacker makes request to /api/datasources/proxy/4/query endpoint with crafted InfluxDB queries
3. Datasource proxy forwards requests using admin-privileged InfluxDB credentials stored in Grafana configuration
4. Attacker executes administrative InfluxDB commands (CREATE USER, DROP DATABASE, etc.) with escalated privileges
5. Attacker creates new admin user or modifies existing data to maintain persistence
6. Attacker can perform denial of service by dropping critical databases

## Root cause
The datasource.sh configuration script was set up with an InfluxDB admin user instead of a restricted read-only account. The Grafana datasource proxy did not enforce least privilege principles and exposed direct backend database access with full administrative capabilities inherited from the configured credentials.

## Attacker mindset
An attacker would recognize that Grafana's datasource proxy feature, when misconfigured with overprivileged credentials, becomes a gateway to backend database compromise. The goal would be to escalate from viewing metrics to administrative database control, enabling data destruction, exfiltration, or service disruption.

## Defensive takeaways
- Always configure datasource credentials with minimum required privileges (read-only where possible)
- Implement role-based access control with separate credentials for different Grafana datasources
- Restrict datasource proxy access through network controls and authentication layers
- Regularly audit Grafana configuration files and datasource credentials for privilege escalation
- Use secret management systems to store and rotate database credentials separately from application config
- Implement query filtering/allowlisting on proxy endpoints to restrict query types
- Monitor datasource proxy usage for unusual query patterns or administrative commands
- Apply principle of least privilege to all backend service accounts

## Variant hunting
Check other Grafana instances in similar infrastructure for admin-configured datasources
Search for other datasource proxy endpoints exposed without authentication
Audit Prometheus, Elasticsearch, and other Grafana datasources for privilege escalation
Review infrastructure-as-code repositories for hardcoded credentials in datasource configurations
Investigate Jenkins, GitLab CI, and other monitoring stacks for similar misconfigurations
Test datasource proxies with SQL injection and NoSQL injection payloads

## MITRE ATT&CK
- T1190
- T1199
- T1078.001
- T1078.003
- T1110
- T1136.001
- T1531

## Notes
This vulnerability affects Kubernetes test infrastructure and demonstrates how operational misconfigurations in monitoring stacks can become critical security weaknesses. The datasource proxy pattern is inherently risky when credentials are not properly restricted. The impact extends beyond confidentiality to integrity and availability through database destruction capabilities.

## Full report
<details><summary>Expand</summary>

## Summary:
new report from part2.
wrong configuration causes Grafana datasource to use root user(with influxdb admin priv).

## Component Version:
test-infra:master

## Steps To Reproduce:
in normally configuration read-only user used by grafana, but in my test i found datasource user wite admin perms.
refer: https://github.com/kubernetes/test-infra/blob/master/velodrome/grafana-stack/datasource.sh
so i think maybe other scripts make this problem.

open url http://velodrome.k8s.io/, find the follwing requests:

```
GET /api/datasources/proxy/4/query?db=metrics&q=SELECT%20%0A%20%201-(sum(%22consistent_builds%22)%2Fsum(%22builds%22))%0AFROM%0A%20%20%22flakes_daily%22%20%0AWHERE%20%0A%20%20time%20%3E%20now()%20-%2030d%0A%20%20AND%20%22job%22%20%3D~%20%2F%5E(pr%3Apull-kubernetes-kubemark-e2e-gce-big%7Cpr%3Apull-kubernetes-bazel-build%7Cpr%3Apull-kubernetes-bazel-test%7Cpr%3Apull-kubernetes-dependencies%7Cpr%3Apull-kubernetes-e2e-gce%7Cpr%3Apull-kubernetes-e2e-gce-100-performance%7Cpr%3Apull-kubernetes-e2e-kind%7Cpr%3Apull-kubernetes-integration%7Cpr%3Apull-kubernetes-node-e2e%7Cpr%3Apull-kubernetes-typecheck%7Cpr%3Apull-kubernetes-verify)%24%2F%0Agroup%20by%20job%2C%20time(20m)%20fill(none)&epoch=ms HTTP/1.1
Host: velodrome.k8s.io
Accept: application/json, text/plain, */*
X-Grafana-Org-Id: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36 Edg/80.0.361.54
Referer: http://velodrome.k8s.io/dashboard/db/job-health-merge-blocking?orgId=1
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: close
```
By trying I found that this datasource is incorrectly configured with a user.
we can use admin perms user throuth proxy access Influxdb.
so I use this vuln, created a admin user.
{F724548}

execute ```show databases,``` we found that we have admin permissions
{F724549}

## Impact

maybe denial of service this component ,because admin can drop all Influxdb database.

</details>

---
*Analysed by Claude on 2026-05-24*
