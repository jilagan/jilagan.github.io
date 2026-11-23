# python3 -I build.py <outdir> <stamped_pdf_dir>
import sys, os, shutil, html, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("data", os.path.join(here, "data.py"))
data = importlib.util.module_from_spec(spec); spec.loader.exec_module(data)

OUT, PDFS = sys.argv[1], sys.argv[2]
BASE = "https://jobenilagan.com"
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

import json, re
PERSON = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Joseph Benjamin R. Ilagan",
    "alternateName": ["Joseph Benjamin Ilagan", "Joben Ilagan"],
    "url": BASE + "/",
    "image": BASE + "/og.png",
    "jobTitle": "Assistant Professor",
    "worksFor": {"@type": "CollegeOrUniversity", "name": "Ateneo de Manila University", "url": "https://www.ateneo.edu"},
    "affiliation": {"@type": "Organization", "name": "John Gokongwei School of Management, Ateneo de Manila University"},
    "sameAs": ["https://scholar.google.com/citations?user=J1x6kG8AAAAJ",
               "https://orcid.org/0000-0002-3748-6468",
               "https://www.linkedin.com/in/jobenilagan/"],
}
PERSON_LD = '<script type="application/ld+json">' + json.dumps(PERSON, ensure_ascii=False) + '</script>\n'

def summary(abstract, n=155):
    t = " ".join(html.unescape(re.sub(r"<[^>]+>", "", abstract)).split())
    if len(t) <= n: return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",;:.") + "…"

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
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
for fn in ("og.png", "favicon.ico", "favicon-32.png", "apple-touch-icon.png"):
    shutil.copy(os.path.join(here, fn), os.path.join(OUT, fn))
open(os.path.join(OUT, ".nojekyll"), "w").close()
with open(os.path.join(OUT, "CNAME"), "w") as f: f.write("jobenilagan.com\n")

# Home page
spec2 = importlib.util.spec_from_file_location("content", os.path.join(here, "content.py"))
content = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(content)
BY_DOI = {p["doi"]: p for p in data.PUBS if p.get("doi")}

def pub_href(p):
    return f'/papers/{p["page"]}/' if p.get("page") else (f'https://doi.org/{p["doi"]}' if p.get("doi") else p.get("url"))

def ref_list(dois, videos):
    rows = []
    for d in dois:
        p = BY_DOI[d]
        venue = html.unescape(p["venue"]).replace("<i>", "").replace("</i>", "")
        venue = venue[3:] if venue.startswith("In ") else venue
        venue = venue.split(", pp.")[0].split(", CCIS")[0].split(", LNCS")[0].split(", LNNS")[0]
        rows.append(f'<li><a href="{esc(pub_href(p))}">{esc(p["title"])}</a> <span class="src">{esc(venue)}, {p["year"]}</span></li>')
    for title, vid in videos:
        rows.append(f'<li><a href="{content.YT}{vid}">{esc(title)}</a> <span class="src">Video</span></li>')
    return '<ul class="refs">\n' + "\n".join(rows) + "\n</ul>\n" if rows else ""

MASTHEAD = """<header class="masthead">
<h1>Joseph Benjamin R. Ilagan</h1>
<p class="roles">
<span>Assistant Professor, John Gokongwei School of Management, Ateneo de Manila University</span>
<span>Director, Ateneo Business Insights Laboratory for Development (BUILD)</span>
<span>Program Director, BS Information Technology Entrepreneurship</span>
</p>
<p class="contact">
""" + open(os.path.join(here, "contact.html"), encoding="utf-8").read().strip() + """
<a href="https://scholar.google.com/citations?user=J1x6kG8AAAAJ">Google Scholar</a>
<a href="https://orcid.org/0000-0002-3748-6468">ORCID</a>
<a href="https://ph.linkedin.com/in/jobenilagan">LinkedIn</a>
</p>
</header>
"""
NAV = """<nav class="sitenav" aria-label="Sections">
<a href="/#research">Research</a> <a href="/#projects">Projects</a> <a href="/#background">Background</a> <a href="/#teaching">Teaching</a> <a href="/publications/">Publications</a>
</nav>
"""

