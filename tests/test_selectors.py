from adgl.selectors import matches

def test_boolean_and_path_selectors():
    obj={"status":"approved","jurisdiction":"EU","source":{"id":"internal"},"tags":["a","b"]}
    assert matches(obj,{"all":[{"status":"approved"},{"jurisdiction":{"in":["EU","US"]}}]})
    assert matches(obj,{"source.id":"internal"})
    assert matches(obj,{"tags":{"contains":"a"}})
    assert not matches(obj,{"status":"draft"})
