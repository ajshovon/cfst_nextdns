import requests

headers = {
    """Accept""": """application/json, text/plain, */*""",
    """Accept-Language""": """en-US,en;q=0.5""",
    """Content-Type""": """application/json""",
    """Origin""": """https://my.nextdns.io""",
    """DNT""": """1""",
    """Connection""": """keep-alive""",
    """Referer""": """https://my.nextdns.io/""",
    """Sec-Fetch-Dest""": """empty""",
    """Sec-Fetch-Mode""": """cors""",
    """Sec-Fetch-Site""": """same-site""",
    """Sec-GPC""": """1""",
    """TE""": """trailers""",
}


# for adding and delete rewrite rules

class rewrite:
    def delete_rule(config, header, idd):
        try:
            response = requests.delete(
                f"https://api.nextdns.io/configurations/{config}/settings/rewrites/{idd}", headers=header)
        except:
            print("Unable to delete rule. HTTP response", response.status_code)

    def add_rule(domain, answer, config, header):
        re_data = {"name": domain, "answer": answer, }
        try:
            response = requests.post(
                f"https://api.nextdns.io/configurations/{config}/settings/rewrites", headers=header, json=re_data)
        except:
            print("Unable to add rule. HTTP response", response.status_code)

# from https://github.com/rhijjawi/NextDNS-API


class account:
    def login(email: str = None, password: str = None, otp: str = None):
        if (email == None or password == None) or (email == None and password == None):
            raise ValueError("No username & password provided")
        else:
            success = False
            json = {"email": f"{email}", "password": f"{password}"}
            while success == False:
                login = requests.post(
                    'https://api.nextdns.io/accounts/@login', headers=headers, json=json)
                if login.text == "OK":
                    success = 1
                elif login.text == """{"requiresCode":true}""":
                    code = otp or input("""Please enter 2FA Code: """)
                    json = {"email": f"{email}",
                            "password": f"{password}", "code": f"{code}"}
                    login = requests.post(
                        'https://api.nextdns.io/accounts/@login', headers=headers, json=json)
                else:
                    raise Exception("Login error!")
            c = login.cookies.get_dict()
            c = c['pst']
            headers['Cookie'] = f'pst={c}'
        return headers


class settings:
    def listsettings(config, header):
        list = requests.get(
            f"https://api.nextdns.io/configurations/{config}/settings", headers=header)
        if list.text == "Not Found":
            raise ValueError("Not Found")
        else:
            list = list.json()
            return list


# read the top speed
f = open("result.csv", "r", encoding='utf-8')
lines = f.readlines()[1]
lines = lines.split(',')[0]
top = lines
f.close()

# read config
config_file = open("nextdns.txt", "r", encoding='utf-8')
config = config_file.readlines()

nextdns_email = config[0].split('=')[1].replace('"', "")
nextdns_pass = config[1].split('=')[1].replace('"', "")
nextdns_id = config[2].split('=')[1].replace('"', "")
target_domains = config[3].split('=')[1].replace(
    '[', "").replace(']', "").replace('"', "").split(",")

try:
    nextdns_email = nextdns_email.replace('\n', '')
except:
    pass

try:
    nextdns_pass = nextdns_pass.replace('\n', '')
except:
    pass

try:
    nextdns_pass = nextdns_pass.replace('\n', '')
except:
    pass


config_file.close()

# config
header = account.login(nextdns_email.strip(), nextdns_pass.strip())
config_id = nextdns_id.strip()
r = settings.listsettings(config_id, header)

# delete old rewrite rule
try:
    re_ids = r['rewrites']
except:
    pass
else:
    for re_id in re_ids:
        rewrite.delete_rule(config_id, header, re_id['id'])


# add new rewrite rules
try:
    for domain in target_domains:
        rewrite.add_rule(domain.strip(), top, config_id, header)
except:
    print("Could not add new rewrite rule!")
