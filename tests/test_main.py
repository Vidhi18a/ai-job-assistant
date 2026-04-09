from app.presentation import match_strength


def test_match_strength_labels_scores_for_ui():
    assert match_strength(0.55) == "Strong match"
    assert match_strength(0.25) == "Moderate match"
    assert match_strength(0.10) == "Low match"
