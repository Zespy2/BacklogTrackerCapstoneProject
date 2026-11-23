"""Sprint 3 recommendation evaluation.

From backend/:
    python evaluations/run_evals.py
    python evaluations/run_evals.py --mode live

Mock mode validates application behavior without sending network requests.
Live mode measures actual provider behavior and requires GEMINI_API_KEY.
"""

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from recommendations.services import recommend_game

GOLDEN_SET = Path(__file__).with_name("golden_set.json")
RESULTS_DIR = Path(__file__).with_name("results")
HALLUCINATION_THRESHOLD = 1.0
CONSISTENCY_THRESHOLD = 0.95
ACCURACY_THRESHOLD = 0.90
REPEATS = 3


def canonical_title(value):
    return value.strip().casefold() if isinstance(value, str) else None


def run_one(case, mode):
    """Call the service with either a controlled SDK mock or the real provider."""
    if mode == "live":
        return recommend_game(case["games"], case.get("favorite_genres", []))

    # Mock response is deterministic by design: this mode checks the SERVICE,
    # not the intelligence or quality of the provider's recommendations.
    accepted = case["expected_games"]
    response = MagicMock()
    response.text = json.dumps({
        "game": accepted[0] if accepted else "",
        "reason": "Matches the requested backlog preferences.",
    })
    with patch.dict(os.environ, {"GEMINI_API_KEY": "mock-key"}):
        with patch("recommendations.services.genai.Client") as mock_client:
            mock_client.return_value.models.generate_content.return_value = response
            result = recommend_game(case["games"], case.get("favorite_genres", []))
            # Nonempty cases must exercise the mocked SDK, not just the fallback.
            if case["games"]:
                mock_client.assert_called_once()
    return result


def evaluate_cases(cases, mode, repeats=REPEATS):
    if len(cases) < 15:
        raise ValueError("At least 15 golden cases are required")
    if len({str(c["id"]) for c in cases}) != len(cases):
        raise ValueError("Golden case IDs must be unique")

    results = []
    hallucination_passes = 0
    hallucination_checks = 0
    accuracy_passes = 0
    accuracy_checks = 0
    consistent_cases = 0
    fallback_count = 0

    for case in cases:
        valid_titles = {
            canonical_title(game.get("title"))
            for game in case["games"]
            if isinstance(game, dict) and canonical_title(game.get("title"))
        }
        expected_titles = {canonical_title(t) for t in case["expected_games"]}
        observed = []
        per_run = []

        for _ in range(repeats):
            result = run_one(case, mode)
            title = canonical_title(result.get("game"))
            source = result.get("source", "unknown")
            fallback_count += int(source == "fallback")
            observed.append(title)

            # No made-up game titles, including when the backlog is empty.
            safe = (title in valid_titles) if valid_titles else (title is None)
            # A failed live-model call must not silently earn an accuracy pass
            # merely because the deterministic fallback selected a golden title.
            accurate = (title in expected_titles) if expected_titles else (title is None)
            if mode == "live" and source == "fallback" and valid_titles:
                accurate = False

            hallucination_checks += 1
            accuracy_checks += 1
            hallucination_passes += int(safe)
            accuracy_passes += int(accurate)
            per_run.append({
                "game": result.get("game"),
                "source": source,
                "hallucination_pass": safe,
                "expected_output_pass": accurate,
            })

        # Consistency is agreement across actual observed outputs, not whether
        # every output matches the expected title.
        consistent = len(set(observed)) == 1
        consistent_cases += int(consistent)
        results.append({
            "id": case["id"],
            "expected_games": case["expected_games"],
            "consistent": consistent,
            "observed": per_run,
        })

    scores = {
        "hallucination": hallucination_passes / hallucination_checks,
        "consistency": consistent_cases / len(cases),
        "expected_output_accuracy": accuracy_passes / accuracy_checks,
    }
    thresholds = {
        "hallucination": HALLUCINATION_THRESHOLD,
        "consistency": CONSISTENCY_THRESHOLD,
        "expected_output_accuracy": ACCURACY_THRESHOLD,
    }
    passed = all(scores[name] >= target for name, target in thresholds.items())
    return {
        "mode": mode,
        "golden_cases": len(cases),
        "repeats_per_case": repeats,
        "scores": scores,
        "thresholds": thresholds,
        "fallback_runs": fallback_count,
        "passed": passed,
        "cases": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("mock", "live"), default="mock")
    args = parser.parse_args()

    if args.mode == "live" and not os.getenv("GEMINI_API_KEY"):
        print("ERROR: Set GEMINI_API_KEY before running the live evaluation.", file=sys.stderr)
        return 2

    try:
        cases = json.loads(GOLDEN_SET.read_text(encoding="utf-8"))
        report = evaluate_cases(cases, args.mode)
    except (OSError, ValueError, KeyError, TypeError, AssertionError) as exc:
        print(f"EVALUATION ERROR: {exc}", file=sys.stderr)
        return 2

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = RESULTS_DIR / f"{args.mode}_latest.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Mode: {args.mode.upper()}")
    print(f"Golden cases: {report['golden_cases']}")
    print(f"Runs per case: {report['repeats_per_case']}")
    for metric, score in report["scores"].items():
        print(f"{metric}: {score:.1%} (threshold: {report['thresholds'][metric]:.1%})")
    print(f"Fallback runs: {report['fallback_runs']}")
    print(f"Results saved: {output}")
    print("EVALUATION PASSED" if report["passed"] else "EVALUATION FAILED")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
