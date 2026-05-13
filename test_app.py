import unittest
from typing import List, Tuple

from app import levenshtein_distance

class TestLevenshteinDistance(unittest.TestCase):
    """Test suite targeting structural boundaries of the Levenshtein distance function."""

    def test_empty_inputs(self):
        """Verify behavior when one or both text string inputs are completely empty."""
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("", "abcdef"), 6)

    def test_identical_inputs(self):
        """Verify that comparing a string to itself returns zero structural operations."""
        self.assertEqual(levenshtein_distance("python", "python"), 0)
        self.assertEqual(levenshtein_distance(" ", " "), 0)
        self.assertEqual(levenshtein_distance("a", "a"), 0)

    def test_single_character_mutations(self):
        """Verify explicit atomic operations: insertions, deletions, and substitutions."""
        self.assertEqual(levenshtein_distance("cat", "bat"), 1)   # Substitution
        self.assertEqual(levenshtein_distance("cat", "cats"), 1)  # Insertion
        self.assertEqual(levenshtein_distance("cat", "ca"), 1)    # Deletion

    def test_case_sensitivity(self):
        """Ensure case differences are evaluated as explicit character substitutions."""
        self.assertEqual(levenshtein_distance("Python", "python"), 1)
        self.assertEqual(levenshtein_distance("ABC", "abc"), 3)

    def test_varying_lengths(self):
        """Verify calculations balance perfectly when swapping parameter ordering constraints."""
        word_a = "kitten"
        word_b = "sitting"
        # Test order symmetry checks
        self.assertEqual(levenshtein_distance(word_a, word_b), 3)
        self.assertEqual(levenshtein_distance(word_b, word_a), 3)

    def test_parameterized_scenarios(self):
        """Run batch validation across diverse, multi-character language structures."""
        test_cases: List[Tuple[str, str, int]] = [
            ("intention", "execution", 5),
            ("rosettacode", "raisethysword", 8),
            ("distance", "editing", 5),
            ("flaw", "lawn", 2),
            ("Saturday", "Sunday", 3)
        ]
        for s1, s2, expected in test_cases:
            with self.subTest(s1=s1, s2=s2, expected=expected):
                self.assertEqual(levenshtein_distance(s1, s2), expected)


if __name__ == "__main__":
    unittest.main()

