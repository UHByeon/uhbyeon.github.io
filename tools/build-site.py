"""Generate the responsive, static uhbyeon's log_ website."""
from pathlib import Path
from html import escape
from datetime import date
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
SITE = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
def ordered_posts(records):
    return sorted(
        records,
        key=lambda post: (date.fromisoformat(post["date"]), post["id"]),
        reverse=True,
    )


POSTS = ordered_posts(json.loads((ROOT / "content/posts.json").read_text(encoding="utf-8")))
NAV = SITE["navigation"]
NAV_BY_KEY = {item["key"]: item for item in NAV}
LOG_KEYS = ("ai", "security", "issues", "vulnerabilities", "development")
SITE_NAME = SITE["name"]
DISPLAY_NAME = SITE.get("display_name", SITE["author"])
NAME_KO = SITE.get("name_ko", "")
RELEASE_LABEL = f'v{SITE["release"]["version"]}-{SITE["release"]["channel"]}'
FONT_URL = "https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap"
ICONS = {
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3m6 0h4"/>',
    "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "archive": '<path d="M3 7h18v14H3zM2 3h20v4H2zM9 11h6"/>',
    "brain": '<path d="M9 4a3 3 0 0 0-5 3 4 4 0 0 0-1 7 4 4 0 0 0 6 5V4zm6 0a3 3 0 0 1 5 3 4 4 0 0 1 1 7 4 4 0 0 1-6 5V4zM6 9h3m6 0h3M6 15h3m6 0h3"/>',
    "shield": '<path d="m12 2 8 4v6c0 5-8 10-8 10S4 17 4 12V6zM9 12l2 2 4-4"/>',
    "activity": '<path d="M2 12h5l3-8 4 16 3-8h5"/>',
    "bug": '<rect x="7" y="7" width="10" height="13" rx="5"/><path d="M9 7V5a3 3 0 0 1 6 0v2M3 9l4 2m10 0 4-2M3 16h4m10 0h4M12 7v13"/>',
    "code": '<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-13-2 16"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "close": '<path d="m5 5 14 14M5 19 19 5"/>',
    "arrow": '<path d="M5 19 19 5M5 5h14v14"/>',
    "bookmark": '<path d="M6 3h12v18l-6-4-6 4z"/>',
    "copy": '<rect x="8" y="8" width="13" height="13" rx="1"/><path d="M16 8V3H3v13h5"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m9 10 6-4M9 14l6 4"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h1m-1 6h1m-1 6h1"/>',
    "chevron": '<path d="m9 5 7 7-7 7"/>',
    "panel": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18m8-12-3 3 3 3"/>',
}


def e(value):
    return escape(str(value), quote=True)


def icon(name, size=18):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def section(post):
    return post.get("section", "development")


for post in POSTS:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", post["id"]):
        raise ValueError("Post IDs must be lowercase URL slugs")
if len({post["id"] for post in POSTS}) != len(POSTS):
    raise ValueError("Post IDs must be unique")


def post_url(post, prefix="./"):
    return f'{prefix}posts/{post["id"]}.html'


def category_url(post, prefix="./"):
    return prefix + NAV_BY_KEY.get(section(post), NAV_BY_KEY["all"])["path"]


def nav_link(item, active, prefix, article=False):
    current = item["key"] == active
    aria = (' aria-current="location"' if article else ' aria-current="page"') if current else ""
    count = sum(section(post) in LOG_KEYS for post in POSTS) if item["key"] == "all" else sum(section(post) == item["key"] for post in POSTS)
    badge = '<span class="nav-badge">[active]</span>' if current else (f'<span class="nav-count">{count:02}</span>' if item["key"] not in ("home", "about") else "")
    disclosure = ' data-all-logs-link aria-controls="log-categories" aria-expanded="true"' if item["key"] == "all" else ""
    return f'<a href="{prefix}{item["path"]}" class="nav-item{" is-active" if current else ""}"{aria}{disclosure}>{icon(item["icon"])}<span class="nav-labels">{e(item["label"])}</span>{badge}</a>'


