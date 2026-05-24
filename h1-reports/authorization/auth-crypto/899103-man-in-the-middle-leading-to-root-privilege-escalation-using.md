# Man in the Middle Attack on Cloud Metadata Service via CAP_NET_RAW in hostNetwork Container

## Metadata
- **Source:** HackerOne
- **Report:** 899103 | https://hackerone.com/reports/899103
- **Submitted:** 2020-06-16
- **Reporter:** champtar
- **Program:** Kubernetes/Google GKE
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Privilege Escalation, Man-in-the-Middle (MITM), Insecure Capability Assignment, Cloud Metadata Service Exploitation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Kubernetes containers with hostNetwork=true and default CAP_NET_RAW capability can perform MITM attacks on the host's network traffic, including cloud metadata service requests. Attackers can intercept unencrypted metadata service responses (http://169.254.169.254) to inject SSH keys and gain root access on the host. This vulnerability affects all major cloud providers (AWS, Azure, GCP, OpenStack) that provision credentials via metadata services.

## Attack scenario
1. Attacker gains code execution in a Kubernetes pod configured with hostNetwork=true (a common misconfiguration for certain workloads)
2. Pod retains default CAP_NET_RAW capability, allowing raw packet manipulation and network sniffing
3. Attacker uses Scapy library to monitor all network traffic on the shared host network interface
4. Attacker identifies host's HTTP requests to cloud metadata service (169.254.169.254) containing credential fetch queries
5. Attacker crafts malicious response packets spoofing the metadata service, injecting attacker's SSH public key into authorized_keys response
6. Host accepts injected SSH key, and attacker SSH connects as root to obtain full host compromise

## Root cause
Kubernetes includes CAP_NET_RAW capability by default for all containers. Combined with hostNetwork=true, this allows containers to perform arbitrary network manipulation. Cloud VMs rely on unencrypted HTTP metadata services for credential provisioning, creating a critical dependency on network isolation that hostNetwork=true violates.

## Attacker mindset
An attacker would recognize that hostNetwork=true pods represent a critical security boundary violation. CAP_NET_RAW is often overlooked as a dangerous capability since it doesn't directly grant filesystem access. By chaining it with metadata service exploitation, the attacker leverages cloud infrastructure assumptions (trusting local network) to achieve complete host compromise with minimal effort.

## Defensive takeaways
- Remove CAP_NET_RAW from default container capabilities or implement allowlist-based approach
- Enforce pod security policies restricting hostNetwork=true to only essential workloads
- Use sysctl net.ipv4.ping_group_range to allow unprivileged ping without CAP_NET_RAW
- Implement egress network policies blocking pod-to-metadata-service traffic unless explicitly required
- Use IMDSv2 (Instance Metadata Service Version 2) on cloud platforms, which uses token-based authentication preventing MITM
- Encrypt metadata service traffic or restrict it to privileged accounts only
- Monitor for suspicious network behavior in containers with CAP_NET_RAW and hostNetwork enabled
- Require explicit capability requests rather than using defaults; audit production workloads for hostNetwork usage
- Consider containerizing privilege-separation: avoid combining hostNetwork with application workloads

## Variant hunting
CAP_NET_ADMIN without CAP_NET_RAW for MITM attacks on privileged protocols
Exploitation of other metadata services: AWS IMDSv1, Azure Instance Metadata Service, OpenStack metadata endpoints
ARP spoofing attacks from hostNetwork pods to redirect traffic to attacker container
DNS spoofing to redirect credential requests to attacker-controlled server
DHCP spoofing to inject malicious configuration including DNS or NTP servers
Exploitation of other default capabilities (CAP_SYS_ADMIN, CAP_NET_ADMIN) combined with hostNetwork
Similar attacks on internal Kubernetes services queried by kubelet (e.g., API server communications)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (vulnerable K8S configuration)
- T1200 - Traffic Redirection/Hijacking (MITM on metadata service)
- T1187 - Man-in-the-Middle (intercepting and modifying HTTP traffic)
- T1556 - Modify Authentication Process (injecting SSH keys)
- T1098 - Account Manipulation (SSH key injection)
- T1134 - Man-in-the-Browser (network-level equivalent)
- T1578 - Modify Cloud Compute Infrastructure (privilege escalation path)
- T1552 - Unsecured Credentials (metadata service exploitation)
- T1611 - Escape to Host (from container to host via MITM)
- T1021.004 - Remote Services - SSH (using injected key for access)

## Notes
This report effectively demonstrates why capability restrictions are critical in containerized environments. The vulnerability chain requires: (1) insecure default (CAP_NET_RAW), (2) insecure pod configuration (hostNetwork=true), and (3) unencrypted service dependency (metadata HTTP). The researcher appropriately calls for breaking changes in Kubernetes defaults. GCP/GKE likely responded with IMDSv2 enforcement and security policy updates. This exemplifies how 'defense in depth' fails when a single misconfiguration negates network isolation assumptions.

## Full report
<details><summary>Expand</summary>

## Summary:
CAP_NET_RAW capability is still included by default in K8S, leading to yet another attack.

An attacker gaining access to a hostNetwork=true container with CAP_NET_RAW capability can listen to all the traffic going through the host and inject arbitrary traffic, allowing to tamper with most unencrypted traffic (HTTP, DNS, DHCP, ...), and disrupt encrypted traffic.
In many cloud deployments the host queries the metadata service at http://169.254.169.254 to get many information including the authorized ssh keys.
This report contains a POC running on GKE, manipulating the metadata service responses to gain root privilege on the host.
The same attack should work on all clouds using similar metadata services to provision ssh keys (Amazon / Azure / OpenStack / ...)

The goal of this report is to ask the K8S team to make a breaking change by removing CAP_NET_RAW from the default capabilities,
as it allows way too many attacks.
K8S could enable `net.ipv4.ping_group_range` to still let users use ping (maybe 99% of CAP_NET_RAW usage)

## Kubernetes Version:
This was tested on a default GKE cluster (1.14.10-gke.36)

## Steps To Reproduce:

1. Create a GKE cluster
```
gcloud beta container --project "copper-frame-263204" clusters create "hostmitm" --zone "us-central1-c" --no-enable-basic-auth --cluster-version "1.14.10-gke.36" --machine-type "n1-standard-1" --image-type "COS" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "3" --enable-stackdriver-kubernetes --enable-ip-alias --network "projects/copper-frame-263204/global/networks/default" --subnetwork "projects/copper-frame-263204/regions/us-central1/subnetworks/default" --default-max-pods-per-node "110" --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0
```

2. Create a hostNetwork=true pod
```
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-node
spec:
  hostNetwork: true
  containers:
    - name: ubuntu
      image: ubuntu:latest
      command: [ "/bin/sleep", "inf" ]
EOF
```

3. Copy our script
```
kubectl cp metadatascapy.py ubuntu-node:/metadatascapy.py
```
(download F869463)

4. Connect to the container
```
kubectl exec -ti ubuntu-node -- /bin/bash
```
(the next commands are in the container shell)

5. Install the needed packages
```
apt update && apt install -y python3-scapy openssh-client
```

6. Generate an ssh key (this is the key that we are going to inject and use to ssh into the host)
```
ssh-keygen -t ed25519 -f /root/.ssh/id_ed25519 -N ""
```

7. Launch the script, wait up to 2min, enjoy
```
python3 /metadatascapy.py
```
(If you see a kubeconfig and some certificates printed, it worked)

## Impact

An attacker able to execute code in a hostNetwork=true container with CAP_NET_RAW capability can, in cloud deployments, easily gain root privileges on the host.

</details>

---
*Analysed by Claude on 2026-05-24*
