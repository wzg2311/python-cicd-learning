# 🐍 Python CI/CD 学习项目 — 完整操作指南

> 从零搭建一套**可运行、可观察、可破坏**的企业级 Python CI/CD 流水线

---

## 📁 项目结构一览

```
python-cicd-learning/
├── .github/
│   └── workflows/
│       └── ci.yml              # ⭐ GitHub Actions CI/CD流水线配置（核心文件）
├── src/
│   ├── __init__.py             # 包初始化
│   ├── calculator.py           # 基础计算器（加减乘除）
│   ├── tax_calculator.py       # 税费计算（个税+增值税+社保）
│   └── config.py               # 项目配置管理
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py      # 计算器测试（30+用例）
│   └── test_tax_calculator.py  # 税费计算测试（20+用例）
├── main.py                     # 程序入口
├── requirements.txt            # 第三方依赖清单
├── pytest.ini                  # pytest配置
├── .flake8                     # 代码风格检查配置
└── .gitignore                  # Git忽略规则
```

---

## 🔧 第一步：本地环境初始化

### 1.1 创建虚拟环境（推荐，隔离依赖）

```bash
cd python-cicd-learning

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

# 安装项目依赖
pip install -r requirements.txt
```

### 1.2 本地运行验证

```bash
# 运行主程序
python main.py

# 运行代码检查（flake8）
flake8 .

# 运行单元测试（pytest）
pytest tests/ -v

# 运行测试并查看覆盖率
pytest tests/ -v --cov=src --cov-report=term-missing
```

> ✅ **如果以上三条命令都能正常运行通过**，说明你的本地环境没问题，可以继续下一步。

---

## 📤 第二步：Git 初始化 & 提交

```bash
cd python-cicd-learning

# 1) 初始化 Git 仓库
git init

# 2) 添加所有文件
git add .

# 3) 创建首次提交
git commit -m "feat: 初始化Python CI/CD学习项目

- 实现基础计算器模块（加减乘除）
- 实现税费计算模块（个税/增值税/社保）
- 编写完整单元测试（50+测试用例）
- 配置GitHub Actions CI/CD流水线
- 包含代码质量检查(flake8)、单元测试(pytest)、模拟部署"
```

---

## 🌐 第三步：推送到 GitHub

### 3.1 在 GitHub 上创建新仓库

