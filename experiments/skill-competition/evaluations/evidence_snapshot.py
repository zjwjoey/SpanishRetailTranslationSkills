"""Private experiment evidence copies; no translation or semantic scoring."""
import hashlib
import json
from pathlib import Path


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def snapshot(source, destination):
    """Create exclusively: an existing frozen file must never be overwritten."""
    data = Path(source).read_bytes()
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as output:
        output.write(data)
    return hashlib.sha256(data).hexdigest()


def verify(root, manifest):
    """Verify an existing freeze's files, including Windows-style paths."""
    base = Path(root).resolve()
    failures = []
    for name, expected in manifest['files'].items():
        target = (base / name.replace('\\', '/')).resolve()
        if not target.is_relative_to(base):
            failures.append({'path': name, 'reason': 'OUTSIDE_ROOT'})
        elif not target.is_file():
            failures.append({'path': name, 'reason': 'MISSING'})
        elif sha256(target) != expected:
            failures.append({'path': name, 'reason': 'HASH_CHANGED'})
    if not manifest['files']:
        failures.append({'reason': 'EMPTY_MANIFEST'})
    return failures


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root')
    parser.add_argument('manifest')
    args = parser.parse_args()
    result = verify(args.root, json.loads(Path(args.manifest).read_text(encoding='utf-8')))
    print(json.dumps({'status': 'FAILED' if result else 'PASS', 'failures': result}, indent=2))
    raise SystemExit(bool(result))
