""" prompt lib"""
from enum import Enum
from .prompts import Prompt,RichPrompt
from .prompts import Images
from .prompts import JudgeType,GenerateSchedule,Notes,ExtraText,Mermaid,GitHelp,Estimate_duration

from .prompts import ChatBox,MetaBox, MeetBox,memoryBox,DedaoExtract,MerMaidChat
class TemplateType(Enum):
    """ template type"""
    JUDGETYPE = 'JudgeType'
    GENERATE_SCHEDULE = 'GenerateSchedule'
    NOTES = 'Notes'
    EXTRATEXT = "ExtraText"
    GITHELP = "GitHelp"
    MERMAID = "Mermaid"
    ESTIMATE_DURATION = "Estimate_duration"
    RICH_IMAGES = "RichImages"
    ChatBox = "ChatBox"
    MetaBox = "MetaBox"
    MeetBox = "MeetBox"
    memoryBox = "memoryBox"
    DedaoExtract = "DedaoExtract"
    Mermaid2canvas = "MerMaidChat"

class Templates:
    """Template Factory"""
    def __new__(cls, template_type: TemplateType) -> Prompt|RichPrompt:
        assert template_type.value in [item.value for item in TemplateType]

        if template_type.value == 'JudgeType':
            return JudgeType()

        elif template_type.value == 'GenerateSchedule':
            # 定义提示模板字符串
            return GenerateSchedule()
        elif template_type.value == 'Notes':
            # 定义提示模板字符串
            return Notes()
        elif template_type.value == 'ExtraText':
            # 定义提示模板字符串
            return ExtraText()
        elif template_type.value == 'GitHelp':
            # 定义提示模板字符串
            return GitHelp()
        elif template_type.value == 'Mermaid':
            # 定义提示模板字符串
            return Mermaid()
        elif template_type.value == 'RichImages':
            # 定义提示模板字符串
            return Images()
        elif template_type.value == 'Estimate_duration':
            # 定义提示模板字符串
            return Estimate_duration()
        elif template_type.value == 'ChatBox':
            # 定义提示模板字符串
            return ChatBox()
        elif template_type.value == 'MetaBox':
            # 定义提示模板字符串
            return MetaBox()
        elif template_type.value == 'MeetBox':
            # 定义提示模板字符串
            return MeetBox()
        elif template_type.value == 'memoryBox':
            # 定义提示模板字符串
            return memoryBox()
        elif template_type.value == 'DedaoExtract':
            # 定义提示模板字符串
            return DedaoExtract()
        elif template_type.value == 'Mermaid2canvas':
            # 定义提示模板字符串
            return MerMaidChat()
        else:
            # 定义提示模板字符串
            return None
