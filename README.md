# SanSite - site vitrine `www.san-tls.com` (GitHub Pages)

Site statique de SAN. Sa **vraie fonction** n'est pas décorative : il fournit les
URL publiques que **Google et Apple vérifient** pour valider les comptes
développeur et l'écran de consentement OAuth.

| Page | URL | Sert à |
|---|---|---|
| Présentation (deck) | `https://www.san-tls.com/` | page d'accueil de l'écran de consentement Google |
| Confidentialité | `/privacy/` | **obligatoire** OAuth Google + soumission App Store |
| CGU | `/cgu/` | **obligatoire** écran de consentement Google |
| Mentions légales | `/mentions/` | conformité LCEN |
| Deep links (Phase E) | `/.well-known/` | App Links / Universal Links |

## Contenu

- `index.html` - le deck de présentation, réaligné sur l'identité de l'app
  (Bleu San `#002DFF`, jaune `#FFD954`). Source : `SAN_pdf.html`.
- `privacy/`, `cgu/`, `mentions/` - **générés** depuis les textes légaux de l'app
  (`SanApp/assets/data/legal/*.json`) par `tools/build_legal.py`.
  Contact réaligné sur `contact@san-tls.com`.
- `CNAME` - domaine personnalisé (`www.san-tls.com`).
- `.nojekyll` - **ne pas supprimer** : sans lui, `.well-known/` renvoie 404.

### Régénérer les pages légales

Les textes légaux vivent dans l'app (source unique de vérité). Après toute
modification des JSON :

```bash
python tools/build_legal.py
```

## Déploiement

### 1. Créer le dépôt et activer Pages

```bash
cd SanSite
git init && git add -A && git commit -m "Site vitrine SAN"
gh repo create SAN-TLS/SanSite --public --source=. --push   # org SAN-TLS
```

GitHub → repo → *Settings* → *Pages* → Source : **Deploy from a branch** →
`main` / `/ (root)`. Le fichier `CNAME` renseigne déjà le domaine.

### 2. DNS chez Squarespace

> ⚠️ **DÉCISION À TRANCHER - conflit avec le runbook backend.**
> `SanBackend/docs/mise_en_production_san_tls.md` §3 indique qu'il existe déjà un
> `CNAME www` (et un `A @`) pointant vers **le site vitrine Squarespace**. Deux
> options :
>
> - **(A - recommandé si la vitrine Squarespace est vide/placeholder)** : ce deck
>   *devient* la vitrine. Repointer `CNAME www → SAN-TLS.github.io`. La consigne
>   « ne pas toucher au CNAME www » du runbook est alors **caduque** - à mettre à
>   jour.
> - **(B - si une vraie vitrine Squarespace existe et doit être gardée)** : servir
>   ce site sur un sous-domaine dédié (`app.san-tls.com` ou `link.san-tls.com`),
>   changer `CNAME` ci-dessus en conséquence, et pointer les URL OAuth dessus.

Enregistrement à ajouter/modifier (Squarespace → Domaines → san-tls.com → DNS) :

| Type | Nom | Données |
|---|---|---|
| CNAME | `www` (ou `app`) | `san-tls.github.io` |

**Ne pas toucher** aux enregistrements du backend/mail : `sanapi` (Railway),
`em`/`img.em`/`r.em` + `brevo1/2._domainkey` (Brevo), MX Google, `_twilio`,
`google._domainkey`.

### 3. Vérification de domaine Google (branding OAuth)

Google Search Console → *Ajouter une propriété* → `san-tls.com` → méthode DNS →
ajouter le **TXT** fourni chez Squarespace. Débloque le branding de l'écran de
consentement.

### 4. Renseigner les URL

- Écran de consentement Google : Accueil `https://www.san-tls.com`,
  Confidentialité `…/privacy`, CGU `…/cgu`, domaine autorisé `san-tls.com`,
  email support `bcayol@san-tls.com` (alias `contact@san-tls.com` pas encore créé
  - pas d'accès admin Workspace au 20/07/2026 ; rebasculer dès que possible).
- App Store Connect : Privacy Policy URL `https://www.san-tls.com/privacy`.

## À faire plus tard

- **Phase E** : déposer `assetlinks.json` + `apple-app-site-association` dans
  `.well-known/` (voir le README de ce dossier).
- Fixer la **date de lancement** dans `index.html` (actuellement « Bientôt »).
