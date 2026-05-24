# Information Disclosure via Exposed composer installed.json File

## Metadata
- **Source:** HackerOne
- **Report:** 1211061 | https://hackerone.com/reports/1211061
- **Submitted:** 2021-05-27
- **Reporter:** rohitburke
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal/Directory Listing, Sensitive Data Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Nextcloud lookup service exposed a composer installed.json file at a publicly accessible path, revealing sensitive metadata about installed dependencies, versions, and GitHub repository references. This information disclosure allows attackers to enumerate the exact software stack and versions used by the Nextcloud installation, facilitating targeted vulnerability research and exploitation.

## Attack scenario
1. Attacker discovers the publicly accessible path /vendor/composer/installed.json on lookup.nextcloud.com
2. Attacker accesses the URL and retrieves complete JSON metadata of all installed Composer dependencies
3. Attacker analyzes the JSON to identify specific package versions and their known vulnerabilities
4. Attacker uses exposed GitHub repository URLs and commit references to download source code for vulnerability analysis
5. Attacker correlates disclosed versions with known CVEs to identify exploitable weaknesses
6. Attacker launches targeted attacks against specific vulnerable dependencies or versions

## Root cause
Web server misconfiguration allowing direct HTTP access to Composer metadata files that should either be restricted or not publicly deployed. The /vendor directory containing generated dependency metadata was not properly protected or excluded from web-accessible directories.

## Attacker mindset
An attacker would view this as valuable reconnaissance data. By knowing exact dependency versions, they can perform targeted vulnerability research, identify EOL packages, and correlate with public vulnerability databases to find exploitable weaknesses specific to this deployment.

