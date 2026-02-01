import sys
import os

# Add local directory to sys.path
sys.path.append(os.getcwd())

try:
    from codebase.system.apex_prime import APEXPrime, Metrics, Verdict
    from codebase.floors import FloorScores, extract_dials
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)


def test_genius_calculation():
    print("Testing Genius Calculation...")

    # Create sample metrics
    metrics = Metrics(
        truth=0.99,
        delta_s=-0.2,
        peace_squared=1.1,
        kappa_r=0.95,
        omega_0=0.04,
        amanah=True,
        tri_witness=0.97,
        rasa=True,
        anti_hantu=True,
        psi=0.99,
    )

    prime = APEXPrime()

    try:
        verdict = prime.judge(metrics, lane="SOFT", query="test", response="test")

        print(f"Verdict: {verdict.verdict}")
        print(f"Genius Stats: {verdict.genius_stats}")

        if verdict.genius_stats["derivation"] != "eigendecomposition":
            print("FAIL: Derivation mismatch")
            sys.exit(1)

        print("SUCCESS")
    except Exception as e:
        print(f"Runtime Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_genius_calculation()
