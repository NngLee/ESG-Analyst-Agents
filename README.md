# 🧠 多智能体 ESG 分析系统

本项目构建了一个基于多智能体架构的 ESG 分析系统，支持通过输入企业名称或股票代码，自动抓取外部信息并进行 ESG 分析与投资判断。

---
## 🔍 项目简介

本项目实现了一个面向 ESG 投资分析的多智能体系统。系统由五个核心 Agent 构成：

- `FirmAgent`: 自动从外部 API 抓取企业公开数据；
- `EnvironmentAgent`: 对环境维度进行分析；
- `SocialAgent`: 对社会责任维度进行分析；
- `GovernanceAgent`: 对治理结构进行分析；
- `InvestorAgent`: 根据 ESG 综合评分生成投资建议。

系统支持命令行输入企业名称或股票代码，自动完成信息采集、ESG 打分、评级、投资建议全流程。
---
## 🚀 使用方式
命令行输入如下命令，进行 ESG 分析：

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

---

## 🧠 系统架构

```text
[用户输入] ──▶ FirmAgent ──┬─▶ EnvironmentAgent
                          ├─▶ SocialAgent
                          ├─▶ GovernanceAgent
                          └─▶ InvestorAgent
```

- 数据来源包括：Yahoo Finance、Alpha Vantage、Wikipedia、OpenAQ、World Bank 等；
- ESG 评分基于《ESG评分标准》及 DeepSeek 模型；
- 投资策略参考《ESG投资策略.docx》文件中定义的四种类型综合判断。

---

## 📁 文件结构

```text
│
├── agents.py           # 多个智能体的类定义
├── tools.py            # 外部数据抓取 API 封装
├── deepseek_api.py     # 调用 DeepSeek 进行 ESG 打分或文本生成
├── model.py            # 多智能体模型主逻辑
├── main.py             # 程序主入口，支持命令行输入
├── requirements.txt    # 所需依赖库
├── .env                # 存放 API key 的环境变量文件
└── README.md           # 项目说明文档（当前文件）
```

---

## 🛡️ 注意事项

- 请妥善保管你的 `.env` 文件，避免公开泄露 API 密钥。
- 部分 API（如 Alpha Vantage）有调用频率限制，建议缓存结果或使用多个 API Key。
- 请确保本地 Python 环境版本为 **3.8+**，并已通过以下方式安装依赖：

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