from pathlib import Path

from autoguard_cf.demo import run

if __name__ == "__main__":
    print(run(Path("outputs/counterfactual.json")))
