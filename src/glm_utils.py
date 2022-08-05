def glm_correct_pred(
    predictions,
    original_avg,
    new_avg,
    ):
    '''
    Correct the predictions of a glm after an over-sampling step.

    Formula is based on:
    www.data-mining-blog.com/tips-and-tutorials/overrepresentation-oversampling/

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

    '''
    
    return 1 / (1 + (1 / original_avg - 1) / (1 / new_avg - 1) * (1 / predictions - 1))
