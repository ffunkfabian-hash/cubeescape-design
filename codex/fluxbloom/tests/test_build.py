"""Capture-only must preserve the provenance of existing rendered sheets."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build import capture_record, main


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output=Path(self.temp.name)
        self.sheet=self.output/'KA01.html'
        self.sheet.write_text('<html>previously rendered sheet</html>')
        self.record={'filename':'KA01.html','geometry_sha256':'old-hash',
                     'prompts':{'de':'existing prompt'},'skins':[{'id':'old-skin'}],
                     'orthographic_views':[{'scale':1.23}]}
        (self.output/'manifest.json').write_text(json.dumps({'records':[self.record]}))

    def test_preserves_all_existing_render_metadata(self):
        self.assertEqual(capture_record(self.output,self.sheet,'old-hash'),self.record)

    def test_rejects_new_geometry_without_relabeling_existing_art(self):
        before=(self.output/'manifest.json').read_bytes()
        with self.assertRaisesRegex(ValueError,'geometry changed'):
            capture_record(self.output,self.sheet,'new-hash')
        self.assertEqual((self.output/'manifest.json').read_bytes(),before)

    def test_requires_existing_sheet_and_manifest_record(self):
        self.sheet.unlink()
        with self.assertRaisesRegex(ValueError,'existing sheet'):
            capture_record(self.output,self.sheet,'old-hash')
        with self.assertRaisesRegex(ValueError,'manifest record'):
            capture_record(self.output,self.output/'KA02.html','old-hash')

    def test_capture_only_keeps_manifest_version_and_metadata_unchanged(self):
        manifest=self.output/'manifest.json'
        data=json.loads(manifest.read_text());data['version']='older-version'
        manifest.write_text(json.dumps(data));before=manifest.read_bytes()
        meta={'slug':'pistol','variant':'A'}
        with patch('collections_codex.load_collection',return_value=[(meta,[])]), \
             patch('build.validate_model',return_value={}), \
             patch('build.geometry_hash',return_value='old-hash'), \
             patch('build.screenshots',return_value=[]), \
             patch('build.contact_sheet'):
            self.assertEqual(main(['--collection','parallax','--capture-only','--output',str(self.output)]),0)
        self.assertEqual(manifest.read_bytes(),before)
        self.assertTrue((self.output/'capture-qa.json').is_file())
