#!/usr/bin/env python3
"""Generate one source poem and two structural translations."""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "generation.json"
STATE_PATH = ROOT / "state" / "generation-state.json"
ARCHIVE_PATH = ROOT / "docs" / "archive.json"
LANGUAGE_DIR = ROOT / "languages"
GENERATED_DIR = ROOT / "poems" / "generated"

LANGUAGE_NAMES = {
    "arem": "アレム語",
    "en": "エン語",
    "vela": "ヴェラ語",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def read_language_specs() -> str:
    blocks: list[str] = []
    for code in ("arem", "en", "vela"):
        path = LANGUAGE_DIR / f"{code}.md"
        blocks.append(f"\n===== {LANGUAGE_NAMES[code]}の仕様 =====\n{path.read_text(encoding='utf-8')}")
    return "\n".join(blocks)


def read_recent_poems(limit: int = 4) -> str:
    files = sorted(GENERATED_DIR.glob("RP-*.md"))[-limit:]
    if not files:
        return "自動生成作品はまだない。初期三作品の規則を仕様書から継承すること。"
    excerpts: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        excerpts.append(f"\n===== {path.name} =====\n{text[:5000]}")
    return "\n".join(excerpts)


def build_prompt(source_language: str, state: dict[str, Any]) -> str:
    other_languages = [code for code in LANGUAGE_NAMES if code != source_language]
    schema = {
        "title_ja": "日本語題名",
        "title_en": "ASCIIまたは英語の短い識別題",
        "theme": "作品の中心題材を短く",
        "summary": "Pages掲載用の日本語概要。80字以内",
        "source_language": source_language,
        "source_poem": "原詩。改行を含む文字列",
        "source_translation_ja": "原詩の日本語訳",
        "translations": [
            {
                "language": other_languages[0],
                "poem": "翻訳詩",
                "translation_ja": "翻訳詩の日本語訳",
                "transformation": "何を保存できず、何へ変換したか",
            },
            {
                "language": other_languages[1],
                "poem": "翻訳詩",
                "translation_ja": "翻訳詩の日本語訳",
                "transformation": "何を保存できず、何へ変換したか",
            },
        ],
        "new_vocabulary": [
            {"language": source_language, "form": "語形", "meaning": "意味または用法"}
        ],
        "new_rules": ["必要な場合だけ。既存規則を壊さない小さな追加規則"],
        "unresolved": ["作品内に残った曖昧さや未解決事項"],
    }

    return f"""
あなたは架空言語学者であり詩人である。三つの人工言語が互いの詩を翻訳し、翻訳不能な構造を別の構造へ変形させる連作を一組だけ作成せよ。

今回の原詩言語は **{LANGUAGE_NAMES[source_language]} ({source_language})** で固定する。
残る二言語へ必ず一篇ずつ翻訳すること。

## 作品上の原則

- 読めない音列を雰囲気だけで並べてはならない。
- 各詩で言語固有の仕掛けが実際に作動し、日本語訳から追跡できるようにする。
- 三つの日本語訳を同じ内容にしない。翻訳による変形を残す。
- 既存語彙を優先し、新語は各言語0〜3語程度に抑える。
- 新規則は必要な場合だけ追加し、既存規則との関係を説明する。
- 題材を毎回ホラーに寄せない。静かな日常、自然、仕事、滑稽、身体、機械、抽象、共同体などから選べる。
- 読後に一つの像または考えが残る詩にする。仕掛けの実演だけで終わらせない。
- 最近の題名、題材、結末、中心像を反復しない。

## 最近の履歴

最近の題材: {json.dumps(state.get('recent_themes', []), ensure_ascii=False)}
最近の題名: {json.dumps(state.get('recent_titles', []), ensure_ascii=False)}
これまでに生じた追加規則: {json.dumps(state.get('new_rules', []), ensure_ascii=False)}

## 三言語の正式仕様

{read_language_specs()}

## 最近の自動生成作品

{read_recent_poems()}

## 出力形式

次のJSONオブジェクトだけを出力すること。Markdownコードフェンス、前置き、後書きは禁止する。
改行を含む詩はJSON文字列内で正しくエスケープすること。

{json.dumps(schema, ensure_ascii=False, indent=2)}
""".strip()


def request_generation(config: dict[str, Any], prompt: str) -> dict[str, Any]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is not set")

    model = config["model"]["name"]
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "言語規則を厳密に扱い、指定されたJSONだけを返す詩人として応答する。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": config["model"].get("temperature", 0.9),
        "max_tokens": 7500,
    }

    request = urllib.request.Request(
        "https://models.github.ai/inference/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2026-03-10",
        },
        method="POST",
    )

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            return parse_json_content(content)
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"GitHub Models request failed: {last_error}")


