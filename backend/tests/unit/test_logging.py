from app.core.logging import mask_pii


def test_mask_pii():
    sample_text = (
        "Contact john.doe@insurance.com or call 555-123-4567 with card 4111-2222-3333-4444."
    )
    masked = mask_pii(sample_text)
    assert "john.doe@insurance.com" not in masked
    assert "[EMAIL_MASKED]" in masked
    assert "555-123-4567" not in masked
    assert "[PHONE_MASKED]" in masked
    assert "4111-2222-3333-4444" not in masked
    assert "[CARD_MASKED]" in masked