## Defensive takeaways
- Restrict web server access to /vendor directories using .htaccess, web server configuration, or firewall rules
- Remove or exclude composer-generated files from production web-accessible directories
- Implement proper directory permissions and deny direct HTTP access to vendor/composer/* files
- Use .gitignore and deployment processes to ensure vendor directories are not exposed
- Regularly audit public-facing paths for unintended information disclosure
- Consider using reverse proxies or WAF rules to block access to sensitive paths

## Variant hunting
Search for similar exposed metadata files: package.json, requirements.txt, Gemfile.lock, go.mod, package-lock.json, yarn.lock, pom.xml, gradle.lock, and other dependency manifests. Check for exposed .env files, configuration files, .git directories, and build artifacts. Examine other Nextcloud installations and similar open-source projects for identical misconfigurations.

## MITRE ATT&CK
- T1526 - Reconnaissance: Gather Victim Identity Information
- T1592 - Gather Victim Identity Information: Software
- T1590 - Gather Victim Network Information
- T1046 - Network Service Discovery

## Notes
The severity is Medium rather than High because this primarily enables reconnaissance rather than direct exploitation. However, in combination with other vulnerabilities or if the disclosed versions contain known CVEs, the impact could be elevated. This is a common misconfiguration in PHP applications where vendor directories are inadvertently exposed. The vulnerability highlights the importance of proper separation between application code and web-accessible directories.

## Full report
<details><summary>Expand</summary>

Hello team,
 
I have found one JSON path at  "https://lookup.nextcloud.com/"  which is leaking some information like Username, email id, version, etc.. 
I guess it show the user who have installed or configure anything through the vendor. I was also able to download some of the zip files of the vendor and much more.

--> Steps To Reproduce:
                  1) Go to this link "https://lookup.nextcloud.com/vendor/composer/installed.json" 
                  2) See the raw data, you will get leakage of some important data.

[
    {
        "name": "psr/http-message",
        "version": "1.0.1",
        "version_normalized": "1.0.1.0",
        "source": {
            "type": "git",
            "url": "https://github.com/php-fig/http-message.git",
            "reference": "f6561bf28d520154e4b0ec72be95418abe6d9363"
        },
        "dist": {
            "type": "zip",
            "url": "https://api.github.com/repos/php-fig/http-message/zipball/f6561bf28d520154e4b0ec72be95418abe6d9363",
            "reference": "f6561bf28d520154e4b0ec72be95418abe6d9363",
            "shasum": ""
        },
        "require": {
            "php": ">=5.3.0"
        },
        "time": "2016-08-06T14:39:51+00:00",
        "type": "library",
        "extra": {
            "branch-alias": {
                "dev-master": "1.0.x-dev"
            }
        },
        "installation-source": "dist",
        "autoload": {
            "psr-4": {
                "Psr\\Http\\Message\\": "src/"
            }
        },
        "notification-url": "https://packagist.org/downloads/",
        "license": [
            "MIT"
        ],
        "authors": [
            {
                "name": "PHP-FIG",
                "homepage": "http://www.php-fig.org/"
            }
        ],
        "description": "Common interface for HTTP messages",
        "homepage": "https://github.com/php-fig/http-message",
        "keywords": [
            "http",
            "http-message",
            "psr",
            "psr-7",
            "request",
            "response"
        ]
    },
    {
        "name": "pimple/pimple",
        "version": "v3.0.2",
        "version_normalized": "3.0.2.0",
        "source": {
            "type": "git",
            "url": "https://github.com/silexphp/Pimple.git",
            "reference": "a30f7d6e57565a2e1a316e1baf2a483f788b258a"
        },
        "dist": {
            "type": "zip",
            "url": "https://api.github.com/repos/silexphp/Pimple/zipball/a30f7d6e57565a2e1a316e1baf2a483f788b258a",
            "reference": "a30f7d6e57565a2e1a316e1baf2a483f788b258a",
            "shasum": ""
        },
        "require": {
            "php": ">=5.3.0"
        },
        "time": "2015-09-11T15:10:35+00:00",
        "type": "library",
        "extra": {
            "branch-alias": {
                "dev-master": "3.0.x-dev"
            }
        },
        "installation-source": "dist",
        "autoload": {
            "psr-0": {
                "Pimple": "src/"
            }
        },
        "notification-url": "https://packagist.org/downloads/",
        "license": [
            "MIT"
        ],
        "authors": [
            {
                "name": "Fabien Potencier",
                "email": "fabien@symfony.com"
            }
        ],
        "description": "Pimple, a simple Dependency Injection Container",
        "homepage": "http://pimple.sensiolabs.org",
        "keywords": [
            "container",
            "dependency injection"
        ]
    },
    {
        "name": "psr/container",
        "version": "1.0.0",
        "version_normalized": "1.0.0.0",
        "source": {
            "type": "git",
            "url": "https://github.com/php-fig/container.git",
            "reference": "b7ce3b176482dbbc1245ebf52b181af44c2cf55f"
        },
        "dist": {
            "type": "zip",
            "url": "https://api.github.com/repos/php-fig/container/zipball/b7ce3b176482dbbc1245ebf52b181af44c2cf55f",
            "reference": "b7ce3b176482dbbc1245ebf52b181af44c2cf55f",
            "shasum": ""
        },
        "require": {
            "php": ">=5.3.0"
        },
        "time": "2017-02-14T16:28:37+00:00",
        "type": "library",
        "extra": {
            "branch-alias": {
                "dev-master": "1.0.x-dev"
            }
        },
        "installation-source": "dist",
        "autoload": {
            "psr-4": {
                "Psr\\Container\\": "src/"
            }
        },
        "notification-url": "https://packagist.org/downloads/",
        "license": [
            "MIT"
        ],
        "authors": [
            {
                "name": "PHP-FIG",
                "homepage": "http://www.php-fig.org/"
            }
        ],
        "description": "Common Container Interface (PHP FIG PSR-11)",
        "homepage": "https://github.com/php-fig/container",
        "keywords": [
            "PSR-11",
            "container",
            "container-interface",
            "container-interop",
            "psr"
        ]
    },
    {
        "name": "container-interop/container-interop",
        "version": "1.2.0",
        "version_normalized": "1.2.0.0",
        "source": {
            "type": "git",
            "url": "https://github.com/container-interop/container-interop.git",
            "reference": "79cbf1341c22ec75643d841642dd5d6acd83bdb8"
        },
        "dist": {
            "type": "zip",
            "url": "https://api.github.com/repos/container-interop/container-interop/zipball/79cbf1341c22ec75643d841642dd5d6acd83bdb8",
            "reference": "79cbf1341c22ec75643d841642dd5d6acd83bdb8",
            "shasum": ""
        },
        "require": {
            "psr/container": "^1.0"
        },
        "time": "2017-02-14T19:40:03+00:00",
        "type": "library",
        "installation-source": "dist",
        "autoload": {
            "psr-4": {
                "Interop\\Container\\": "src/Interop/Container/"
            }
        },
        "notification-url": "https://packagist.org/downloads/",
        "license": [
            "MIT"
        ],
        "description": "Promoting the interoperability of container objects (DIC, SL, etc.)",
        "homepage": "https://github.com/container-interop/container-interop"
    },
    {
        "name": "nikic/fast-route",
        "version": "v1.2.0",
        "version_normalized": "1.2.0.0",
        "source": {
            "type": "git",
            "url": "https://github.com/nikic/FastRoute.git",
            "reference": "b5f95749071c82a8e0f58586987627054400cdf6"
        },
        "dist": {
            "type": "zip",
            "url": "https://api.github.com/repos/nikic/FastRoute/zipball/b5f95749071c82a8e0f58586987627054400cdf6",
            "reference": "b5f95749071c82a8e0f58586987627054400cdf6",
            "shasum": ""
        },
        "require": {
            "php": ">=5.4.0"
        },
        "time": "2017-01-19T11:35:12+00:00",
        "type": "library",
        "installation-source": "dist",
        "autoload": {
            "psr-4": {
                "FastRoute\\": "src/"
            },
            "files": [
                "src/functions.php"
            ]
        },
        "notification-url": "https://packagist.org/downloads/",
        "license": [
            "BSD-3-Clause"
        ],
        "authors": [
            {
                "name": "Nikita Popov",
                "email": "nikic@php.net"
            }
        ],
        "description": "Fast request router for PHP",
        "keywords": [
            "router",
            "routing"
        ]
    },
    {
        "name": "slim/slim",
        "version": "3.8.1",
        "version_normalized": "3.8.1.0",
        "source": {
            "type": "git",
            "url": "https://github.com/slimphp/Slim.git",
            "reference": "5385302707530b2bccee1769613ad769859b826d"
        },
        "dist": {
            "type": "zip",
            "url": "https://api.github.com/repos/slimphp/Slim/zipball/538530

</details>

---
*Analysed by Claude on 2026-05-24*
