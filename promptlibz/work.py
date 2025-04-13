from llama_index.core import PromptTemplate
from quickuse.llms import get_llm

template = """
让我们一步步从用户的模糊需求中分析出明确且具体的需求步骤：

第一步：提取用户表述中的关键词和重点内容。
第二步：将关键词和重点内容转化成具体的步骤和需求。
第三步：复核步骤和需求确保其明确具体且无二义性。
第四步：将上述步骤和需求整理成明确的需求描述。

用户需求表述：
---
{user_statement}
---

问题：请将上述用户需求表述转化为明确的需求描述。
"""

def analyze(multi_line_input):
    llm = get_llm()
    analyze_template = PromptTemplate(template=template)
    response = llm.complete(analyze_template.format(user_statement=multi_line_input))
    return response.text



if __name__ == "__main__":
    import sys
    multi_line_input = sys.stdin.read()
    print(analyze(multi_line_input))

import pandas as pd
from addict import Dict
import random
import json
import re
from llama_index.llms.openai import OpenAI
import os

class GetInfo():
    def __init__(self,canvas_file:str):
        self.canvas_file = canvas_file
        self.dicts = self.load(canvas_file)
        self.nodes = pd.DataFrame(self.dicts['nodes'])
        self.edges = pd.DataFrame(self.dicts['edges'])
        
    def load(self,folder):
        with open(folder,'r') as f:
            text = f.read()
        return json.loads(text)
    
    def clean_data_custom(self):
        self.edges_ = self.edges[['id','fromNode','fromSide','toNode','toSide']]
        self.nodes_ = self.nodes[['color','id','text']]

        return {"nodes":self.nodes_.to_dict(),
               "edges":self.edges_.to_dict()}
    
    def update_df_by(self,df1,df2):
        df1_ = df1.set_index('id', inplace=False)
        df2_ = df2.set_index('id', inplace=False)
        df1_.update(df2_)
        df1_.reset_index(inplace=True)
        return df1_
    
    def up_data_custom(self,x):
        nodes = pd.DataFrame(x['nodes'])
        edges = pd.DataFrame(x['edges'])
        self.nodes_updated = self.update_df_by(self.nodes,nodes)
        self.edges_updated = self.update_df_by(self.edges,edges)
        
        return {"nodes":list(self.nodes_updated.T.to_dict().values()),
                "edges":list(self.edges_updated.T.to_dict().values())
               }

def extract_json_code(text):
    pattern = r'```json([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches

def clean_json(result):
    # 清洗 JSON 数据
    json_string = extract_json_code(result.text)[-1]
    cleaned_json = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', json_string)
    cleaned_json = cleaned_json.replace(' ','')
    return cleaned_json

def decodeJson(cleaned_json):
    try:
        parsed_dict = json.loads(cleaned_json, strict=False)
        print("JSON 解析成功！")
        # 打印解析后的字典
    except json.JSONDecodeError as e:
        print("JSON 解析失败:", e)
    return parsed_dict

templates = '''
please step by step:

基本介绍:
    这里有两幅图数据结构表示的工程图, 第一张是流程图,介绍了基本的工作流程, 第二张是施工图,具体描述了正在进行的工作和工作的状态
    
1 我希望你可以可以深入了解他们,并理解他们的含义.
2 根据施工图的颜色和描述等信息, 根据下列规则判断和操作
3 输出修改后的流程图



判断规则如下:
---
如果施工图中的nodes的颜色是4, 那么说明这个工作已经完成.
理解施工图中完成的工作和流程图中流程的对应关系, 将对应的流程图中的nodes 的颜色改为4
注意 输出的json格式不要有任何注释内容
---

流程图如下:
---
{flow}
---
施工图如下:
---
{work}
---

修改后的流程图:
'''
file_path = "/Users/zhaoxuefeng/本地文稿/百度空间/cloud/Obsidian/知识体系尝试/工作/事件看板"

