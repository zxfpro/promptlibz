from llama_index.core import PromptTemplate
from llama_index.core.prompts import RichPromptTemplate

class JudgeType(PromptTemplate):
    def __init__(self):
        super().__init__(template = """
我需要你将任务名归类为下列五类中的一类,我会提供输出格式案例.

# 枚举类型:
    代码与练习: 需要进行编码或不断重复的练习任务
    实验与学习: 需要探索未知学习新知的任务
    整理与优化: 需要做一些常规任务或优化现有程序
    设计: 设计一个系统任务或者规划内容
    开会与对齐: 需要与别人进行对齐信息或者自己整理思路

# 历史归类:
{history}

# 输出格式
```type
设计
```
---

任务: {task}
""")

class GenerateSchedule(PromptTemplate):
    def __init__(self):
        super().__init__(template = """
你是一个日程管理者, 擅长做日程安排并按照标准格式输出.

有以下几点需要注意:
    1 **不需要输出多余内容 严格按照输出格式**.
    2 将日常规划做到未来时间, 而不是已经过去的时间, 现在的时间为: {current_utc_time}
    3 日常规划要避开用户习惯占用的时间

用户习惯:
---
{habit}
---

输出格式:
我会输入一段文字,里面包含了我今天需要做的任务的标题,以及任务预估的消耗时间(例如2P P代表一个番茄钟,也就是30分钟 2P就是60分钟)
任务可以拆开, 只需要保证总时间是对的.
我希望可以获得合理的时间安排并按照 "开始时间 结束时间 任务标题" 的格式输出,其中 "$" 是分隔符,标签以 # 开头应该去掉.


例子输入:
---
- [ ] 2P 研究一下算法知识吧
- [ ] 2P 数据结构 #长期
- [ ] 4P 时间复杂度算法 #长期
- [ ] 4P 做一些整理和知识层面上 的游走

例子输出:
2月11日8:00$2月11日9:00$研究一下算法知识吧
2月11日9:00$2月11日10:00$数据结构
2月11日13:00$2月11日15:00$时间复杂度算法
2月11日17:00$2月11日19:00$做一些整理和知识层面上 的游走

---
{text}
""")

class ExtraText(PromptTemplate):
    def __init__(self):
        super().__init__(template = """
我希望你可以对一个内容进行汇总和总结, 我会给你一段网页的内容，你来用一些简短的文字告诉我这篇内容的主要信息, 以及列出其中相关的重点和链接

网页内容:
---
{text}
---
{vvvc}
输出信息:
""")


class Mermaid(PromptTemplate):
    def __init__(self):
        super().__init__(template = """
我们聊天的回答需要使用 Mermaid 语法, 
只允许使用最简单的mermaid 语法
首先定义结点, 再绘制连线, 不要使用修饰信息
节点内容为执行步骤或任务, 要求明确且可实行 (使用动宾结构)   所有中文都要用引号

{}
""")
        best_model = "gemini-2.5-flash-preview-04-17-thinking"


class prompts(PromptTemplate):
    def __init__(self):
        super().__init__(template = """

""")




class Images(RichPromptTemplate):
    
    def __init__(self):
        super().__init__(template_str = """
Describe the following image:
{{ image_path | image}}
工作
""")
