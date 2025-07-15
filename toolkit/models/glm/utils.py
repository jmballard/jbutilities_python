def correct_pred(
    predictions,
    original_avg,
    new_avg,
):
    """
    Correct the predictions of a glm after an over-sampling step.

    Formula is based on:
    www.data-mining-blog.com/tips-and-tutorials/overrepresentation-oversampling/

    Note/Limitation: Works only if both averages are between 0 and 1.

    Parameters
    ----------
    predictions : Series
        GLM predictions
    original_avg : double
        The original average prediction
    new_avg : double
        The new average prediction

    Returns
    -------
    A series containing the corrected predictions

    """

    if (0 >= original_avg) or (original_avg >= 1):
        raise ValueError("original_avg must be between 0 and 1 (exclusive).")
    if (0 >= new_avg) or (new_avg >= 1):
        raise ValueError("new_avg must be between 0 and 1 (exclusive).")

    return 1 - 1 / (
        1 + (1 / original_avg - 1) / (1 / new_avg - 1) * (1 / predictions - 1)
    )
