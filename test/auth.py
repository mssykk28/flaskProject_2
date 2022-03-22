import http.client

conn = http.client.HTTPSConnection("dev-2jun8kx9.us.auth0.com")

payload = "{\"client_id\":\"uvH95PfQpY3wzcufeQ8pkUssiJ7C09oZ\"," \
          "\"client_secret\":\"tTaFIjDxhZCR1KdYisLBDJz2KDzPlnp-Slnv4JyIcMLEXxR6gTPhbjC__YVM2o-p\"," \
          "\"audience\":\"http://127.0.0.1:5000/auth\",\"grant_type\":\"client_credentials\"}"

headers = {"content-type": "application/json"}

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
