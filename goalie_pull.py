import math
from functools import lru_cache


@lru_cache
def ep_np(
    score_diff: int,
    time: int,
    prob_of_no_score: float=0.987,
    prob_team_scores: float=0.0065,
    prob_team_concedes: float=0.0065,
) -> float:
    """
    Function calculates the expected point values of a team who doesn't pull
    their goalie at all no matter what

    Inputs:
    score_diff - The score differential as a positive or negative integer
    time  - seconds left in the game
    prob_of_no_score - probability of a neither team scoring in a ten second block
    prob_team_scores - probability of a team scoring in a ten second block
    prob_team_concedes - probability of a team conceding a goal in a ten second block

    Outputs:
    expected_points  - the expected point value of a team given the score_diff difference
                       and time left in the game
    """
    if time == 0:
        if score_diff < 0:
            if score_diff < -1:
                return 0
            elif score_diff == -1:
                return prob_team_scores * 1.5
        elif score_diff == 0:
            return (prob_of_no_score * 1.5) + (prob_team_scores * 2)
        else:
            if score_diff > 1:
                return (prob_of_no_score * 2) + (prob_team_scores * 2) + (prob_team_concedes * 2)
            elif score_diff == 1:
                return (prob_of_no_score * 2) + (prob_team_scores * 2) + (prob_team_concedes * 1.5)
    else:

        return (
            (prob_of_no_score * ep_np(score_diff, time - 10))
            + (prob_team_scores * ep_np(score_diff + 1, time - 10))
            + (prob_team_concedes * ep_np(score_diff - 1, time - 10))
        )


@lru_cache
def ep_po(
        score_diff: int,
        time: int,
        prob_of_no_score: float=0.9624,
        prob_team_scores: float=0.0118,
        prob_team_concedes: float=0.0258
        ) -> float:
    """
    Function calculates the expected point values of a team who could or could
    not pull their goalie depending on the situation

    Inputs:
    score_diff - The score differential as a positive or negative integer
    time  - seconds left in the game
    prob_of_no_score - probability of a neither team scoring in a ten second block
    prob_team_scores - probability of a team scoring in a ten second block
    prob_team_concedes - probability of a team conceding a goal in a ten second block

    Outputs:
    expected_points  - the expected point value of the team
    """
    if time == 0:
        if score_diff < 0:
            if score_diff < -1:
                return 0
            elif score_diff == -1:
                return prob_team_scores * 1.5
        elif score_diff == 0:
            return (prob_of_no_score * 1.5) + (prob_team_scores * 2)
        else:
            if score_diff > 1:
                return (prob_of_no_score * 2) + (prob_team_scores * 2) + (prob_team_concedes * 2)
            elif score_diff == 1:
                return (prob_of_no_score * 2) + (prob_team_scores * 2) + (prob_team_concedes * 1.5)
    else:
        return (
            (
                prob_of_no_score
                * max(
                    ep_po(score_diff, time - 10),
                    ep_np(score_diff, time - 10),
                )
            )
            + (
                prob_team_scores
                * max(
                    ep_po(score_diff + 1, time - 10),
                    ep_np(score_diff + 1, time - 10),
                )
            )
            + (
                prob_team_concedes
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