def sidebar_navigation(active, prefix, article=False):
    children = "".join(nav_link(NAV_BY_KEY[key], active, prefix, article) for key in LOG_KEYS)
    group = f'<div class="nav-group"><div class="nav-group-row{" is-active" if active == "all" else ""}"><button type="button" class="nav-group-toggle" id="log-group-toggle" aria-label="all_logs 분류 접기" aria-controls="log-categories" aria-expanded="true">{icon("chevron",12)}</button>{nav_link(NAV_BY_KEY["all"],active,prefix,article)}</div><div class="side-subnav" id="log-categories" data-has-active="{str(active in LOG_KEYS).lower()}">{children}</div></div>'
    return nav_link(NAV_BY_KEY["home"],active,prefix,article) + group + nav_link(NAV_BY_KEY["about"],active,prefix,article)


def page(title, path_label, content, active="home", nested=False, article=False, view="default", article_post=None):
    prefix = "../" if nested else "./"
    asset_version = hashlib.sha256((ROOT / "styles.css").read_bytes()).hexdigest()[:8]
    script_version = hashlib.sha256((ROOT / "script.js").read_bytes()).hexdigest()[:8]
    reference_style = ""
    if view != "default":
        reference_version = hashlib.sha256((ROOT / "reference-views.css").read_bytes()).hexdigest()[:8]
        reference_style = f'<link href="{prefix}reference-views.css?v={reference_version}" rel="stylesheet">'
    sidebar = sidebar_navigation(active, prefix, article)
    bottom_active = "all" if active in LOG_KEYS and active != "development" else active
    bottom = "".join(f'<a href="{prefix}{NAV_BY_KEY[key]["path"]}" class="{"is-active" if bottom_active == key else ""}"' + (' aria-current="page"' if active == key and not article else '') + f'>{icon(NAV_BY_KEY[key]["icon"], 20)}<span>{e(NAV_BY_KEY[key]["label"])}</span></a>' for key in ("home", "all", "development", "about"))
    menu_button = f'<button class="icon-button menu-toggle" id="menu-toggle" aria-controls="sidebar" aria-expanded="false" aria-label="전체 메뉴 열기">{icon("menu",21)}</button>'
    sidebar_button = f'<button type="button" class="icon-button sidebar-toggle" id="sidebar-toggle" aria-controls="sidebar" aria-expanded="true" aria-label="좌측 메뉴 접기" title="좌측 메뉴 접기">{icon("panel",20)}</button>'
    search_action = f'<a class="icon-button" href="{prefix}posts.html#search-input" aria-label="기록 검색">{icon("search",20)}</a>'
    if view == "article":
        back = category_url(article_post,prefix)
        header = f'<div class="article-header-left">{sidebar_button}<a class="header-back" href="{back}">&lt; cd ..</a><span class="article-file-path">/ ~/{e(path_label.replace(" / ","/"))}</span></div><div class="header-actions"><button class="icon-button" data-bookmark aria-label="Bookmark" aria-pressed="false">{icon("bookmark",18)}</button><button class="icon-button" data-share aria-label="Share">{icon("share",18)}</button>{search_action}{menu_button}</div>'
    else:
        context = f'<span class="header-context">/ {e(title)}</span>' if view in ("archive","profile") else ""
        status = '<span class="header-status"><i></i>ready : main</span>' if view == "default" else ""
        header = f'<div class="header-identity">{sidebar_button}<a class="brand" href="{prefix}index.html" aria-label="{e(SITE_NAME)} 홈">{icon("terminal",24)}<span>{e(SITE_NAME.removesuffix("_"))}<span class="brand-cursor">_</span></span><span class="brand-dot" aria-hidden="true"></span></a>{context}</div><div class="header-actions">{status}{search_action}{menu_button}</div>'
    page_path = f'<div class="page-path"><span><b>~</b> / {e(path_label)}</span><span class="path-note">a personal knowledge archive</span></div>' if view == "default" else ""
    if view == "archive":
        footer = f'<footer class="reference-footer archive-footer"><span>buffer: {e(path_label)}/clean</span><span>{e(SITE_NAME)} / built with curiosity.</span></footer>'
    elif view == "profile":
        footer = ""
    elif view == "article":
        footer = f'<footer class="reference-footer article-footer"><span>{e(SITE_NAME)} / built with curiosity.</span></footer>'
    else:
        footer = f'<footer class="page-footer home-footer"><p><span>$ echo</span> "작은 기록이 다음의 나를 만듭니다."</p><span class="footer-signature">{e(SITE_NAME)} / built with curiosity.</span></footer>'
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="description" content="{e(title)} — {e(SITE_NAME)}"><meta name="theme-color" content="#10141a"><title>{e(SITE_NAME)} · {e(title)}</title><link rel="icon" href="{prefix}favicon.ico?v=4" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png?v=4"><link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg?v=4"><link rel="apple-touch-icon" sizes="180x180" href="{prefix}apple-touch-icon.png?v=4"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{e(FONT_URL)}" rel="stylesheet"><link href="{prefix}styles.css?v={asset_version}" rel="stylesheet">{reference_style}<script src="{prefix}script.js?v={script_version}" defer></script></head>
<body class="view-{view}" data-active-section="{active}" data-prefix="{prefix}" data-site-name="{e(SITE_NAME)}" data-author="{e(SITE["author"])}" data-display-name="{e(DISPLAY_NAME)}" data-name-ko="{e(NAME_KO)}"><a class="skip-link" href="#main">본문으로 건너뛰기</a><header class="site-header">{header}</header>
<button class="menu-backdrop" id="menu-backdrop" tabindex="-1" aria-label="전체 메뉴 닫기" hidden></button><aside class="sidebar" id="sidebar" aria-label="전체 탐색"><div class="sidebar-heading"><span>workspace</span><button class="icon-button drawer-close" aria-label="메뉴 닫기">{icon("close")}</button></div><p class="nav-command">$ log --menu</p><nav class="side-nav" aria-label="주 메뉴">{sidebar}</nav><div class="sidebar-footer"><p>// keep exploring.<br>// keep a log.</p><div class="build-status"><span class="build-indicator" aria-hidden="true"></span><span>{e(RELEASE_LABEL)}</span></div></div></aside>
<div class="workspace"><main id="main" class="page-shell">{page_path}{content}{footer}</main></div><nav class="bottom-nav" aria-label="모바일 주 메뉴">{bottom}</nav><p id="interaction-status" class="sr-only" role="status" aria-live="polite"></p></body></html>'''


def code_frame(text, label, code_id, language="text", copy=True):
    numbers = "\n".join(f"{i:02}" for i in range(1, len(text.splitlines()) + 1))
    button = f'<button class="copy-button" data-copy-target="{code_id}" aria-label="{e(label)} 코드 복사">{icon("copy", 13)}<span>Copy</span></button>' if copy else ""
    return f'<div class="code-frame"><div class="code-bar"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span><span>{e(label)}</span><span class="code-language">{e(language)}</span>{button}</div><div class="code-content"><span class="line-numbers" aria-hidden="true">{numbers}</span><pre tabindex="0"><code id="{code_id}">{e(text)}</code></pre></div></div>'


def rows(posts, prefix="./"):
    output = []
    for number,post in enumerate(posts,1):
        output.append(f'<article class="log-row"><span class="row-number">{number:02}</span><div><div class="post-meta"><a href="{category_url(post,prefix)}">{e(post["category"])}</a><span>·</span><time datetime="{post["date"]}">{post["date"].replace("-", ".")}</time><span>· {e(post["reading"])} 읽기</span></div><h3><a href="{post_url(post,prefix)}">{e(post["title"])}</a></h3><p>{e(post["summary"])}</p></div><a class="row-arrow" href="{post_url(post,prefix)}" aria-label="{e(post["title"])} 읽기">{icon("arrow")}</a></article>')
    return "".join(output)


def home():
    posts = ordered_posts(POSTS)
    recent = posts[:4]
    recent_html = rows(recent) if recent else '<p class="recent-empty">아직 게시된 글이 없습니다.</p>'
    hero_code = "// a little progress, every day.\nconst day = {\n  build: 'something',\n  learn: 'one thing',\n  write: 'it down'\n};\nkeepGoing(day);"
    pinned = f'<a class="pinned-note" href="./about.html"><div class="pin-eyebrow">{icon("bookmark",15)} 처음 오셨다면 · 추천 글 {icon("arrow",15)}</div><h2>안녕하세요, {e(NAME_KO)}입니다.</h2><p>인공지능과 정보보안을 공부하며 읽고, 만들고, 정리한 내용을 남깁니다.</p><footer><span>about_me.md</span><span>open profile →</span></footer></a>'
    return f'''<section class="hero"><p class="command">$ cat about_me.md</p><h1>생각을 코드로,<br>경험을 <span>기록으로.</span></h1><p class="hero-description">문제를 풀고, 작은 도구를 만들고, 배운 것을 남깁니다.<br>계속 업데이트되는 개발자의 작업 노트.</p><div class="hero-links"><a class="terminal-button" href="./posts.html">기록 둘러보기 {icon("arrow",15)}</a><span>// {len(posts)} articles logged</span></div></section><div class="home-panels"><div class="daily-log">{code_frame(hero_code,"daily-log.ts","daily-code","TS",False)}<p>└ 오늘의 배움을 한 줄씩.</p></div>{pinned}</div><section class="recent-logs" id="recent-logs"><header class="section-heading"><div><span>~/logs</span><h2>최근 기록</h2><small>{len(posts):02}</small></div><a href="./posts.html">all_logs {icon("arrow",14)}</a></header>{recent_html}</section><div class="topic-grid"><a href="./development.html">{icon("code",24)}<div><h2>개발 노트</h2><p>배운 것과 해결한 문제를 정리합니다.</p></div>{icon("arrow",16)}</a><a href="./papers-ai.html">{icon("brain",24)}<div><h2>인공지능 논문</h2><p>읽고 이해한 내용을 차곡차곡.</p></div>{icon("arrow",16)}</a></div>'''


