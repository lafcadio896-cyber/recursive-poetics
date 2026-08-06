from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- reading-format-v2 -->"

LEARNING = {
"RP-0001": {
"arem": [("tar / tor / tur / tir", "鳥。語根 t-r。現在→離行→欠如→内在"), ("raf / rif", "屋根。語根 r-f。現在／内在"), ("val / vol / vul / vil", "声。語根 v-l。現在→離行→欠如→内在"), ("nav / niv", "雨。語根 n-v。現在／内在"), ("na / vi / ra / do", "接触／内部／離行／後方残留")],
"en": [("tu ko", "鳥"), ("ko ra", "屋根"), ("ra na", "雨が始まる"), ("na ve", "雨"), ("ve sa", "声"), ("sa li", "残る"), ("li so", "静けさになる"), ("so mi", "屋根が覚えている"), ("mi re", "去ったもの"), ("re tu", "去ったものを鳥と呼ぶ")],
"vela": [("tora / lori / nalu", "鳥／静かに休む／屋根"), ("toralo / rinalu", "屋根が覚えている／去った後の鳥"), ("nave / mise / mase", "雨／歌う／窓"), ("navemi / semase", "雨が繰り返す／失われた歌"), ("mira / more / nalu", "明かり／描く／屋根"), ("miramo / renalu", "昼の光が描く／羽のない空所")]
},
"RP-0002": {
"en": [("ma ri", "光"), ("ri se", "水面に触れる"), ("se ra", "月"), ("ra tu", "沈む"), ("tu ko", "鳥"), ("ko na", "戻って歌う"), ("na ve", "雨"), ("ve li", "家に残る"), ("li ho", "息"), ("ho du", "扉の後ろにある"), ("du re", "失われる"), ("re ma", "戻ってくる")],
"arem": [("mar / mir / mor / mur / mer", "光。現在→内在→離行→欠如→接近"), ("man / min / mon / mun / men", "月。同じ五相"), ("tar / tir / tor / tur / ter", "鳥。同じ五相"), ("nav / niv / nov / nuv / nev", "雨。同じ五相"), ("har / hir / hor / hur / her", "息。同じ五相")],
"vela": [("mora / seyo / ratu", "月／見る／海"), ("morase / yoratu", "月が沈む／朝が来た後に"), ("hara / dume / rino", "息／扉の向こう／戻る"), ("haradu / merino", "息が近づく／どの身体からでもなく"), ("mare / lino / saku", "光／水面／触れる"), ("mareli / nosaku", "誰かが呼ぶ／消された名前")]
},
"RP-0003": {
"vela": [("nami / sera / toku", "名／手／眠る"), ("namise / ratoku", "手だけが覚えている／声が忘れたもの"), ("nave / lori / mase", "雨／静かに休む／窓"), ("navelo / rimase", "死者たちが戻る／顔を持たずに"), ("tora / lori / nalu", "鳥／静かに休む／屋根"), ("toralo / rinalu", "屋根が覚えている／去った後の鳥")],
"arem": [("nal / nil / nul", "名。現在→内在→欠如"), ("kat / kit / kut", "手。現在→内在→欠如"), ("nav / niv / nuv", "雨。現在→内在→欠如"), ("mar / mir / mur", "光。現在→内在→欠如"), ("tar / tir / tur", "鳥。現在→内在→欠如")],
"en": [("tu ko", "鳥"), ("ko ra", "屋根"), ("ra na", "雨が始まる"), ("na ve", "雨"), ("ve lo", "静かに休む"), ("lo ri", "窓"), ("ri ma", "朝"), ("ma se", "開く"), ("se tu", "カーテン")]
},
"RP-0004": {
"arem": [("mar / mir / mur / mer", "光。現在→内在→欠如→接近"), ("sal / sil / sul / sel", "水。現在→内在→欠如→接近"), ("val / vil / vul / vel", "声。現在→内在→欠如→接近"), ("lam / lim / lum / lem", "家。現在→内在→欠如→接近"), ("har / hir / hur / her", "息。現在→内在→欠如→接近"), ("dar / dir / dur / der", "扉。現在→内在→欠如→接近")],
"en": [("ma ri", "光"), ("ri se", "水面に触れる"), ("se no", "記憶になる"), ("no ta", "名"), ("ta ku", "手の中にある"), ("ku ve", "声"), ("ve li", "家に残る"), ("li ho", "息"), ("ho du", "扉の後ろにある"), ("du re", "失われる"), ("re ma", "戻ってくる")],
"vela": [("mare / lino / saku", "光／水面／触れる"), ("mareli / nosaku", "誰かが呼ぶ／消された名前"), ("nami / sera / toku", "名／手／眠る"), ("namise / ratoku", "手だけが覚えている／声が忘れたもの"), ("vela / nori / mado", "声／家／残る"), ("velano / rimado", "家が開いている／死者の後ろで"), ("hara / dume / rino", "息／扉の向こう／戻る"), ("haradu / merino", "息が近づく／どの身体からでもなく")]
}}

NAMES = {"arem": "アレム語", "en": "エン語", "vela": "ヴェラ語"}
ORDER = ["arem", "en", "vela"]

