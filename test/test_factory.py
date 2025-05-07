import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest




from promptlibz import Templates, TemplateType

def test_Functionality():
    prompt = Templates(TemplateType.JUDGETYPE)
    assert type(prompt.format(task = '任务')) == str


class Test_Performance():
    def __init__(self):
        pass

    def test_judgetype(self):
        # TODO
        prompt = Templates(TemplateType.JUDGETYPE)