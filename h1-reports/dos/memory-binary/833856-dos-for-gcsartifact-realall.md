# Denial of Service in Prow Spyglass via Uncontrolled GCS Artifact Download

## Metadata
- **Source:** HackerOne
- **Report:** 833856 | https://hackerone.com/reports/833856
- **Submitted:** 2020-03-29
- **Reporter:** lazydog
- **Program:** Kubernetes
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Uncontrolled Resource Consumption
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can trigger arbitrary large object downloads from Google Cloud Storage by manipulating the artifactName parameter in Prow's Spyglass lens endpoint, causing memory exhaustion and denial of service. The vulnerability allows concurrent requests to amplify the impact, potentially exhausting server resources and rendering the CI/CD infrastructure unavailable.

## Attack scenario
1. Attacker identifies the vulnerable Spyglass endpoint at /spyglass/lens/buildlog/rerender
2. Attacker crafts HTTP request with malicious artifacts parameter pointing to large GCS objects (e.g., multi-GB files)
3. Attacker sends concurrent requests (e.g., 30+ parallel requests) to maximize memory consumption
4. Server fetches full content of large objects into memory via ioutil.ReadAll() without size limits
5. Server memory exhaustion occurs as multiple large objects are simultaneously loaded
6. Legitimate requests timeout or fail, resulting in complete denial of service for Prow infrastructure

## Root cause
The GCSArtifactFetcher.ReadAll() method in gcsartifact.go:205 uses ioutil.ReadAll() to load entire artifact contents into memory without implementing size validation, rate limiting, or streaming constraints. The artifact parameter is directly controlled by user input through the HTTP request without sanitization.

## Attacker mindset
An attacker targeting Kubernetes CI/CD infrastructure seeks to disrupt build and test pipelines. By exploiting the unvalidated artifact download mechanism, they can achieve maximum impact with minimal effort—simply crafting HTTP requests with references to large objects already present in GCS.

## Defensive takeaways
- Implement maximum artifact size limits before downloading; reject requests exceeding thresholds
- Use streaming/chunked reading instead of ioutil.ReadAll() to limit memory consumption per request
- Add rate limiting and concurrent request throttling per user/IP to artifact endpoints
- Validate and whitelist allowed artifact names/paths; implement strict path traversal protection
- Implement request timeout and memory usage monitoring for artifact operations
- Consider authentication/authorization checks on artifact access requests
- Add metrics/alerts for abnormal spike in artifact downloads or memory usage

## Variant hunting
Similar endpoints handling file downloads/streaming without size constraints
Other test infrastructure components (Jenkins, BuildKite) with artifact serving capabilities
APIs accepting file path parameters that trigger backend retrieval operations
Web interfaces for log/artifact viewing in CI/CD systems without input validation
S3, Azure Blob, or other cloud storage integrations with uncontrolled read operations

## MITRE ATT&CK
- T1190
- T1499
- T1561

## Notes
Reporter demonstrated proof-of-concept through simulation code showing memory exhaustion under concurrent load. The vulnerability is particularly critical given Prow's central role in Kubernetes testing infrastructure. The spyglass lens feature appears to lack input validation and resource consumption controls. Patch should prioritize streaming-based artifact delivery with configurable size limits.

## Full report
<details><summary>Expand</summary>

Hi,
I'm not be goot at english,
if have anything don’t understand, please contact me.

Thanks!

## Summary:
attackers can control artifactName list make google storage client download large object cause denial of service.
## Component Version:
kubenetes/test-infra:master(SHA:fea5af139ecdac00e5efa46539bc80bd0f9e951c)

## Steps To Reproduce:
  1. request this url, we can see the http response is slowly.so i analyze the code process flow.
```
https://prow.k8s.io/spyglass/lens/buildlog/rerender?req={"artifacts":["k8s-test-cache.tar.gz"],"index":0,"src":"gcs/kubernetes-jenkins/cache/poc/"}
```{F764935}
  2. in "/spyglass/lens/" endpoint handle function, we can control the req.artifacts params make google storage client download a large object in memory. the vuln code flow like this:

```
test-infra/prow/cmd/deck/main.go:702  func handleArtifactView() ->
test-infra/prow/cmd/deck/main.go:1151 sg.FetchArtifacts(..., request.Artifacts) ->
test-infra/prow/spyglass/artifacts.go:119 s.GCSArtifactFetcher.artifact(..., artifactname) ->
etc..(path process, url sign)
test-infra/prow/cmd/deck/main.go:1175 lens.Body(artifacts) ->
test-infra/prow/spyglass/lenses/buildlog/lens.go:190 logLinesAll(artifact) ->
test-infra/prow/spyglass/lenses/buildlog/lens.go:213 artifact.ReadAll() ->
test-infra/prow/spyglass/gcsartifact.go:205 ioutil.ReadAll(reader)
```
{F764922}
  3.ensure prow infra is not interrupted, i write the simple code to simulation the vuln code, and use `ab -n 30 -c 30 http://localhost:8090/download` command concurrent request website.
```
package main

import (
    "net/http"
    "fmt"
    "io/ioutil"
    "strings"
)

func client() (r *http.Response, err error){
    var res *http.Response
    var hc = &http.Client{}
    // req, err := http.NewRequest("GET", "https://storage.googleapis.com/kubernetes-jenkins/cache/poc/k8s-test-cache.tar.gz", nil)
    req, err := http.NewRequest("GET", "http://localhost/10MB.BIN", nil)
    if err != nil {
        return nil, err
    }

    res, err = hc.Do(req)
    if err != nil {
        return nil, err
    }

    return res, nil
}

func download(w http.ResponseWriter, req *http.Request) {
    res, err := client()
    if err != nil {
        fmt.Fprintf(w, "err")
    }

    defer res.Body.Close()

    read, err := ioutil.ReadAll(res.Body)
    if err != nil {
        fmt.Fprintf(w, "err")
    }

    lines := strings.Split(string(read), "\n")
    data := strings.Join(lines, "")
    fmt.Fprintf(w, data)
}

func main() {
    http.HandleFunc("/download", download)

    http.ListenAndServe(":8090", nil)
}
```
result:
{F764944}

4.i think concurrent request the prow spyglass endpoint  also make server out of memory.

## Impact

attacker can send HTTP request to the prow can cause an a denial of service by control the fetcher download large object.

</details>

---
*Analysed by Claude on 2026-05-24*
