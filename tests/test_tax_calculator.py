"""
税费计算模块单元测试
覆盖：个税计算、增值税计算、社保计算、边界条件
"""
import sys
import os
import pytest

# 确保可以导入src模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tax_calculator import (
    TaxCalculator,
    calc_personal_tax,
    calc_vat,
    PERSONAL_INCOME_TAX_BRACKETS,
    VAT_RATES,
    SOCIAL_INSURANCE_RATES
)


@pytest.fixture
def tax_calc():
    """创建税费计算器实例"""
    return TaxCalculator()


# ==================== 个人所得税测试 ====================
class TestPersonalIncomeTax:
    """个人所得税计算测试"""

    def test_no_tax_for_low_income(self, tax_calc):
        """收入低于起征点，不交税"""
        result = tax_calc.calculate_personal_income_tax(0)
        assert result['tax_amount'] == 0.0

    def test_lowest_bracket(self, tax_calc):
        """最低税率档: 应纳税所得3000元，税率3%"""
        result = tax_calc.calculate_personal_income_tax(3000)
        assert result['tax_rate'] == '3%'
        assert result['quick_deduction'] == 0
        assert result['tax_amount'] == pytest.approx(90.0)

    def test_second_bracket(self, tax_calc):
        """第二档: 10000元应纳税所得"""
        # 10000 * 10% - 210 = 790
        result = tax_calc.calculate_personal_income_tax(10000)
        assert result['tax_rate'] == '10%'
        assert result['tax_amount'] == pytest.approx(790.0)

    def test_third_bracket(self, tax_calc):
        """第三档: 20000元应纳税所得"""
        # 20000 * 20% - 1410 = 2590
        result = tax_calc.calculate_personal_income_tax(20000)
        assert result['tax_rate'] == '20%'
        assert result['tax_amount'] == pytest.approx(2590.0)

    def test_top_bracket(self, tax_calc):
        """最高档: 超高收入（月应纳税所得100000元）"""
        # 100000 * 45% - 15160 = 29840
        result = tax_calc.calculate_personal_income_tax(100000)
        assert result['tax_rate'] == '45%'
        assert result['tax_amount'] > 0

    def test_negative_income(self, tax_calc):
        """负数或零收入不应产生税额"""
        result = tax_calc.calculate_personal_income_tax(-5000)
        assert result['tax_amount'] == 0.0

    def test_returns_dict_with_all_keys(self, tax_calc):
        """返回值必须包含所有必要字段"""
        result = tax_calc.calculate_personal_income_tax(15000)
        expected_keys = {'taxable_income', 'tax_rate', 'quick_deduction', 'tax_amount'}
        assert set(result.keys()) == expected_keys


# ==================== 增值税测试 ====================
class TestVAT:
    """增值税计算测试"""

    def test_general_taxpayer(self, tax_calc):
        """一般纳税人13%增值税"""
        result = tax_calc.calculate_vat(10000, 'general')
        assert result['vat_rate'] == '13%'
        assert result['vat_amount'] == pytest.approx(1300.0)
        assert result['amount_inclusive'] == pytest.approx(11300.0)

    def test_small_scale_taxpayer(self, tax_calc):
        """小规模纳税人3%增值税"""
        result = tax_calc.calculate_vat(10000, 'small')
        assert result['vat_rate'] == '3%'
        assert result['vat_amount'] == pytest.approx(300.0)
        assert result['amount_inclusive'] == pytest.approx(10300.0)

    def test_zero_amount(self, tax_calc):
        """零金额不含税"""
        result = tax_calc.calculate_vat(0, 'general')
        assert result['vat_amount'] == 0.0

    def test_unknown_type_defaults_to_general(self, tax_calc):
        """未知纳税人类型默认按一般纳税人处理"""
        result = tax_calc.calculate_vat(1000, 'unknown_type')
        assert result['vat_rate'] == '13%'

    def test_vat_returns_complete_info(self, tax_calc):
        """返回值包含完整的增值税信息"""
        result = tax_calc.calculate_vat(5000, 'general')
        assert 'amount_exclusive' in result
        assert 'vat_rate' in result
        assert 'vat_amount' in result
        assert 'amount_inclusive' in result


# ==================== 社保公积金测试 ====================
class TestSocialInsurance:
    """社保公积金计算测试"""

    def test_tier1_city_normal_salary(self, tax_calc):
        """一线城市，正常工资基数"""
        result = tax_calc.calculate_social_insurance(20000, city_tier=1)
        # 一线城市范围: 5000-30000, 20000在范围内
        assert result['salary_base'] == 20000
        assert result['total'] > 0
        # 验证各险种都有值
        for detail in result['details'].values():
            assert detail['amount'] > 0

    def test_below_minimum_base(self, tax_calc):
        """工资低于缴费基数下限，按下限计算"""
        result = tax_calc.calculate_social_insurance(3000, city_tier=1)
        # 一线城市下限5000
        assert result['salary_base'] == 5000

    def test_above_maximum_base(self, tax_calc):
        """工资超过缴费基数上限，按上限计算"""
        result = tax_calc.calculate_social_insurance(100000, city_tier=1)
        # 一线城市上限30000
        assert result['salary_base'] == 30000

    def test_different_city_tiers(self, tax_calc):
        """不同城市等级有不同的基数范围"""
        tier1 = tax_calc.calculate_social_insurance(25000, city_tier=1)
        tier3 = tax_calc.calculate_social_insurance(25000, city_tier=3)
        # 一线城市能容纳25000，三线不能（上限15000）
        assert tier1['salary_base'] == 25000
        assert tier3['salary_base'] == 15000

    def test_social_details_structure(self, tax_calc):
        """验证返回结构完整性"""
        result = tax_calc.calculate_social_insurance(15000)
        assert 'salary_base' in result
        assert 'details' in result
        assert 'total' in result
        # 确认所有险种都在
        for name in SOCIAL_INSURANCE_RATES.keys():
            assert name in result['details']


# ==================== 模块级便捷函数测试 ====================
class TestModuleFunctions:
    """模块级便捷函数测试"""

    def test_calc_personal_tax_function(self):
        """calc_personal_tax() 可用"""
        result = calc_personal_tax(8000)
        assert 'tax_amount' in result

    def test_calc_vat_function(self):
        """calc_vat() 可用"""
        result = calc_vat(5000)
        assert 'vat_amount' in result
