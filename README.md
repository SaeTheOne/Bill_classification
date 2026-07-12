一个基于 PySide6 的本地账单分类工具，支持微信和支付宝账单的自动分类。

## ✨ 功能特点

- 📊 支持微信、支付宝账单导入（CSV/Excel 格式）
- 🏷️ 三级分类体系（一级分类 → 二级分类 → 三级分类）
- 🔍 正则表达式规则匹配，精准分类
- ✏️ 用户自定义关键词追加（无需修改系统规则）
- 📝 未分类交易自动导出，方便补充规则
- 💾 分类规则可视化编辑（增删改查）
- 🎯 右键菜单 + Delete 键快速删除分类
- 📱 界面自适应屏幕大小

## 📁 项目结构
Bill_classification/
├── main.py # 程序入口
├── categories_config.json # 系统分类规则
├── user_keywords.json # 用户追加的关键词
├── core/
│ ├── init.py
│ ├── category_manager.py # 分类管理核心
│ ├── worker.py # 后台处理线程
│ └── user_keywords_manager.py # 用户关键词管理
└── ui/
├── init.py
├── main_window.py # 主窗口
├── category_dialog.py # 分类管理对话框
└── widgets.py # 自定义控件

text

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/Bill_classification.git
cd Bill_classification
2. 创建虚拟环境（推荐）
bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate   # Linux/Mac
3. 安装依赖
bash
pip install PySide6 openpyxl python-dateutil
4. 运行
bash
python main.py
📖 使用说明
导入账单
将微信/支付宝导出的 CSV/Excel 文件拖入程序窗口

点击「开始处理」按钮

程序会自动分类并生成 完成/sc.xlsx

管理分类规则
点击菜单栏「分类管理」→「管理分类规则」：

添加分类：点击对应的添加按钮（支持批量，用空格分隔）

重命名：双击分类名称

删除：右键菜单或按 Delete 键

追加关键词：选择三级分类，点击「追加关键词」

分类层级
text
支出 (一级)
├── 食品餐饮 (二级)
│   ├── 三餐 (三级) ← 规则在此
│   ├── 零食 (三级)
│   └── 饮料酒水 (三级)
├── 健康医疗 (二级)
│   └── 医院 (三级)
└── ...
收入 (一级)
├── 工资 (二级)
├── 收红包 (二级)
└── ...
用户关键词 vs 系统规则
特性	系统规则	用户关键词
文件	categories_config.json	user_keywords.json
优先级	低	高
修改方式	编辑 JSON 文件	UI 界面追加
匹配方式	正则表达式	包含匹配
💡 用户关键词优先级更高，适合快速添加自定义分类，不会破坏系统规则。

🔧 配置文件说明
categories_config.json
系统分类规则，使用正则表达式匹配：

json
{
  "支出": {
    "食品餐饮": {
      "三餐": "餐饮|饭店|餐厅|食堂|快餐|早餐|午餐|晚餐|夜宵|外卖|盒饭|便当",
      "零食": "零食|小吃|饼干|薯片|糖果|巧克力|坚果|果冻|辣条|薯条"
    }
  }
}
user_keywords.json
用户追加的关键词，由 UI 管理：

json
{
  "支出/食品餐饮/饮料酒水": ["桃桃乌龙", "芒果布丁"],
  "支出/出行交通/共享单车": ["先骑后付"]
}
📤 输出格式
处理完成后生成 完成/sc.xlsx：

日期	收支类型	金额	类别	子类	所属账本	收支账户	备注
2026-06-27	支出	33.4	食品餐饮	三餐	日常账本	微信钱包	...
未分类交易会生成 完成/未分类交易.xlsx。

📋 依赖
Python 3.8+

PySide6 >= 6.0.0

openpyxl >= 3.0.0

python-dateutil >= 2.8.0

🤝 贡献
欢迎提交 Issue 和 Pull Request！

📄 许可证
MIT License
"@ | Out-File -FilePath README.md -Encoding UTF8
