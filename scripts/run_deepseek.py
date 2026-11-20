#!/usr/bin/env python3
"""Run a design skill against the DeepSeek API (DeepSeek-only).

The skill's SKILL.md is sent as the system prompt; the brief is the user
message. Only https://api.deepseek.com is used.

Usage:
    export DEEPSEEK_API_KEY=sk-...
    python3 scripts/run_deepseek.py <skill> "<brief>"
    python3 scripts/run_deepseek.py <skill> --brief-file brief.md --model deepseek-reasoner
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ENDPOINT = "https://api.deepseek.com/chat/completions"
MODELS = ("deepseek-chat", "deepseek-reasoner")


def read_skill(name: str) -> str:
    path = SKILLS / name / "SKILL.md"
    if not path.is_file():
        available = ", ".join(sorted(p.name for p in SKILLS.iterdir() if p.is_dir()))
        raise SystemExit(f"skill '{name}' not found. Available: {available}")
    return path.read_text(encoding="utf-8")


def build_payload(model: str, skill_text: str, brief: str, max_tokens: int) -> dict:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": skill_text},
            {"role": "user", "content": brief},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stream": False,
    }


def call_deepseek(payload: dict, api_key: str) -> str:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        raise SystemExit(f"DeepSeek HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"DeepSeek connection error: {error.reason}") from error
    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as error:
        raise SystemExit(f"Unexpected DeepSeek response: {body}") from error


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a design skill against the DeepSeek API.")
    parser.add_argument("skill", help="skill folder name, e.g. landing-page-design")
    parser.add_argument("brief", nargs="?", default="", help="brief text")
    parser.add_argument("--brief-file", help="read the brief from a file")
    parser.add_argument("--model", default="deepseek-chat", choices=MODELS)
    parser.add_argument("--max-tokens", type=int, default=4000)
    parser.add_argument("--dry-run", action="store_true", help="print the request, do not call the API")
    args = parser.parse_args()

    brief = args.brief
    if args.brief_file:
        brief = Path(args.brief_file).read_text(encoding="utf-8")
    if not brief.strip():
        raise SystemExit("empty brief: pass text or --brief-file")

    payload = build_payload(args.model, read_skill(args.skill), brief, args.max_tokens)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY is not set (see .env.example)")

    print(call_deepseek(payload, api_key))


if __name__ == "__main__":
    main()
