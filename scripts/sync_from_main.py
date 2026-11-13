"""Bring this app up to date with the main Gold Trader app, keeping Mike's own look.

Usage: python scripts/sync_from_main.py ../gold-sell-timer/index.html

Copies the main app's page and changes only the branding (name, logo text,
navy colours), the widget download link, and where the price data is read from
(the main app's hourly data). Everyone's "My gold" entries stay on their own
phone and are never shared.
"""
import re
import sys

src = open(sys.argv[1]).read()
s = src

# where the hourly data comes from (the main app, same site)
s = s.replace('fetchJSON("data.json?', 'fetchJSON("../gold-sell-timer/data.json?')
s = s.replace('fetchJSON("news.json?', 'fetchJSON("../gold-sell-timer/news.json?')

# branding
s = s.replace('<h1>Gold <span>Trader</span></h1>', '<h1>Dorset Gold <span>&amp; Jewellery</span></h1>')
s = s.replace('Dorset Jewellers · when to sell gold · UK, live', 'Gold Trader · when to sell gold · UK, live')
s = s.replace('<title>Gold Trader</title>', '<title>Dorset Gold &amp; Jewellery · Gold Trader</title>')
s = s.replace('<meta name="apple-mobile-web-app-title" content="Gold Trader">', '<meta name="apple-mobile-web-app-title" content="Dorset Gold">')
s = s.replace('Dorset Jewellers icon', 'Dorset Gold &amp; Jewellery icon')
s = s.replace('alt="Dorset Jewellers"', 'alt="Dorset Gold &amp; Jewellery"')
s = s.replace('Dorset Jewellers', 'Dorset Gold &amp; Jewellery')

# Mike's widget app
cur = re.search(r'gold-trader-widget-v[0-9-]+\.apk', open('index.html').read())
s = re.sub(r'gold-trader-widget-v[0-9-]+\.apk', cur.group(0) if cur else 'gold-trader-widget-v1-1.apk', s)

# navy colour scheme
cmap = {'#0f0e0c': '#0a1020', '#1a1815': '#121a2e', '#12110f': '#0d1426', '#2c2924': '#233050', '#1f1d19': '#18213a',
        '#a39d90': '#9aa6bf', '#f3efe6': '#eef2f8', '#3a3630': '#2a3552', '#7d776b': '#7a86a0', '#cfc8b8': '#c7cfdf',
        '#7d9cc4': '#c0c8d6', '#6b655a': '#5a6580', '#8a8478': '#7a86a0', '#24211d': '#1a2440'}
for a, b in cmap.items():
    s = re.sub(re.escape(a), b, s, flags=re.I)
s = s.replace('rgba(15,14,12,', 'rgba(10,16,32,').replace('rgba(26,24,21,1)', 'rgba(18,26,46,1)')

left = [m for m in ('Dorset Jewellers', 'fetchJSON("data.json', 'fetchJSON("news.json') if m in s]
if left:
    sys.exit("Not fully converted: " + ", ".join(left))
open('index.html', 'w').write(s)
print("index.html updated from the main app")
