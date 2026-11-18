"""Decode local manifest images and verify hashes; requires Pillow."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def verify(directory):
    directory = Path(directory).resolve()
    manifest = directory / 'download-manifest.json'
    rows = json.loads(manifest.read_text(encoding='utf-8-sig'))
    if isinstance(rows, dict):
        rows = [rows]
    if not isinstance(rows, list) or not rows:
        raise ValueError('Manifest must contain at least one image')
    hashes = set()
    verified = []
    for row in rows:
        filename = row.get('file', row.get('File'))
        path = (directory / filename).resolve()
        if not path.is_relative_to(directory):
            raise ValueError('Image path escapes batch directory')
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        expected = row.get('sha256', row.get('SHA256'))
        if expected and digest.lower() != expected.lower():
            raise ValueError('SHA256 mismatch: ' + filename)
        with Image.open(path) as image:
            image.load()
            width, height, fmt = image.width, image.height, image.format
        for lower, upper, actual in [('expected_width', 'Width', width),
                                     ('expected_height', 'Height', height),
                                     ('expected_bytes', 'Bytes', len(data))]:
            value = row.get(lower, row.get(upper))
            if value is not None and int(value) != actual:
                raise ValueError('Metadata mismatch for ' + lower + ': ' + filename)
        algorithm = row.get('source_checksum_algorithm')
        checksum = row.get('source_checksum')
        if algorithm and checksum:
            if algorithm not in ('md5', 'sha256'):
                raise ValueError('Unsupported source checksum algorithm')
            if hashlib.new(algorithm, data).hexdigest().lower() != checksum.lower():
                raise ValueError('Source checksum mismatch: ' + filename)
        verified.append({'file': filename, 'width': width, 'height': height,
                         'bytes': len(data), 'format': fmt, 'sha256': digest,
                         'duplicate_content': digest in hashes})
        hashes.add(digest)
    return {'images': len(rows), 'unique_images': len(hashes),
            'all_decoded': True, 'files': verified}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.directory), ensure_ascii=False, indent=2))
