# Remote Code Execution through Extension Bypass in concrete5 Logging Settings

## Metadata
- **Source:** HackerOne
- **Report:** 841947 | https://hackerone.com/reports/841947
- **Submitted:** 2020-04-06
- **Reporter:** mayllart
- **Program:** concrete5 CMS
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Authentication Bypass, Input Validation Bypass, Arbitrary File Write
- **CVEs:** None
- **Category:** memory-binary

## Summary
concrete5 CMS contains a critical RCE vulnerability in the logging settings functionality where attackers can bypass file extension validation by manipulating HTTP parameters. By omitting the 'logging_mode' parameter, validation logic is skipped, allowing arbitrary PHP files to be written and executed on the server.

## Attack scenario
1. Attacker authenticates to the concrete5 administrative panel (or gains authenticated access)
2. Attacker navigates to Dashboard > System > Environment > Logging settings page
3. Attacker intercepts the HTTP POST request and modifies parameters: sets 'logFile' to a .php filename and either removes or manipulates 'logging_mode' parameter
4. Due to flawed conditional logic, the extension validation check is bypassed since it only executes when both 'handler==file' AND 'logging_mode' are set
5. Attacker sends malicious request, causing the application to save the PHP filename as the log file path in configuration
6. Attacker injects PHP code through application parameters that get logged, then accesses the PHP file via browser to achieve remote code execution

## Root cause
The extension validation code is nested inside an if condition that requires both 'handler==file' AND 'logging_mode' to be present. An attacker can bypass this by omitting 'logging_mode', causing the code to skip validation and proceed directly to the configuration save logic, which has no extension validation. The logic assumes that if these parameters aren't set, the file extension validation isn't needed, creating a logical flaw.

## Attacker mindset
An attacker would recognize that conditional validation creates a security gap. By understanding the intended flow, they exploit the assumption that missing parameters mean the code path won't be reached. They manipulate the HTTP request to create an unexpected code path that saves unvalidated user input to critical configuration.

## Defensive takeaways
- Implement validation checks OUTSIDE of conditional logic - validate all file extensions regardless of other parameters
- Use a whitelist approach for file extensions and enforce it at the earliest point
- Separate parameter validation from business logic - validate all inputs before any conditional processing
- Implement server-side restrictions on where log files can be written (dedicated log directory)
- Use configuration constants for sensitive paths rather than user input
- Implement code review focusing on conditional validation logic where attackers can manipulate conditions
- Add logging and monitoring for configuration changes, especially file path modifications
- Consider using immutable/read-only configuration for sensitive settings

## Variant hunting
Search for other conditional validation patterns where extension checks depend on parameter presence
Look for configuration save functions that accept file paths without extension validation
Identify other dashboard settings pages that accept file paths as input
Check for similar patterns where validation is nested in conditionals that can be bypassed
Review other logging/file upload functionality for similar bypass techniques
Search for instances where 'logging_mode' or similar mode parameters control validation flow

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1505 - Server Software Component
- T1134 - Access Token Manipulation
- T1583 - Acquire Infrastructure

## Notes
This is a high-impact vulnerability as it allows unauthenticated-to-RCE with valid admin access. The bug demonstrates a common security pattern failure where developers assume certain code paths won't be reached if specific parameters are missing. The vulnerability is trivial to exploit once identified - simply modifying HTTP parameters to bypass validation. The logging functionality provides a convenient delivery mechanism as application logs capture user input. Patching requires moving validation outside conditionals and implementing a whitelist approach for extensions and file paths.

## Full report
<details><summary>Expand</summary>

Summary:
=====================

The Application concrete5 CMS available on github is vulnerable to remote code execution through the functionality of setting the log file in "Loggin Settings". It is possible to bypass the portion of code responsible for the verification of the extension of the log file (.log).

Description:
=====================

The code in the {path_of_installation}/concrete5/concrete/controllers/single_page/dashboard/system/environment/logging.php has a vulnerable function (update_loggin()). This function has a condition that verifies if the parameter "handler" in the HTTP request is equal to "file" and, if the parameter "logging_mode" has any value. In case one of these conditions is not met the application will not proceed to verify if the extension of the log file ends with ".log" and will go straight to the next if, which verifies if there is any error (in case, there are not) and set the "concrete.log.configuration.simple.file.file" variable to the value of "logFile" parameter in the HTTP request. By doing that it is possible to set the log file to a .php file in the system. An attacker may be able to inject PHP code in the log File by injecting it on parameters in the application. Then, by requesting the file in the browser the code will get executed.

