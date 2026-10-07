# 本地使用与改造

本项目的核心是根目录 `SKILL.md`，接口实现写在其中的 Python 代码块里。新增的
`examples/quote.py` 直接加载原文件中的代码，修改 `SKILL.md` 后示例也会使用新的实现。

## 环境

本次已创建 `.venv` 并安装依赖，使用 Python 3.12。以后在其他机器重新克隆时，在项目根目录执行：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

依赖清单沿用上游要求，未锁定版本。`.venv`、`.env` 和抓取结果 `reports/` 已加入 Git 忽略规则。

## 取一份行情

```bash
.venv/bin/python examples/quote.py 600519 sz000001 sh000001 510300
```

输出 JSON，包含数据来源、请求 URL、抓取时间及每只证券的行情。支持前缀、后缀和聚宽代码。
`000001` 默认是平安银行；上证指数请用 `sh000001` 或 `000001.SH`。
`fetched_at` 是抓取时间，休市或停牌时返回的价格可能来自最近一次交易；原实现的 `is_stale`
和 `stale_reason` 字段会保留。没有返回行情的代码会报错，避免把空结果当成成功。

需要保存结果时：

```bash
mkdir -p reports
.venv/bin/python examples/quote.py 600519 > reports/quote.json
```

其他接口按 `SKILL.md` 顶部的「端点路由速查」找到对应章节，并先加载章节要求的共用 helper。
在 Codex 中打开本项目目录，说明需要使用 `SKILL.md` 的哪个数据能力即可。

## 改代码与验证

接口改动以 `SKILL.md` 为准；补充对应的 `tests/` 测试，然后运行：

```bash
.venv/bin/python -m unittest discover -s tests
```

默认测试使用模拟数据，不访问真实端点。在线测试需要按各测试文件顶部说明显式设置环境变量。
本次安装后的验证结果：168 项测试，165 项通过，3 项在线测试按默认设置跳过。另已用腾讯真实接口
成功读取贵州茅台、平安银行、上证指数和沪深 300 ETF 的行情。

## GitHub 与上游同步

远端约定：`origin` 是自己的 GitHub 仓库，`upstream` 是 `simonlin1212/a-stock-data`。
修改前创建分支，提交后推送到自己的仓库：

```bash
git switch -c feature/my-change
git add SKILL.md tests/
git commit -m "Describe the change"
git push -u origin feature/my-change
```

拉取原作者更新时，先确认本地修改已提交，再执行：

```bash
git fetch upstream
git switch main
git merge upstream/main
git push origin main
```

遇到冲突需审查并解决。保留原项目的 `LICENSE`、版权声明和上游来源。