FILTERS = [("all", "All"), *[(key, NAV_BY_KEY[key]["label"]) for key in LOG_KEYS]]


def filters(posts, by_category=False):
    values = [("all","All")]+[(category,category) for category in dict.fromkeys(p["category"] for p in posts)] if by_category else FILTERS
    parts = []
    for key,label in values:
        count = len(posts) if key == "all" else sum((p["category"] if by_category else section(p)) == key for p in posts)
        parts.append(f'<button type="button" class="filter-button{" is-active" if key == "all" else ""}" data-filter="{e(key)}" aria-pressed="{str(key == "all").lower()}">[{e(label)} ({count})]</button>')
    field = "category" if by_category else "section"
    return f'<div class="filter-strip" data-filter-field="{field}" role="group" aria-label="기록 분류 필터">'+"".join(parts)+'</div>'


def search_box():
    return f'<label class="search-box">{icon("search",15)}<input type="text" inputmode="search" id="search-input" aria-label="제목과 본문으로 기록 검색" placeholder="Filter logs... ($ /keyword)"></label>'


def search_data(post):
    return e(" ".join([post["title"],post["category"],post["summary"],*[b[1] for b in post["body"]]]))


def reference_code(text, label, code_id, copy=False, article=False):
    numbers="\n".join(f"{i:02}" for i in range(1,len(text.splitlines())+1))
    button = f'<button class="copy-button" data-copy-target="{code_id}" aria-label="코드 복사"><span>COPY</span></button>' if copy else ""
    return f'<div class="code-frame reference-code"><div class="code-bar"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span><span>{e(label)}</span>{button}</div><div class="code-content"><span class="line-numbers" aria-hidden="true">{numbers}</span><pre tabindex="0"><code id="{code_id}">{e(text)}</code></pre></div></div>'


