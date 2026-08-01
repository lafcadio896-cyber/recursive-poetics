# recursive-poetics

架空言語が互いの詩を翻訳し、そのたびに詩の構造そのものが変形していく実験詩集です。

意味の一致ではなく、翻訳先の言語が**何を保存できず、代わりにどの構造へ変形したか**を作品として残します。

## 三つの言語

| 言語 | 仕掛け | 仕様 |
|---|---|---|
| アレム語 | 子音が概念、母音が距離・存在状態を表す | [`languages/arem.md`](languages/arem.md) |
| エン語 | 隣接する二語の間にだけ意味が生じる | [`languages/en.md`](languages/en.md) |
| ヴェラ語 | 黙読と朗読で語の境界と意味が変わる | [`languages/vela.md`](languages/vela.md) |

## 最初の翻訳環

三つの原詩を三言語で相互翻訳し、九つの詩形を収録しています。

1. [`帰光`](poems/01-returning-light.md) — アレム語原詩
2. [`始点のない朝`](poems/02-morning-without-origin.md) — エン語原詩
3. [`窓に雨がある`](poems/03-rain-at-window.md) — ヴェラ語原詩

## 自動生成

生成方針の草案は [`GENERATION.md`](GENERATION.md) にあります。

設定の差し込み先として [`config/generation.json`](config/generation.json) を用意していますが、現時点では `enabled: false` です。実行頻度と実行時刻は未決定です。

一回の実行では、原詩一篇と残り二言語への翻訳を生成し、三つの詩形を一組としてPRにします。

## Pages

閲覧用ページは [`docs/`](docs/) にあります。GitHub Pagesを有効にする場合は、公開元を `main` ブランチの `/docs` に設定します。