llm = OpenAI(
    model="gpt-4o",
    api_key='sk-tQ17YaQSAvb6REf474A112Eb57064c5d9f6a9599F96a35A6',
    api_base='https://api.bianxieai.com/v1',
    temperature=0.1,
)

def main():
    flow_path = 'project-ChatWallet-beta.canvas'
    flow_path2= 'project-ChatWallet-beta2.canvas'
    work_path = 'project-ChatWallet-beta施工图.canvas'
    
    
    # flow_path = '测试11.canvas'
    # work_path = '测试11施工图.canvas'
    inf = GetInfo(os.path.join(file_path,flow_path))
    inf2 = GetInfo(os.path.join(file_path,work_path))

    flow = inf.clean_data_custom()
    work = inf2.clean_data_custom()
    print('start')
    print(templates.format(flow = flow, work = work),'<<<<<<<<<<')
    result = llm.complete(templates.format(flow = flow, work = work))
    print('output')
    print(result.text,'text')
    cleaned_json = clean_json(result)
    parsed_dict = decodeJson(cleaned_json)
    ens = inf.up_data_custom(parsed_dict)
    aac = json.dumps(ens)
    
    with open(os.path.join(file_path,flow_path2),'w') as f:
        f.write(aac)

if __name__ == "__main__":
    main()


from enum import Enum
from llama_index.core import PromptTemplate
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from quickuse.tools.retools import extract_python_code
import os
import re
import json
import time

from enum import Enum
class Side(Enum):
    right = "right"
    left = "right"
    top = "top"
    bottom = "bottom"

class Edge:
    __slots__ = ['fromNode', 'fromSide', 'id','label', 'styleAttributes', 'toNode', 'toSide']

    def __init__(self, 
                 from_node: str, 
                 from_side: Side, 
                 id: str, 
                 style_attributes: dict,
                 label:str,
                 to_node: str, 
                 to_side: Side):
        self.fromNode = from_node
        self.fromSide = from_side.value
        self.id = id
        self.styleAttributes = style_attributes
        self.label = label
        self.toNode = to_node
        self.toSide = to_side.value

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}

class Node:
    __slots__ = ['height', 'width', 'x', 'y', 'id', 'type','text','styleAttributes']

    def __init__(self, 
                 height: int = 60, 
                 width: int = 260, 
                 x: str = 440, 
                 y: dict = 80, 
                 id: str='1', 
                 type = "text",
                 text: str = "开始",
                 styleAttributes:dict={}):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.id = id
        self.type = type
        self.text = text
        self.styleAttributes = styleAttributes

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}


# 全局配置
api_key = os.environ.get('OPENAI_API_KEY')

# 初始化 LLM 和 Embedding 模型
llm = OpenAI(
    model="gpt-4o",
    api_key='sk-tQ17YaQSAvb6REf474A112Eb57064c5d9f6a9599F96a35A6',
    api_base='https://api.bianxieai.com/v1',
    temperature=0.1,
)
embed_model = OpenAIEmbedding(api_key=api_key)
Settings.embed_model = embed_model
Settings.llm = llm


