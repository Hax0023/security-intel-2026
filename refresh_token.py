import json,os,time,requests
CF=os.path.expanduser("~/.claude/.credentials.json")
SF=os.path.expanduser("~/.config/anthropic/credentials/default.json")
URL="https://api.anthropic.com/v1/oauth/token"
CID="9d1c250a-e61b-44d9-88ed-5944d1962f5e"
def main():
 full=json.load(open(CF)); oa=full["claudeAiOauth"]
 hrs=(int(oa["expiresAt"])/1000-time.time())/3600
 if hrs>1: print(f"OK {hrs:.1f}h left"); return
 print("Refreshing...")
 r=requests.post(URL,
  json={"grant_type":"refresh_token","refresh_token":oa["refreshToken"],"client_id":CID},
  headers={"Content-Type":"application/json","anthropic-beta":"oauth-2025-04-20"},
  timeout=20)
 r.raise_for_status(); d=r.json()
 ei=d.get("expires_in",28800)
 oa["accessToken"]=d["access_token"]
 oa["refreshToken"]=d.get("refresh_token",oa["refreshToken"])
 oa["expiresAt"]=int((time.time()+ei)*1000)
 full["claudeAiOauth"]=oa; json.dump(full,open(CF,"w"),indent=2)
 sk=json.load(open(SF)) if os.path.exists(SF) else {}
 sk.update({"version":"1.0","type":"oauth_token","access_token":oa["accessToken"],"refresh_token":oa["refreshToken"],"expires_at":int(time.time()+ei)})
 json.dump(sk,open(SF,"w"),indent=2); os.chmod(SF,0o600)
 exp=time.strftime("%Y-%m-%d %H:%M",time.localtime(oa["expiresAt"]//1000))
 print("Token refreshed. New expiry: "+exp)
main()