def parse_json_content(content: str) -> dict[str, Any]:
    text = content.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise json.JSONDecodeError("No JSON object found", text, 0)
    value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Model response must be a JSON object")
    return value


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def validate_generation(data: dict[str, Any], expected_source: str, state: dict[str, Any]) -> None:
    for field in ("title_ja", "title_en", "theme", "summary", "source_poem", "source_translation_ja"):
        require_text(data.get(field), field)

    if data.get("source_language") != expected_source:
        raise ValueError("The model changed the required source language")

    if data["title_ja"] in state.get("recent_titles", []):
        raise ValueError("The model repeated a recent title")

    source_lines = [line for line in data["source_poem"].splitlines() if line.strip()]
    if len(source_lines) < 3:
        raise ValueError("The source poem is too short")

    translations = data.get("translations")
    if not isinstance(translations, list) or len(translations) != 2:
        raise ValueError("Exactly two translations are required")

    expected_targets = set(LANGUAGE_NAMES) - {expected_source}
    actual_targets: set[str] = set()
    japanese_versions = {data["source_translation_ja"].strip()}
    for index, translation in enumerate(translations):
        if not isinstance(translation, dict):
            raise ValueError(f"translations[{index}] must be an object")
        language = translation.get("language")
        if language not in expected_targets:
            raise ValueError(f"Unexpected translation language: {language}")
        actual_targets.add(language)
        require_text(translation.get("poem"), f"translations[{index}].poem")
        japanese = require_text(translation.get("translation_ja"), f"translations[{index}].translation_ja")
        require_text(translation.get("transformation"), f"translations[{index}].transformation")
        japanese_versions.add(japanese)

    if actual_targets != expected_targets:
        raise ValueError("Both target languages must appear exactly once")
    if len(japanese_versions) != 3:
        raise ValueError("The three Japanese translations must differ")

    for optional_list in ("new_vocabulary", "new_rules", "unresolved"):
        value = data.get(optional_list, [])
        if not isinstance(value, list):
            raise ValueError(f"{optional_list} must be an array")


def quote_block(text: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def render_markdown(serial: int, generated_at: datetime, data: dict[str, Any]) -> str:
    source = data["source_language"]
    translations = {item["language"]: item for item in data["translations"]}
    ordered_targets = [code for code in ("arem", "en", "vela") if code != source]

    parts = [
        f"# {data['title_ja']}",
        "",
        f"- 管理番号：`RP-{serial:04d}`",
        f"- 生成日時：{generated_at.isoformat(timespec='minutes')}",
        f"- 原詩言語：{LANGUAGE_NAMES[source]}",
        f"- 題材：{data['theme']}",
        "",
        data["summary"],
        "",
        f"## 原詩 — {LANGUAGE_NAMES[source]}",
        "",
        quote_block(data["source_poem"]),
        "",
        "### 日本語訳",
        "",
        data["source_translation_ja"],
    ]

    for target in ordered_targets:
        item = translations[target]
        parts.extend(
            [
                "",
                f"## 翻訳 — {LANGUAGE_NAMES[target]}",
                "",
                quote_block(item["poem"]),
                "",
                "### 日本語訳",
                "",
                item["translation_ja"],
                "",
                "### 翻訳による変形",
                "",
                item["transformation"],
            ]
        )

    vocabulary = data.get("new_vocabulary", [])
    rules = data.get("new_rules", [])
    unresolved = data.get("unresolved", [])

    parts.extend(["", "## 今回生じた語彙・規則", ""])
    if vocabulary:
        for item in vocabulary:
            if isinstance(item, dict):
                language = LANGUAGE_NAMES.get(str(item.get("language")), str(item.get("language", "不明")))
                parts.append(f"- **{language} / {item.get('form', '—')}**：{item.get('meaning', '—')}")
            else:
                parts.append(f"- {item}")
    else:
        parts.append("- 新規語彙なし。")

    if rules:
        parts.append("")
        parts.append("### 新規則")
        parts.append("")
        parts.extend(f"- {rule}" for rule in rules)

    parts.extend(["", "## 未解決事項", ""])
    if unresolved:
        parts.extend(f"- {item}" for item in unresolved)
    else:
        parts.append("- なし。")

    parts.append("")
    return "\n".join(parts)


def main() -> int:
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)
    if not config.get("enabled"):
        print("Generation is disabled.")
        return 0

    order = config["language_selection"]["order"]
    index = int(state.get("next_language_index", 0)) % len(order)
    source_language = order[index]
    serial = int(state.get("last_serial", 0)) + 1

    prompt = build_prompt(source_language, state)
    data = request_generation(config, prompt)
    validate_generation(data, source_language, state)

    timezone = ZoneInfo(config.get("timezone", "Asia/Tokyo"))
    generated_at = datetime.now(timezone)
    output_dir = ROOT / config["output"]["directory"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"RP-{serial:04d}.md"
    output_path.write_text(render_markdown(serial, generated_at, data), encoding="utf-8", newline="\n")

    repo = os.environ.get("GITHUB_REPOSITORY", "lafcadio896-cyber/recursive-poetics")
    archive = load_json(ARCHIVE_PATH)
    if not isinstance(archive, list):
        raise ValueError("docs/archive.json must contain an array")
    archive.insert(
        0,
        {
            "id": f"RP-{serial:04d}",
            "title": data["title_ja"],
            "date": generated_at.date().isoformat(),
            "source_language": source_language,
            "source_language_name": LANGUAGE_NAMES[source_language],
            "summary": data["summary"],
            "theme": data["theme"],
            "href": f"https://github.com/{repo}/blob/main/{output_path.relative_to(ROOT).as_posix()}",
        },
    )
    write_json(ARCHIVE_PATH, archive)

    recent_themes = [data["theme"], *state.get("recent_themes", [])][:12]
    recent_titles = [data["title_ja"], *state.get("recent_titles", [])][:40]
    new_rules = [*state.get("new_rules", []), *data.get("new_rules", [])][-30:]
    state.update(
        {
            "last_serial": serial,
            "next_language_index": (index + 1) % len(order),
            "recent_themes": recent_themes,
            "recent_titles": recent_titles,
            "new_rules": new_rules,
        }
    )
    write_json(STATE_PATH, state)

    print(f"Generated {output_path.relative_to(ROOT)} from {source_language}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Generation failed: {error}", file=sys.stderr)
        raise