1. 打开 [github.com](https://github.com)，登录账号
2. 点击右上角 **"+" → "New repository"**
3. 填写信息：
   - Repository name: `python-cicd-learning`（或你喜欢的名字）
   - Description: `Python CI/CD Learning Project`
   - **不要勾选** README、.gitignore、License（我们本地已有这些文件！）
4. 点击 **Create repository**

### 3.2 推送代码

GitHub 创建完成后会显示推送命令，按以下方式执行：

```bash
# 关联远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/python-cicd-learning.git

# 设置主分支名（GitHub默认main，老仓库可能是master）
git branch -M main

# 首次推送到 GitHub
git push -u origin main
```

### 3.3 观察 CI/CD 流水线运行！

🎉 **推送成功后，自动触发以下流程：**

1. 打开你的仓库页面: `https://github.com/YOUR_USERNAME/python-cicd-learning`
2. 点击顶部的 **"Actions"** 标签页
3. 你会看到 **"Python CI/CD Pipeline"** 正在运行！
4. 点击进去可以看到每个 Job 的实时日志输出

> 💡 **首次运行可能需要等待30秒~1分钟**，因为GitHub需要启动新的Runner来执行。

---

## 🐛 第四步：故意制造 Bug，观察 CI 自动拦截！

这是最关键的一步——**亲身体验 CI 如何帮你挡住有问题的代码**。

### 4.1 制造一个逻辑 Bug（让测试失败）

打开 `src/calculator.py`，找到加法函数，**故意改错**：

```python
# 原来（正确）:
def add(self, a: float, b: float) -> float:
    return a + b

# 改成（故意引入bug）：
def add(self, a: float, b: float) -> float:
    return a * b          # ❌ 把 + 改成了 * （加法变乘法！）
```

### 4.2 提交并推送 Bug 代码

```bash
# 查看修改了哪些文件
git diff

# 提交这个 bug
git add src/calculator.py
git commit -m "bug: 故意制造加法bug用于演示CI拦截效果"

# 推送到 GitHub（CI 会自动触发）
git push origin main
```

### 4.3 观察 CI 失败！

1. 回到 GitHub 仓库的 **Actions** 页面
2. 你会发现这次流水线 **❌ 红色失败** 了！
3. 点开失败的 Job，查看 pytest 的报错信息：
   ```
   FAILED tests/test_calculator.py::TestAdd::test_positive_numbers
   AssertionError: assert 6 == 5   ← 预期 2+3=5，实际返回 2*3=6
   ```

### 4.4 修复 Bug 并重新提交

把代码改回正确的版本：

```python
# 改回正确实现：
def add(self, a: float, b: float) -> float:
    return a + b
```

然后：

```bash
git add src/calculator.py
git commit -m "fix: 修复加法运算bug"
git push origin main
```

→ 再次观察 Actions 页面，流水线应该恢复为 **✅ 绿色通过**！

### 4.5 更多「故意搞坏」的实验

| 实验 | 怎么做 | 哪一步会失败 |
|------|--------|-------------|
| **语法错误** | 在某行末尾多打个冒号 `:` | flake8 代码检查 |
| **除零Bug** | 注释掉 `if b == 0` 的判断 | pytest 测试用例 |
| **导入错误** | 改错 import 路径 | pytest 无法导入模块 |
| **缩进错误** | 删掉某个函数的缩进 | flake8 缩进检查 |

> 🧪 **建议每种都试一次**，感受不同类型的错误在哪个环节被捕获。

---

## 📖 第五步：大白话解释每步 CI/CD 流程的价值

### 整体流程图

```
开发者写代码 → Git Push → GitHub 触发 Actions
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌─────────┐    ┌──────────┐    ┌──────────┐
              │ Lint    │───▶│  Test    │───▶│ Deploy   │
              │ 代码检查 │    │ 单元测试  │    │  部署上线 │
              └─────────┘    └──────────┘    └──────────┘
                 ❌拦住         ❌拦住           ✅才能到这
```

### Step-by-step 大白话解读

| 步骤 | 干了什么 | 真实工作中的价值 |
|------|---------|----------------|
| **① Checkout（拉代码）** | 从 GitHub 下载最新代码到一台干净的虚拟机上 | 就像你刚入职拿到一份全新的代码，从零开始跑起来。确保每次构建的环境是干净的，不会受上次的残留影响 |
| **② Setup Python（配环境）** | 安装指定版本的 Python 解释器 | 团队里每个人电脑上的 Python 版本不一样？CI 保证大家用的是同一个版本，避免「我这边能跑啊」的问题 |
| **③ Install Dependencies（装依赖）** | 根据 requirements.txt 安装第三方库 | 记录所有依赖及其精确版本。就像菜谱里的食材清单——缺什么一目了然，新人接手也能装出一样的环境 |
| **④ Flake8（代码风格检查）** | 扫描代码是否符合 PEP8 规范（命名、行长、复杂度等） | 相当于**语文老师批改作文**——不是看对不对，而是看写得规不规范。统一代码风格，降低团队协作成本 |
| **⑤ Pytest（单元测试）** | 运行所有自动化测试用例，验证功能是否正常 | 这是**最核心的一道防线**！相当于工厂的质检员——每件产品出厂前都要检测。测试不过 = 有缺陷的产品不能出货 |
| **⑥ Deploy（部署）** | 只有前面的步骤全部通过，才允许部署上线 | 这就是**门禁系统**——前面任何一道关卡没过，代码就别想上线到生产环境。保护用户不受 Bug 影响 |

### 为什么这比「手动测试」强？

```
手动测试流程（传统方式）：
  写代码 → 自己测一下 → 觉得没问题 → 直接上线 → 用户反馈Bug 😱
  
CI/CD 自动化流程（现代化方式）：
  写代码 → push → 自动跑全套检查+测试 → 通过后才上线 → 用户收到稳定版本 😊
```

**核心价值总结成三句话：**

1. **快** —— 提交代码后几分钟内就知道有没有问题，不用等人肉测试
2. **准** —— 机器不会漏测、不会疲劳、不会「差不多就行了」，每次执行标准一致
3. **安全** —— 有问题的代码被自动拦截在生产环境之外，用户永远不会用到有 Bug 的版本

---

## 📚 进阶学习方向

掌握了这套基础 CI/CD 后，你可以继续探索：

- [ ] **添加更多测试场景** —— 边界值、异常路径、性能测试
- [ ] **接入代码覆盖率门槛** —— 要求覆盖率不低于80%才通过
- [ ] **多环境部署** —— 开发环境 / 测试环境 / 生产环境分别部署
- [ ] **集成 Slack/钉钉通知** —— 构建失败时自动发消息提醒团队
- [ ] **Docker 容器化部署** —— 用 Docker 替换模拟部署，真正发布服务
- [ ] **Code Review 强制** —— 配置 Branch Protection Rules，必须 Review 才能合并

---

## ❓ 常见问题 (FAQ)

**Q: CI 运行太慢怎么办？**
A: 本项目规模小，通常 30 秒~1 分钟完成。大型项目可以通过并行 Job、缓存依赖等优化。

**Q: 免费额度够用吗？**
A: GitHub 公开仓库的 Actions 免费额度很大（每月 2000 分钟），个人学习完全够用。

**Q: 必须要用 Ubuntu 吗？**
A: 不一定，也可以选 `windows-latest` 或 `macos-latest`。但 Ubuntu 最常用且免费。

**Q: 如何查看历史构建记录？**
A: 仓库页面 → Actions 标签 → 左侧可以看到每次运行的列表，点进去看详情和日志。
