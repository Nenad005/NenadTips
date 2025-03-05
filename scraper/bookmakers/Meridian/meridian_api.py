import json
import sys
import requests
sys.path.insert(1, '../')
from bookmaker import Bookmaker
import time


s = requests.Session()

headers=  {
    "accept" : 'application/json, text/plain, */*',
    "accept-language" : 'sr',
    "authorization" : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjoiMTAwMDAyIiwidXNlcl9uYW1lIjoiZTA4MzMwNzMtMWMxZC00NzQ5LThlZWQtZjg4ZjgzY2UzYmQ1OWZlZjhmNTMtMzRlNi00MTNlLTgyZjctMDBkZWJlMTIxYzQ5IiwiZW1waXJlYmV0X2NvbXBhbnlfaWQiOiIxIiwiYmV0c2hvcF9pZCI6IjEwMDkyNSIsIm1hcmtldF9pZCI6IjEwMDI0NSIsInNlc3Npb25faWQiOiJlMDgzMzA3My0xYzFkLTQ3NDktOGVlZC1mODhmODNjZTNiZDU5ZmVmOGY1My0zNGU2LTQxM2UtODJmNy0wMGRlYmUxMjFjNDkiLCJjcmVhdGVkX2F0IjoxNzQxMTk2MTAyODY3LCJhdXRob3JpdGllcyI6WyJhY2NvdW50Il0sInBsYXRmb3JtIjoiV0VCX0RFU0tUT1AiLCJjbGllbnRfaWQiOiJ3ZWItc2VyYmlhIiwiZW1waXJlYmV0X2JldHNob3BfaWQiOiIxNjc3IiwiYXVkIjpbImFjY291bnQiXSwiZXhwaXJlc19hdCI6MTc0MTE5OTcwMjg2NywiZW1waXJlYmV0X21hcmtldF9pZCI6IjEwOSIsInNjb3BlIjpbIkdFTkVSQUwiXSwiZXhwIjoxNzQxMTk5NzAyLCJqdGkiOiJmNzZjZDJiMC1iZDM2LTRjMjgtYTkwYy01OGE3OWNiOWY1YmEifQ.KQblMq7ReYkJyjzp8OqPUKH_mfQEp89swIU4VhsvARk',
    "origin" : 'https//meridianbet.rs',
    "priority" : 'u=1, i',
    "referer" : 'https//meridianbet.rs/',
    "sec-ch-ua" : '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile" : '?0',
    "sec-ch-ua-platform" : '"Windows"',
    "sec-fetch-dest" : 'empty',
    "sec-fetch-mode" : 'cors',
    "sec-fetch-site" : 'cross-site',
    "user-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

leagues = []
page = 0
print(f"Requesting page {page} . . .")
response = s.get(url=f"https://online.meridianbet.com/betshop/api/v1/standard/sport/58/leagues?page={page}&time=THREE_DAYS", headers=headers)
content = json.loads(response.content)
while response.status_code == 200 and len(content["payload"]["leagues"]) > 0:
    leagues.extend(content["payload"]["leagues"])
    time.sleep(1)
    page +=1 
    print(f"Requesting page {page} . . .")
    response = s.get(url=f"https://online.meridianbet.com/betshop/api/v1/standard/sport/58/leagues?page={page}&time=THREE_DAYS", headers=headers)
    content = json.loads(response.content)

if (response.status_code != 200):
    print(f"Greska : {response.status_code}")

print(response)
with open("response.txt", "w") as f:
    json.dump(leagues, f)