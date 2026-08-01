# recursive-poetics

架空言語が互いの詩を翻訳し、そのたびに詩の構造そのものが変形していく実験詩集です。

意味の一致ではなく、翻訳先の言語が**何を保存できず、代わりにどの構造へ変形したか**を作品として残します。

## 三つの言語

| 言語 | 仕掛け | 仕様 | 語彙集 |
|---|---|---|---|
| アレム語 | 子音が概念、母音が距離・存在状態を表す | [`languages/arem.md`](languages/arem.md) | [`lexicon/arem.md`](lexicon/arem.md) |
| エン語 | 隣接する二語の間にだけ意味が生じる | [`languages/en.md`](languages/en.md) | [`lexicon/en.md`](lexicon/en.md) |
| ヴェラ語 | 黙読と朗読で語の境界と意味が変わる | [`languages/vela.md`](languages/vela.md) | [`lexicon/vela.md`](lexicon/vela.md) |

語彙集の共通運用規則は [`lexicon/README.md`](lexicon/README.md) にあります。新作で使用した新語は、作品と同時に語彙集へ追加します。

## 言語としての状態

三言語は、自然言語のように何でも会話できる完成言語ではなく、詩的機能を中心に設計した人工言語です。

初期作品には辞書確定前の語義衝突があるため、語彙集で正規語彙と旧用法を区別しています。今後の作品では正規語彙を固定し、読者が辞書から自力で翻訳できる状態へ育てます。

## 最初の翻訳環

三つの原詩を三言語で相互翻訳し、九つの詩形を収録しています。

1. [`帰光`](poems/01-returning-light.md) — アレム語原詩
2. [`始点のない朝`](poems/02-morning-without-origin.md) — エン語原詩
3. [`窓に雨がある`](poems/03-rain-at-window.md) — ヴェラ語原詩

## 自動生成

ChatGPTのスケジュール機能が、月曜・水曜・金曜の午前3時03分（Asia/Tokyo）に一組の相互翻訳詩を生成します。

- 原詩言語はアレム語 → エン語 → ヴェラ語の順で循環
- 一回につき原詩1篇と翻訳2篇を生成
- 生成前に言語仕様・語彙集・過去作品・状態ファイルを読む
- 新語と新規則を語彙集へ追記
- 語義衝突を検出した場合は公開しない
- 完成物は `main` に直接反映
- 人間によるレビュー、承認、修正は行わない

詳細は [`GENERATION.md`](GENERATION.md)、機械設定は [`config/generation.json`](config/generation.json) にあります。

## Pages

閲覧用ページは [`docs/`](docs/) にあります。GitHub Pagesの公開元を `main` ブランチの `/docs` に設定すると、初期作品と自動生成アーカイブを閲覧できます。
