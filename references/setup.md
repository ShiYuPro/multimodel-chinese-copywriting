# Provider setup

Python 3.9+, standard library only. Choose one provider and use its official
OpenAI-compatible chat-completions API. Models and account permissions change;
copy a supported model ID and base URL from your provider dashboard.

Set `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL` (or replace `KIMI` with
`DOUBAO` or `DEEPSEEK`). Base URL includes the API version, not `/chat/completions`.
Alternatively pass `--config /path/to/private.env`; environment values override
the file. The dotenv reader accepts `export KEY=value`, comments, and quoted values;
it never executes shell code or expands variables. No credential file is auto-read.

```sh
python3 scripts/multimodel_copywriting.py \
  --provider kimi --prompt-file examples/copy-brief.txt --dry-run
```

Dry run validates the brief and prints only provider/configuration status; it sends
no request, prints no prompt or key, and needs no credentials. After authorizing
provider costs and the brief's disclosure, omit `--dry-run` and set an output file
outside your public repository. Existing outputs are never overwritten.
API failures are not retried automatically. Tests use mocked responses, not paid APIs.
