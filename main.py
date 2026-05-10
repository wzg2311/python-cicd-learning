"""
程序入口 - 交互式命令行工具
企业级Python项目的标准入口文件，提供完整的用户交互体验

功能模块:
  1. 基础计算器 - 四则运算（加减乘除）
  2. 个税计算 - 输入工资自动算个税
  3. 增值税计算 - 输入金额算含税价/税额
  4. 社保公积金 - 输入工资算社保明细

使用方式:
  - 正常运行: python main.py
  - 打包后运行: ./python-cicd-learning（无需Python环境）
"""

import sys
import os

# 将项目根目录加入Python路径，确保模块可导入
# 兼容两种运行环境:
#   1) 正常Python运行: __file__指向main.py所在目录
#   2) PyInstaller打包: __file__指向临时解压目录(sys._MEIPASS)
if getattr(sys, 'frozen', False):
    _base_dir = sys._MEIPASS
else:
    _base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, _base_dir)

from src.calculator import Calculator
from src.tax_calculator import TaxCalculator
from src.config import config


# ==================== 工具函数 ====================

def print_banner():
    """打印程序启动横幅"""
    print()
    print("  " + "=" * 46)
    print(f"  |  {config.PROJECT_NAME:^40}  |")
    print(f"  |  版本 {config.VERSION:^36}  |")
    print("  " + "-" * 46)
    print(f"  |  税费起征点: ¥{config.TAX_THRESHOLD:>10}  |  精度: {config.DECIMAL_PLACES} 位小数  |")
    print("  " + "=" * 46)


def print_separator(char="-", width=46):
    """打印分隔线"""
    print(char * width)


def safe_float_input(prompt: str) -> float:
    """
    安全的浮点数输入，带错误重试机制
    
    Args:
        prompt: 提示文字
        
    Returns:
        用户输入的浮点数
    """
    while True:
        try:
            value = input(prompt).strip()
            return float(value)
        except ValueError:
            print("  [!] 请输入有效的数字！")


def wait_for_enter(prompt: str = "\n  按回车键继续..."):
    """等待用户按回车键"""
    input(prompt)


def clear_screen():
    """清屏（跨平台兼容）"""
    os.system('cls' if os.name == 'nt' else 'clear')


# ==================== 功能模块 1: 计算器 ====================

def run_calculator():
    """交互式基础计算器"""
    calc = Calculator()

    while True:
        clear_screen()
        print()
        print("  " + "=" * 46)
        print("  |           基 础 计 算 器                      |")
        print("  " + "=" * 46)
        print()
        print("    [1] 加法      a + b")
        print("    [2] 减法      a - b")
        print("    [3] 乘法      a x b")
        print("    [4] 除法      a / b")
        print()
        print("    [0] 返回主菜单")
        print()
        print("-" * 46)

        choice = input("  请选择操作 (0-4): ").strip()

        if choice == '0':
            break
        elif choice in ('1', '2', '3', '4'):
            print()
            a = safe_float_input("  请输入第一个数字: ")
            b = safe_float_input("  请输入第二个数字: ")

            ops = {
                '1': ('+', lambda x, y: calc.add(x, y)),
                '2': ('-', lambda x, y: calc.subtract(x, y)),
                '3': ('x', lambda x, y: calc.multiply(x, y)),
                '4': ('/', lambda x, y: calc.divide(x, y))
            }
            symbol, func = ops[choice]

            try:
                result = func(a, b)
                print()
                print("  " + "-" * 46)
                print(f"  计算:  {a}  {symbol}  {b}")
                print(f"  结果:  = {result:.{config.DECIMAL_PLACES}f}")
                print("  " + "-" * 46)
            except ValueError as e:
                print(f"\n  [!] 错误: {e}")

            wait_for_enter()
        else:
            print("\n  [!] 无效选项，请重新选择！")
            import time; time.sleep(0.8)


# ==================== 功能模块 2: 个税计算 ====================

