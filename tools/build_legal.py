#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les pages légales du site vitrine SAN (privacy / cgu / mentions)
à partir des textes JSON embarqués dans l'application mobile
(SanApp/assets/data/legal/*.json), source unique de vérité.

- Réaligne le contact sur contact@san-tls.com (décision du 20/07/2026).
- Style aligné sur l'identité de l'app : Bleu San #002DFF, Playfair Display + Instrument Sans.

Usage :
    python tools/build_legal.py
"""
from __future__ import annotations
import html
import json
from pathlib import Path

# --- Chemins ---------------------------------------------------------------
HERE = Path(__file__).resolve().parent          # .../SanSites/tools
SITE = HERE.parent                              # .../SanSites
# Source des textes légaux = l'app mobile (source unique de vérité).
# Le repo du site pouvant être déplacé (SanSite/, SAN/SanSites/, ...), on cherche
# SanApp/assets/data/legal en remontant l'arborescence depuis ce fichier.
_REL = Path("SanApp") / "assets" / "data" / "legal"
LEGAL_SRC = None
for _base in [SITE, *SITE.parents]:
    _candidate = _base / _REL
    if _candidate.exists():
        LEGAL_SRC = _candidate
        break
if LEGAL_SRC is None:
    # Repli : chemin absolu attendu sur ce poste.
    LEGAL_SRC = Path(r"C:/Users/seerm/IdeaProjects/SanApp/assets/data/legal")

# --- Adresse e-mail canonique ---------------------------------------------
OLD_EMAIL = "contact@san.maashrees.com"
NEW_EMAIL = "contact@san-tls.com"

DOCS = {
    "privacy":  ("privacy.json",  "Politique de confidentialité", "privacy"),
    "cgu":      ("cgu.json",      "Conditions Générales d'Utilisation", "cgu"),
    "mentions": ("mentions.json", "Mentions légales", "mentions"),
}

# --- Gabarit HTML ----------------------------------------------------------
PAGE_TMPL = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} - SAN</title>
<meta name="description" content="{title} de l'application SAN."/>
<meta name="robots" content="index, follow"/>
<link rel="icon" type="image/png" href="/favicon.png"/>
<link rel="shortcut icon" href="/favicon.ico"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
  :root {{ --blue:#002DFF; --yel:#FFD954; --dark:#1C1209; --muted:#6b5d50; --line:rgba(28,18,9,.10); --bg:#FEFAF5; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Instrument Sans',system-ui,sans-serif; color:var(--dark); background:var(--bg); font-size:1.08rem; line-height:1.75; }}
  .topbar {{ border-bottom:1px solid var(--line); background:#fff; }}
  .topbar-inner {{ max-width:820px; margin:0 auto; padding:1.2rem 1.5rem; display:flex; align-items:center; justify-content:space-between; }}
  .brand {{ font-family:'Playfair Display',serif; font-weight:900; font-size:1.4rem; letter-spacing:-.02em; color:var(--dark); text-decoration:none; display:inline-flex; align-items:center; gap:.6rem; }}
  .brand span {{ color:var(--blue); }}
  .brand img {{ height:36px; width:auto; display:block; }}
  .back {{ font-size:.95rem; font-weight:600; color:var(--blue); text-decoration:none; }}
  main {{ max-width:820px; margin:0 auto; padding:3.5rem 1.5rem 6rem; }}
  h1 {{ font-family:'Playfair Display',serif; font-weight:900; font-size:clamp(2.2rem,5.5vw,3rem); line-height:1.15; letter-spacing:-.025em; margin-bottom:.7rem; }}
  .meta {{ font-size:.88rem; color:var(--muted); margin-bottom:2.2rem; text-transform:uppercase; letter-spacing:.06em; font-weight:500; }}
  .intro {{ font-size:1.15rem; color:#3a2e22; margin-bottom:2.8rem; font-weight:400; line-height:1.8; }}
  .intro p + p {{ margin-top:1rem; }}
  section {{ margin-bottom:2.5rem; }}
  h2 {{ font-family:'Playfair Display',serif; font-weight:700; font-size:1.5rem; letter-spacing:-.01em; margin-bottom:.8rem; border-top:1px solid var(--line); padding-top:1.6rem; }}
  h2 .num {{ color:var(--blue); margin-right:.4rem; }}
  h3 {{ font-weight:600; font-size:1.18rem; margin:1.3rem 0 .5rem; }}
  p {{ margin-bottom:.8rem; }}
  ul {{ margin:.5rem 0 1rem 1.4rem; }}
  li {{ margin-bottom:.45rem; }}
  dl {{ margin:.8rem 0; display:grid; grid-template-columns:max-content 1fr; gap:.5rem 1.2rem; font-size:1.05rem; }}
  dt {{ font-weight:600; color:var(--muted); }}
  .note {{ background:#FFF6DA; border-left:4px solid var(--yel); padding:.85rem 1.2rem; border-radius:0 8px 8px 0; font-size:1.02rem; margin:.8rem 0; }}
  .items-label {{ font-weight:600; margin-top:.8rem; }}
  a {{ color:var(--blue); }}
  footer {{ max-width:820px; margin:0 auto; padding:2.5rem 1.5rem 4.5rem; border-top:1px solid var(--line); font-size:.92rem; color:var(--muted); }}
  footer a {{ font-weight:600; text-decoration:none; }}
  .footer-links {{ display:flex; gap:1.4rem; flex-wrap:wrap; margin-bottom:1rem; font-size:.98rem; }}
</style>
</head>
<body>
<header class="topbar"><div class="topbar-inner">
  <a class="brand" href="/"><img src="/assets/logo/SAN_transparent.png" alt="SAN Logo"/></a>
  <a class="back" href="/">&larr; Accueil</a>
</div></header>
  <a class="back" href="/">&larr; Accueil</a>
</div></header>
<main>
  <h1>{title}</h1>
  <div class="meta">{meta}</div>
  {intro}
  {sections}
</main>
<footer>
  <div class="footer-links">
    <a href="/privacy/">Confidentialité</a>
    <a href="/cgu/">CGU</a>
    <a href="/mentions/">Mentions légales</a>
  </div>
  SAN - SAS · 1 Ruelle de Paris, 94450 Limeil-Brévannes · <a href="mailto:{email}">{email}</a>
</footer>
</body>
</html>
"""


def esc(text: str) -> str:
    return html.escape(str(text).replace(OLD_EMAIL, NEW_EMAIL))


def render_block(node: dict) -> str:
    """Rend body / items / fields / itemsLabel / note d'une section ou sous-section."""
    out = []
    for para in node.get("body", []):
        out.append(f"<p>{esc(para)}</p>")
    if node.get("fields"):
        out.append("<dl>")
        for f in node["fields"]:
            out.append(f"<dt>{esc(f['label'])}</dt><dd>{esc(f['value'])}</dd>")
        out.append("</dl>")
    if node.get("itemsLabel"):
        out.append(f"<p class='items-label'>{esc(node['itemsLabel'])}</p>")
    if node.get("items"):
        out.append("<ul>")
        for it in node["items"]:
            out.append(f"<li>{esc(it)}</li>")
        out.append("</ul>")
    if node.get("note"):
        out.append(f"<div class='note'>{esc(node['note'])}</div>")
    return "\n".join(out)


def render_section(sec: dict) -> str:
    num = sec.get("id", "")
    num_html = f"<span class='num'>{esc(num)}</span>" if num else ""
    parts = [f"<section><h2>{num_html}{esc(sec['heading'])}</h2>"]
    parts.append(render_block(sec))
    for sub in sec.get("subsections", []):
        sub_num = sub.get("id", "")
        sub_num_html = f"{esc(sub_num)} " if sub_num else ""
        parts.append(f"<h3>{sub_num_html}{esc(sub['heading'])}</h3>")
        parts.append(render_block(sub))
    parts.append("</section>")
    return "\n".join(parts)


def build(doc_key: str) -> None:
    fname, title, folder = DOCS[doc_key]
    data = json.loads((LEGAL_SRC / fname).read_text(encoding="utf-8"))

    # Métadonnées (version/date variables selon le document)
    bits = []
    if data.get("version"):
        bits.append(f"Version {esc(data['version'])}")
    if data.get("effectiveDate"):
        bits.append(f"En vigueur le {esc(data['effectiveDate'])}")
    if data.get("lastUpdated"):
        bits.append(f"Mise à jour : {esc(data['lastUpdated'])}")
    meta = " · ".join(bits)

    intro_html = ""
    if data.get("intro"):
        intro_html = "<div class='intro'>" + "".join(
            f"<p>{esc(p)}</p>" for p in data["intro"]) + "</div>"

    sections_html = "\n".join(render_section(s) for s in data.get("sections", []))

    page = PAGE_TMPL.format(
        title=esc(title), meta=meta, intro=intro_html,
        sections=sections_html, email=NEW_EMAIL,
    )
    out_dir = SITE / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"  [OK] {folder}/index.html  ({len(page):,} octets)")


if __name__ == "__main__":
    print(f"Source légale : {LEGAL_SRC}")
    if not LEGAL_SRC.exists():
        raise SystemExit(f"Introuvable : {LEGAL_SRC} - ajuste le chemin en tête du script.")
    for key in DOCS:
        build(key)
    print("Terminé.")
