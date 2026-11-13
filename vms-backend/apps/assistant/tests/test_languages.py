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


class ExampleAnswerTests(SimpleTestCase):
    def test_guide_shows_a_worked_tetun_answer_using_the_glossary(self):
        guide = language_guide("tet")
        self.assertIn("Example answer in Tetun", guide)
        self.assertIn("ema na’in 188 mak to’o", guide)
        self.assertIn("rejeita iha odamatan", guide)

    def test_guide_shows_a_worked_portuguese_answer(self):
        self.assertIn("Example answer in Portuguese", language_guide("pt"))

    def test_examples_never_mention_a_download_button(self):
        # Seen live: the model copied the example's "the button is below" into
        # answers that offered no file -- an invented button.
        from apps.assistant.languages import _EXAMPLE_PT, _EXAMPLE_TET

        self.assertNotIn("butaun", _EXAMPLE_TET.lower())
        self.assertNotIn("botão", _EXAMPLE_PT.lower())

    def test_guide_ties_the_button_sentence_to_offer_download(self):
        self.assertIn("only when you called offer_download", language_guide("en"))
