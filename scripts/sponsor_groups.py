"""Règles de fusion des promoteurs CTIS.

1. key() : normalise un nom (casse, accents, ponctuation, suffixes juridiques) pour regrouper
   les variantes d'écriture d'une même entité.
2. GROUPS : regroupe les filiales d'un même groupe pharma sous un libellé unique
   (regex appliquée à la clé normalisée). MSD et Merck KGaA restent volontairement distincts.
"""
import re
import unicodedata

SUF = r'\b(inc|incorporated|ltd|limited|llc|ag|gmbh|co kg|kg|sa|s a|sas|s a s|bv|b v|nv|n v|ab|a s|as|spa|s p a|srl|s r l|sl|s l|slu|plc|corp|corporation|co|company|ug|oy|oyj|kft|sro|s r o|zrt|ehf|aps|pty|international|intl)\b'

def key(n):
    n = unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower()
    n = n.replace('&', ' and ')
    n = re.sub(r'[^a-z0-9 ]', ' ', n)
    n = re.sub(SUF, ' ', n)
    n = re.sub(r'\b(the|and)\b', ' ', n)
    return re.sub(r'\s+', ' ', n).strip()

# Regroupements "groupe pharma" (filiales d'un même groupe) : (libellé, regex sur la clé normalisée)
GROUPS = [
    ('Sanofi', r'^sanofi\b'),
    ('Novartis', r'^novartis\b'),
    ('Roche', r'^(f hoffmann la roche|roche farma)\b'),
    ('Johnson & Johnson (Janssen)', r'^(janssen|johnson johnson)\b'),
    ('Bayer', r'^bayer\b'),
    ('MSD (Merck Sharp & Dohme)', r'^merck sharp dohme\b'),
    ('GSK', r'^(glaxosmithkline|gsk)\b'),
    ('AstraZeneca', r'^astrazeneca\b'),
    ('AbbVie', r'^abbvie\b'),
    ('Eli Lilly', r'^eli lilly\b'),
    ('Boehringer Ingelheim', r'^boehringer ingelheim\b'),
    ('Bristol Myers Squibb (incl. Celgene)', r'^(bristol myers squibb|celgene)\b'),
    ('Astellas', r'^astellas\b'),
    ('Daiichi Sankyo', r'^daiichi sankyo\b'),
    ('Servier', r'^(institut de recherches internationales servier|servier)\b'),
    ('Ipsen', r'^ipsen\b|an ipsen$'),
    ('UCB', r'^ucb\b'),
    ('Menarini', r'^(a )?menarini\b'),
    ('Grifols', r'^grifols\b'),
    ('Moderna', r'^moderna\b'),
    ('BioNTech', r'^biontech\b'),
    ('Otsuka', r'^otsuka\b'),
    ('Teva', r'^teva\b'),
    ('Sun Pharma', r'^sun pharmaceutical\b'),
    ('Jazz Pharmaceuticals', r'^jazz pharmaceuticals\b'),
    ('Incyte', r'^incyte\b'),
    ('BeOne Medicines', r'^beone medicines\b'),
    ('Ferring', r'^ferring\b'),
    ('Biogen', r'^biogen idec\b'),
    ('Zambon', r'^zambon\b'),
]
