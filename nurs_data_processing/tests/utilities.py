from ..missing_results import MissingResults
from ..model_result import ClassifierResult

def missing_mining_checks(result, n):
    if not isinstance(result, MissingResults):
        raise TypeError(f"Result expected to be of type `MissingResult`.  "
                        f"Actually of  type '{type(result)}'")
    if not len(result) == n:
        raise AttributeError(f"Expected result to be of length {n}.  Actually of length {len(result)}")
    for i in result:
        if not isinstance(i, ClassifierResult):
            raise TypeError(f"Expected each item of result to be of type 'ClassifierResult'."
                            f"Found at least one of type {type(i)}")
