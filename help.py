
f = requests.request('GET', 'http://myip.dnsomatic.com')
ip = f.text
print(ip)