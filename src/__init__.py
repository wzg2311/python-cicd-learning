# Python CI/CD Learning Project
# 企业级Python项目CI/CD学习示例

"""
src - 核心业务模块
  ├── __init__.py      模块初始化
  ├── calculator.py    基础计算器（加减乘除）
  ├── tax_calculator.py 税费计算业务逻辑
  └── config.py        项目配置管理

tests - 单元测试
  ├── test_calculator.py   计算器测试
  └── test_tax_calculator.py 税费计算测试

.github/workflows/ci.yml  - GitHub Actions CI/CD流水线配置
main.py                    - 程序入口
requirements.txt           - 第三方依赖管理
.flake8                   - 代码风格检查配置
"""
