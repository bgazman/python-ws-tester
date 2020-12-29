import difflib
import os

def diff(expected, actual):
    """
    Helper function. Returns a string containing the unified diff of two multiline strings.
    """
    expected =  os.linesep.join([s for s in expected.splitlines() if s])
    actual=  os.linesep.join([s for s in actual.splitlines() if s])
    expected = expected.splitlines(1)
    actual  = actual.splitlines(1)
    diff=difflib.unified_diff(expected, actual)

    return ''.join(diff)

# def diff2(expected, actual):
#     """
#     Helper function. Returns a string containing the unified diff of two multiline strings.
#     """
#     expected = expected.splitlines(1)
#     actual = actual.splitlines(1)
#     differ = difflib.Differ()
#     diff = differ.compare(expected,actual)
#
#     return ''.join(diff)