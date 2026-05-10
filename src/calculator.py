"""
基础计算器模块 - 提供加减乘除四则运算
企业级项目中，工具模块通常放在独立的包中供其他模块调用
"""


class Calculator:
    """基础计算器类，封装四则运算逻辑"""

    def add(self, a: float, b: float) -> float:
        """加法运算"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """乘法运算"""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """
        除法运算
        Raises:
            ValueError: 当除数为0时抛出异常
        """
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


# 模块级便捷函数（函数式调用风格）
def add(a: float, b: float) -> float:
    """加法快捷函数"""
    return Calculator().add(a, b)


def subtract(a: float, b: float) -> float:
    """减法快捷函数"""
    return Calculator().subtract(a, b)


def multiply(a: float, b: float) -> float:
    """乘法快捷函数"""
    return Calculator().multiply(a, b)


def divide(a: float, b: float) -> float:
    """除法快捷函数"""
    return Calculator().divide(a, b)
