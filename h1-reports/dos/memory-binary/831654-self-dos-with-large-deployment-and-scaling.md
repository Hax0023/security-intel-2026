# Self-Inflicted DoS with Large Deployment and Scaling

## Metadata
- **Source:** HackerOne
- **Report:** 831654 | https://hackerone.com/reports/831654
- **Submitted:** 2020-03-25
- **Reporter:** wiardvanrij
- **Program:** Kubernetes
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Denial of Service, Resource Exhaustion, Authenticated API Abuse
- **CVEs:** None
- **Category:** memory-binary

## Summary
An authenticated user can trigger a Denial of Service attack on a Kubernetes cluster by creating a deployment with large environment variables and repeatedly scaling it up and down. This causes excessive API server and etcd memory/CPU consumption, rendering the cluster unresponsive within minutes on production-like infrastructure.

## Attack scenario
1. Attacker creates a deployment with environment variables sized near the maximum allowed limit
2. Attacker scales deployment to a high replica count (e.g., 999 pods) via API calls
3. Attacker rapidly scales the deployment down to 1 replica
4. Attacker repeats the scale-up/down cycle multiple times in succession, optionally with concurrent requests
5. API server and etcd experience exponential memory and CPU consumption during each scaling operation
6. Cluster master nodes become unresponsive and throttled, making the entire cluster inaccessible

## Root cause
Kubernetes API server and etcd do not adequately throttle or limit resource consumption during rapid scaling operations of deployments with large object payloads. Each scaling operation generates extensive object processing, reconciliation, and state transitions that accumulate in memory without sufficient garbage collection or rate limiting.

## Attacker mindset
A disgruntled authenticated user or insider with basic Kubernetes API knowledge can deliberately disrupt cluster availability. The attack is trivial to execute (simple curl commands in a loop), requires no privilege escalation, and has maximum impact with minimal effort. The attacker may not fully understand the internal mechanisms but discovers the vulnerability through experimentation.

## Defensive takeaways
- Implement resource quotas and pod limits per namespace to constrain maximum replicas and environment variable sizes
- Add rate limiting on scale operations to prevent rapid successive scaling requests
- Implement API server rate limiting and request throttling for authenticated users
- Set up etcd memory limits and monitoring with alerting for unusual consumption patterns
- Consider implementing vertical pod autoscaling limits and backoff mechanisms for rapid replica changes
- Monitor API server and etcd performance metrics; set up circuit breakers for runaway operations
- Educate users on cluster resource limits and implement policy enforcement via admission controllers
- Implement comprehensive audit logging of all scaling operations for forensic analysis

## Variant hunting
Test with other large object types (ConfigMaps, Secrets) combined with rapid CRUD operations
Attempt DoS using other scaling mechanisms (HorizontalPodAutoscaler rapid toggle, StatefulSet scaling)
Exploit large annotation or label payloads combined with scaling
Test concurrent scaling of multiple deployments simultaneously
Investigate if similar attacks work against other Kubernetes controllers (DaemonSets, Jobs)
Examine impact of large custom resources (CRDs) with rapid scaling

## MITRE ATT&CK
- T1190
- T1498.1
- T1499.1
- T1499.4

## Notes
This is an authenticated DoS vulnerability that does not require elevated privileges. The reporter demonstrates practical impact on a 3-master production-like cluster that became unresponsive within minutes. The vulnerability touches on both the API layer and etcd performance characteristics. The reporter notes uncertainty about whether the issue stems primarily from large environment variables or the scaling mechanism itself - likely both factors compound the problem. No immediate mitigation exists for existing deployments; fixes would require upstream Kubernetes improvements to scale operation processing efficiency.

## Full report
<details><summary>Expand</summary>

Report Submission Form

