## Run CloudflareSpeedTest and Update IP in NextDNS Automatically

This is a python script that updates the IP (rewrite rules) of given domains in NextDNS to use best CloudFlare IP from CloudflareSpeedTest result

### Requirements

- NextDNS account: https://my.nextdns.io/

- CloudflareSpeedTest windows binary:

  - Source code: https://github.com/XIU2/CloudflareSpeedTest
  - Latest Release: https://github.com/XIU2/CloudflareSpeedTest/releases/latest

- Python3 installed

- DNS over HTTPS support (will use firefox as example here)

### How to use...

- Extract the CloudflareSpeedTest windows release zip

- Clone this repo to that extracted folder

  ```
  git clone https://github.com/shovon668/cfst_nextdns .
  ```

- Rename "nextdns_sample.txt" to "nextdns.txt"

- Config the "nextdns.txt" and save it. It should look something like this:

  ```
  nextDNS_email = "example@example.com"
  nextDNS_password = "$SuPpErStRoNgP@ssOrD#"
  nextDNS_id = "sm123"
  target_domains = ["exampledomain1.com", "exampledomain2.com", "exampledomain3.com", "and so on..."]
  ```

- Goto firefox and enable DoH and use your NextDNS DoH endpoint

- Double click RUN.bat, wait for few minutes. Check NextDNS rewrite rule when finished. The IP should be the top ip of result.csv

#### Credits:

- https://github.com/XIU2/CloudflareSpeedTest

- https://github.com/rhijjawi/NextDNS-API
