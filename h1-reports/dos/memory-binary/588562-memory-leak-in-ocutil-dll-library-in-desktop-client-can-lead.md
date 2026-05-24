# Memory Leak in OCUtil.dll IsChildFile Function Leading to Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 588562 | https://hackerone.com/reports/588562
- **Submitted:** 2019-05-23
- **Reporter:** cwave
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Memory Leak, Denial of Service, Resource Exhaustion
- **CVEs:** CVE-2020-8229
- **Category:** memory-binary

## Summary
The IsChildFile function in OCUtil.dll (FileUtil.cpp) allocates memory on line 42 but fails to properly deallocate it, causing unbounded memory consumption. An attacker can repeatedly invoke this function via the Windows Explorer context menu to exhaust memory and crash the explorer.exe process.

## Attack scenario
1. Attacker obtains access to a system running Nextcloud Windows client with OCUtil.dll installed
2. Attacker loads OCUtil_x64.dll and obtains function pointer to IsChildFile via GetProcAddress
3. Attacker calls IsChildFile repeatedly in a loop with specially crafted long file path arguments
4. Each function call allocates memory that is never freed, causing heap growth
5. System memory becomes depleted and explorer.exe crashes due to out-of-memory condition
6. User experiences denial of service with Windows Explorer becoming unresponsive

## Root cause
The IsChildFile function allocates memory dynamically but does not properly deallocate it in all code paths. The function likely allocates memory for path processing or string manipulation without corresponding deallocation before function return.

## Attacker mindset
An attacker seeking to disrupt user workflow would recognize that library functions exposed through Windows Explorer integration provide a reliable trigger point for memory exhaustion. By exploiting context menu functionality, the attack can be performed through normal user interactions without requiring elevated privileges.

## Defensive takeaways
- Implement automatic memory management (smart pointers) in C++ code to prevent manual deallocation errors
- Use static code analysis tools to detect memory leaks before shipping
- Implement memory limits or throttling for repeated function calls in context menu handlers
- Audit all dynamic memory allocations to ensure corresponding deallocations in all code paths
- Consider using memory profiling tools during development and QA testing
- Implement error handling and resource cleanup in exception paths
- Validate and sanitize file path inputs to prevent excessive processing

## Variant hunting
Search for other functions in OCUtil.dll that perform path manipulation without proper memory cleanup
Examine FileUtil.cpp for similar patterns where memory is allocated but not freed
Test other Nextcloud client library functions that accept file path parameters
Review context menu handler implementations for similar issues
Check for other instances of wchar_t buffer allocation in file utility functions

## MITRE ATT&CK
- T1499.004
- T1499

## Notes
The vulnerability requires the Nextcloud Windows client to be installed. The PoC demonstrates the leak can be triggered through direct library loading and repeated function calls. The impact is elevated due to the function being used by explorer.exe for context menu functionality, making it accessible to any local user. The researcher provided working PoC code and affected binaries, enabling easy reproduction.

## Full report
<details><summary>Expand</summary>

The function IsChildFile(const wchar_t* rootFolder, const wchar_t* file) in FileUtil.cpp allocates memory on line 42 and fails to free it.

The following PoC code can provide evidence. The code and the PoC executable is attached to this report. Also OCUtils.dll and OCUtils_x64.dll library which is delivered with Nextclound Windows installer was included in the attachment.

Steps to reproduce:
1. Launch tests.exe (see attachment) or compile the attached VS2017 solution and launch the resulted executable
2. Make sure OCUtil_x64 library is in the System library path
3. Open Windows Task Manager and watch how the amount of memory for tests.exe process is increasing.

A Visual Studio debugging session screenshot is also attached whre you can see the memory in use.

#include "pch.h"
#include <iostream>
#include <windows.h>

typedef bool(__cdecl *f_IsChildFile)(const wchar_t* rootFolder, const wchar_t* file);

int main()
{
	HINSTANCE hGetProcIDDLL = LoadLibrary(L"OCUtil_x64.dll");

	if (!hGetProcIDDLL) {
		std::cout << "could not load the dynamic library" << std::endl;
		return EXIT_FAILURE;
	}

	f_IsChildFile isChildFile = (f_IsChildFile)GetProcAddress(hGetProcIDDLL, "?IsChildFile@FileUtil@@SA_NPEB_W0@Z");
	if (!isChildFile) {
		std::cout << "could not locate the function" << std::endl;
		return EXIT_FAILURE;
	}

	std::cout << "Function is at " << isChildFile;

	const wchar_t * folder = L"C:\\TestFolder";
	const wchar_t * file = L"C:\\As they rounded a bend in the path that ran beside the river, Lara recognized the silhouette of a fig tree atop a nearby hill. The weather was hot and the days were long. The fig tree was in full leaf, but not yet bearing fruit. Soon Lara spotted other";

	bool res; 

	while (1) {
		res = isChildFile(folder, file);
		std::cout << res << "\n";
	}

	return 0;
}

## Impact

Memory leaks have two common and sometimes overlapping causes:

- Error conditions and other exceptional circumstances.

- Confusion over which part of the program is responsible for freeing the memory.

In this case, the memory allocated in FileUtil.cpp at line 42 is not always freed or returned by the function.

Most memory leaks result in general software reliability problems, but if an attacker can intentionally trigger a memory leak, the attacker may be able to launch a denial of service attack (by crashing the program) or take advantage of other unexpected program behavior resulting from a low memory condition 

The function IsChildFile(const wchar_t* rootFolder, const wchar_t* file) is part of OCUtil.dll library which is delivered with Nextcloud Windows installer and it is loaded in explorer.exe process in order to provide context menu functionalities. 
By using the context menu functionality multiple times, explorer.exe could pottentialy run out of memory.

</details>

---
*Analysed by Claude on 2026-05-24*