## Summary:
Good day! 
I was just messing around with some functions and trying to see what the impact was on my cluster. I found out that it took quite some resources to process a larger deployment, especially when scaling it. 
When I check your security release process I noticed that it did include "Authenticated User" - DOS (https://github.com/kubernetes/security/blob/master/security-release-process.md#denial-of-service) so I figured I should just make a report of this.

The summary is: 

When you define a deployment that contains loads of env variables, we can easily increase the size of what is being processed. When we start to scale & downscale this deployment, we get a massive increase in the API/ETCD memory & CPU usage. 

In my case, I literally ruined my cluster that consists of 3 master nodes (4 vCPUs, 15 GB memory each)

## Kubernetes Version:
1.15.10

## Component Version:

## Steps To Reproduce:

Short story:

  1. Create a deployment that is near to the max chars allowed with env vars.
  1. Scale it to N-number of nodes where N could be "whatever" - I've tested it with 99 nodes and 999, both seem to be increasing cluster usage
  1. Scale it back down to 1
  1. Repeat for a while.

Long story:

1  Create a deployment

Please check out my example deployment file here: https://gist.github.com/wiardvanrij/21e516993603282e174da399002d95a3
As it is really huge.
It is good to note that I just used a random image and defined really low cpu/mem limits in order to allow many pods to get created without hitting some cluster/node limit

 2   Save this as `scale.json`

```
{
    "kind": "Scale",
    "apiVersion": "autoscaling/v1",
    "metadata": {
      "name": "nginx",
      "namespace": "default"
    },
    "spec": {
      "replicas": 999
    }
}  
```

3  And save this as `scaledown.json`

```
{
    "kind": "Scale",
    "apiVersion": "autoscaling/v1",
    "metadata": {
      "name": "nginx",
      "namespace": "default"
    },
    "spec": {
      "replicas": 1
    }
}  
```
4 create a `run.sh`

```
curl -X PUT 127.0.0.1:8001/apis/apps/v1/namespaces/default/deployments/nginx/scale -H "Content-Type: application/json" -d @scale.json
curl -X PUT 127.0.0.1:8001/apis/apps/v1/namespaces/default/deployments/nginx/scale -H "Content-Type: application/json" -d @scaledown.json
curl -X PUT 127.0.0.1:8001/apis/apps/v1/namespaces/default/deployments/nginx/scale -H "Content-Type: application/json" -d @scale.json
curl -X PUT 127.0.0.1:8001/apis/apps/v1/namespaces/default/deployments/nginx/scale -H "Content-Type: application/json" -d @scaledown.json
curl -X PUT 127.0.0.1:8001/apis/apps/v1/namespaces/default/deployments/nginx/scale -H "Content-Type: application/json" -d @scale.json
curl -X PUT 127.0.0.1:8001/apis/apps/v1/namespaces/default/deployments/nginx/scale -H "Content-Type: application/json" -d @scaledown.json
... repeat above for a bunch of times (50x or so).
```

5 I've used kube proxy for easy access

run `kubectl proxy` to make a proxy to your cluster

6 run the run.sh file
`./run.sh`  and optionally you could run this multiple times for some "concurrency" 

7 What you could see

Massive usage in CPU power on the master nodes AND memory usage on for certain the API part of k8s, perhaps the nodes too, but I lost control of everything to see exactly what went down.
Eventually, you should not able to contact your cluster anymore and the nodes remain unresponsive/heavy throttled. 

## Notes

This feels really "basic" as for a DOS, though I really wanted to point something out.
I was actually learning deeper internals of k8s and I just made this "work" when I saw some spikes in my metrics. Therefore I wanted to make the note that:
- I actually made my cluster completely useless with this, but I'm uncertain if the ENV vars and/or the scaling are the sole reason.
- I've got no idea what is really happening, because even when I stopped my "script" - the entire cluster was still unresponsive.
- I've first tested this locally with KIND, and used KOPS to set up a "production like" cluster, and even with 3 somewhat decent master nodes, it was gone in minutes.


## Supporting Material/References:
Deployment file:
https://gist.github.com/wiardvanrij/21e516993603282e174da399002d95a3

## Impact

DOS on the entire k8s cluster.

</details>

---
*Analysed by Claude on 2026-05-24*
