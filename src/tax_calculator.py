"""
税费计算模块 - 模拟真实业务逻辑
包含：个税计算、增值税计算、社保计算等企业常见场景
"""
from .calculator import Calculator

# 个税累进税率表（2024年标准）
PERSONAL_INCOME_TAX_BRACKETS = [
    (3000, 0.03, 0),       # 不超过3000元: 3%
    (12000, 0.10, 210),    # 超过3000-12000部分: 10%, 速算扣除210
    (25000, 0.20, 1410),   # 超过12000-25000部分: 20%
    (35000, 0.25, 2660),   # 超过25000-35000部分: 25%
    (55000, 0.30, 4410),   # 超过35000-55000部分: 30%
    (80000, 0.35, 7160),   # 超过55000-80000部分: 35%
    (float('inf'), 0.45, 15160)  # 超过80000部分: 45%
]

# 增值税税率
VAT_RATES = {
    'general': 0.13,      # 一般纳税人: 13%
    'small': 0.03,        # 小规模纳税人: 3%
}

# 社保缴费比例（企业+个人合计）
SOCIAL_INSURANCE_RATES = {
    'pension': 0.24,      # 养老保险 24%（企业16%+个人8%）
    'medical': 0.105,     # 医疗保险 10.5%
    'unemployment': 0.015,  # 失业保险 1.5%
    'housing_fund': 0.12,   # 住房公积金 12%
}


class TaxCalculator:
    """税费计算器 - 封装各类税费计算逻辑"""

    def __init__(self):
        self.calc = Calculator()

    def calculate_personal_income_tax(self, taxable_income: float) -> dict:
        """
        计算个人所得税（累进税率）
        
        Args:
            taxable_income: 应纳税所得额（已扣除起征点5000元/月和专项扣除后的金额）
            
        Returns:
            包含税率、速算扣除数、应纳税额的字典
        """
        if taxable_income <= 0:
            return {'tax_rate': 0, 'quick_deduction': 0, 'tax_amount': 0.0}

        for threshold, rate, deduction in PERSONAL_INCOME_TAX_BRACKETS:
            if taxable_income <= threshold:
                tax_amount = self.calc.multiply(taxable_income, rate) - deduction
                return {
                    'taxable_income': round(taxable_income, 2),
                    'tax_rate': f"{int(rate * 100)}%",
                    'quick_deduction': deduction,
                    'tax_amount': round(max(0, tax_amount), 2)
                }

    def calculate_vat(self, amount: float, taxpayer_type: str = 'general') -> dict:
        """
        计算增值税
        
        Args:
            amount: 不含税金额
            taxpayer_type: 纳税人类型 ('general'或'small')
            
        Returns:
            含税金额、税额、不含税金额的字典
        """
        rate = VAT_RATES.get(taxpayer_type, VAT_RATES['general'])
        tax = self.calc.multiply(amount, rate)
        total_with_tax = self.calc.add(amount, tax)

        return {
            'amount_exclusive': round(amount, 2),
            'vat_rate': f"{int(rate * 100)}%",
            'vat_amount': round(tax, 2),
            'amount_inclusive': round(total_with_tax, 2)
        }

    def calculate_social_insurance(self, salary: float, city_tier: int = 1) -> dict:
        """
        计算社保公积金缴纳金额
        
        Args:
            salary: 工资基数
            city_tier: 城市等级，影响缴费基数上下限
            
        Returns:
            各险种缴纳明细及总额
        """
        # 不同城市等级的缴费基数范围
        base_limits = {
            1: (5000, 30000),  # 一线城市
            2: (4000, 22000),  # 二线城市
            3: (3000, 15000),  # 三线及其他城市
        }
        min_base, max_base = base_limits.get(city_tier, base_limits[3])

        # 确定实际缴费基数
        actual_base = max(min_base, min(salary, max_base))

        result = {'salary_base': actual_base, 'details': {}}
        total = 0.0

        for name, rate in SOCIAL_INSURANCE_RATES.items():
            amount = self.calc.multiply(actual_base, rate)
            result['details'][name] = {
                'rate': f"{int(rate * 100)}%",
                'amount': round(amount, 2)
            }
            total = self.calc.add(total, amount)

        result['total'] = round(total, 2)
        return result


# 模块级便捷函数
def calc_personal_tax(income: float) -> dict:
    """个税计算快捷函数"""
    return TaxCalculator().calculate_personal_income_tax(income)


def calc_vat(amount: float, taxpayer_type: str = 'general') -> dict:
    """增值税计算快捷函数"""
    return TaxCalculator().calculate_vat(amount, taxpayer_type)
