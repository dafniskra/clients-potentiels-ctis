"""Génère le dashboard « Clients Potentiels CTIS » à partir d'un export CSV du registre CTIS.

Usage :
    python3 scripts/build_dashboard.py [chemin/vers/export.csv]

Sans argument, prend l'export le plus récent de data/ (CTIS_trials_*.csv).
Produit :
    docs/index.html               dashboard autonome (données intégrées)
    docs/fusions_promoteurs.csv   table des noms de promoteurs fusionnés
Aucune dépendance : bibliothèque standard Python 3.9+.
"""
import csv, re, json, sys, unicodedata, collections as C
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sponsor_groups import key, GROUPS
from synonyms import SYN

csv.field_size_limit(10**9)
REPO = Path(__file__).resolve().parent.parent
if len(sys.argv) > 1:
    SRC = Path(sys.argv[1])
else:
    candidates = sorted((REPO / 'data').glob('CTIS_trials_*.csv'))
    if not candidates:
        sys.exit('Aucun export trouvé : placez un fichier CTIS_trials_AAAAMMJJ.csv dans data/')
    SRC = candidates[-1]


rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))

def pdate(s):
    try: return datetime.strptime(s, '%d/%m/%Y')
    except Exception: return None

def phase_group(p):
    p = p.lower()
    if 'phase i and phase ii' in p: return 'Phase I/II'
    if 'phase ii and phase iii' in p: return 'Phase II/III'
    if 'phase iii and phase iv' in p: return 'Phase III/IV'
    if '(phase iv)' in p: return 'Phase IV'
    if '(phase iii)' in p: return 'Phase III'
    if '(phase ii)' in p: return 'Phase II'
    if '(phase i)' in p: return 'Phase I'
    return 'Other'

class Dict:
    def __init__(self): self.items = []; self.idx = {}
    def __call__(self, v):
        if v not in self.idx: self.idx[v] = len(self.items); self.items.append(v)
        return self.idx[v]

STATUS, PHASE, AREA, COUNTRY = Dict(), Dict(), Dict(), Dict()
T, per_trial, raw_counts = [], [], C.Counter()
for r in rows:
    areas = []
    try: areas = [re.sub(r'\s*\[[^\]]*\]', '', a).replace('Diseases - ', '').strip() for a in json.loads(r['Therapeutic area'])]
    except Exception: pass
    countries = sorted({p.split(':')[0].strip() for p in r['Location(s) and recruitment status'].split(',') if ':' in p})
    ages = r['Age group']
    ag = (1 if '0-17' in ages or 'In utero' in ages else 0) | (2 if '18-64' in ages else 0) | (4 if '65+' in ages else 0)
    ph = r['Trial phase']
    sub = 1 if 'First administration' in ph else (2 if 'Bioequivalence' in ph else 0)
    n = r['Number of participants enrolled']
    d, u = pdate(r['Decision date']), pdate(r['Last updated'])
    T.append([
        r['Trial number'], r['Title of the trial'].strip(), STATUS(r['Overall trial status']), PHASE(phase_group(ph)), sub,
        sorted({AREA(a) for a in areas}), [COUNTRY(c) for c in countries], d.year if d else 0, ag,
        1 if r['Trial results'] == 'Yes' else 0, int(n) if n.isdigit() else 0,
        1 if r['Trial region'].startswith('In both') else 0, u.strftime('%Y-%m-%d') if u else '',
        '' if r['Product'].strip() in ('', 'N/A') else re.sub(r'\s+', ' ', r['Product']).strip(),
        d.strftime('%Y-%m-%d') if d else '',
    ])
    ns = [x.strip() for x in r['Sponsor/Co-Sponsors'].split(', ')]
    ts = [x.strip() for x in r['Sponsor type'].split(', ')]
    if len(ns) != len(ts): ns = [r['Sponsor/Co-Sponsors'].strip()]; ts = [ts[0]]
    per_trial.append(list(zip(ns, ts)))
    for x in set(ns): raw_counts[x] += 1

by_key = C.defaultdict(list)
for x in raw_counts:
    k = key(x)
    g = next((lab for lab, pat in GROUPS if re.search(pat, k)), None)
    by_key[('G', g) if g else ('K', k)].append(x)
canon = {}
for gk, names in by_key.items():
    label = gk[1] if gk[0] == 'G' else max(names, key=lambda x: (raw_counts[x], x))
    for x in names: canon[x] = label

agg = {}
for i, pairs in enumerate(per_trial):
    seen = set()
    for x, t in pairs:
        c = canon[x]
        if c in seen: continue
        seen.add(c)
        a = agg.setdefault(c, dict(t=[], types=C.Counter(), ent=C.Counter(), prods=[]))
        a['t'].append(i); a['types'][t] += 1; a['ent'][x] += 1
        p = rows[i]['Product'][:60]
        if p and p != 'N/A' and p not in a['prods']: a['prods'].append(p)