def archive_card(post):
    pre=next((text for tag,text in post["body"] if tag == "pre"),None)
    code_id=f'preview-{post["id"]}'
    copy = f'<button class="copy-button card-copy" data-copy-target="{code_id}" aria-label="코드 복사">{icon("copy",14)}<span>Copy</span></button>' if pre else ""
    code = reference_code(pre,post.get("code_language",""),code_id) if pre else ""
    return f'<article class="archive-card" data-post data-section="{e(section(post))}" data-category="{e(post["category"])}" data-search="{search_data(post)}"><div class="archive-card-heading"><div><div class="snippet-file"><span class="tag">{e(post["category"])}</span><span>{e(post["id"])}.md</span></div><h2><a href="{post_url(post)}">{e(post["title"])}</a></h2></div>{copy}</div>{code}<div class="card-note"><span>//</span><p>{e(post["summary"])}</p></div></article>'


def archive(key="all", legacy_category=None):
    item=NAV_BY_KEY[key]
    selected=[p for p in POSTS if p["category"] == legacy_category] if legacy_category else [p for p in POSTS if (section(p) in LOG_KEYS if key == "all" else section(p) == key)]
    intro={"all":"전체 기록","ai":"읽고 이해한 인공지능 논문","security":"정보보안 논문을 읽으며","issues":"살펴본 기술과 보안 이슈","vulnerabilities":"취약점의 원인과 대응","development":"개발하면서 적은 메모"}[key]
    desc={"all":"논문을 읽고 정리한 내용부터 보안 이슈와 개발 메모까지, 모든 글을 모았습니다.","ai":"논문이 다루는 문제와 접근 방법, 읽으면서 궁금했던 점을 정리합니다.","security":"위협을 분석하는 방법과 논문에서 제안한 대응을 살펴봅니다.","issues":"관심 있게 본 소식과 그 배경을 정리합니다.","vulnerabilities":"취약점이 발생하는 조건과 원인, 대응 방법을 정리합니다.","development":"구현하다 막힌 부분과 해결 과정, 다시 찾아볼 내용을 남깁니다."}[key]
    cards="".join(archive_card(p) for p in selected)
    empty='<div class="empty-library"><p class="command">$ ls ./records</p><h2>아직 기록이 없습니다.</h2><p>첫 번째 기록을 이곳에 차곡차곡 남길 예정입니다.</p></div>' if not selected else ""
    return f'<div class="archive-topline"><span><b>~/{e(item["label"])}</b><small>⑂ [branch: main ▾]</small></span>{search_box()}</div><header class="page-intro"><p class="reference-command"><b>$</b><span>grep -r "tip" ./{e(item["label"])}</span><i class="prompt-cursor" aria-hidden="true"></i></p><h1>{e(intro)}</h1><p>{e(desc)}</p></header>{filters(selected) if key == "all" and not legacy_category else ""}<span id="post-count" class="sr-only">{len(selected)}</span><div class="archive-cards">{cards}</div>{empty}<p class="search-empty" id="search-empty" hidden>일치하는 기록이 없습니다.</p><p class="sr-only" id="search-status" role="status" aria-live="polite"></p>'


