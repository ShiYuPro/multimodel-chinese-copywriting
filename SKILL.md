---
name: multimodel-chinese-copywriting
description: Draft Simplified Chinese copy using a user-selected Kimi, Doubao, or DeepSeek API, then verify facts and implement it. Use when external-model drafting or comparison is requested; not every Chinese text edit.
---

# Multi-model Chinese copywriting

When external drafting is requested and authorized, use the selected provider for the first complete draft, then verify facts and implement the result. Read [setup](references/setup.md) before the first API call. Provider use can incur charges; installing this skill does not authorize paid calls or sending private information. Never silently claim a model was used when its request failed.

Mechanical replacement of approved text, deletion, spelling fixes, and internal rules or technical records do not require an external draft. User-selected providers override the default route.

## Suggested routing (user preference wins)

- Use Doubao first for ordinary public copy, conversational rewriting, and natural mainland Chinese expression.
- Use Kimi first for restrained tone, disclosure boundaries, sensitive wording, or copy where saying less is valuable.
- Use DeepSeek first for argument, critique, counterargument, structural diagnosis, and reasoning-heavy copy.
- Add a second model when the first draft feels unnatural, makes a doubtful judgment, or the choice materially affects the result.
- Consider all three for brand homepages, major partnerships, pricing/payment, health, safety, compliance, or another high-value public surface.
- Do not run multiple models mechanically when one good draft plus verification is enough.

No model is a factual authority. All three have added plausible but unsupported product claims even when told not to. Verify every public fact against source code, a real rendered page, authoritative material, or facts the user explicitly approved.

## Workflow

1. Read the relevant source and rendered page when layout or hierarchy matters.
2. Reuse relevant, approved product context already available; ask only for missing facts that materially affect the draft. Assemble a complete brief before calling a model. Separate task/audience/position/purpose, confirmed public facts, private background, preserved roles, and unknowns or prohibitions.
3. Treat newly mentioned personal or business details as background by default. A fact said in conversation is not automatically approved public copy.
4. Put the brief in a temporary file outside the project, then run `python3 <skill-dir>/scripts/multimodel_copywriting.py --provider <doubao|kimi|deepseek> --prompt-file <brief-file>`.
5. If comparison is warranted, call another provider with the identical factual brief. Do not let one model see the other's draft unless the task is explicitly critique or synthesis.
6. Preserve useful voice; change what is needed for facts, disclosure boundaries, completeness, duplication, page role, localization, or implementation constraints.
7. If the user asked only for diagnosis or discussion, do not edit project files. If the user asked for a change, implement and verify it.
8. State briefly which model drafted the copy and what Codex changed afterward.

## Brief format

```text
任务：
读者与其具体问题：
读者的主要顾虑（有证据时填写）：
位置与作用：
希望读者形成的判断：
唯一下一步行动：
可公开事实：
仅供理解、禁止写入：
必须保留：
需要避免：
期望输出：
```

Use positive instructions where possible. Keep hard prohibitions for actual factual, privacy, disclosure, legal, or product boundaries instead of stacking stylistic “do not” rules.

## Guardrails

- Never print, return, log, or place an API key in a prompt, project file, output, memory, or deployment record.
- Read credentials from environment variables, or an explicitly supplied `--config` dotenv file. Never discover or read unrelated credential stores.
- Never send one provider's key or private response to another provider.
- Do not send secrets, private records, unpublished commercial details, or background marked non-public to any external model unless the user explicitly authorizes that disclosure.
- If a request fails, report that provider's failure. A local draft may be offered or produced when the user authorizes a fallback; label its actual author.
- Use a model ID supported by the user’s account. Provider-specific thinking options are not assumed; configure the chosen endpoint explicitly.
- Do not modify public copy incrementally whenever the user supplies another fact. Rebuild the brief first.
