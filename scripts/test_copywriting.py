import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

spec=importlib.util.spec_from_file_location('copywriting',Path(__file__).with_name('multimodel_copywriting.py'))
a=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class Drafting(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.brief=self.root/'brief.txt'
        self.brief.write_text('Public fictional product brief')
        self.args=['--provider','kimi','--prompt-file',str(self.brief)]
        self.env={'KIMI_API_KEY':'test-secret-not-real','KIMI_BASE_URL':'https://example.com/v1','KIMI_MODEL':'test-model'}

    def run_main(self, extra=(), response=None, env=None):
        output=io.StringIO()
        opener=MagicMock()
        opener.open.return_value.__enter__.return_value=io.StringIO(json.dumps(response))
        with patch.dict(os.environ,self.env if env is None else env,clear=True), patch.object(a.urllib.request,'build_opener',return_value=opener), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code=a.main(self.args+list(extra))
        return code,output.getvalue(),opener

    def test_dry_run_without_key_makes_no_call(self):
        code,out,opener=self.run_main(['--dry-run'],env={})
        self.assertEqual(code,0)
        opener.open.assert_not_called()
        self.assertFalse(json.loads(out)['request_sent'])
        self.assertNotIn(self.brief.read_text(),out)

    def test_environment_overrides_explicit_file(self):
        p=self.root/'private.env'
        p.write_text('export KIMI_MODEL="file-model"\n# comment\nKIMI_API_KEY=unused\n')
        with patch.dict(os.environ,self.env,clear=True):
            self.assertEqual(a.load_config(p)['KIMI_MODEL'],'test-model')

    def test_success_writes_output(self):
        p=self.root/'draft.txt'
        code,out,opener=self.run_main(['--output-file',str(p)],{'choices':[{'message':{'content':'文案'}}]})
        self.assertEqual(code,0,out)
        self.assertEqual(p.read_text(),'文案\n')
        self.assertEqual(opener.open.call_count,1)

    def test_no_overwrite_or_api_call(self):
        p=self.root/'draft.txt'; p.write_text('existing')
        code,out,opener=self.run_main(['--output-file',str(p)])
        self.assertNotEqual(code,0)
        opener.open.assert_not_called()
        self.assertEqual(p.read_text(),'existing')

    def test_invalid_content_fails(self):
        for response in [[],{}, {'choices':[{'message':{'content':['not text']}}]}]:
            code,out,_=self.run_main(response=response)
            self.assertEqual(code,5,out)
            self.assertNotIn(self.env['KIMI_API_KEY'],out)

    def test_unsafe_endpoint_not_called(self):
        for base in ['http://example.com','https://user:password@example.com','https://example.com?key=secret']:
            env={**self.env,'KIMI_BASE_URL':base}
            code,out,opener=self.run_main(env=env)
            self.assertNotEqual(code,0)
            opener.open.assert_not_called()
            self.assertNotIn(base,out)

    def test_redirect_is_blocked(self):
        self.assertIsNone(a.NoRedirect().redirect_request(None,None,302,'',{},'https://other.test'))

if __name__=='__main__': unittest.main()