Vulnerable code:

```
public function update_logging()
    {
        $config = $this->app->make('config');
        if (!$this->token->validate('update_logging')) {
            $this->error->add($this->token->getErrorMessage());
        }
        if ($this->request->request->get('handler') == 'file' && $this->request->request->get('logging_mode')) { // this if condition that can be bypassed
            $logFile = $this->request->request->get('logFile');
            $filesystem = new Filesystem();
            $directory = dirname($logFile);
            if ($filesystem->isFile($logFile) && !$filesystem->isWritable($logFile)) {
                $this->error->add(t('Log file exists but is not writable by the web server.'));
            }
            if (!$filesystem->isFile($logFile) && (!$filesystem->isDirectory($directory) || !$filesystem->isWritable($directory))) {
                $this->error->add(t('Log file does not exist on the server. The directory of the file provided must exist and be writable on the web server.'));
            }
            $filename = basename($logFile);
            if (!$filename || substr($filename, -4) != '.log') {
                $this->error->add(t('The filename provided must be a valid filename and end with .log'));
            }
        }
        if (!$this->error->has()) {// it is possible to jump straight to this condition and set the log file to a .php file.
            $intLogErrorsPost = $this->post('ENABLE_LOG_ERRORS') == 1 ? 1 : 0;
            $intLogEmailsPost = $this->post('ENABLE_LOG_EMAILS') == 1 ? 1 : 0;
            $intLogApiPost = $this->post('ENABLE_LOG_API') == 1 ? 1 : 0;

            $config->save('concrete.log.errors', $intLogErrorsPost);
            $config->save('concrete.log.emails', $intLogEmailsPost);
            $config->save('concrete.log.api', $intLogApiPost);

            $mode = $this->request->request->get('logging_mode');
            if ($mode != 'advanced') {
                $mode = 'simple';
                $config->save('concrete.log.configuration.simple.core_logging_level',
                    $this->request->request->get('logging_level')
                );
                $config->save('concrete.log.configuration.simple.handler',
                    $this->request->request->get('handler')
                );
                $config->save('concrete.log.configuration.simple.file.file',
                    $this->request->request->get('logFile') //set the PHP 
                );
            }
            $config->save('concrete.log.enable_dashboard_report',
                $this->request->request->get('enable_dashboard_report') ? true : false);
            $config->save('concrete.log.configuration.mode', $mode);

            $this->redirect('/dashboard/system/environment/logging', 'logging_saved');
        }
```

Steps To Reproduce:
=====================

1) Login to the administrative panel of the application and navigate to :http://{concrete5_website}/index.php/dashboard/system/environment/logging. Set the File variable to: {INSTALLATION_PATH_OF_CONCRETE5}/pwned.php, send the request and intercept it.

{F776879}

2) Change the handler parameter in the HTTP request to any value. By doing that we will get straight to the next "if condition" mentioned before. However, by doing that the handler will be set to its default value (Database) in the backend.

{F776880}

{F776881}

3) Now we need to make the handler get the "file" value. We change the "Handler" in the panel to the "File" option and send the request again. Then, the request is intercepted and the value in the parameter "logging_mode" of the HTTP request must be completely erased. 

{F776882}

By doing that we will go straight to the next if, since the condition: $this->request->request->get('logging_mode'))` is not met. Right after entering the next if condition, the value of "logging_mode" will get restored to the value of "simple":

```
if ($mode != 'advanced') {
                $mode = 'simple';
```

4) To get the code execution to work we now need to inject the malicious PHP code in the log file. This can be achieve by trying to login with a user called: <?php system('id'); ?>.

{F776883}

We can see the file is now created in the server with the malicious content.

{F776884}

{F776885}

5) By accessing the file in the browser it is possible to verify that the code is successfully executed.

{F776886}

Resubmitted the report since it was missing the "crayons".

Thanks!!

## Impact

OS command execution in the webserver under the permissions of the OS user executing the server application, being able to completely modify the application code or compromise the server (reading, editing, adding or removing files). In case of selecting a .php file that already exists in the server it will have log text appended to it and will interrupt the application operation (example: select the index.php as the log file) by resulting in a malformed php file.

</details>

---
*Analysed by Claude on 2026-05-12*
