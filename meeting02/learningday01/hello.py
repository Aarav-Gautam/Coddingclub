import requests
r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
r.status_code()
r.headers['content-type']
'application/json; charset=utf8'
r.encoding
'utf-8'
r.text
'{"authenticated": true,'
r.json()
{'authenticated': True,}




''' 
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

'''