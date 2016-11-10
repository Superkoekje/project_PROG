import http.client, urllib

user = "uttiio3bxkq154v1muwo1be5avonrn"
message = "shoop die doo"

conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "a317qx6onvf1ziwvvrrevzjh38boei",
    "user": user,
    "message": message,
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
