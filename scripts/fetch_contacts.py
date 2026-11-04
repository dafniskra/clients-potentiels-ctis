"""Collects sponsor details from the public CTIS API for target sponsors.

For each target sponsor (10 trials or fewer in CTIS), the script fetches its most
recently updated trial from https://euclinicaltrials.eu/ctis-public-api/retrieve/<number>
and keeps:
  - headquarters city and country of the sponsor organisation (public, organisation data)
  - third parties named on the trial, e.g. CROs (public, organisation data)
  - the sponsor's public and scientific contact points (name, e-mail, phone)

Contact points can name real people: they are personal data (GDPR). They are written
only to data/private/contacts.json, which is git-ignored, and must never be committed
or published (docs/ is meant for GitHub Pages).

Usage:
    python3 scripts/fetch_contacts.py               # sponsors with a trial in France (default)
    python3 scripts/fetch_contacts.py --all-small   # every sponsor with 10 trials or fewer

The sponsor list is read from docs/index.html, so run build_dashboard.py first.
Re-running resumes: sponsors already in contacts.json are skipped.
"""
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sponsor_groups import key

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'data' / 'private' / 'contacts.json'
API = 'https://euclinicaltrials.eu/ctis-public-api/retrieve/'
DELAY = 1.0          # seconds between requests
MAX_TRIALS = 2       # trials tried per sponsor when the sponsor is not found in the first one


def load_dashboard_data():
    page = (REPO / 'docs' / 'index.html').read_text(encoding='utf-8')
    raw = re.search(r'const DB = (\{.*?\});\n', page, re.S).group(1).replace('<\\/', '</')
    return json.loads(raw)


def fetch(number):
    req = urllib.request.Request(API + number, headers={'User-Agent': 'ctis-prospect-research/1.0', 'Accept': 'application/json'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code not in (429, 500, 502, 503, 504):
                raise
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(DELAY * 5 * (attempt + 1))
    return None


def clean(v):
    return html.unescape(v).strip() if isinstance(v, str) and v.strip() else None


def contact(c):
    return {k: v for k, v in {
        'name': clean(c.get('functionalName')),
        'email': clean(c.get('functionalEmailAddress')),
        'phone': clean(c.get('telephone')),
    }.items() if v}


def extract(trial, names):
    """Returns the details of the sponsor entry matching one of `names`, or None."""
    part1 = ((trial or {}).get('authorizedApplication') or {}).get('authorizedPartI') or {}
    sponsors = part1.get('sponsors') or []
    keys = {key(n) for n in names}
    match = next((s for s in sponsors if key((s.get('organisation') or {}).get('name', '')) in keys), None)
    if match is None and len(sponsors) == 1:
        match = sponsors[0]      # single sponsor whose name is spelt differently in the CSV export
    if match is None:
        return None
    addr = (match.get('addresses') or [{}])[0]
    a = addr.get('address') or {}
    third = []
    for t in match.get('thirdParties') or []:
        n = ((t.get('organisationAddress') or {}).get('organisation') or {}).get('name')
        if n and n not in third:
            third.append(n)
    contacts = []
    for kind, field in (('Public', 'publicContacts'), ('Scientific', 'scientificContacts')):
        for c in match.get(field) or []:
            d = contact(c)
            if d and d not in [{k: v for k, v in x.items() if k != 'type'} for x in contacts]:
                contacts.append({'type': kind, **d})
    return {
        'organisation': (match.get('organisation') or {}).get('name'),
        'city': clean(a.get('city')),
        'country': clean(a.get('countryName')),
        'org_email': clean(addr.get('email')),
        'org_phone': clean(addr.get('phone')),
        'third_parties': third,
        'contacts': contacts,
    }


def main():
    db = load_dashboard_data()
    T, S = db['T'], db['S']
    france = db['country'].index('France')
    all_small = '--all-small' in sys.argv
    targets = [s for s in S if len(s['t']) <= 10 and (all_small or any(france in T[i][6] for i in s['t']))]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}
    todo = [s for s in targets if s['name'] not in done]
    print(f'{len(targets)} target sponsors, {len(targets) - len(todo)} already done, {len(todo)} to fetch '
          f'(about {len(todo) * DELAY * 1.3 / 60:.0f} min)', flush=True)

    for n, s in enumerate(todo, 1):
        names = [s['name']] + [e[0] for e in s.get('ent', [])]
        trials = sorted(s['t'], key=lambda i: T[i][12], reverse=True)[:MAX_TRIALS]
        info = None
        for i in trials:
            info = extract(fetch(T[i][0]), names)
            time.sleep(DELAY)
            if info:
                info['trial'] = T[i][0]
                break
        done[s['name']] = info or {'not_found': True, 'trial': T[trials[0]][0]}
        done[s['name']]['fetched'] = date.today().isoformat()
        if n % 25 == 0 or n == len(todo):
            OUT.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding='utf-8')
            print(f'  {n}/{len(todo)}', flush=True)

    OUT.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding='utf-8')
    found = [v for v in done.values() if not v.get('not_found')]
    print(f'Done: {len(found)} sponsors with details, {len(done) - len(found)} not found -> {OUT}')


if __name__ == '__main__':
    main()
