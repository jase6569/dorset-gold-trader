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
s = s.replace('const MM_URL = "mastermelt.json";', 'const MM_URL = "../gold-sell-timer/mastermelt.json";')

# Mike's own saved data: his keys are prefixed "dg:" so his app never shares data with Jase's on one phone
MAIN_STORE = """const store = {
  get(k){ try { return localStorage.getItem(k); } catch(e){ return null; } },
  set(k,v){ try { localStorage.setItem(k,v); } catch(e){} },
  del(k){ try { localStorage.removeItem(k); } catch(e){} }
};
"""
MIKE_STORE = '// Keys are prefixed so this app never shares saved data with other Gold Trader copies on the same phone.\nconst SP = "dg:";\nconst store = {\n  get(k){ try { let v = localStorage.getItem(SP + k); if (v === null && !localStorage.getItem(SP + "migrated")) { v = localStorage.getItem(k); } return v; } catch(e){ return null; } },\n  set(k,v){ try { localStorage.setItem(SP + k, v); } catch(e){} },\n  del(k){ try { localStorage.removeItem(SP + k); } catch(e){} }\n};\n// one-off: copy this app\'s earlier saved data into its own keys\ntry { if (!localStorage.getItem(SP + "migrated") && localStorage.getItem("buyingLog") === "1") localStorage.setItem(SP + "migrated", "1");  // a phone with Jase\'s own app: never copy his data\n  if (!localStorage.getItem(SP + "migrated")) { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (!k.startsWith(SP) && !k.includes(":") && localStorage.getItem(SP + k) === null) localStorage.setItem(SP + k, localStorage.getItem(k)); } localStorage.setItem(SP + "migrated", "1"); } } catch(e){}\n'
assert MAIN_STORE in s, "main app's storage block changed: update sync_from_main.py"
s = s.replace(MAIN_STORE, MIKE_STORE)

# Mike's app is his alone: Buy log, Make more money and lot alerts always on, and lot alerts
# go to his usual alert channel (Jase's go to a private one so Adam doesn't get them)
for a, b in [('const PRO_ON = () => store.get("buyingLog") === "1";', 'const PRO_ON = () => true;'),
             ('const LOT_TO_MAIN = false;', 'const LOT_TO_MAIN = true;'),
             ('<p class="sub" id="blNote" style="margin-top:10px;display:none">', '<p class="sub" style="margin-top:10px">'),
             ('<a href="buying-log/" class="navlink" id="blNav" style="display:none">', '<a href="buying-log/" class="navlink">'),
             ('(it starts <b>gt-</b>)', '(it starts <b>dg-</b>)'),
             ('placeholder="gt-…"', 'placeholder="dg-…"')]:
    assert a in s, "main app changed, not found: " + a
    s = s.replace(a, b)
s = re.sub(r'/\* Buying log: only shown on phones where it has been switched on[^\n]*\n[^\n]*\nif \(store\.get\("buyingLog"\) === "1"\)[^\n]*\n', '', s, flags=re.S)

# branding
s = s.replace('<h1>Gold <span>Trader</span></h1>', '<h1>Dorset Gold <span>&amp; Jewellery</span></h1>')
s = s.replace('Dorset Jewellers · when to sell gold · UK, live', 'Gold Trader · when to sell gold · UK, live')
s = s.replace('Dorset Gold &amp; Jewellery · when to sell gold · UK, live', 'Gold Trader · when to sell gold · UK, live')   # main app's name since Nov 2026
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

# Mike's setup checklist at the top of the Guide, with its progress card on the Advice page
here = __import__("os").path.dirname(__file__)
SETUP = open(__import__("os").path.join(here, "mike_setup.html")).read()
SETUP_JS = open(__import__("os").path.join(here, "mike_setup_tail.html")).read()
HELP = '<section class="page" id="p-help">\n'
assert HELP in s and s.count("</body>") == 1, "main app changed: update the setup injection in sync_from_main.py"
s = s.replace(HELP, HELP + SETUP, 1).replace("</body>", SETUP_JS + "</body>", 1)

left = [m for m in ('Dorset Jewellers', 'fetchJSON("data.json', 'fetchJSON("news.json') if m in s]
if left:
    sys.exit("Not fully converted: " + ", ".join(left))
open('index.html', 'w').write(s)
print("index.html updated from the main app")
