# Path Traversal in HackerOne ML API `/predict/report_weakness_id` Endpoint Leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 2032778 | https://hackerone.com/reports/2032778
- **Submitted:** 2023-06-20
- **Reporter:** jobert
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Path Traversal, Arbitrary File Access, Remote Code Execution, CWE-22
- **CVEs:** None
- **Category:** uncategorised

## Summary
HackerOne's internal ML API endpoint `/predict/report_weakness_id` is vulnerable to path traversal via unsanitized `version` and `trained_at` parameters that are directly interpolated into file system paths. An attacker can traverse the directory structure and load arbitrary tokenizer/model files, potentially achieving remote code execution through malicious joblib artifacts.

## Attack scenario
1. Attacker identifies the ML API endpoint and its expected JSON parameters (version, trained_at, input)
2. Attacker crafts path traversal payloads using `../` sequences in the `trained_at` or `version` fields
3. Attacker sends POST request with traversal payload to escape the intended models directory
4. Application constructs file path with user-controlled input without validation, accessing unintended directories
5. Attacker loads a malicious joblib file (either pre-planted or through secondary vulnerability) via `AutoTokenizer.from_pretrained()`
6. Joblib deserialization executes arbitrary Python code during model loading, achieving RCE

## Root cause
Direct string interpolation of user-supplied `request.version` and `request.trained_at` parameters into `pathlib.Path()` without validation, sanitization, or canonicalization. The Hugging Face `AutoTokenizer.from_pretrained()` function then loads from this attacker-controlled path, and joblib's unsafe deserialization can lead to code execution.

## Attacker mindset
An internal threat actor or compromised account holder exploiting the assumption that ML inference endpoints are trusted. The attacker leverages path traversal to escape sandbox constraints and access sensitive model files or inject malicious ones. This is a classic case of insufficient input validation in seemingly 'internal' APIs.

## Defensive takeaways
- Always validate and sanitize user input before using it in file system operations; use allowlists for version/trained_at values
- Use `pathlib.Path.resolve()` and verify the resolved path is within the expected directory using `.is_relative_to()` or similar checks
- Implement strict path canonicalization and reject paths containing `..` or suspicious patterns
- Run ML inference services with minimal filesystem permissions; consider using chroot/containers to limit traversal scope
- Use joblib with `allow_pickle=False` or consider safer serialization formats (e.g., SafeTensors for transformers)
- Implement input validation using regex or enums to restrict version/trained_at to known values (e.g., `^v\d+$` and ISO8601 format)
- Apply principle of least privilege to API endpoints; restrict access to internal ML APIs via network segmentation or authentication
- Perform security code review on all model loading/deserialization paths

## Variant hunting
Search for other endpoints using pathlib.Path with f-strings that interpolate request parameters
Identify any use of `AutoTokenizer.from_pretrained()`, `torch.load()`, or other model loading functions without path validation
Check for similar path traversal patterns in other ML inference APIs (e.g., `/predict/*` endpoints)
Look for joblib usage without `allow_pickle=False` in deserialization workflows
Hunt for other request parameters (e.g., `model_name`, `checkpoint`, `weights_path`) that might be similarly vulnerable
Examine version control history for recent changes to path construction logic that may have removed validation

## MITRE ATT&CK
- T1190
- T1083
- T1059

## Notes
This vulnerability is particularly dangerous because it affects an internal ML API, which may be assumed to be less critical than external-facing endpoints. The combination of path traversal + unsafe deserialization (joblib) creates a reliable RCE vector. The reporter demonstrates practical PoC using Docker, suggesting reproducibility. HackerOne's scope as a security platform makes this especially sensitive. The fix requires multi-layered defenses: input validation, path canonicalization, least privilege execution, and safer serialization.

## Full report
<details><summary>Expand</summary>

HackerOne has an internal machine learning API that exposes inference endpoints for numerous machine learning / artificial intelligence solutions. In one of the endpoints, `/predict/report_weakness_id`, which is used to classify report input, a path traversal vulnerability exists that could lead to remote code execution.

# Proof of concept
The `request.version` and `request.trained_at` parameters are both vulnerable to path traversal. To reproduce, run any of the following curl commands inside the local Docker container:

**trained_at**
```
curl -X POST http://localhost:8082/predict/report_weakness_id -H 'content-type: application/json' -d'{"version":"v1", "trained_at": "2023-01-01T00:00:00Z/../../..", "input": [{"title": "test xss", "num_of_top_predictions": 3}]}'
```

**version**
```
curl -X POST http://localhost:8082/predict/report_weakness_id -H 'content-type: application/json' -d'{"version":"v1/../../../..", "trained_at": "2023-01-01T00:00:00Z", "input": [{"title": "test xss", "num_of_top_predictions": 3}]}'
```

The vulnerable code is shown below. The `version` and `trained_at` inputs are interpolated directly into the path, as can be seen on line 29. The `AutoTokenizer.from_pretrained` function is then called to load the tokenizer into memory.

```python
@app.post(
    "/predict/report_weakness_id",
    summary="An endpoint to suggest report's weakness id.",
)
async def report_weakness_id(request: ReportWeaknessIdModelRequest):
    """
    To try the endpoint in the Swagger UI, click on **Try it out** and copy-paste the below example in the request body box
    ```
    {
        "version":"v1",
        "trained_at": "2023-01-01T00_00_00Z",
        "input": [
            {
                "title": "test xss",
                "num_of_top_predictions": 3
            }
        ]
    }
    ```
    """
    input = request.input[0]
    title = preprocess_text(input.title)

    top_n = int(
        input.num_of_top_predictions or 3
    )  # as a start, it's by default set as 3

    model_dirpath = pathlib.Path(
        f"{os.path.dirname(__file__)}/../models/report_weakness_id/{request.version}/{request.trained_at}/"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_dirpath, use_fast=True)
```

## Impact

An attacker would be able to execute arbitrary python code if they were able to get a joblib file onto the ML API (i.e. as a temporary file).

</details>

---
*Analysed by Claude on 2026-05-24*
