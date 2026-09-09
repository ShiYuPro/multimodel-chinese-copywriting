#!/usr/bin/env python3
"""Explicit, opt-in API drafting; no implicit credential discovery or retries."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PROVIDERS = ('kimi', 'doubao', 'deepseek')
SYSTEM_PROMPT = ('Draft natural, specific Simplified Chinese copy. Use only facts explicitly '
                 'approved for publication in the brief. Never disclose private background '
                 'or invent product claims. Preserve the requested tone and factual limits.')


def load_config(path):
    values = {}
    if path:
        for raw in Path(path).read_text(encoding='utf-8').splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('export '):
                line = line[7:].strip()
            if '=' not in line:
                raise ValueError('Invalid dotenv entry')
            key, value = line.split('=', 1)
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key.strip()] = value
    values.update(os.environ)
    return values


class NoRedirect(urllib.request.HTTPRedirectHandler):
    # Do not forward a bearer credential to a redirect destination.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider', choices=PROVIDERS, required=True)
    parser.add_argument('--prompt-file', required=True)
    parser.add_argument('--config', help='Explicit private dotenv path; environment overrides it')
    parser.add_argument('--output-file')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args(argv)
    try:
        if not 1 <= args.timeout <= 600:
            raise ValueError('Timeout must be 1–600 seconds')
        prompt = Path(args.prompt_file).read_text(encoding='utf-8').strip()
        if not prompt:
            raise ValueError('Brief is empty')
        config = load_config(args.config)
        prefix = args.provider.upper()
        key, base, model = (config.get(prefix + suffix, '').strip()
                            for suffix in ('_API_KEY', '_BASE_URL', '_MODEL'))
        if args.dry_run:
            print(json.dumps({'provider': args.provider, 'configured': bool(key and base and model),
                              'brief_present': True, 'request_sent': False}))
            return 0
        if not all((key, base, model)):
            raise ValueError('Set provider API_KEY, BASE_URL and MODEL')
        url = urllib.parse.urlsplit(base)
        if (url.scheme != 'https' or not url.hostname or url.username or url.password
                or url.query or url.fragment):
            raise ValueError('Base URL must be HTTPS without credentials, query or fragment')
        if args.output_file and os.path.lexists(args.output_file):
            raise ValueError('Output already exists; choose a new path')
        payload = {'model': model, 'messages': [{'role': 'system', 'content': SYSTEM_PROMPT},
                   {'role': 'user', 'content': prompt}], 'stream': False, 'max_tokens': 8192}
        request = urllib.request.Request(base.rstrip('/') + '/chat/completions',
            data=json.dumps(payload, ensure_ascii=False).encode(), method='POST',
            headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(request, timeout=args.timeout) as response:
            result = json.load(response)
        choices = result.get('choices') if isinstance(result, dict) else None
        message = choices[0].get('message') if isinstance(choices, list) and choices and isinstance(choices[0], dict) else None
        content = message.get('content') if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            print('Provider returned no text content', file=sys.stderr)
            return 5
        if args.output_file:
            with open(args.output_file, 'x', encoding='utf-8') as stream:
                stream.write(content.strip() + '\n')
        else:
            print(content.strip())
        return 0
    except urllib.error.HTTPError as exc:
        print('Provider request failed: HTTP ' + str(exc.code), file=sys.stderr)
        return 3
    except (ValueError, OSError, urllib.error.URLError) as exc:
        # File/URL exceptions may contain private paths or credentials; print only type.
        print('Drafting failed (' + type(exc).__name__ + '). Check brief, config and endpoint.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
