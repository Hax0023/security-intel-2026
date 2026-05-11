#!/usr/bin/env python3
import json,os,re,time,anthropic
from anthropic.lib.credentials._providers import CredentialsFile

creds=json.load(open(os.path.expanduser("~/.claude/.credentials.json")))["claudeAiOauth"]
print("Token expires:",time.strftime("%Y-%m-%d %H:%M",time.localtime(int(creds["expiresAt"]/1000))))

base=os.path.expanduser("~/.config/anthropic")
os.makedirs(base+"/configs",exist_ok=True)
os.makedirs(base+"/credentials",mode=0o700,exist_ok=True)
json.dump({"authentication":{"type":"user_oauth","client_id":"9d1c250a-e61b-44d9-88ed-5944d1962f5e"}},open(base+"/configs/default.json","w"),indent=2)
cf=base+"/credentials/default.json"
d={"version":"1.0","type":"oauth_token","access_token":creds["accessToken"],"refresh_token":creds["refreshToken"],"expires_at":int(creds["expiresAt"]/1000)}
json.dump(d,open(cf,"w"),indent=2)
os.chmod(cf,0o600)
print("Credential files written to",base)

provider=CredentialsFile("default")
client=anthropic.Anthropic(credentials=provider)
resp=client.messages.create(model="claude-haiku-4-5-20251001",max_tokens=10,messages=[{"role":"user","content":"AUTH_OK?"}])
print("Claude says:",resp.content[0].text)
print("OAuth setup complete!")
