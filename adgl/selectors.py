import re
from .util import get_path

def _cmp(actual, spec):
    if not isinstance(spec, dict): return actual == spec
    for op, expected in spec.items():
        op = op.lower()
        if op in ('equals','eq') and actual != expected: return False
        if op in ('not_equals','neq') and actual == expected: return False
        if op == 'in' and actual not in expected: return False
        if op == 'not_in' and actual in expected: return False
        if op == 'exists' and ((actual is not None) != bool(expected)): return False
        if op == 'missing' and ((actual is None) != bool(expected)): return False
        if op == 'contains':
            if isinstance(actual,(list,tuple,set)):
                if expected not in actual: return False
            elif actual is None or str(expected) not in str(actual): return False
        if op == 'prefix' and (actual is None or not str(actual).startswith(str(expected))): return False
        if op == 'suffix' and (actual is None or not str(actual).endswith(str(expected))): return False
        if op == 'regex' and (actual is None or re.search(str(expected),str(actual)) is None): return False
        if op == 'between':
            lo, hi = expected
            if actual is None or not (lo <= actual <= hi): return False
        if op == 'before' and (actual is None or not (str(actual) < str(expected))): return False
        if op == 'after' and (actual is None or not (str(actual) > str(expected))): return False
        if op == 'overlaps':
            if not isinstance(actual,(list,tuple,set)) or not set(actual).intersection(expected): return False
        if op == 'within' and actual not in expected: return False
    return True

def matches(obj, selector, context=None):
    if not selector: return True
    if 'all' in selector: return all(matches(obj,s,context) for s in selector['all'])
    if 'any' in selector: return any(matches(obj,s,context) for s in selector['any'])
    if 'none' in selector: return not any(matches(obj,s,context) for s in selector['none'])
    if 'not' in selector: return not matches(obj,selector['not'],context)
    return all(_cmp(get_path(obj,path), expected) for path,expected in selector.items())

def filter_objects(objects, selector, context=None): return [o for o in objects if matches(o,selector,context)]