def profile_json_html(profile):
    result=[]
    for line in json.dumps(profile,ensure_ascii=False,indent=2).splitlines():
        cursor=0
        parts=[]
        for match in re.finditer(r'"(?:\\.|[^"\\])*"',line):
            parts.append(e(line[cursor:match.start()]))
            is_key=line[match.end():].lstrip().startswith(":")
            parts.append(f'<span class="json-key"' + ('>' if is_key else ' data-value>') + e(match.group())+'</span>')
            cursor=match.end()
        parts.append(e(line[cursor:]))
        result.append("".join(parts))
    return "\n".join(result)


def about():
    profile={"name":DISPLAY_NAME,"name_ko":NAME_KO,"github":SITE["author"],"space":SITE_NAME,"interests":SITE["interests"],"note":"작은 기록이 다음의 나를 만듭니다."}
    technologies=SITE.get("tech_stack",[])
    stack="".join(f'<div class="tech-badge"><i></i><span>{e(t["name"])}</span><small>{e(t.get("version",""))}</small></div>' for t in technologies)
    contact=SITE.get("contacts",{})
    rows=[]
    for key,label in (("github","GitHub"),("twitter","Twitter"),("email","Email")):
        value=contact.get(key,"")
        value_html=e(value) if value else "—"
        if value and key in ("github","twitter") and value.startswith("https://"):
            value_html=f'<a href="{e(value)}">{e(value.removeprefix("https://"))} ↗</a>'
        if key == "email":
            value_html=f'<span id="contact-email">{value_html}</span><button class="email-copy" data-copy-target="contact-email"'+('' if value else ' disabled')+'><span>[copy]</span></button>'
        rows.append(f'<div><span class="tree-branch">{"└──" if key == "email" else "├──"}</span><span>{label}:</span>{value_html}</div>')
    return f'''<header class="profile-intro"><div class="profile-path"><span><b>~</b> / profile / <em>interactive_cli</em></span><small>bash</small></div><div><h1>터미널 프로필 <span>&amp; CLI</span></h1><small class="interactive-badge">{icon("terminal",12)} interactive</small></div></header><section class="profile-terminal" aria-label="블로그 소개 터미널"><div class="code-bar"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span><span>zsh — 80x24</span><span>UTF-8</span></div><div class="terminal-screen" id="cli-output" role="log" aria-label="명령 실행 결과"><div class="cli-welcome"><strong>{e(SITE_NAME)}</strong><p>Type <b>[help]</b> or click quick suggestions below to run commands.</p></div><div class="cli-entry"><p class="cli-prompt"><b>$</b> whoami</p><p class="cli-answer">{e(DISPLAY_NAME)} ({e(NAME_KO)}) · @{e(SITE["author"])}</p></div><div class="cli-entry"><p class="cli-prompt"><b>$</b> cat profile.json</p><pre class="profile-json">{profile_json_html(profile)}</pre></div><div class="cli-entry"><p class="cli-prompt"><b>$</b> tech-stack --visual</p><div class="tech-stack-panel"><div><span>// core technologies &amp; toolchains</span><span>{len(technologies)} loaded</span></div><div class="tech-badges">{stack}</div></div></div><div class="cli-entry"><p class="cli-prompt"><b>$</b> contact --links</p><div class="contact-tree">{"".join(rows)}</div></div><div id="cli-dynamic-output"></div><div class="active-prompt"><b>$</b><span id="terminal-input-display"></span><i class="prompt-cursor" aria-hidden="true"></i></div></div><div class="cli-controls"><div class="quick-commands"><button data-command="help">[help]</button><button data-command="posts">[posts]</button><button data-command="projects">[projects]</button><button data-command="skills">[skills]</button><button data-command="clear">[clear]</button></div><form id="cli-form" class="cli-form"><span aria-hidden="true">$</span><label class="sr-only" for="cli-input">블로그 탐색 명령 입력</label><input id="cli-input" type="text" placeholder="Type 'help' or command..." autocomplete="off" autocapitalize="off" spellcheck="false"><button type="submit">RUN ↵</button></form></div></section><div class="cli-status">// status: ready for input</div>'''


