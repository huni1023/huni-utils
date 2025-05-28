import numpy as np

def calculate_item_difficulty(
        max_score: int,
        response_ls: list
    ) -> float:
    """calculate classical item difficulty

    Parameters
    ----------
    max_score : int
        _description_
    response_ls : list
        _description_

    Returns
    -------
    list
        _description_
    """
    assert max_score > 0, "max_score should be greater than 0"
    if np.sum(np.isnan(response_ls)) > 0:
        raise ValueError("response_ls contains nan value")
    
    return np.mean(response_ls) / max_score


def calculate_item_discrimination(
        total_score_ls: list,
        score_ls: list
    ) -> float:
    r"""calculate classical item discrimination

    The discrimination in CTT means correlation btw total test score without item itself and item score
    """
    if np.sum(np.isnan(total_score_ls)) > 0 or np.sum(np.isnan(score_ls)) > 0:
        raise ValueError("total_score_ls or score_ls contains nan value")
    assert len(total_score_ls) == len(score_ls), "total_score_ls and score_ls should have same length"

    # substract score from total score
    total_subscore_ls = total_score_ls - score_ls

    # if unique value count of total_subscore_ls is 1, return np.nan
    # if this code is ignored, np will print warning
    if np.unique(total_subscore_ls).shape[0] == 1:
        return np.nan

    return np.corrcoef(score_ls, total_subscore_ls)[0, 1]
