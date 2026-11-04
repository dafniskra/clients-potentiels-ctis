# Clients Potentiels CTIS

Dashboard de prospection qui identifie les promoteurs d'essais cliniques les plus actifs en Europe, à partir du registre public **CTIS** (EU Clinical Trials Information System). Il sert à prioriser les clients potentiels d'une plateforme de gestion d'essais cliniques.

Le dashboard est une page HTML autonome : toutes les données y sont intégrées, il suffit d'ouvrir `docs/index.html` dans un navigateur (connexion internet requise pour les polices et la bibliothèque de graphiques).

## Contenu

```
data/CTIS_trials_20261104.csv   Export brut du registre CTIS (10 000 essais, 4 novembre 2026)
docs/index.html                 Dashboard généré (à ouvrir dans un navigateur)
docs/fusions_promoteurs.csv     Noms de promoteurs fusionnés, pour relecture
scripts/build_dashboard.py      Génère docs/ à partir de l'export CSV
scripts/sponsor_groups.py       Règles de fusion des promoteurs
scripts/synonyms.py             Correspondances marque commerciale ↔ molécule (DCI)
src/template.html               Gabarit du dashboard (HTML, CSS, JavaScript)
```

## Fonctionnalités

- **Indicateurs et graphiques** recalculés selon les filtres : promoteurs, essais, essais en recrutement, pays couverts ; top promoteurs, top pays, aires thérapeutiques, phases.
- **Filtres au niveau des essais** : chaque promoteur est reclassé sur ses seuls essais correspondants.
  - produit ou molécule (plusieurs termes séparés par des virgules, marques et molécules reliées) ;
  - pays, aire thérapeutique, phase, statut, type de promoteur ;
  - année d'autorisation, date de mise à jour, population, taille de l'essai, portée géographique, nombre de pays, résultats publiés ;
  - nombre minimum / maximum d'essais, première administration chez l'homme, bioéquivalence, etc.
- **Raccourcis** : petites biotechs actives, oncologie en France, immunothérapies anti-PD-1 / PD-L1, phases précoces, promoteurs académiques.
- **Fiche promoteur** : entités regroupées, pays, aires, phases, produits et derniers essais.
- **Export CSV** de la vue filtrée (promoteurs ou essais), séparateur `;`, compatible Excel.

## Régénérer le dashboard

Aucune dépendance : Python 3.9 ou plus récent suffit.

```bash
python3 scripts/build_dashboard.py
```

Le script prend l'export le plus récent de `data/` (`CTIS_trials_*.csv`) et réécrit `docs/index.html` et `docs/fusions_promoteurs.csv`. Pour un autre fichier :

```bash
python3 scripts/build_dashboard.py chemin/vers/export.csv
```

Pour mettre à jour les données : exporter les essais depuis [euclinicaltrials.eu](https://euclinicaltrials.eu) au même format CSV, le déposer dans `data/` sous le nom `CTIS_trials_AAAAMMJJ.csv`, puis relancer le script. Pensez aussi à mettre à jour la date d'extraction citée dans `src/template.html` (pied de page et constante `EXTRACT`).

Pour modifier l'interface, éditer `src/template.html` (jamais `docs/index.html`, qui est écrasé à chaque génération).

## Méthode

**Fusion des promoteurs** (`scripts/sponsor_groups.py`)
1. Les variantes d'écriture d'une même entité sont regroupées automatiquement : casse, accents, ponctuation, suffixes juridiques (Inc., AG, GmbH, S.A.…).
2. Les filiales d'un même groupe pharma sont regroupées selon une liste établie à la main (Sanofi, Johnson & Johnson / Janssen, Bristol Myers Squibb + Celgene, GSK, Boehringer Ingelheim…). MSD et Merck KGaA restent distincts.
3. Un essai déposé par plusieurs filiales d'un même groupe n'est compté qu'une fois pour ce groupe.

Résultat sur l'export du 4 novembre 2026 : 2 264 promoteurs, dont 89 regroupés.

**Score client potentiel** : `(2 × essais + 4 × essais en recrutement) × 1,3` pour les laboratoires et l'industrie. C'est une heuristique de priorisation, pas un classement officiel.

**Participants** : les essais déclarant plus de 100 000 participants sont exclus des totaux (valeurs aberrantes).

## Limites connues

- L'export compte exactement 10 000 lignes, probablement la limite d'export du registre : les données ne sont sans doute pas exhaustives.
- Le champ produit est vide pour 2 121 essais ; ils n'apparaissent pas quand un filtre produit est actif.
- Le filtre produit retient aussi les essais où le produit sert de comparateur.
- La correspondance marque ↔ molécule ne couvre qu'environ 140 médicaments courants (`scripts/synonyms.py`).

## Source des données

Registre public CTIS de l'Agence européenne des médicaments : [euclinicaltrials.eu](https://euclinicaltrials.eu). Les données restent soumises aux conditions d'utilisation de l'EMA.
