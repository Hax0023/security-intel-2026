# Reflected XSS on developers.zomato.com via Swagger UI

## Metadata
- **Source:** HackerOne
- **Report:** 418823 | https://hackerone.com/reports/418823
- **Submitted:** 2018-10-04
- **Reporter:** areizen
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Unpatched Component Vulnerability
- **CVEs:** None
- **Category:** web-api

## Summary
The developers.zomato.com documentation endpoint uses an outdated version of Swagger UI vulnerable to reflected XSS attacks. An attacker can inject malicious payloads through the swagger specification endpoint that get rendered without proper sanitization, allowing arbitrary JavaScript execution in the victim's browser.

## Attack scenario
1. Attacker identifies that developers.zomato.com/documentation uses an old Swagger UI version
2. Attacker crafts a malicious Swagger specification JSON containing XSS payloads in fields like description, title, or other metadata fields
3. Attacker creates a phishing link pointing to the documentation endpoint with the malicious swagger spec as a parameter
4. Developer clicks the malicious link, causing the Swagger UI to render the attacker's payload
5. JavaScript payload executes in the victim's browser context with access to their session/credentials
6. Attacker can steal authentication tokens, session cookies, or perform actions on behalf of the victim

## Root cause
The Swagger UI version deployed on developers.zomato.com contains an unpatched XSS vulnerability in its JSON parsing and rendering logic. The application fails to properly sanitize user-controlled input from the swagger specification before rendering it as HTML, allowing script injection through various specification fields.

## Attacker mindset
An attacker targeting developer communities recognizes that Swagger/OpenAPI documentation pages are frequently accessed and trusted by developers. They exploit the trust placed in official documentation platforms, using outdated dependencies as a vector for credential theft or malware distribution. The use of standard tooling (Swagger UI) makes the attack surface less obvious to defenders.

## Defensive takeaways
- Maintain up-to-date versions of all frontend frameworks and UI libraries, especially those processing user or external data
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Sanitize all user-controlled and external input before rendering as HTML, regardless of expected format
- Use security scanning tools to identify outdated or vulnerable dependencies in CI/CD pipelines
- Apply output encoding based on context (HTML encoding, JavaScript encoding, URL encoding)
- Conduct regular security audits of API documentation platforms which are high-value attack targets
- Consider using a Software Composition Analysis (SCA) tool to track third-party vulnerabilities

## Variant hunting
Search for other endpoints using Swagger UI or similar documentation frameworks on Zomato's infrastructure. Check for similar XSS vulnerabilities in other versions of Swagger UI across different Zomato subdomains. Investigate if the vulnerability exists in cached or archived versions of the documentation. Test other API documentation tools (ReDoc, Rapidoc) for similar injection vectors.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539

## Notes
The report demonstrates the critical importance of dependency management in security-sensitive applications. Swagger UI is widely used and frequently targeted. The vulnerability likely affects the 'url' parameter in the Swagger specification, which old versions may render without sanitization. This type of vulnerability on a developer platform is particularly dangerous as it targets technical users who may have elevated privileges or access to sensitive systems.

## Full report
<details><summary>Expand</summary>