def article(post,index):
    headings=[(f'section-{i}',text) for i,(tag,text) in enumerate(post["body"],1) if tag == "h3"]
    toc="".join(f'<a href="#{anchor}"><span>{i:02}.</span>{e(text)}</a>' for i,(anchor,text) in enumerate(headings,1))
    blocks=[]
    section_number=0
    for i,(tag,text) in enumerate(post["body"],1):
        if tag == "p":blocks.append(f'<p>{e(text)}</p>')
        elif tag == "h3":
            section_number+=1
            blocks.append(f'<h2 id="section-{i}"><span>#{section_number:02}</span>{e(text)}</h2>')
        elif tag == "pre":blocks.append(reference_code(text,post.get("code_label",post["id"]+".md"),f'article-code-{i}',True,True))
        else:raise ValueError(f'Unknown body block: {tag}')
    neighbors=[]
    for offset,label in ((-1,"< PREV_LOG"),(1,"NEXT_LOG >")):
        target=index+offset
        if 0<=target<len(POSTS):
            item=POSTS[target]
            neighbors.append(f'<a class="{"nav-next" if offset==1 else "nav-prev"}" href="./{item["id"]}.html"><span>{e(label)}</span><h3>{e(item["title"])}</h3></a>')
    return f'''<header class="article-heading"><p class="reference-command"><b>$</b><span>cat article.md | render</span><i class="prompt-cursor" aria-hidden="true"></i></p><div class="article-category"><span class="tag">[{e(post["category"])}]</span><small>#{index+1:02}</small></div><h1>{e(post["title"])}</h1><div class="article-meta"><span class="article-author">Author: {e(DISPLAY_NAME)}</span><i>•</i><time datetime="{post["date"]}">{post["date"].replace("-", ".")}</time><i>•</i><span>{e(post["reading"].replace("분",""))} min read</span></div></header><nav class="article-toc" aria-label="이 글의 목차"><div><span>{icon("list",16)} TABLE_OF_CONTENTS.IDX</span><small>{len(headings)} {"section" if len(headings) == 1 else "sections"}</small></div>{toc}</nav><article class="article-body">{"".join(blocks)}</article><div class="article-tags"><span>TAGS:</span><a href="{category_url(post,'../')}">#{e(post["category"])}</a></div><nav class="post-navigation" aria-label="이전 글과 다음 글">{"".join(neighbors)}</nav>'''


