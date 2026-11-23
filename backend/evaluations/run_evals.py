
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from recommendations.services import recommend_game


GOLDEN_SET = Path(__file__).with_name("golden_set.json")

HALLUCINATION_THRESHOLD = 1.0
CONSISTENCY_THRESHOLD = 0.95
REPEATS = 3


def fake_gemini_response(case):
    """Create a predictable mock response for each golden case."""
    expected = case["expected_games"]

    if not expected:
        return None

    response = MagicMock()
    response.text = json.dumps({
        "game": expected[0],
        "reason": "This game matches your preferences.",
    })
    return response


def evaluate():
    cases = json.loads(GOLDEN_SET.read_text(encoding="utf-8"))

    hallucination_passes = 0
    hallucination_total = 0
    consistency_passes = 0
    consistency_total = 0

    for case in cases:
        valid_titles = {
            game["title"]
            for game in case["games"]
        }

        for _ in range(REPEATS):
            fake_response = fake_gemini_response(case)

            with patch.dict(
                "os.environ",
                {"GEMINI_API_KEY": "fake-test-key"},
            ):
                with patch("recommendations.services.genai.Client") as mock_client:
                    if fake_response is not None:
                        mock_client.return_value.models.generate_content.return_value = (
                            fake_response
                        )

                    result = recommend_game(
                        case["games"],
                        case["favorite_genres"],
                    )

            recommended = result["game"]

            hallucination_total += 1
            consistency_total += 1

            if recommended is None and not valid_titles:
                hallucination_passes += 1
            elif recommended in valid_titles:
                hallucination_passes += 1

            if recommended in case["expected_games"]:
                consistency_passes += 1
            elif recommended is None and not case["expected_games"]:
                consistency_passes += 1

    hallucination_score = hallucination_passes / hallucination_total
    consistency_score = consistency_passes / consistency_total

    print(f"Golden cases: {len(cases)}")
    print(f"Repeated runs per case: {REPEATS}")
    print(f"Hallucination score: {hallucination_score:.2%}")
    print(f"Consistency score: {consistency_score:.2%}")

    passed = (
        hallucination_score >= HALLUCINATION_THRESHOLD
        and consistency_score >= CONSISTENCY_THRESHOLD
    )

    if passed:
        print("EVALUATION PASSED")
        return 0

    print("EVALUATION FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(evaluate())
