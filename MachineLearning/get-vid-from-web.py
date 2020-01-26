import re
import requests
from bs4 import BeautifulSoup

site = 'http://192.168.1.114:8000/index.html'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]

#for url in urls:
#	print(url)
#	filename = re.search(r'/([\w_-]+[.](mjpg|jpg|gif|png))$', url)
#	with open(filename.group(1), 'wb') as f:
#		if 'http' not in url:
			# sometimes an image source can be relative 
			# if it is provide the base url which also happens 
			# to be the site variable atm. 
url = 'http://192.168.1.114:8000/stream.mjpg' 
print(url)
response = requests.get(url)

print(response.content)
f.write(response.content)

