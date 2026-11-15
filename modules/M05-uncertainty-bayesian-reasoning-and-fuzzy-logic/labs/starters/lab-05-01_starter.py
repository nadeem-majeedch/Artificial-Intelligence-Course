"""LAB-05-01 starter — a Bayesian decision, then a fuzzy controller.

The Bayesian half is complete: two independent causes, one shared effect. The fuzzy
half is a skeleton with the membership functions given and the rule base left to you.

Run:  python lab-05-01_starter.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "code"))

from variable_elimination import Factor, variable_elimination  # noqa: E402


def network():
    """P(Rain), P(Sprinkler), P(Wet | Rain, Sprinkler) as factors."""
    rain = Factor(["Rain"], {(True,): 0.2, (False,): 0.8})
    sprinkler = Factor(["Sprinkler"], {(True,): 0.1, (False,): 0.9})
    wet = Factor(["Wet", "Rain", "Sprinkler"], {
        (True, True, True): 0.99, (True, True, False): 0.90,
        (True, False, True): 0.90, (True, False, False): 0.00,
        (False, True, True): 0.80, (False, True, False): 0.00,
        (False, False, True): 0.00, (False, False, False): 0.00,
    })
    return [rain, sprinkler, wet]


def main():
    factors = network()
    p_rain_given_wet, mass = variable_elimination(factors, "Rain", {"Wet": True})
    p_sprinkler_given_wet, _ = variable_elimination(factors, "Sprinkler", {"Wet": True})
    print(f"P(Wet) = {mass:.4f}")
    print(f"P(Rain | Wet)      = {p_rain_given_wet:.4f}")
    print(f"P(Sprinkler | Wet) = {p_sprinkler_given_wet:.4f}")
    print("explaining away: both rise, and their product over-counts the evidence\n")

    # ---------------------------------------------------------------- fuzzy half
    def cold(temperature):
        return max(0.0, min(1.0, (15 - temperature) / 10))       # 1 below 5 C, 0 above 15 C

    def hot(temperature):
        return max(0.0, min(1.0, (temperature - 20) / 10))       # 0 below 20 C, 1 above 30 C

    def fan_slow(temperature):
        # TODO: define slow/medium/fast memberships on the fan speed (0-100 %)
        raise NotImplementedError

    readings = [4, 12, 22, 28]
    print("temperature -> cold, hot memberships")
    for t in readings:
        print(f"  {t:>3} C: cold={cold(t):.2f} hot={hot(t):.2f}")

    # TODO: add three rules (cold -> slow, mild -> medium, hot -> fast), defuzzify by
    # centroid, and print the fan speed for each reading. Compare with a threshold
    # controller that switches at 18 C and state which one you would ship, and why.


if __name__ == "__main__":
    main()
