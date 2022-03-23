import http.client

conn = http.client.HTTPSConnection("dev-2jun8kx9.us.auth0.com")

payload = "{\"client_id\":\"hoge\"," \
          "\"client_secret\":\"hoge\"," \
          "\"audience\":\"http://127.0.0.1:5000/auth\",\"grant_type\":\"client_credentials\"}"

headers = {"content-type": "application/json"}

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