prompt = """
你是一个python工程师, 你负责将mermaid格式转化为特定的函数调用,函数的方式会在下方给出
你需要给出相关代码
注意:
不需要再次定义函数,只需要给出转化部分

函数说明:
---
class Side(Enum):
    right = "right"
    left = "right"
    top = "top"
    bottom = "bottom"
    
class Edge:
    __slots__ = ['fromNode', 'fromSide', 'id','label', 'styleAttributes', 'toNode', 'toSide']

    def __init__(self, 
                 from_node: str, 
                 from_side: Side, 
                 id: str, 
                 style_attributes: dict,
                 label:str,
                 to_node: str, 
                 to_side: Side):
        self.fromNode = from_node
        self.fromSide = from_side.value
        self.id = id
        self.styleAttributes = style_attributes
        self.label = label
        self.toNode = to_node
        self.toSide = to_side.value

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}

class Node:
    __slots__ = ['height', 'width', 'x', 'y', 'id', 'type','text','styleAttributes']

    def __init__(self, 
                 height: int = 60, 
                 width: int = 260, 
                 x: str = 440, 
                 y: dict = 80, 
                 id: str='1', 
                 type = "text",
                 text: str = "开始",
                 styleAttributes:dict={}):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.id = id
        self.type = type
        self.text = text
        self.styleAttributes = styleAttributes

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}

---

for example:

mermaid

```mermaid
graph TD
    A[开始] --> B[准备采访问题]
    B --> C[进行采访]
    C --> D{采访者回答是否满意?}
    D -->|是| E[记录回答]
    D -->|否| F[调整问题]
```

转化为:

```python
edges = [Edge(from_node="218966d3990f15f6", from_side=Side.bottom, id="905bbe317b954c36",label="是", style_attributes={"pathfindingMethod": None}, to_node="2823d50c24e7534d", to_side=Side.top).to_dict(),
         Edge(from_node="218966d3990f15f6", from_side=Side.bottom, id="42b4f715b308c43e",label="否", style_attributes={"pathfindingMethod": None}, to_node="cfd410b6ee11ba81", to_side=Side.top).to_dict(),
         Edge(from_node="de67d252e584c626", from_side=Side.bottom, id="f4a1354b4f865171",label=None, style_attributes={"pathfindingMethod": "square"}, to_node="a385eec25062ed45", to_side=Side.top).to_dict(),
         Edge(from_node="a385eec25062ed45", from_side=Side.bottom, id="84b6c9a22fb05ad1",label=None, style_attributes={"pathfindingMethod": "square"}, to_node="0cc873f796f38c97", to_side=Side.top).to_dict(),
         Edge(from_node="0cc873f796f38c97", from_side=Side.bottom, id="b4ec373818d7df5c",label=None, style_attributes={"pathfindingMethod": "square"}, to_node="218966d3990f15f6", to_side=Side.top).to_dict(),
        ]
nodes = [Node(id ="218966d3990f15f6",text="采访者回答是否满意",x=-280,y=120).to_dict(),
         Node(id ="2823d50c24e7534d",text="记录回答",x=-500,y=320).to_dict(),
         Node(id ="cfd410b6ee11ba81",text="调整问题",x=-20,y=320).to_dict(),
         Node(id ="de67d252e584c626",text="开始",x=-280,y=-300).to_dict(),
         Node(id ="a385eec25062ed45",text="准备采访问题",x=-280,y=-160).to_dict(),
         Node(id ="0cc873f796f38c97",text="进行采访",x=-280,y=-20).to_dict(),
]
```


start:
---

mermaid
{mermaid}

转化为:
"""



def main(mermaid:str,path:str):
    """
    mermaid
    path
    """
    prompt_temp = PromptTemplate(prompt)
    resp = llm.complete(prompt_temp.format(mermaid=mermaid))
    python_code_str = extract_python_code(resp.text)
    codes = "\n".join(python_code_str) 

    info = {"nodes":None,
            "edges":None}

    exec(codes, globals(), info)
    with open(path,'w') as f:
        f.write(json.dumps(info))
    return 'success'

if __name__ == "__main__":

    import sys
    mermaid = sys.stdin.read()
    path = f"/Users/zhaoxuefeng/本地文稿/百度空间/cloud/Obsidian/知识体系尝试/工作/事件看板/Create_AI_{str(time.time())[:-8]}.canvas"
    result = main(mermaid,path)
    print(result)


temp = PromptTemplate("""
你是一个架构设计师, 我们之间会根据一个主题做讨论, 你会维护并不断更新一个mermaid框架图代码,这也是你的最终产出.

你将分两步完成以下任务:
步骤一 收集信息:
    1 为让我们的主题收集相关信息, 或者相关的可能的技术站
    2 列出相关技术产的性质优势不足

步骤二 根据手里的信息修改mermaid框架图

mermaid框架图
```

```

主题:{topic}
""")