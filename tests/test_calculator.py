"""
计算器模块单元测试
覆盖：正常场景、边界值、异常场景、数据类型验证
"""
import sys
import os
import pytest

# 确保可以导入src模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.calculator import Calculator, add, subtract, multiply, divide


@pytest.fixture
def calc():
    """创建计算器实例的fixture，每个测试函数都会获得一个全新的实例"""
    return Calculator()


# ==================== 加法测试 ====================
class TestAdd:
    """加法运算测试套件"""

    def test_positive_numbers(self, calc):
        """正数加法: 2 + 3 = 5"""
        assert calc.add(2, 3) == 5

    def test_negative_numbers(self, calc):
        """负数加法: -1 + (-3) = -4"""
        assert calc.add(-1, -3) == -4

    def test_mixed_signs(self, calc):
        """正负数混合: -5 + 10 = 5"""
        assert calc.add(-5, 10) == 5

    def test_zero(self, calc):
        """零值测试: 0 + 100 = 100"""
        assert calc.add(0, 100) == 100

    def test_floats(self, calc):
        """浮点数加法: 0.1 + 0.2 = 0.3（注意浮点精度）"""
        result = calc.add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-9  # 使用近似比较处理浮点精度

    def test_large_numbers(self, calc):
        """大数值测试"""
        assert calc.add(999999999, 1) == 1000000000

    def test_commutative(self, calc):
        """交换律验证: a+b == b+a"""
        a, b = 42, 17
        assert calc.add(a, b) == calc.add(b, a)


# ==================== 减法测试 ====================
class TestSubtract:
    """减法运算测试套件"""

    def test_positive_result(self, calc):
        """正常减法: 10 - 3 = 7"""
        assert calc.subtract(10, 3) == 7

    def test_negative_result(self, calc):
        """结果为负: 3 - 10 = -7"""
        assert calc.subtract(3, 10) == -7

    def test_same_number(self, calc):
        """相同数相减: 5 - 5 = 0"""
        assert calc.subtract(5, 5) == 0


# ==================== 乘法测试 ====================
class TestMultiply:
    """乘法运算测试套件"""

    def test_basic_multiply(self, calc):
        """基础乘法: 4 * 5 = 20"""
        assert calc.multiply(4, 5) == 20

    def test_by_zero(self, calc):
        """乘以零: 任何数 * 0 = 0"""
        assert calc.multiply(12345, 0) == 0

    def test_by_one(self, calc):
        """乘以一: 数 * 1 = 原数"""
        assert calc.multiply(99, 1) == 99

    def test_by_negative(self, calc):
        """负数乘法: 正 * 负 = 负"""
        assert calc.multiply(6, -3) == -18

    def test_two_negatives(self, calc):
        """两负数相乘: 负 * 负 = 正"""
        assert calc.multiply(-4, -7) == 28


# ==================== 除法测试 ====================
class TestDivide:
    """除法运算测试套件"""

    def test_basic_divide(self, calc):
        """基础除法: 20 / 4 = 5"""
        assert calc.divide(20, 4) == 5

    def test_fractional_result(self, calc):
        """小数结果: 7 / 2 = 3.5"""
        assert calc.divide(7, 2) == 3.5

    def test_divide_by_one(self, calc):
        """除以一: 数 / 1 = 原数"""
        assert calc.divide(42, 1) == 42

    def test_divide_by_itself(self, calc):
        """自身除以自身: n / n = 1（n≠0）"""
        assert calc.divide(17, 17) == 1

    def test_divide_by_zero_raises_error(self, calc):
        """除零应抛出ValueError异常（这是关键测试！）"""
        with pytest.raises(ValueError, match="除数不能为零"):
            calc.divide(10, 0)

    def test_divide_zero_by_nonzero(self, calc):
        """零做被除数: 0 / n = 0"""
        assert calc.divide(0, 5) == 0


# ==================== 模块级函数测试 ====================
class TestModuleFunctions:
    """测试模块级便捷函数"""

    def test_add_function(self):
        """add() 函数可用"""
        assert add(1, 2) == 3

    def test_subtract_function(self):
        """subtract() 函数可用"""
        assert subtract(10, 4) == 6

    def test_multiply_function(self):
        """multiply() 函数可用"""
        assert multiply(3, 7) == 21

    def test_divide_function(self):
        """divide() 函数可用"""
        assert divide(15, 3) == 5