body = MASTHEAD + NAV + f'<p class="intro">{esc(content.INTRO)}</p>\n'
body += '<section class="section" id="research" aria-labelledby="research-h">\n<h2 id="research-h">Research</h2>\n'
for t in content.RESEARCH:
    body += f'<div class="item">\n<h3>{esc(t["title"])}</h3>\n<p>{t["text"]}</p>\n' + ref_list(t["papers"], t["videos"]) + "</div>\n"
body += '<p class="more"><a href="/publications/">All publications</a></p>\n</section>\n'
body += '<section class="section" id="projects" aria-labelledby="projects-h">\n<h2 id="projects-h">Projects</h2>\n'
for pr in content.PROJECTS:
    name = f'<a href="{esc(pr["url"])}">{esc(pr["name"])}</a>' if pr.get("url") else esc(pr["name"])
    body += f'<div class="item">\n<h3>{name}</h3>\n<p>{pr["text"]}</p>\n' + ref_list(pr.get("papers", []), pr.get("videos", [])) + "</div>\n"
body += "</section>\n"
body += f'<section class="section" id="background" aria-labelledby="background-h">\n<h2 id="background-h">Background</h2>\n<p>{esc(content.BACKGROUND_INTRO)}</p>\n<dl class="cv">\n'
for role, desc in content.BACKGROUND:
    body += f"<dt>{esc(role)}</dt>\n" + (f"<dd>{esc(desc)}</dd>\n" if desc else "<dd></dd>\n")
body += "</dl>\n</section>\n"
body += f'<section class="section" id="teaching" aria-labelledby="teaching-h">\n<h2 id="teaching-h">Teaching</h2>\n<p>{esc(content.TEACHING_INTRO)}</p>\n<ul class="courses">\n'
for code, title, url in content.TEACHING:
    t = f'<a href="{esc(url)}">{esc(title)}</a>' if url else esc(title)
    body += f'<li><span class="code">{esc(code)}</span> <span>{t}</span></li>\n'
body += "</ul>\n" + "".join(f"<p>{n}</p>\n" for n in content.TEACHING_NOTES) + "</section>\n"

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(head("Joseph Benjamin R. Ilagan, Ateneo de Manila University",
                 "Research, projects and publications of Joseph Benjamin R. Ilagan, Assistant Professor at the John Gokongwei School of Management, Ateneo de Manila University.",
                 "/", PERSON_LD) + body + FOOT)

# Publications page
years = []
for p in data.PUBS:
    if not years or years[-1][0] != p["year"]:
        years.append((p["year"], []))
    years[-1][1].append(p)
pbody = '<p class="back"><a href="/">Joseph Benjamin R. Ilagan</a></p>\n' + NAV
pbody += """<section class="pubs" aria-labelledby="pubs-h">
<h1 id="pubs-h">Publications</h1>
<p class="pubs-note">Newest first. Free author copies are linked as PDFs where the publisher allows it. Open-access versions are marked.</p>
"""
for y, items in years:
    pbody += f'<section class="year" aria-label="{y}">\n<h3>{y}</h3>\n<ol>\n' + "\n".join(pub_item(p) for p in items) + "\n</ol>\n</section>\n"
pbody += "</section>\n"
os.makedirs(os.path.join(OUT, "publications"), exist_ok=True)
with open(os.path.join(OUT, "publications", "index.html"), "w", encoding="utf-8") as f:
    f.write(head("Publications | Joseph Benjamin R. Ilagan",
                 "Publications of Joseph Benjamin R. Ilagan, with free author copies where publishers allow.",
                 "/publications/") + pbody + FOOT)

# Paper pages
urls = ["/", "/publications/"]
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
    page = f"""<p class="back"><a href="/">Joseph Benjamin R. Ilagan</a> / <a href="/publications/">Publications</a></p>
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
        f.write(head(f'{p["title"]} | {first}{etal} {p["year"]}', summary(d["abstract"]), path, metahtml) + page + FOOT)

with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"<url><loc>{BASE}{u}</loc></url>\n")
    f.write("</urlset>\n")
print("built", OUT, len(data.PUBS), "pubs,", len(urls) - 1, "paper pages")
