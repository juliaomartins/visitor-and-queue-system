"""The language section of the system prompt."""

from django.test import SimpleTestCase

from apps.assistant.languages import GLOSSARY, SPECIALIST, language_guide


class LanguageGuideTests(SimpleTestCase):
    def test_specialist_languages_are_the_dashboards_three(self):
        self.assertEqual(SPECIALIST, ("en", "pt", "tet"))

    def test_guide_names_interface_language_and_falls_back(self):
        self.assertIn("interface language is Tetun", language_guide("tet"))
        self.assertIn("interface language is Portuguese", language_guide("pt"))
        self.assertIn("interface language is English", language_guide("xx"))

    def test_guide_carries_every_glossary_row(self):
        guide = language_guide("en")
        for en, pt, tet in GLOSSARY:
            self.assertIn(f"{en} | {pt} | {tet}", guide)

    def test_glossary_has_required_terms(self):
        english = {row[0] for row in GLOSSARY}
        self.assertLessEqual(
            {"visitor", "badge", "refused at the door", "entrance report", "arrived"},
            english,
        )

    def test_glossary_uses_the_dashboards_tetun_spellings(self):
        tetun = {row[0]: row[2] for row in GLOSSARY}
        self.assertEqual(tetun["visitor"], "vizitante")
        self.assertEqual(tetun["badge"], "kartaun")
        self.assertEqual(tetun["arrived"], "to’o")

    def test_guide_pins_european_portuguese_and_tetun_rules(self):
        guide = language_guide("en")
        for rule in ("European Portuguese", "registo", "Tetun Dili", "ema na’in", "dd/mm/yyyy"):
            self.assertIn(rule, guide)
