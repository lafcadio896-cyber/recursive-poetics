from pathlib import Path

DOCS = Path("docs")

READER_JS = r'''(() => {
  const roots = {
    mr:'光', sl:'水・水面', nl:'名', kt:'手', vl:'声', lm:'家', hr:'息・呼吸', dr:'扉・境界',
    nv:'雨', ms:'窓', tr:'鳥', rf:'屋根', mn:'月', sr:'海', kl:'子ども', yr:'夜明け', dt:'死者'
  };
  const phases = {a:'現在相', i:'内在相', o:'離行相', u:'欠如相', e:'接近相'};
  const relations = {na:'接触している・上にある', vi:'内部にある', ra:'離れていく', do:'後ろに残る', ve:'近づいていく'};
  const enPairs = {
    'ma ri':'光','ri se':'水面に触れる','se no':'記憶になる','no ta':'名','ta ku':'手の中にある',
    'ku ve':'声','ve li':'家に残る','li ho':'息','ho du':'扉の後ろにある','du re':'失われる','re ma':'戻ってくる',
    'se ra':'月','ra tu':'沈む','tu ko':'鳥','ko na':'戻って歌う','na ve':'雨','ko ra':'屋根',
    'ra na':'雨が始まる','ve sa':'声','sa li':'残る','li so':'静けさになる','so mi':'屋根が覚えている',
    'mi re':'去ったもの','re tu':'去ったものを鳥と呼ぶ','ve lo':'静かに休む','lo ri':'窓',
    'ri ma':'朝','ma se':'開く','se tu':'カーテン','tu ra':'飛び立つ（欠落読み）'
  };
  const vela = {
    nave:'雨',lori:'静かに休む',mase:'窓',mira:'明かり',seno:'燃える',talu:'廊下',sali:'子ども',more:'描く',navi:'扉',keno:'朝',vari:'開く',sume:'カーテン',tora:'鳥',mise:'歌う',nalu:'屋根',
    mare:'光',lino:'水・水面',saku:'触れる',nami:'名',sera:'手',toku:'眠る・静止する',vela:'声',nori:'家',mado:'残る',hara:'息',dume:'扉の向こう',rino:'戻る',
    kali:'子ども',mora:'月',seyo:'見る',ratu:'海',vame:'覚えている',nika:'記憶の中の子ども',kesu:'開いた扉',meyo:'夜明け',
    mareli:'誰かが呼ぶ',nosaku:'消された名前',namise:'手だけが覚えている',ratoku:'声が忘れたもの',velano:'家が開いている',rimado:'死者の後ろで',haradu:'息が近づく',merino:'どの身体からでもなく',
    kalimo:'昨日が始まる',raseyo:'扉の後で',ratuva:'海が覚えている',menika:'まだ起きていないこと',kesume:'夜明けが戻る',yokali:'子どもがそれを開いたために',morase:'月が沈む',yoratu:'朝が来た後に',
    navelo:'死者たちが戻る',rimase:'顔を持たずに',mirase:'誰も気づかない',notalu:'すでに中に立っている',salimo:'家が覚えている',renavi:'あなたの手',kenova:'あなたの名は失われた',risume:'それでも返事をする',torami:'上を見てはいけない',senalu:'屋根が呼吸している',
    toralo:'屋根が覚えている',rinalu:'去った後の鳥',navemi:'雨が繰り返す',semase:'失われた歌',miramo:'昼の光が描く',renalu:'羽のない空所'
  };

  function aremToken(token) {
    const clean = token.toLowerCase().replace(/[^a-z]/g, '');
    if (relations[clean]) return relations[clean];
    if (clean.length !== 3) return token;
    const root = clean[0] + clean[2];
    return roots[root] && phases[clean[1]] ? `${phases[clean[1]]}の${roots[root]}` : token;
  }
  function translateArem(line) {
    return line.split(/\s+/).filter(Boolean).map(aremToken).join(' ｜ ');
  }
  function enSequence(sequence) {
    const words = sequence.trim().split(/\s+/).filter(Boolean);
    const meanings = [];
    for (let i = 0; i < words.length - 1; i++) {
      const pair = `${words[i]} ${words[i + 1]}`;
      meanings.push(enPairs[pair] || `未説明語対：${pair}`);
    }
    return meanings.join(' → ');
  }
  function translateEn(line) {
    if (line.includes('→')) return line.split('→').map(enSequence).join(' ／ 変化後：');
    return enSequence(line);
  }
  function velaSequence(sequence) {
    return sequence.trim().split(/[\s/]+/).filter(Boolean).map(word => vela[word] || `未説明語：${word}`).join(' ｜ ');
  }
  function translateVela(line) {
    if (line.includes('→')) {
      const [surface, spoken] = line.split('→');
      return `連音 ${surface.trim()} ／ 発声：${velaSequence(spoken)}`;
    }
    return velaSequence(line);
  }
  function translate(section, line) {
    if (section.id === 'arem') return translateArem(line);
    if (section.id === 'en') return translateEn(line);
    if (section.id === 'vela') return translateVela(line);
    return '';
  }

  document.querySelectorAll('.language-poem').forEach(section => {
    section.querySelectorAll('pre.verse').forEach(pre => {
      if (pre.closest('.parallel-verse')) return;
      const lines = pre.textContent.trim().split('\n').map(line => line.trim()).filter(Boolean);
      const grid = document.createElement('div');
      grid.className = 'parallel-verse';
      grid.innerHTML = '<div class="parallel-head">原詩</div><div class="parallel-head">逐語訳</div>';
      lines.forEach(line => {
        const original = document.createElement('div');
        original.className = 'parallel-original';
        original.textContent = line;
        const translated = document.createElement('div');
        translated.className = 'parallel-translation';
        translated.textContent = translate(section, line);
        grid.append(original, translated);
      });
      pre.replaceWith(grid);
    });
  });
})();
'''

