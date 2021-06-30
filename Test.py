
"All we need for API is these 4 lines"


import requests

data=requests.get("http://api.open-notify.org/astros.json")
parsed_data=data.json()
print(parsed_data)

for i in parsed_data["people"]:
    print(i["name"])