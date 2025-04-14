import random

def generate_quiz(known_phrases):
    if len(known_phrases) < 3:
        return None  # 최소 3개 이상 있어야 퀴즈 가능

    correct = random.choice(known_phrases)
    correct_phrase = correct["phrase"]
    correct_meaning = correct["meaning"]

    # 정답 외 다른 보기들
    others = [item for item in known_phrases if item != correct]
    wrong_choices = random.sample(others, 2)
    options = [correct_meaning] + [item["meaning"] for item in wrong_choices]
    random.shuffle(options)

    return {
        "question": correct_phrase,
        "answer": correct_meaning,
        "choices": options
    }
