import time
from app.bot import answer, REFUSAL


def ask_twice(q1, q2):
    """Ask q1, then ask q2 while passing the conversation so far."""
    r1 = answer(q1)["answer"]
    history = f"User: {q1}\nBot: {r1}"
    time.sleep(3)
    r2 = answer(q2, history=history)["answer"]
    return r2.lower()


def test_followup_water_damage():
    r2 = ask_twice("How long is the warranty?", "Does it cover water damage?")
    assert any(w in r2 for w in ["not", "no ", "n't"])


def test_followup_five_ghz():
    r2 = ask_twice("How do I set up Wi-Fi?", "What about 5 GHz?")
    assert "2.4" in r2


def test_followup_refund_days():
    r2 = ask_twice("Can I return the fan?", "How long does the refund take?")
    assert "7" in r2


def test_pronoun_followup_needs_history():
    # "that" has no keywords, so the bot must use the earlier turn
    r2 = ask_twice("What is the refund policy?", "How long does that take?")
    assert "7" in r2 or "15" in r2


def test_gibberish_input_is_handled():
    time.sleep(3)
    result = answer("asdf qwerty zxcv")
    assert REFUSAL.lower() in result["answer"].lower()