PHARMA = {'Pharmaceutical company', 'Industry', 'SME', 'Non-Pharmaceutical company'}
S = []
for name, a in agg.items():
    typ = a['types'].most_common(1)[0][0]
    rec = dict(name=name, type=typ, ph=typ in PHARMA, t=a['t'], pr=a['prods'][:3])
    if len(a['ent']) > 1: rec['ent'] = [[x, c] for x, c in a['ent'].most_common()]
    S.append(rec)

# ---- produits : suggestions + synonymes marque/DCI
def norm(x): return ''.join(ch for ch in unicodedata.normalize('NFD', x.lower()) if unicodedata.category(ch) != 'Mn')
PN = [norm(t[13]) for t in T]
STOP = re.compile(r'placebo|solution|saline|sodium chloride|chlorure|poudre|powder|comprim|tablet|capsule|g[eé]lule|suspension|l[oö]sning|opl[oø]sning|injection|injectable|infusion|perfusion|concentrat|emulsion|cream|creme|ointment|vehicle|diluent|water for|^bi$|^bay$|vaccine$|^the |^for ', re.I)
def base(x):
    x = re.split(r'\s+\d|\s*\(|\s*,|\s+(?:film|tablet|capsule|solution|concentrate|powder|injection|oral|for |comprim|poudre|g[eé]lule)', x.strip(), 1, flags=re.I)[0]
    return x.strip(' .-/')
cnt = C.Counter()
for t in T:
    if t[13]: cnt.update({base(x).upper() for x in t[13].split(', ') if base(x)})
sugg = {}
for name, c in cnt.most_common():
    if c < 3 or len(name) < 4 or not re.match(r'^[A-ZÀ-Ý]', name) or STOP.search(name): continue
    sugg.setdefault(norm(name), [name.title() if not re.search(r'\d', name) else name, c])
for group in SYN:
    for m in group:
        k = norm(m)
        n = sum(1 for p in PN if any(norm(g) in p for g in group))
        if n: sugg[k] = [m.title(), n]
SUGG = sorted(sugg.values(), key=lambda x: (-x[1], x[0]))[:900]
# ---- sponsor details from the CTIS API (scripts/fetch_contacts.py), when available
# Public build: organisation data only (HQ city/country, third parties).
# Private build: also the contact points, which can name people (GDPR) -> private/ (git-ignored).
CONTACTS = REPO / 'data' / 'private' / 'contacts.json'
details = json.loads(CONTACTS.read_text(encoding='utf-8')) if CONTACTS.exists() else {}
PRIVATE_CT = {}
for s_ in S:
    d = details.get(s_['name'])
    if not d or d.get('not_found'):
        continue
    if d.get('country'): s_['hq'] = d['country']
    if d.get('city'): s_['city'] = d['city']
    s_['tp'] = d.get('third_parties', [])[:12]
    s_['tpn'] = len(d.get('third_parties', []))
    ct = list(d.get('contacts', []))
    if d.get('org_email') or d.get('org_phone'):
        org = {'type': 'Organisation', 'email': d.get('org_email'), 'phone': d.get('org_phone')}
        ct.append({k: v for k, v in org.items() if v})
    if ct: PRIVATE_CT[s_['name']] = ct

tpl = (REPO / 'src' / 'template.html').read_text(encoding='utf-8')
assert tpl.count('__DATA__') == 1

def render_page(data):
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    body = tpl.replace('__DATA__', js)
    # full HTML document: <title>/<style> go in the head, the rest in the body
    cut = body.index('</style>') + len('</style>')
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            + body[:cut] + '\n</head>\n<body>\n' + body[cut:] + '\n</body>\n</html>\n')

DATA = dict(T=T, S=S, syn=[[norm(m) for m in g] for g in SYN], sugg=SUGG, status=STATUS.items, phase=PHASE.items, area=AREA.items, country=COUNTRY.items)
html = render_page(DATA)
out = REPO / 'docs'
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(html, encoding='utf-8')

if PRIVATE_CT:
    priv_dir = REPO / 'private'
    priv_dir.mkdir(exist_ok=True)
    S_priv = [dict(s_, ct=PRIVATE_CT[s_['name']]) if s_['name'] in PRIVATE_CT else s_ for s_ in S]
    (priv_dir / 'prospects_with_contacts.html').write_text(render_page(dict(DATA, S=S_priv, private=True)), encoding='utf-8')

# table de correspondance des fusions, pour relecture
with open(out / 'fusions_promoteurs.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Merged name', 'Original CTIS name', 'Trials (original name)'])
    for s_ in sorted(S, key=lambda s_: -len(s_['t'])):
        for n, c in s_.get('ent', []):
            w.writerow([s_['name'], n, c])

print(f"Source : {SRC.name}")
print(f"{len(T)} essais, {len(S)} promoteurs ({sum('ent' in s_ for s_ in S)} groupes fusionnés)")
print(f"-> {out / 'index.html'} ({len(html) / 1e6:.1f} MB)")
print(f"-> {out / 'fusions_promoteurs.csv'}")
print(f"Sponsor details (CTIS API): {sum('hq' in s_ for s_ in S)} sponsors, contacts for {len(PRIVATE_CT)}")
if PRIVATE_CT:
    print(f"-> {REPO / 'private' / 'prospects_with_contacts.html'} (private: never commit or publish)")
