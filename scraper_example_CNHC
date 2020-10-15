!pip install requests_html
from requests_html import HTMLSession

session = HTMLSession()

r = session.get('https://www.otcmarkets.com/stock/CNHC/security')
r.html.render(sleep=1)

print(r.html.find('div'))
