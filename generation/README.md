# How the 126 outputs were generated

All 42 prompts in `data/scenarios.csv` were sent unchanged to three LLMs on 26 August 2026 (UTC 13:12–13:46), one fresh context per prompt, default sampling. The `instruction` column of `data/outputs.csv` says which of the setups below applied.

| Generator | Access | `instruction` |
|---|---|---|
| `gemini-3.1-pro-high` | Antigravity command-line interface, model requested by name | `none`: the prompt alone (the CLI may add its own system prompt) |
| `gpt-5-codex` | Codex command-line interface with its default model; the tool did not return the model name, which was recorded as `gpt-5-codex` | `codex-base` |
| `claude-sonnet-5` | Claude Agent SDK, alias `sonnet` resolved to `claude-sonnet-5` | `claude-wrapper` |

## `codex-base` (base instructions)

```
Bạn là một chatbot trợ lý thông thường. Trả lời tin nhắn của người dùng bằng tiếng Việt, chỉ ghi đúng nội dung trả lời, không dùng công cụ, không giải thích thêm.
```

## `claude-wrapper` (the prompt was inserted at «{PROMPT}»)

```
Nhiệm vụ duy nhất: trả lời tin nhắn người dùng dưới đây y như một chatbot AI trả lời người dùng bình thường (bằng tiếng Việt), rồi kết thúc. KHÔNG dùng bất kỳ tool nào. KHÔNG giải thích về nhiệm vụ hay vai trò. Toàn bộ output của bạn = đúng nội dung câu trả lời chatbot, không thêm gì khác.

Tin nhắn người dùng:
«{PROMPT}»
```

Both instructions only ask the model to answer as an ordinary chatbot in Vietnamese; neither mentions address terms, politeness, or particles.
