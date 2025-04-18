

from enum import Enum
from typing import List, Any

class EnumClassName(Enum):
    Option1 = 'Option1'
    Option2 = 'Option2'
    Option3 = 'Option3'
    # 添加更多选项

class FactoryClassName:
    def __new__(cls, enum_type: EnumClassName) -> Any:
        assert enum_type.value in [i.value for i in EnumClassName]
        instance = None

        if enum_type.value == 'Option1':
            # 配置 Option1 的实例
            # 例如：
            # instance = SomeClass(param1=value1, param2=value2)
            pass

        elif enum_type.value == 'Option2':
            # 配置 Option2 的实例
            # 例如：
            # instance = AnotherClass(param1=value1, param2=value2)
            pass

        elif enum_type.value == 'Option3':
            # 配置 Option3 的实例
            # 例如：
            # instance = YetAnotherClass(param1=value1, param2=value2)
            pass

        else:
            raise Exception('Unknown enum_type')

        return instance