# AI Design Skills — DeepSeek fork

> Fork of [elayadesign/ai-design-skills](https://github.com/elayadesign/ai-design-skills) adapted to run **only with DeepSeek**: [DeepSeek Harness](https://github.com/deepseek-ai) (DSH) and the DeepSeek API. The original Claude/Cursor/Codex instructions were replaced by DeepSeek-only ones; the skills themselves are provider-agnostic Markdown.

A growing collection of design skills. Each skill is a self-contained folder; install the ones you need.

## Skills

| Skill | What it does |
|---|---|
| [`landing-page-design`](./skills/landing-page-design/SKILL.md) | Builds a landing page from scratch — intake questions, page structure, conversion copy, plus a full visual system (type, spacing, radius, motion) |
| [`figma-designer`](./skills/figma-designer/SKILL.md) | Designs inside Figma with real structure: spacing, radius and color variables, named text styles, auto layout, components with every state, and a Foundations frame that updates with the tokens |

## Install in DeepSeek Harness (DSH)

DSH reads user skills from `~/.agents/skills/<name>/SKILL.md`.

```bash
./scripts/install_dsh.sh
```

Then start a new DSH session (or restart it) so the catalog picks the skills up. The script honours `DSH_SKILLS_DIR` if you keep skills elsewhere.

## Run a skill with the DeepSeek API

```bash
export DEEPSEEK_API_KEY=sk-...
python3 scripts/run_deepseek.py landing-page-design "Landing para una estética canina en Guadalajara"
```

Options:

```bash
python3 scripts/run_deepseek.py --help
# --model deepseek-chat | deepseek-reasoner   (default: deepseek-chat)
# --brief-file brief.md                        read the brief from a file
# --max-tokens 4000
# --dry-run                                    print the request without calling the API
```

The script sends the skill as the system prompt and your brief as the user message, using only `https://api.deepseek.com`. Nothing else is called.

## Validate

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover tests
```

## License

MIT — see [LICENSE](./LICENSE). Original skills by [Elaya](https://github.com/elayadesign).
