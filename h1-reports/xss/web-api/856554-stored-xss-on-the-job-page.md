# Stored XSS on the job page via Kubernetes namespace parameter

## Metadata
- **Source:** HackerOne
- **Report:** 856554 | https://hackerone.com/reports/856554
- **Submitted:** 2020-04-22
- **Reporter:** mike12
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe Template Rendering
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in GitLab's job page environments block where the Kubernetes namespace parameter from .gitlab-ci.yml is rendered without proper sanitization. An attacker can inject malicious JavaScript by specifying a crafted namespace value in the CI/CD pipeline configuration, which executes when any user views the job details page.

## Attack scenario
1. Attacker creates or gains access to a GitLab project repository
2. Attacker adds a .gitlab-ci.yml file with a malicious payload in the kubernetes.namespace field (e.g., '<img src=x onerror=alert(1)>')
3. Attacker triggers a pipeline build by committing the malicious configuration
4. Victim user navigates to CI/CD > Jobs and opens the job details page
5. The environments_block.vue component renders the unsanitized namespace parameter, executing the injected JavaScript
6. Attacker's payload executes in the victim's browser context, allowing credential theft or session hijacking

## Root cause
The environments_block.vue Vue component uses template interpolation with %{kubernetesNamespace} placeholder at multiple locations (lines 125, 156, 251, etc.) without proper HTML escaping or sanitization. The Kubernetes namespace value from the CI/CD pipeline configuration is directly rendered into the DOM without validation or encoding.

## Attacker mindset
An attacker with repository write access seeks to compromise other users viewing the same project. By storing malicious code in CI/CD configuration, the payload persists and affects all users who view the job page, making it an effective persistence mechanism for credential harvesting or privilege escalation within the GitLab instance.

## Defensive takeaways
- Always sanitize and escape user-controlled input before rendering in DOM, especially in Vue.js templates using v-text instead of v-html
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Validate CI/CD pipeline configuration parameters against whitelists for expected formats
- Use Vue.js's built-in XSS protection by avoiding v-html and using text binding instead
- Implement server-side validation and sanitization for pipeline configuration metadata
- Apply security scanning in CI/CD to detect malicious patterns in configuration files
- Perform code reviews focusing on template rendering and user input handling

## Variant hunting
Search for other Vue components that render pipeline metadata, environment variables, or deployment configuration. Look for any use of v-html or direct innerHTML assignments with values derived from .gitlab-ci.yml, deployment configurations, or other user-controllable pipeline data. Check Kubernetes-related features and any environment/deployment information display components.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1539 - Steal Web Session Cookie
- T1111 - Multi-Factor Authentication Interception
- T1187 - Forced Authentication

## Notes
The vulnerability affects all users with access to the project, making it a high-impact stored XSS. The attack surface includes any GitLab instance where users can create projects with CI/CD pipelines. The fix requires implementing proper output encoding in the Vue template and potentially adding input validation at the pipeline schema level.

## Full report
<details><summary>Expand</summary>

Hello Gitlab!

### Steps to reproduce:
1. Run Gitlab `docker run --detach --hostname gitlab.example.com --publish 443:443 --publish 80:80 --publish 22:22 --name gitlab gitlab/gitlab-ce:latest`
2. Create a new project with README.md
3. Go to Operations->Kubernetes
	1. Click on the "Add Kubernetes cluster" button
	2. Select the "Add existing cluster" tab
	3. Kubernetes cluster name: cluster-example
	4. API URL: https://google.com
	5. Service Token: token-example
	6. Uncheck the "GitLab-managed cluster" checkbox
	7. Click on the "Add Kubernetes cluster" button
4. Add ".gitlab-ci.yml" file to the repository (to the master branch)

    ```
    deploy:
      stage: deploy
      script:
        - echo "Example"
      environment:
        name: production
        url: https://google.com
        kubernetes:
          namespace: <img src=x onerror=alert(1)>
      only:
      - master
    ```
5. Go to CI/CD->Jobs and open the last job
{F799680}
{F799681}

#### Vulnerable code

All vulnerable code is in one file [environments_block.vue](https://gitlab.com/gitlab-org/gitlab/-/blob/c2da59f0376ee8d99ce16100d5c481234bbf9f8a/app/assets/javascripts/jobs/components/environments_block.vue)

1. [Line 125](https://gitlab.com/gitlab-org/gitlab/-/blob/c2da59f0376ee8d99ce16100d5c481234bbf9f8a/app/assets/javascripts/jobs/components/environments_block.vue#L125)
2. [Line 156](https://gitlab.com/gitlab-org/gitlab/-/blob/c2da59f0376ee8d99ce16100d5c481234bbf9f8a/app/assets/javascripts/jobs/components/environments_block.vue#L156)
3. [Line 251](https://gitlab.com/gitlab-org/gitlab/-/blob/c2da59f0376ee8d99ce16100d5c481234bbf9f8a/app/assets/javascripts/jobs/components/environments_block.vue#L251)
4. And other places where `%{kubernetesNamespace}` is used

## Impact

An attacker can:

1. Perform any action within the application that a user can perform
2. Steal sensitive user data
3. Steal user's credentials

</details>

---
*Analysed by Claude on 2026-05-12*
