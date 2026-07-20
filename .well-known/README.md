# `.well-known/` - fichiers de vérification deep-link (Phase E)

Ce dossier sert les fichiers que **Android et iOS lisent automatiquement** pour
autoriser l'ouverture de l'app SAN depuis un lien `https://www.san-tls.com/...`
(App Links / Universal Links). Il n'est **pas encore actif** : il attend deux
valeurs qui n'existent qu'une fois le keystore Android et le compte Apple créés.

> ⚠️ **`.nojekyll` à la racine du dépôt est OBLIGATOIRE.** Sans lui, GitHub Pages
> (Jekyll) ignore tout dossier commençant par un point et `.well-known/` renvoie 404.

## 1. `assetlinks.json` (Android)

À créer ici (`/.well-known/assetlinks.json`) avec le **SHA-256 de la clé Play App
Signing** (pas la clé d'upload) - cf. `SanApp/docs/guide_configuration_identite_application.md` §3.3 et §6.4 :

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "fr.san.sanApp",
    "sha256_cert_fingerprints": ["<SHA-256 Play App Signing>"]
  }
}]
```

## 2. `apple-app-site-association` (iOS)

⚠️ **Sans extension de fichier**, servi en `application/json`. À créer avec le
`TeamID.BundleID` :

```json
{
  "applinks": {
    "apps": [],
    "details": [{
      "appID": "<TeamID>.fr.san.sanApp",
      "paths": ["/app/*"]
    }]
  }
}
```

Puis, dans l'app iOS, capability *Associated Domains* → `applinks:www.san-tls.com`.

## 3. Cohérence d'hôte (important)

Historiquement, `SanApp/docs/guide_configuration_identite_application.md` visait
l'apex `san-tls.com`. Comme le site vitrine est servi sur **`www.san-tls.com`**,
tout doit viser `www` **sans redirection** (Apple ne suit pas les redirections
pour l'AASA) :

- deep links → `https://www.san-tls.com/app/...`
- Redirect URLs Supabase / Stripe → idem
- capability iOS → `applinks:www.san-tls.com`

Aligner ces 2-3 lignes dans le guide identité au moment de la Phase E.