def timeline():
    entries = []
    for i,post in enumerate(POSTS,1):
        entries.append(f'<article class="timeline-entry" data-post data-section="{e(section(post))}" data-search="{search_data(post)}"><div class="post-meta"><span class="tag">log-{i:04}</span><time datetime="{post["date"]}">{post["date"].replace("-", ".")}</time><span>{e(post["category"])} · {e(post["reading"])} 읽기</span></div><h2><a href="{post_url(post)}">{e(post["title"])}</a></h2><p>{e(post["summary"])}</p><footer><span>* author: @{e(SITE["author"])} · 예시 기록</span><a href="{post_url(post)}">// read log {icon("arrow",13)}</a></footer></article>')
    return f'<div class="archive-topline"><span><b>~/logs / timeline</b> <small>⑂ main</small></span>{search_box()}</div><header class="timeline-command"><p class="command">$ log --list --graph</p><p>Total: <b id="post-count">{len(POSTS)}</b> records <span>|</span> {len({p["category"] for p in POSTS})} categories</p><small>용도 미정 · 커밋 목록형 레이아웃 미리보기</small></header>{filters(POSTS)}<div class="timeline-list">{"".join(entries)}</div><p class="search-empty" id="search-empty" hidden>일치하는 기록이 없습니다.</p><p id="search-status" class="sr-only" role="status" aria-live="polite"></p>'


def write(filename, text):
    destination = ROOT / filename
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(text,encoding="utf-8")


write("index.html",page("~/workspace","workspace",home()))
for key in ("all","ai","security","issues","vulnerabilities","development"):
    item=NAV_BY_KEY[key]
    write(item["path"],page(item["label"],item["label"],archive(key),key,view="archive"))
write("about.html",page("about_me","profile / about_me",about(),"about",view="profile"))
write("timeline.html",page("timeline 미리보기","logs / timeline",timeline(),"all"))
for filename,category in (("projects.html","프로젝트"),("retrospectives.html","회고")):
    write(filename,page(category,category,archive("development",category),"development",view="archive"))
for index,post in enumerate(POSTS):
    key=section(post) if section(post) in NAV_BY_KEY else "all"
    write(f'posts/{post["id"]}.html',page(post["title"],f'logs / {post["id"]}.md',article(post,index),key,True,True,view="article",article_post=post))
print(f"Generated {11 + len(POSTS)} pages for {SITE_NAME}")
