


from .utils import get_unittest
import os
from factory.prompt import TemplateFactory,TemplateType
from .utils import read_py, write_py,extract_python_code,trans_, get_df_info
from llama_index.core import PromptTemplate
from llama_index.core import Settings

import pandas as pd
import io




def made_code(prompt,code_path):


    qa_template = TemplateFactory(TemplateType.SIMPLEPY)

    qa_template2 = TemplateFactory(TemplateType.SIMPLEPY2)


    infos = read_py(code_path)
    py_name,py_content,path,duty,location,interaction = trans_(infos)
    template_ = qa_template.format(py_name=py_name,py_content = py_content,prompt = prompt,
                                              duty=duty,location=location,interaction=interaction)
    print(template_)
    
    response = Settings.llm.complete(template_)
    python_code = extract_python_code(response.text)

    response2 = Settings.llm.complete(qa_template2.format(code1=py_content,code2=python_code))
    python_code2 = extract_python_code(response2.text)
    write_py(path,'\n'.join([duty,location,interaction,'']) + '# ***************'.join(python_code2))

def made_unittest(code_path,test_path):
    qa_template = TemplateFactory(TemplateType.SIMPLEPY)

    infos = read_py(code_path)
    prompt_u = f'''
    ai_build.py 文件发生了更新, 更新内容如下, 我希望你将test代码做对应更新
    {infos['content']}
    '''
    infos = read_py(test_path)
    py_name,py_content,path,duty,location,interaction = trans_(infos)
    template_ = qa_template.format(py_name=py_name,py_content = py_content,prompt = prompt_u,
                                              duty=duty,location=location,interaction=interaction)
    print(template_)
    response = Settings.llm.complete(template_)
    python_code = extract_python_code(response.text)
    write_py(path,'\n'.join([duty,location,interaction,'']) + '# ***************'.join(python_code))

