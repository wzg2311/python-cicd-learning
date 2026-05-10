"""
程序入口 - main.py
企业级Python项目的标准入口文件，演示如何调用各业务模块
"""

import sys
import os

# 将项目根目录加入Python路径，确保模块可导入
# 兼容两种运行环境:
#   1) 正常Python运行: __file__指向main.py所在目录
#   2) PyInstaller打包: __file__指向临时解压目录(sys._MEIPASS)
if getattr(sys, 'frozen', False):
    # PyInstaller 打包后的可执行文件
    _base_dir = sys._MEIPASS
else:
    # 正常 Python 解释器运行
    _base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, _base_dir)

from src.calculator import Calculator
from src.tax_calculator import TaxCalculator
from src.config import config


def print_banner():
    """打印程序启动横幅"""
    banner = f"""
    ╔══════════════════════════════════════╗
    ║  {config.PROJECT_NAME:^34}  ║
    ║  版本: {config.VERSION:^28}  ║
    ║  环境: {config.ENV:^28}  ║
    ╚══════════════════════════════════════╝
    """
    print(banner)


def demo_basic_calculation():
    """演示基础计算功能"""
    print("\n📐 基础计算器演示:")
    print("-" * 40)

    calc = Calculator()
    test_cases = [
        ('加法', calc.add, 10, 5),
        ('减法', calc.subtract, 10, 3),
        ('乘法', calc.multiply, 7, 8),
        ('除法', calc.divide, 20, 4),
    ]

    for name, func, a, b in test_cases:
        result = func(a, b)
        print(f"  {name}: {a} 和 {b} → {result}")

    # 演示异常处理（除零错误）
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"\n  ⚠️ 除零测试（预期异常）: {e}")


def demo_tax_calculation():
    """演示税费计算功能"""
    print(f"\n💰 税费计算演示 (起征点: ¥{config.TAX_THRESHOLD}):")
    print("-" * 40)

    tax_calc = TaxCalculator()

    # 个税计算示例
    salaries = [8000, 15000, 30000, 50000, 100000]
    print("  个人所得税（月应纳税所得额）:")
    for salary in salaries:
        taxable = max(0, salary - config.TAX_THRESHOLD)
        result = tax_calc.calculate_personal_income_tax(taxable)
        print(f"    工资¥{salary:>7} → 税率{result['tax_rate']}, 应纳税¥{result['tax_amount']}")

    # 增值税示例
    print("\n  增值税计算（不含税价¥10000）:")
    for t in ['general', 'small']:
        vat = tax_calc.calculate_vat(10000, t)
        print(f"    {t}纳税人: 含税价¥{vat['amount_inclusive']}, 税额¥{vat['vat_amount']}")

    # 社保示例
    print("\n  社保公积金（工资基数¥20000, 一线城市）:")
    social = tax_calc.calculate_social_insurance(20000, city_tier=1)
    print(f"    缴费基数: ¥{social['salary_base']}")
    for item, detail in social['details'].items():
        print(f"      {item}: {detail['rate']} = ¥{detail['amount']}")
    print(f"    合计缴纳: ¥{social['total']}")


def main():
    """主函数 - 程序入口"""
    print_banner()

    env_info = config.get_env_info()
    print("\n📋 当前配置:")
    for key, value in env_info.items():
        print(f"  {key}: {value}")

    demo_basic_calculation()
    demo_tax_calculation()

    print("\n✅ 程序运行完成！")
    return 0


if __name__ == '__main__':
    sys.exit(main())
