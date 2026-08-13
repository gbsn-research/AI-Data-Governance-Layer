import pytest
from adgl.compiler import compile_policy, PolicyError


def test_unknown_operation_rejected():
    policy={
      'adgl':{'version':'0.3'}, 'policy':{'id':'bad','version':1},
      'case':{'id':'x'},
      'rules':[{'id':'r','do':[{'totally_made_up':{}}]}],
      'decision':{'default':'PERMITTED'}, 'audit':{'required':True}
    }
    with pytest.raises(PolicyError):
        compile_policy(policy)


def test_namespaced_extension_allowed():
    policy={
      'adgl':{'version':'0.3'}, 'policy':{'id':'ext','version':1},
      'case':{'id':'x'},
      'rules':[{'id':'r','do':[{'ext:example':{'value':1}}]}],
      'decision':{'default':'PERMITTED'}, 'audit':{'required':True}
    }
    compile_policy(policy)