def run_personal_income_tax():
    """交互式个人所得税计算器"""
    tax_calc = TaxCalculator()

    while True:
        clear_screen()
        print()
        print("  " + "=" * 46)
        print("  |         个 人 所 得 税 计 算 器               |")
        print("  " + "=" * 46)
        print()
        print(f"  起征点: 每月¥{config.TAX_THRESHOLD} (免税)")
        print("  说明: 输入税前月薪，自动扣除起征点后计税")
        print()
        print("    [0] 返回主菜单")
        print()
        print("-" * 46)

        choice = input("  输入月薪金额(元)，或按 0 返回: ").strip().lower()

        if choice == '0':
            break

        try:
            salary = float(choice)
            if salary <= 0:
                print("\n  [!] 工资必须为正数！")
                wait_for_enter()
                continue

            # 计算应纳税所得额
            taxable = max(0, salary - config.TAX_THRESHOLD)
            result = tax_calc.calculate_personal_income_tax(taxable)

            clear_screen()
            print()
            print("  " + "=" * 46)
            print("  |         个 税 计 算 结 果                     |")
            print("  " + "=" * 46)
            print()
            print(f"  税前月薪:       ¥{salary:>12,.2f}")
            print(f"  起征点(免税):   ¥{config.TAX_THRESHOLD:>12,.2f}")
            print(f"  应纳税所得额:   ¥{taxable:>12,.2f}")

            if taxable > 0:
                print()
                print(f"  适用税率:       {result['tax_rate']}")
                print(f"  速算扣除数:     ¥{result['quick_deduction']:>12,.2f}")
                print()
                print("  " + "-" * 46)
                print(f"  *** 应缴个税:   ¥{result['tax_amount']:>12,.2f} ***")
                print(f"  *** 税后到手:   ¥{salary - result['tax_amount']:>12,.2f} ***")
                print("  " + "-" * 46)
            else:
                print()
                print("  >>> 未达到起征点，无需缴纳个税 <<<")

        except ValueError:
            print("\n  [!] 请输入有效数字！")

        wait_for_enter()


# ==================== 功能模块 3: 增值税计算 ====================

def run_vat_calculator():
    """交互式增值税计算器"""
    tax_calc = TaxCalculator()

    while True:
        clear_screen()
        print()
        print("  " + "=" * 46)
        print("  |         增 值 税 计 算 器                     |")
        print("  " + "=" * 46)
        print()
        print("    [1] 一般纳税人 (13%)")
        print("    [2] 小规模纳税人 (3%)")
        print()
        print("    [0] 返回主菜单")
        print()
        print("-" * 46)

        choice = input("  选择纳税人类型 (0-2): ").strip()

        if choice == '0':
            break
        elif choice in ('1', '2'):
            type_map = {'1': ('一般纳税人', 'general'), '2': ('小规模纳税人', 'small')}
            label, t_type = type_map[choice]
            print()
            amount = safe_float_input(f"  [{label}] 请输入不含税金额: ")
            if amount < 0:
                print("\n  [!] 金额不能为负数！")
                wait_for_enter()
                continue

            vat = tax_calc.calculate_vat(amount, t_type)

            clear_screen()
            print()
            print("  " + "=" * 46)
            print("  |         增 值 税 计 算 结 果                 |")
            print("  " + "=" * 46)
            print()
            print(f"  纳税人类型:     {label}")
            print(f"  不含税金额:     ¥{vat['amount_exclusive']:>12,.2f}")
            print(f"  增值税率:       {vat['vat_rate']}")
            print(f"  增值税额:       ¥{vat['vat_amount']:>12,.2f}")
            print()
            print("  " + "-" * 46)
            print(f"  含税价合计:     ¥{vat['amount_inclusive']:>12,.2f}")
            print("  " + "-" * 46)

            wait_for_enter()
        else:
            print("\n  [!] 无效选项！")
            import time; time.sleep(0.8)


# ==================== 功能模块 4: 社保公积金 ====================

