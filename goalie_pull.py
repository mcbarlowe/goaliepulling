import math
from functools import lru_cache


@lru_cache
def ep_np(score_diff, time):
    """
    Function calculates the expected point values of a team who doesn't pull
    their goalie at all no matter what

    Inputs:
    score_diff - The score differential as a positive or negative integer
    time  - seconds left in the game

    Outputs:
    expected_points  - the expected point value of a team given the score_diff difference
                       and time left in the game
    """
    if time == 0:
        if score_diff < 0:
            if score_diff < -1:
                return 0
            elif score_diff == -1:
                return 0.0065 * 1.5
        elif score_diff == 0:
            return (0.987 * 1.5) + (0.0065 * 2)
        else:
            if score_diff > 1:
                return (0.987 * 2) + (0.0065 * 2) + (0.0065 * 2)
            elif score_diff == 1:
                return (0.987 * 2) + (0.0065 * 2) + (0.0065 * 1.5)
    else:

        return (
            (0.987 * ep_np(score_diff, time - 10))
            + (0.0065 * ep_np(score_diff + 1, time - 10))
            + (0.0065 * ep_np(score_diff - 1, time - 10))
        )


@lru_cache
def ep_po(score_diff, time):
    """
    Function calculates the expected point values of a team who could or could
    not pull their goalie depending on the situation

    Inputs:
    score_diff - The score differential as a positive or negative integer
    time  - seconds left in the game

    Outputs:
    expected_points  - the expected point value of the team
    """
    if time == 0:
        if score_diff < 0:
            if score_diff < -1:
                return 0
            elif score_diff == -1:
                return 0.0118 * 1.5
        elif score_diff == 0:
            return (0.9624 * 1.5) + (0.0118 * 2)
        else:
            if score_diff > 1:
                return (0.9624 * 2) + (0.0118 * 2) + (0.0118 * 2)
            elif score_diff == 1:
                return (0.9624 * 2) + (0.0118 * 2) + (0.0258 * 1.5)
    else:
        return (
            (
                0.9624
                * max(
                    ep_po(score_diff, time - 10),
                    ep_np(score_diff, time - 10),
                )
            )
            + (
                0.0118
                * max(
                    ep_po(score_diff + 1, time - 10),
                    ep_np(score_diff + 1, time - 10),
                )
            )
            + (
                0.0258
                * max(
                    ep_po(score_diff - 1, time - 10),
                    ep_np(score_diff - 1, time - 10),
                )
            )
        )


if __name__ == "__main__":
    print(ep_np(-1, 10))
    print(ep_np(-2, 200))
    print(ep_po(-2, 300))
