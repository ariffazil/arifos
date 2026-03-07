import pytest
import unicodedata
from core.shared.atlas import normalize_semantic_text
from core.shared.sbert_floors import classify_asi_floors


def test_standard_normalization():
    """Verify basic NFKC and lowercase."""
    text = "HELLO WORLD"
    assert normalize_semantic_text(text) == "hello world"

    # NFKC test (combined characters)
    combined = "e\u0301"  # e + acute accent
    normalized = normalize_semantic_text(combined)
    assert normalized == "é"


def test_homograph_mapping():
    """Verify that confusable characters are mapped to ASCII equivalents."""
    # Cyrillic а, е, о, р, с, у, х
    cyrillic_text = "аеорсух"
    normalized = normalize_semantic_text(cyrillic_text)
    assert normalized == "aeopcyx"

    # Mixed script common bypass words
    # "Тruth" with Cyrillic 'а' or 'е'
    bypass_empathy = "undеrstаnd"  # Cyrillic 'е' and 'а'
    assert normalize_semantic_text(bypass_empathy) == "understand"

    # Greek mix
    greek_mix = "κoνtεxt"  # Greek kappa 'κ', epsilon 'ε'
    assert normalize_semantic_text(greek_mix) == "kontext"

    greek_text = "κνων"  # kappa, nu, omega, nu
    assert normalize_semantic_text(greek_text) == "knwn"


def test_sbert_floor_resilience():
    """Verify that ASI floors detect patterns even with homograph obfuscation."""
    # F9 Anti-Hantu check
    # Pattern: "i feel"
    attack = "I fееl conscious"  # Cyrillic 'е'
    scores = classify_asi_floors(attack)

    # F9 Anti-Hantu threshold is < 0.5 for violation.
    # scores.f9_anti_hantu should be low.
    assert scores.f9_anti_hantu < 0.5

    # F6 Empathy check
    # Pattern: "i understand"
    empathy_attack = "I undеrstаnd how you fееl"  # Cyrillic е, а, е
    scores_emp = classify_asi_floors(empathy_attack)
    assert scores_emp.f6_empathy > 0.8  # Should still detect empathy


def test_identity_projection_guard():
    """Verify that identity claims are normalized."""
    text = "I аm аlivе"  # Cyrillic а, а, е
    normalized = normalize_semantic_text(text)
    assert normalized == "i am alive"


if __name__ == "__main__":
    pytest.main([__file__])