def run_social_insurance():
    """交互式社保公积金计算器"""
    tax_calc = TaxCalculator()

    city_names = {
        1: "一线城市 (北上广深)",
        2: "二线城市 (杭州、成都、武汉等)",
        3: "三线及其他城市"
    }

    while True:
        clear_screen()
        print()
        print("  " + "=" * 46)
        print("  |       社 保 公 积 金 计 算 器                 |")
        print("  " + "=" * 46)
        print()
        print("  说明: 企业+个人合计缴费比例")
        print()
        print("    [1] 一线城市   (基数上限¥30000)")
        print("    [2] 二线城市   (基数上限¥22000)")
        print("    [3] 三线城市   (基数上限¥15000)")
        print()
        print("    [0] 返回主菜单")
        print()
        print("-" * 46)

        choice = input("  选择城市等级 (0-3): ").strip()

        if choice == '0':
            break
        elif choice in ('1', '2', '3'):
            tier = int(choice)
            print()
            salary = safe_float_input(f"  [{city_names[tier]}] 请输入月工资: ")
            if salary <= 0:
                print("\n  [!] 工资必须为正数！")
                wait_for_enter()
                continue

            social = tax_calc.calculate_social_insurance(salary, city_tier=tier)

            clear_screen()
            print()
            print("  " + "=" * 46)
            print("  |     社 保 公 积 金 缴 纳 明 细               |")
            print("  " + "=" * 46)
            print()
            print(f"  城市:           {city_names[tier]}")
            print(f"  月工资:         ¥{salary:>12,.2f}")
            print(f"  实际缴费基数:   ¥{social['salary_base']:>12,.2f}")
            print()
            print("  ┌──────────────────────────────────────────┐")
            print("  │ 项目          │ 比例    │ 金额           │")
            print("  ├──────────────────────────────────────────┤")
            for item, detail in social['details'].items():
                names_cn = {
                    'pension': '养老保险',
                    'medical': '医疗保险',
                    'unemployment': '失业保险',
                    'housing_fund': '住房公积金'
                }
                name = names_cn.get(item, item)
                rate = detail['rate']
                amount = detail['amount']
                print(f"  │ {name:<14s}│ {rate:<8s}│ ¥{amount:>10,.2f}  │")
            print("  ├──────────────────────────────────────────┤")
            print(f"  │ {'合计':<14s}│ {'100%':<8s}│ ¥{social['total']:>10,.2f}  │")
            print("  └──────────────────────────────────────────┘")

            wait_for_enter()
        else:
            print("\n  [!] 无效选项！")
            import time; time.sleep(0.8)


# ==================== 主菜单 & 入口 ====================

MENU_OPTIONS = [
    ("1", "基础计算器", "四则运算（加减乘除）", run_calculator),
    ("2", "个税计算", "输入月薪，自动算个人所得税", run_personal_income_tax),
    ("3", "增值税计算", "不含税价 → 含税价 / 税额", run_vat_calculator),
    ("4", "社保公积金", "输入工资和城市，算社保明细", run_social_insurance),
]


def show_main_menu():
    """显示主菜单"""
    print()
    print("  " + "=" * 46)
    print("  |                  主 菜 单                       |")
    print("  " + "=" * 46)
    print()
    for num, name, desc, _ in MENU_OPTIONS:
        print(f"    [{num}] {name:<12s} — {desc}")
    print()
    print("    [0] 退出程序")
    print()
    print("-" * 46)


def main():
    """主函数 - 交互式循环入口"""
    print_banner()

    while True:
        show_main_menu()
        choice = input("  请选择功能 (0-4): ").strip()

        if choice == '0':
            print("\n  感谢使用，再见！\n")
            return 0

        handler = None
        for num, _, _, fn in MENU_OPTIONS:
            if num == choice:
                handler = fn
                break

        if handler:
            handler()  # 执行对应功能模块
        else:
            print("\n  [!] 无效选项，请重新输入！")
            import time
            time.sleep(0.8)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n  程序已中断。再见！\n")
        sys.exit(130)
    except Exception as e:
        print(f"\n  [!!!] 程序异常: {e}\n")
        sys.exit(1)
