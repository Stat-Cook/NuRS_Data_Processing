"""
Tools for reporting on a single missing mining test.
"""
from collections import namedtuple

ClassifierResult = namedtuple("ClassifierResult", ("Variable", "Model", "Features", "Score"))