def md_block(pid):
    parts = [MARKER, "\n## 読解ガイド — 逐語訳と学習語彙\n", "以下は詩的な解釈ではなく、辞書に登録された構造を追うための補助である。自然な日本語訳とは分けて読む。\n"]
    for lang in ORDER:
        rows = LEARNING[pid][lang]
        parts += [f"### {NAMES[lang]} — 構造直訳\n", "| 語・語対 | 辞書上の読み |\n|---|---|\n"]
        parts += [f"| `{a}` | {b} |\n" for a,b in rows]
        if lang == "arem":
            parts.append("\n子音骨格が概念、母音が存在相を示す。自然訳で補われた主語・時制・因果は、原語そのものには含まれない。\n")
        elif lang == "en":
            parts.append("\n単語単独では訳さず、隣接する二語を一単位として左から読む。始点変更による因果は解釈であり、語対の意味自体は変わらない。\n")
        else:
            parts.append("\n表層語と発声語を別々に逐語化する。同じ連続音列から得られる二つの語列を、ひとつの日本語文へ混ぜない。\n")
    parts.append("\n### 今回覚えられる語\n\n上表のうち、既出作品でも反復している語を優先して覚える。辞書語義と自然訳が異なる場合は、辞書語義を基準とする。\n")
    return "".join(parts)

def html_block(pid):
    out = [MARKER, '<section class="reading-guide" id="reading-guide">', '<header class="language-header"><p class="language-kicker">LEARNING APPENDIX</p><h2>逐語訳と学習語彙</h2></header>', '<p class="guide-intro">詩的な自然訳と、辞書に基づく構造直訳を分けて読むための補助です。</p>']
    for lang in ORDER:
        out.append(f'<section class="gloss-language"><h3>{NAMES[lang]}</h3><div class="gloss-table"><table><thead><tr><th>語・語対</th><th>辞書上の読み</th></tr></thead><tbody>')
        for a,b in LEARNING[pid][lang]:
            out.append(f'<tr><td><code>{a}</code></td><td>{b}</td></tr>')
        out.append('</tbody></table></div>')
        note = {"arem":"子音骨格が概念、母音が存在相を示します。自然訳で補った因果は原語そのものと区別します。","en":"単語単独ではなく、全隣接語対を左から追います。","vela":"表層語と発声語を別々に逐語化し、二つの読みを混合しません。"}[lang]
        out.append(f'<p class="structure-note">{note}</p><div class="lexicon-links"><a href="../lexicon/{lang}.html">{NAMES[lang]}辞書</a></div></section>')
    out.append('<div class="remember-words"><h3>今回覚えられる語</h3><p>上表の反復語を優先して覚えます。自然訳と差がある場合は辞書語義を基準にします。</p></div></section>')
    return "".join(out)

def insert_before(text, anchor, block):
    if MARKER in text:
        return text
    pos = text.find(anchor)
    if pos < 0:
        return text + "\n" + block
    return text[:pos] + block + "\n\n" + text[pos:]

for pid in LEARNING:
    md = ROOT / "poems" / "generated" / f"{pid}.md"
    text = md.read_text(encoding="utf-8")
    text = insert_before(text, "## 今回", md_block(pid))
    md.write_text(text, encoding="utf-8")

    html = ROOT / "docs" / "poems" / f"{pid}.html"
    text = html.read_text(encoding="utf-8")
    text = insert_before(text, "</main>", html_block(pid))
    html.write_text(text, encoding="utf-8")

spec = ROOT / "GENERATION.md"
s = spec.read_text(encoding="utf-8")
rule = '''\n## 標準読解フォーマット\n\n各言語章は、必ず次の層を分離して掲載する。\n\n1. 架空言語本文\n2. 逐語訳または構造直訳\n3. 自然な日本語訳\n4. その言語固有の構造説明\n5. 翻訳による変形\n6. Pages内の辞書リンク\n7. 今回覚えられる語彙\n\n逐語訳では辞書語義を優先し、自然な日本語にするための主語・時制・因果・情緒を無断で混ぜない。補足した要素は自然訳または構造説明へ分離する。アレム語は語根と母音相、エン語は全隣接語対、ヴェラ語は表層分節と発声分節を必ず示す。\n'''
if "## 標準読解フォーマット" not in s:
    s += rule
    spec.write_text(s, encoding="utf-8")

css = ROOT / "docs" / "reader.css"
c = css.read_text(encoding="utf-8")
css_add = '''\n/* reading-format-v2 */\n.reading-guide { margin: 8rem 0 4rem; padding-top: 4rem; border-top: 1px solid var(--ink); }\n.guide-intro, .structure-note { max-width: 46rem; line-height: 1.9; }\n.gloss-language { margin-top: 4rem; }\n.gloss-table { overflow-x: auto; margin: 1.5rem 0; }\n.gloss-table table { width: 100%; border-collapse: collapse; }\n.gloss-table th, .gloss-table td { padding: .8rem .6rem; border-bottom: 1px solid var(--line, #d8d4ca); text-align: left; vertical-align: top; }\n.gloss-table th { font-family: var(--mono); font-size: .68rem; letter-spacing: .08em; color: var(--muted); }\n.remember-words { margin-top: 5rem; padding: 2rem 0; border-top: 1px solid var(--ink); }\n'''
if "reading-format-v2" not in c:
    css.write_text(c + css_add, encoding="utf-8")