There is a vulnerability in [https://developers.zomato.com/documentation](https://developers.zomato.com/documentation) due to an old version of Swagger UI

**Step to reproduce:**
- Create an endpoint containing : 
```json
{"swagger":"2.0","info":{"description":"This is a sample server Petstore server.  You can find out more about Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).  For this sample, you can use the api key `special-key` to test the authorization filters.","version":"1.0.0","title":"Swagger Petstore","termsOfService":"http://swagger.io/terms/","contact":{"email":"apiteam@swagger.io"},"license":{"name":"Apache 2.0","url":"http://www.apache.org/licenses/LICENSE-2.0.html"}},"host":"localhost:4567","basePath":"/v2","tags":[{"name":"pet","description":"Everything about your Pets","externalDocs":{"description":"Find out more","url":"http://swagger.io"}},{"name":"store","description":"Access to Petstore orders"},{"name":"user","description":"Operations about user","externalDocs":{"description":"Find out more about our store","url":"http://swagger.io"}}],"schemes":["http"],"paths":{"/pet":{"post":{"tags":["pet"],"summary":"Add a new pet to the store","description":"","operationId":"addPet","consumes":["application/json","application/xml"],"produces":["application/xml","application/json"],"parameters":[{"in":"body","name":"body","description":"Pet object that needs to be added to the store","required":true,"schema":{"$ref":"#/definitions/Pet"}}],"responses":{"405":{"description":"Invalid input"}},"security":[{"petstore_auth":["write:pets","read:pets"]}]},"put":{"tags":["pet"],"summary":"Update an existing pet","description":"","operationId":"updatePet","consumes":["application/json","application/xml"],"produces":["application/xml","application/json"],"parameters":[{"in":"body","name":"body","description":"Pet object that needs to be added to the store","required":true,"schema":{"$ref":"#/definitions/Pet"}}],"responses":{"400":{"description":"Invalid ID supplied"},"404":{"description":"Pet not found"},"405":{"description":"Validation exception"}},"security":[{"petstore_auth":["write:pets","read:pets"]}]}},"/pet/findByStatus":{"get":{"tags":["pet"],"summary":"Finds Pets by status","description":"Multiple status values can be provided with comma separated strings","operationId":"findPetsByStatus","produces":["application/xml","application/json"],"parameters":[{"name":"status","in":"query","description":"Status values that need to be considered for filter","required":true,"type":"array","items":{"type":"string","enum":["available","pending","sold"],"default":"available"},"collectionFormat":"multi"}],"responses":{"200":{"description":"successful operation","schema":{"type":"array","items":{"$ref":"#/definitions/Pet"}}},"400":{"description":"Invalid status value"}},"security":[{"petstore_auth":["write:pets","read:pets"]}]}},"/pet/findByTags":{"get":{"tags":["pet"],"summary":"Finds Pets by tags","description":"Muliple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing.","operationId":"findPetsByTags","produces":["application/xml","application/json"],"parameters":[{"name":"tags","in":"query","description":"Tags to filter by","required":true,"type":"array","items":{"type":"string"},"collectionFormat":"multi"}],"responses":{"200":{"description":"successful operation","schema":{"type":"array","items":{"$ref":"#/definitions/Pet"}}},"400":{"description":"Invalid tag value"}},"security":[{"petstore_auth":["write:pets","read:pets"]}],"deprecated":true}},"/pet/{petId}":{"get":{"tags":["pet"],"summary":"Find pet by ID","description":"Returns a single pet","operationId":"getPetById","produces":["application/xml","application/json"],"parameters":[{"name":"petId","in":"path","description":"ID of pet to return","required":true,"type":"integer","format":"int64"}],"responses":{"200":{"description":"successful operation","schema":{"$ref":"#/definitions/Pet"}},"400":{"description":"Invalid ID supplied"},"404":{"description":"Pet not found"}},"security":[{"api_key":[]}]},"post":{"tags":["pet"],"summary":"Updates a pet in the store with form data","description":"","operationId":"updatePetWithForm","consumes":["application/x-www-form-urlencoded"],"produces":["application/xml","application/json"],"parameters":[{"name":"petId","in":"path","description":"ID of pet that needs to be updated","required":true,"type":"integer","format":"int64"},{"name":"name","in":"formData","description":"Updated name of the pet","required":false,"type":"string"},{"name":"status","in":"formData","description":"Updated status of the pet","required":false,"type":"string"}],"responses":{"405":{"description":"Invalid input"}},"security":[{"petstore_auth":["write:pets","read:pets"]}]},"delete":{"tags":["pet"],"summary":"Deletes a pet","description":"","operationId":"deletePet","produces":["application/xml","application/json"],"parameters":[{"name":"api_key","in":"header","required":false,"type":"string"},{"name":"petId","in":"path","description":"Pet id to delete","required":true,"type":"integer","format":"int64"}],"responses":{"400":{"description":"Invalid ID supplied"},"404":{"description":"Pet not found"}},"security":[{"petstore_auth":["write:pets","read:pets"]}]}},"/pet/{petId}/uploadImage":{"post":{"tags":["pet"],"summary":"uploads an image","description":"","operationId":"uploadFile","consumes":["multipart/form-data"],"produces":["application/json"],"parameters":[{"name":"petId","in":"path","description":"ID of pet to update","required":true,"type":"integer","format":"int64"},{"name":"additionalMetadata","in":"formData","description":"Additional data to pass to server","required":false,"type":"string"},{"name":"file","in":"formData","description":"file to upload","required":false,"type":"file"}],"responses":{"200":{"description":"successful operation","schema":{"$ref":"#/definitions/ApiResponse"}}},"security":[{"petstore_auth":["write:pets","read:pets"]}]}},"/store/inventory":{"get":{"tags":["store"],"summary":"Returns pet inventories by status","description":"Returns a map of status codes to quantities","operationId":"getInventory","produces":["application/json"],"parameters":[],"responses":{"200":{"description":"successful operation","schema":{"type":"object","additionalProperties":{"type":"integer","format":"int32"}}}},"security":[{"api_key":[]}]}},"/store/order":{"post":{"tags":["store"],"summary":"Place an order for a pet","description":"","operationId":"placeOrder","produces":["application/xml","application/json"],"parameters":[{"in":"body","name":"body","description":"order placed for purchasing the pet","required":true,"schema":{"$ref":"#/definitions/Order"}}],"responses":{"200":{"description":"successful operation","schema":{"$ref":"#/definitions/Order"}},"400":{"description":"Invalid Order"}}}},"/store/order/{orderId}":{"get":{"tags":["store"],"summary":"Find purchase order by ID","description":"For valid response try integer IDs with value >= 1 and <= 10. Other values will generated exceptions","operationId":"getOrderById","produces":["application/xml","application/json"],"parameters":[{"name":"orderId","in":"path","description":"ID of pet that needs to be fetched","required":true,"type":"integer","maximum":10.0,"minimum":1.0,"format":"int64"}],"responses":{"200":{"description":"successful operation","schema":{"$ref":"#/definitions/Order"}},"400":{"description":"Invalid ID supplied"},"404":{"description":"Order not found"}}},"delete":{"tags":["store"],"summary":"Delete purchase order by ID","description":"For valid response try integer IDs with positive integer value. Negative or non-integer values will generate API errors","operationId":"deleteOrder","produces":["application/xml","application/json"],"parameters":[{"name":"orderId","in":"path","description":"ID of the order that needs to be deleted","required":true,"type":"integer","minimum":1.0,"format":"int64"}],"responses":{"400":{"descrip

</details>

---
*Analysed by Claude on 2026-05-12*
