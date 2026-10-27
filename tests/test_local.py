"""Contrôles des pages statiques, sans dépendance externe."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'pages').glob('*.html'))


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []
        self.ids = []
        self.headings = 0
        self.lang = None
        self.input_types = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.headings += 1
        if tag == 'input':
            self.input_types.append((attrs.get('type', 'text'), attrs.get('name', '')))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for name in ('href', 'src', 'action'):
            if attrs.get(name):
                self.references.append((tag, name, attrs[name]))


DOCUMENTS = {}
for path in HTML_FILES:
    parsed = Document()
    parsed.feed(path.read_text(encoding='utf-8'))
    DOCUMENTS[path.resolve()] = parsed


class StaticSiteTests(unittest.TestCase):
    def test_structure_and_no_sensitive_input(self):
        for path, document in DOCUMENTS.items():
            with self.subTest(page=path.relative_to(ROOT)):
                self.assertEqual(document.lang, 'fr')
                self.assertEqual(len(document.ids), len(set(document.ids)), 'IDs dupliqués')
                if path.name != 'assurances-professionnels-entreprises.html':
                    self.assertEqual(document.headings, 1, 'Une page doit avoir un seul titre h1')
                for typ, name in document.input_types:
                    self.assertNotEqual(typ.lower(), 'password')
                    self.assertNotIn(name.lower(), {'password', 'motdepasse', 'siret', 'email', 'telephone'})

    def test_all_page_references_are_local_and_resolve(self):
        for path, document in DOCUMENTS.items():
            for tag, attr, reference in document.references:
                with self.subTest(page=path.relative_to(ROOT), element=tag, reference=reference):
                    uri = urlsplit(reference)
                    self.assertNotIn(uri.scheme, ('http', 'https', 'ftp'), 'Dépendance réseau inattendue')
                    if uri.scheme:
                        self.assertEqual(uri.scheme, 'tel', 'Seuls les liens téléphoniques sont autorisés')
                        continue
                    target = (path.parent / unquote(uri.path)).resolve() if uri.path else path
                    if target.is_dir():
                        target = target / 'index.html'
                    self.assertTrue(target.is_file(), f'Ressource absente : {target}')
                    if uri.fragment and target.suffix == '.html':
                        target_doc = DOCUMENTS.get(target)
                        self.assertIsNotNone(target_doc, f'Page HTML non analysée : {target}')
                        self.assertIn(unquote(uri.fragment), target_doc.ids, f'Ancre introuvable : {uri.fragment}')

    def test_css_resources_are_local_and_exist(self):
        css = (ROOT / 'styles.css').read_text(encoding='utf-8')
        for value in re.findall(r'url\(([^)]+)\)', css):
            url = value.strip().strip('"\'')
            if url.startswith('data:'):
                continue
            with self.subTest(url=url):
                self.assertFalse(urlsplit(url).scheme, 'Ressource CSS distante')
                self.assertTrue((ROOT / unquote(urlsplit(url).path)).is_file(), 'Ressource CSS absente')

    def test_generated_pages_are_up_to_date(self):
        generated = [ROOT / name for name in ('agences.html', 'catalogue.html', 'contact.html', 'devis.html', 'espace-client.html')]
        generated += sorted((ROOT / 'pages').glob('*.html'))
        before = {path: path.read_bytes() for path in generated}
        subprocess.run([sys.executable, str(ROOT / 'scripts/generate_local_pages.py')], cwd=ROOT, check=True, capture_output=True)
        for path in generated:
            with self.subTest(page=path.relative_to(ROOT)):
                self.assertEqual(before[path], path.read_bytes(), 'Page générée non à jour')


if __name__ == '__main__':
    unittest.main()
