# python3 -I build.py <outdir> <stamped_pdf_dir>
import sys, os, shutil, html, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("data", os.path.join(here, "data.py"))
data = importlib.util.module_from_spec(spec); spec.loader.exec_module(data)

OUT, PDFS = sys.argv[1], sys.argv[2]
BASE = "https://jilagan.github.io"
ME = data.ME
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,600&display=swap" rel="stylesheet">')

GA_ID = "G-C9JYW8ZK09"
ANALYTICS = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
             '<script>window.dataLayer = window.dataLayer || [];'
             'function gtag(){dataLayer.push(arguments);}'
             f"gtag('js', new Date());gtag('config', '{GA_ID}');</script>\n")

def esc(s): return html.escape(s, quote=True)

def authors_html(lst):
    return ", ".join(f"<b>{esc(a)}</b>" if a == ME else esc(a) for a in lst)

def head(title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
{ANALYTICS}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="{'website' if path == '/' else 'article'}">
<meta property="og:site_name" content="Joseph Benjamin R. Ilagan">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
{extra}{FONTS}
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="wrap">
"""

FOOT = """<footer>
<p>Copies on this site are author versions posted under the publishers’ self-archiving terms. For citation, use the published version linked from each entry.</p>
<p>Joseph Benjamin Ilagan, Ateneo de Manila University, Quezon City, Philippines</p>
</footer>
</div>
</body>
</html>
"""

def links(p):
    out = []
    if p.get("page"):
        out.append(f'<a class="pdf" href="/papers/{p["page"]}/">{p.get("pdflabel", "Accepted manuscript PDF")}</a>')
    if p.get("doi"):
        label = p.get("doilabel", "Publisher")
        out.append(f'<a href="https://doi.org/{esc(p["doi"])}">{label}</a>')
    if p.get("url"):
        out.append(f'<a href="{esc(p["url"])}">{esc(p["urllabel"])}</a>')
    return " ".join(f"<span>{x}</span>" for x in out)

def pub_item(p):
    href = f'/papers/{p["page"]}/' if p.get("page") else (f'https://doi.org/{p["doi"]}' if p.get("doi") else p.get("url"))
    return (f'<li class="pub">\n<p class="t"><a href="{esc(href)}">{esc(p["title"])}</a></p>\n'
            f'<p class="a">{authors_html(p["authors"])}</p>\n'
            f'<p class="v">{p["venue"]}.</p>\n'
            f'<p class="l">{links(p)}</p>\n</li>')

os.makedirs(OUT, exist_ok=True)
shutil.copy(os.path.join(here, "style.css"), os.path.join(OUT, "style.css"))
shutil.copy(os.path.join(here, "og.png"), os.path.join(OUT, "og.png"))
open(os.path.join(OUT, ".nojekyll"), "w").close()

# Home page
years = []
for p in data.PUBS:
    if not years or years[-1][0] != p["year"]:
        years.append((p["year"], []))
    years[-1][1].append(p)

body = f"""<header class="masthead">
<h1>Joseph Benjamin R. Ilagan</h1>
<p class="roles">
<span>Assistant Professor, John Gokongwei School of Management, Ateneo de Manila University</span>
<span>Director, Ateneo Business Insights Laboratory for Development (BUILD)</span>
<span>Program Director, BS Information Technology Entrepreneurship</span>
</p>
<p class="contact">
<a href="mailto:jbilagan@ateneo.edu">jbilagan@ateneo.edu</a>
<a href="https://scholar.google.com/citations?user=J1x6kG8AAAAJ">Google Scholar</a>
<a href="https://orcid.org/0000-0002-3748-6468">ORCID</a>
<a href="https://ph.linkedin.com/in/jobenilagan">LinkedIn</a>
</p>
</header>
<p class="intro">I build and evaluate AI systems for learning and for small businesses, using design-based research. Current work covers conversational tutoring and learning simulations for entrepreneurship and management education, AI-assisted workflows in research and administration, data tools for micro and small enterprises, and digital public infrastructure for identity verification. I joined Ateneo full-time in 2019 after more than 26 years in industry and completed a PhD in Computer Science in 2026.</p>

<section class="pubs" aria-labelledby="pubs-h">
<h2 id="pubs-h">Publications</h2>
<p class="pubs-note">Newest first. Free author copies are linked as PDFs where the publisher allows it. Open-access versions are marked.</p>
"""
for y, items in years:
    body += f'<section class="year" aria-label="{y}">\n<h3>{y}</h3>\n<ol>\n' + "\n".join(pub_item(p) for p in items) + "\n</ol>\n</section>\n"
body += "</section>\n"

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(head("Joseph Benjamin R. Ilagan, Ateneo de Manila University",
                 "Publications of Joseph Benjamin R. Ilagan, Assistant Professor at the John Gokongwei School of Management, Ateneo de Manila University.",
                 "/") + body + FOOT)

# Paper pages
urls = ["/"]
for p in data.PUBS:
    slug = p.get("page")
    if not slug: continue
    d = data.PAPERS[slug]
    path = f"/papers/{slug}/"
    urls.append(path)
    pdir = os.path.join(OUT, "papers", slug)
    os.makedirs(pdir, exist_ok=True)
    shutil.copy(os.path.join(PDFS, d["pdf"]), os.path.join(pdir, d["pdf"]))
    pdf_url = f"{BASE}{path}{d['pdf']}"
    meta = [("citation_title", p["title"])]
    meta += [("citation_author", a) for a in p["authors"]]
    meta += [("citation_publication_date", d["date"])]
    meta += [(k, d[f]) for k, f in (("citation_journal_title", "journal"), ("citation_inbook_title", "book"),
             ("citation_conference_title", "conference"), ("citation_series_title", "series")) if d.get(f)]
    meta += [("citation_firstpage", d["firstpage"]),
             ("citation_lastpage", d["lastpage"]),
             ("citation_publisher", d["publisher"]),
             ("citation_doi", p["doi"]),
             ("citation_pdf_url", pdf_url),
             ("citation_abstract_html_url", f"{BASE}{path}")]
    meta += [("citation_keywords", "; ".join(d["keywords"]))]
    metahtml = "".join(f'<meta name="{k}" content="{esc(v)}">\n' for k, v in meta)
    first = p["authors"][0].split()[-1]
    etal = " et al." if len(p["authors"]) > 2 else (f" and {p['authors'][1].split()[-1]}" if len(p["authors"]) == 2 else "")
    cite = f'{", ".join(p["authors"])} ({p["year"]}). {p["title"]}. {html.unescape(p["venue"]).replace("<i>","").replace("</i>","")}. https://doi.org/{p["doi"]}'
    pdflabel = "Download PDF" + (" (preprint)" if "Preprint" in d["version"] else " (accepted manuscript)")
    page = f"""<p class="back"><a href="/">Joseph Benjamin R. Ilagan</a></p>
<article class="paper">
<h1>{esc(p["title"])}</h1>
<p class="a">{authors_html(p["authors"])}</p>
<p class="v">{p["venue"]}, {p["year"]}.</p>
<p class="actions"><a class="pdf" href="{d['pdf']}">{pdflabel}</a> <a href="https://doi.org/{esc(p['doi'])}">Published version ({d.get("pubshort", "Springer")})</a></p>
<h2>Abstract</h2>
<p class="abstract">{d["abstract"]}</p>
<p class="kw">Keywords: {esc("; ".join(d["keywords"]))}</p>
<h2>About this copy</h2>
<p class="notice">{d["version"]}. {d["notice"]}</p>
<h2>Cite as</h2>
<p class="cite">{esc(cite)}</p>
</article>
"""
    with open(os.path.join(pdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(head(f'{p["title"]} | {first}{etal} {p["year"]}', p["title"], path, metahtml) + page + FOOT)

with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"<url><loc>{BASE}{u}</loc></url>\n")
    f.write("</urlset>\n")
print("built", OUT, len(data.PUBS), "pubs,", len(urls) - 1, "paper pages")
