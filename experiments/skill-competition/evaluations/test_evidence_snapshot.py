import tempfile
import unittest
from pathlib import Path

from evidence_snapshot import snapshot, verify


class EvidenceTests(unittest.TestCase):
    def test_snapshot_survives_source_change_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, frozen = root / 'live.json', root / 'run' / 'frozen.json'
            source.write_bytes(b'original')
            digest = snapshot(source, frozen)
            source.write_bytes(b'changed')
            self.assertEqual(verify(root, {'files': {'run\\frozen.json': digest}}), [])
            with self.assertRaises(FileExistsError):
                snapshot(source, frozen)
            self.assertEqual(frozen.read_bytes(), b'original')

    def test_changed_and_missing_evidence_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'live'
            source.write_bytes(b'original')
            digest = snapshot(source, root / 'frozen')
            (root / 'frozen').write_bytes(b'tampered')
            failures = verify(root, {'files': {'frozen': digest, 'absent': digest}})
            self.assertEqual([f['reason'] for f in failures], ['HASH_CHANGED', 'MISSING'])

    def test_outside_root_and_empty_manifest_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(verify(folder, {'files': {'../outside': 'hash'}})[0]['reason'], 'OUTSIDE_ROOT')
            self.assertEqual(verify(folder, {'files': {}})[0]['reason'], 'EMPTY_MANIFEST')


if __name__ == '__main__':
    unittest.main()
