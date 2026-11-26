"""Static integrity tests for the OPSFORGE Streamlit Build Lab.

Run from the repository root:
    python -m unittest discover -s build-lab/tests -v

These tests intentionally use only the Python standard library; they do not
claim to replace a live Streamlit smoke test or external-link monitoring.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
APP_FILE = APP_DIR / "app.py"
ASSET_DIR = APP_DIR / "assets"


def load_app_source() -> tuple[str, ast.Module]:
    source = APP_FILE.read_text(encoding="utf-8")
    return source, ast.parse(source, filename=str(APP_FILE))


def literal_assignment(tree: ast.Module, variable: str):
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == variable for target in node.targets):
                return ast.literal_eval(node.value)
    raise AssertionError(f"Could not find literal assignment for {variable}")


class BuildLabIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source, cls.tree = load_app_source()
        cls.projects = literal_assignment(cls.tree, "PROJECTS")
        cls.concepts = literal_assignment(cls.tree, "CONCEPTS")
        cls.research = literal_assignment(cls.tree, "RESEARCH")

    def test_app_is_valid_python(self):
        self.assertTrue(self.tree.body, "app.py should not be empty")

    def test_all_multipage_renderers_exist_and_are_registered(self):
        expected = {
            "render_portfolio",
            "render_concepts",
            "render_research",
            "render_evaluate",
            "render_linkedin_studio",
        }
        defined = {
            node.name for node in self.tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        self.assertTrue(expected.issubset(defined), f"Missing renderers: {expected - defined}")
        self.assertIn("st.navigation(PAGES)", self.source)
        self.assertIn("navigation.run()", self.source)
        self.assertNotIn("st.tabs(", self.source)

    def test_project_and_concept_artwork_exists(self):
        records = self.projects + self.concepts
        filenames = {record["image"] for record in records}
        missing = sorted(name for name in filenames if not (ASSET_DIR / name).is_file())
        self.assertFalse(missing, f"Missing SVG assets: {missing}")

    def test_concept_gallery_has_twelve_distinct_concepts_and_artworks(self):
        self.assertEqual(len(self.concepts), 12)
        self.assertEqual(len({item["name"] for item in self.concepts}), len(self.concepts))
        self.assertEqual(len({item["image"] for item in self.concepts}), len(self.concepts))

    def test_research_ids_are_unique_and_have_http_sources(self):
        ids = [item["id"] for item in self.research]
        self.assertEqual(len(ids), len(set(ids)), "Research IDs must be unique")
        for item in self.research:
            self.assertTrue(item["url"].startswith("https://"), item["title"])

    def test_every_project_research_mapping_resolves(self):
        valid_ids = {item["id"] for item in self.research}
        for project in self.projects:
            unknown = set(project.get("research_ids", [])) - valid_ids
            self.assertFalse(unknown, f'{project["name"]} has unknown research IDs: {unknown}')

    def test_linkedin_studio_uses_mapped_research_and_edited_punchline(self):
        node = next(
            n for n in self.tree.body
            if isinstance(n, ast.FunctionDef) and n.name == "render_linkedin_studio"
        )
        source = ast.get_source_segment(self.source, node) or ""
        self.assertIn('r["id"] in p.get("research_ids",[])', source)
        self.assertIn("{punchline}", source)
        self.assertIn("pub_draft_signature", source)
        self.assertIn('st.session_state["linkedin_draft"]', source)

    def test_artwork_loader_has_missing_file_fallback_and_cache(self):
        self.assertIn("@st.cache_data(show_spinner=False)", self.source)
        self.assertIn("except (FileNotFoundError, OSError, UnicodeDecodeError)", self.source)
        self.assertIn("artwork unavailable", self.source)

    def test_accessible_sidebar_styles_and_dark_theme_exist(self):
        self.assertIn('[data-testid="stSidebar"] * { color:#e8f1ff !important; }', self.source)
        theme_file = APP_DIR.parent / ".streamlit" / "config.toml"
        self.assertTrue(theme_file.is_file(), "Repository-root .streamlit/config.toml is required")
        theme = theme_file.read_text(encoding="utf-8")
        self.assertIn('base = "dark"', theme)
        self.assertIn('textColor = "#E8EEF9"', theme)

    def test_evaluation_csv_uses_csv_writer_and_concept_specific_filename(self):
        self.assertIn("writer=csv.writer(csv_buffer,quoting=csv.QUOTE_MINIMAL)", self.source)
        self.assertIn('file_name=f"opsforge-evaluation-{concept_slug}.csv"', self.source)


if __name__ == "__main__":
    unittest.main()
