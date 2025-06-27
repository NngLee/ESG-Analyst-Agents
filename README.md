
# 🧠 多智能体 ESG 分析系统

本项目构建了一个基于多智能体架构的 ESG 分析系统，支持通过输入企业名称或股票代码，自动抓取外部信息并进行 ESG 分析与投资判断，支持命令行和图形化界面两种交互方式。

---

## 🔍 项目简介

本项目实现了一个面向 ESG 投资分析的多智能体系统。系统由五个核心 Agent 构成：

- `FirmAgent`: 自动从外部 API 抓取企业公开数据；
- `EnvironmentAgent`: 对环境维度进行分析；
- `SocialAgent`: 对社会责任维度进行分析；
- `GovernanceAgent`: 对治理结构进行分析；
- `InvestorAgent`: 根据 ESG 综合评分生成投资建议。

系统支持两种运行方式：
- 命令行模式（适合批量处理和自动化分析）；
- 图形用户界面（GUI）模式，便于展示 ESG 得分、评级、投资建议等信息。

---

## 🚀 使用方式

### ✅ 命令行模式

```bash
python main.py 腾讯
```

或使用股票代码：

```bash
python main.py 000001.SZ
```

支持以下可选参数（推荐使用）：

```bash
python main.py "企业名称或股票代码" --city "城市" --country "国家代码" --cik "CIK代码"
```

### 🖥️ 图形界面模式

直接运行以下命令即可启动 ESG 智能分析平台 GUI：

```bash
python gui.py
```

界面提供输入框与分析按钮，用户只需输入企业名称，点击“开始分析”，即可获得 ESG 各维度评分、综合评级和系统生成的投资建议文本。

---

## 🧠 系统架构

```text
[用户输入] ──▶ FirmAgent ──┬─▶ EnvironmentAgent──▶ InvestorAgent
                           ├─▶ SocialAgent
                           ├─▶ GovernanceAgent
                          
```

- 数据来源包括：Yahoo Finance、Alpha Vantage、Wikipedia、OpenAQ、World Bank 等；
- ESG 评分基于 ESG 维度打分规则和 DeepSeek 模型；
- 投资策略参考 ESG 策略组合（负面筛选、正面筛选、整合、影响力投资）综合判断。

---

## 📁 文件结构

```text
│
├── agents.py           # 多个智能体的类定义
├── model.py            # 多智能体模型主逻辑
├── tools.py            # 外部数据抓取 API 封装
├── utils.py            # 辅助工具函数
├── gui.py              # GUI 图形界面程序（推荐使用）
├── deepseek_api.py     # ESG文本分析接口调用（DeepSeek等）
├── main.py             # 程序主入口（命令行模式）
├── background.jpeg     # GUI 背景图资源
├── .env                # 存放 API key 的环境变量文件
├── requirements.txt    # 所需依赖库
└── README.md           # 项目说明文档（当前文件）
```

---

## 🛡️ 注意事项

- 请妥善保管你的 `.env` 文件，避免公开泄露 API 密钥。
- 部分 API（如 Alpha Vantage）有调用频率限制，建议缓存结果或使用多个 API Key。
- 本地运行前请确保已安装 Python 3.8+，并执行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 开发者

- 作者：@Zhangxin Li      Liyao Chang
- 联系方式：2200011085@stu.pku.edu.cn
- 最后更新：2025 年 6 月

---

## 📜 许可证

本项目采用 MIT License 许可协议。