CSS = r'''
/* parallel-poem-v3 */
.parallel-verse {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  margin: 0;
  border-top: 1px solid var(--line);
  font-size: clamp(.88rem, 1.45vw, 1rem);
}
.parallel-head {
  padding: .7rem 0 1rem;
  color: var(--muted);
  border-bottom: 1px solid var(--ink);
  font-family: var(--mono);
  font-size: .64rem;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.parallel-head:nth-child(2) { padding-left: 1.5rem; border-left: 1px solid var(--line); }
.parallel-original,
.parallel-translation {
  min-width: 0;
  padding: 1rem 0;
  border-bottom: 1px solid var(--line);
  line-height: 1.85;
}
.parallel-original {
  padding-right: 1.5rem;
  font-family: var(--mono);
  overflow-wrap: anywhere;
}
.parallel-translation {
  padding-left: 1.5rem;
  border-left: 1px solid var(--line);
}
@media (max-width: 620px) {
  .parallel-verse { grid-template-columns: 1fr; }
  .parallel-head { display: none; }
  .parallel-original {
    padding: 1.25rem 0 .45rem;
    border-bottom: 0;
  }
  .parallel-original::before,
  .parallel-translation::before {
    display: block;
    margin-bottom: .5rem;
    color: var(--muted);
    font-family: var(--mono);
    font-size: .58rem;
    letter-spacing: .1em;
  }
  .parallel-original::before { content: '原詩'; }
  .parallel-translation::before { content: '逐語訳'; }
  .parallel-translation {
    padding: 0 0 1.25rem;
    border-left: 0;
  }
}
'''

RULES = r'''

## Pages本文の並列表記

作品ページでは、架空言語本文と対応する日本語の逐語訳を同じ行の左右に配置する。

```text
原詩                 逐語訳
Mar na sal.           現在相の光｜接触している｜現在相の水
```

- PC・タブレットでは二列で表示する
- スマートフォンでは「原詩」「逐語訳」の順に縦積みする
- 一行の原詩と一行の逐語訳を一対一で対応させる
- 自然な日本語訳と翻訳による変形は、並列表記の後に独立して掲載する
- アレム語は各語の語根と母音相が見える直訳にする
- エン語は単語訳ではなく全隣接語対の意味列を表示する
- ヴェラ語は表層分節と発声分節を別々に表示する
- 今後生成するHTMLは `.parallel-verse`、`.parallel-original`、`.parallel-translation` の構造を直接出力する
'''


def main() -> None:
    (DOCS / "reader.js").write_text(READER_JS, encoding="utf-8")

    for page in sorted((DOCS / "poems").glob("RP-*.html")):
        text = page.read_text(encoding="utf-8")
        if "../reader.js" not in text:
            text = text.replace("</head>", '  <script src="../reader.js" defer></script>\n</head>')
            page.write_text(text, encoding="utf-8")

    css_path = DOCS / "reader.css"
    css = css_path.read_text(encoding="utf-8")
    if "/* parallel-poem-v3 */" not in css:
        css_path.write_text(css.rstrip() + "\n" + CSS.strip() + "\n", encoding="utf-8")

    generation = Path("GENERATION.md")
    text = generation.read_text(encoding="utf-8")
    if "## Pages本文の並列表記" not in text:
        generation.write_text(text.rstrip() + RULES + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
