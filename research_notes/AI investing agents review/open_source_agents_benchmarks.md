# Open-source LLM trading agents and the evidence on how well LLMs trade (as of 2 Nov 2026)

Method note: this session could not open pages directly. arxiv.org, nof1.ai mirrors, forklog.com and iweaver.ai would not resolve, and the GitHub API was not enabled. So every finding below comes from search-result summaries of the cited pages, not from reading the full text. Star counts in particular are snapshots from aggregators taken in different months. Check them on GitHub before publishing.

## 1. Notable open-source repos where an LLM makes trading decisions

### Takeaway
The best-known projects are multi-agent research and decision frameworks. TradingAgents has about 70k-92k stars, ai-hedge-fund about 50k and FinRobot about 7k. Most default to backtests or paper trading and do not wire into a live broker. Claude is usually one of several interchangeable LLM backends rather than the default. Actual Claude-driven trading mostly happens through Alpaca's official MCP server plus Claude Desktop or Claude Code, and in hobbyist or hackathon bots with unverified results.

### Cited Findings
**TradingAgents (TauricResearch)**
- Open-source Python framework built on LangGraph. It has analyst agents, bullish and bearish researcher agents that "critically assess the insights provided by the Analyst Team" through structured debates, a trader agent and risk managers. Licence is Apache-2.0. The paper is arXiv 2412.20138 (Yijia Xiao et al., Dec 2024). — [ossinsight](https://ossinsight.io/analyze/TauricResearch/TradingAgents); [dev.co](https://dev.co/ai/frameworks/tradingagents); [gittrend](https://gittrend.io/repo/TauricResearch/TradingAgents)
- Star counts conflict by snapshot date:
  - about 91.7k stars and 17.7k forks, latest release v0.3.1 (5 Jul 2026)
  - about 69.4k stars and 13.4k forks, last push 1 May 2026
  - 85,174 stars on SourcePulse
  - "nearly 50K" in March 2026

  The project is actively maintained as of mid-2026. — [oosmetrics](https://oosmetrics.com/repo/TauricResearch/TradingAgents); [SourcePulse](https://www.sourcepulse.org/projects/2368224); [themenonlab, Mar 2026](https://themenonlab.blog/blog/ai-finance-github-repos-march-2026)

**ai-hedge-fund (virattt)**
- About 50k-51k stars and 9k+ forks. — [reskilll](https://blogs.reskilll.com/ai-hedge-fund-the-50k-star-open-source-multi-agent-investment-system/); [edgen](https://www.edgen.tech/news/post/new-ai-hedge-fund-with-12-legendary-investors-gets-51k-github-stars)
- Investor-persona agents such as Buffett, Munger, Burry and Cathie Wood each give an independent view on a stock. A portfolio-manager agent combines those views into a buy, sell or hold signal. The repo also has a backtester and a React 18 / TypeScript front end with a React Flow visual workflow editor. Reported agent counts vary from 12 to 19 as the roster grew. — [themenonlab](https://themenonlab.blog/blog/ai-hedge-fund-multi-agent); [pyshine](https://pyshine.com/AI-Hedge-Fund-Multi-Agent-Investment-System/); [perplexityaimagazine](https://perplexityaimagazine.com/?p=1752); [qbitai, Apr 2026](https://www.qbitai.com/2026/04/400350.html)

**FinRobot (AI4Finance Foundation)**
- Described as "the first AI agent framework specifically designed for equity research", using multi-agent chain-of-thought (arXiv 2411.08804, Nov 2024; platform paper arXiv 2405.14767). Licence is Apache-2.0, and it installs from PyPI. Recent snapshots show about 6.6k-7.5k stars. It produces research and valuation reports rather than placing trades. — [arXiv 2411.08804](https://arxiv.org/html/2411.08804v1); [SourcePulse](https://www.sourcepulse.org/projects/1844779); [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2FAI4Finance-Foundation%2FFinRobot); [neurohive](https://neurohive.io/en/state-of-the-art/finrobot-open-source-multi-agent-framework-for-automated-equity-research/)

**AI-Trader (HKUDS, University of Hong Kong)**
- Billed as "the first fully-automated, live, and data-uncontaminated evaluation benchmark" for LLM agents (arXiv 2512.10971). It covers US stocks, China A-shares and crypto, and agents gather information themselves. About 11.4k stars. Since extended into AI-Trader v2 and a live bench at ai4trade.ai. One Chinese-language write-up claimed DeepSeek returned +9.68% and "crushed GPT" in its NASDAQ-100 contest. — [hyper.ai](https://hyper.ai/en/papers/2512.10971); [SourcePulse](https://www.sourcepulse.org/projects/17524338); [CSDN](https://damodev.csdn.net/6a437d96662f9a54cb86c215.html)

**Alpaca MCP server (official, alpacahq)**
- Exposes 43 Trading API functions covering equities, ETFs, crypto and multi-leg options. Works with Claude Desktop and other MCP clients. Needs Python 3.10+, uv and Alpaca API keys. Supports paper trading with a simulated $100K account. — [Alpaca docs](https://docs.alpaca.markets/docs/alpaca-mcp-server); [alpaca.markets/mcp-server](https://alpaca.markets/mcp-server)
- Listings warn that the server "will have access to your Alpaca account and can place real trades". Community forks also exist; tedlikeskix/alpaca-mcp-server is about 25 stars and paper-by-default. — [playbooks](https://playbooks.com/mcp/tedlikeskix-alpaca-trading); [GitHub tedlikeskix](https://github.com/tedlikeskix/alpaca-mcp-server)

**ChatGPT-Micro-Cap-Experiment (Nathan Smith)**
- A $100 portfolio of US micro-caps chosen by ChatGPT, run for about six months (late June to late December 2025). The repo has Python tracking scripts and trade logs, and updates were posted on Substack and HackerNoon. — [Decrypt](https://decrypt.co/332826/high-school-students-chatgpt-trading-bot)
- Early press reported +23.8% in four weeks against +3.9% for the Russell 2000 and +3.5% for XBI. — [Decrypt](https://decrypt.co/332826/high-school-students-chatgpt-trading-bot); [Benzinga](https://www.benzinga.com/markets/equities/25/08/46783783/redditors-100-chatgpt-day-trading-experiment-trounces-two-benchmark-indexes-with-24-returns-here)
- Final outcome: $82.88 (about -17%) with a maximum drawdown of -50.33% on 6 Nov 2025. On 22 Dec 2025 the portfolio was -30% while the baseline was +9.1%. The author said it failed to beat benchmarks. The author also ran a DeepSeek vs GPT-4o variant. — [HackerNoon final report](https://hackernoon.com/can-chatgpt-outperform-the-market-final-report); [HackerNoon week 26](https://hackernoon.com/can-chatgpt-outperform-the-market-week-26); [Substack](https://nathanbsmith729.substack.com/p/deepseek-vs-gpt4-o-ai-micro-cap-portfolio)

**Agent Market Arena (The-FinAI)**
- Repo that wraps agents as HTTP endpoints for a live benchmark (see section 3). — [GitHub](https://github.com/The-FinAI/Agent_Market_Arena)

**Claude Code / Claude-specific bots**
- No verified, long-running open-source Claude Code plus Alpaca track record was found. What exists:
  - Guides for a scheduled Claude Code agent that researches, trades on Alpaca paper and writes a journal entry. — [MindStudio](https://www.mindstudio.ai/blog/build-ai-trading-agent-claude-code-alpaca); [MindStudio routines](https://www.mindstudio.ai/blog/how-to-build-ai-trading-agent-claude-code-routines)
  - Hackathon bots, for example BARCO, which uses Claude Opus 4.5 as its "decision brain" via MCP on Alpaca paper. One 0DTE options entry self-reported $100k turning into $179k over three paper sessions. — [lablab BARCO](https://lablab.ai/ai-hackathons/alpaca-ai-trading-agents-hackathon/guacalita/barco-alpaca-ai-trading-agent); [lablab 0DTE](https://lablab.ai/ai-hackathons/alpaca-ai-trading-agents-hackathon/kiba/alpaca-0dte-auto-trade)
  - A two-hour Claude Code scalping test on a Bybit sub-account of about $2,500. — [sozai transcript](https://sozai.app/transcript/claude-code-free-scalping-bot-results/)
  - Personal blogs. — [mejba.me](https://www.mejba.me/blog/claude-ai-automate-stock-trading); [peterc.org](https://peterc.org/misc/tradingbot.html)

### Inferences
- Popularity reflects interest in the architecture, not trading performance. None of the high-star repos publishes an audited live track record.
- "Claude makes trades" in practice means Claude Desktop or Claude Code calling Alpaca MCP tools, or Claude chosen as the LLM backend in TradingAgents or ai-hedge-fund through their LLM-provider configuration.
- The micro-cap experiment is a clean example of the press cycle: an early viral +24% headline, then a -17% finish and a -50% drawdown that got far less coverage.

### Gaps
- I could not get live star counts, exact licences for ai-hedge-fund and the micro-cap repo, or current commit activity because the GitHub API was blocked. ai-hedge-fund is commonly reported as MIT-licensed, but I could not confirm it.
- I could not confirm the official alpacahq/alpaca-mcp-server star count or whether it supports live trading by default.
- I did not research FinGPT, FinRL, FinMem or nof1's own repo.

## 2. Typical project structure, core loop, prompt patterns and guardrails

### Takeaway
Nearly all projects follow the same pipeline:
1. Fetch data: prices and indicators, fundamentals, news and sentiment.
2. Have role-specialised LLM agents analyse it, often with a bull vs bear debate.
3. Have a trader or portfolio-manager agent emit a structured decision, usually JSON with action, size, confidence and rationale.
4. Run deterministic risk checks that the model cannot override.
5. Send the order through a broker API, usually Alpaca paper.

The key guardrails are hard-coded position and leverage caps, paper-first deployment, and human approval of tool calls.

### Cited Findings
- TradingAgents pipeline: analyst team (fundamental, sentiment, news, technical) → bullish and bearish researchers debate → trader → risk-management team → final decision. It is orchestrated as a LangGraph graph. — [dev.co](https://dev.co/ai/frameworks/tradingagents); [gittrend](https://gittrend.io/repo/TauricResearch/TradingAgents)
- ai-hedge-fund pipeline: persona agents and analysis agents each emit a signal → a risk manager sets limits → a portfolio manager aggregates them into a buy, sell or hold decision. — [pyshine](https://pyshine.com/AI-Hedge-Fund-Multi-Agent-Investment-System/); [themenonlab](https://themenonlab.blog/blog/ai-hedge-fund-multi-agent)
- Agent Market Arena tests four agent designs: InvestorAgent (single-agent baseline), TradeAgent and HedgeFundAgent (different risk styles), and DeepFundAgent (memory-based reasoning). — [emergentmind](https://www.emergentmind.com/papers/2510.11695)
- Alpha Arena setup: every model got the same input and a $10k account, traded autonomously, and was sent new market data at fixed intervals (S1: crypto perpetuals on Hyperliquid; S1.5: US stock tokens on trade.xyz). — [bitcoinethereumnews](https://bitcoinethereumnews.com/tech/grok-4-20-leads-alpha-arena-season-1-5-with-22-38-return-on-trade-xyz/); [gncrypto](https://www.gncrypto.news/news/qwen-wins-alpha-arena-season-1-with-22-percent-returns/)
  - A practitioner write-up describes system-prompt engineering in the Alpha Arena style for its own bot. — [Medium/kojott](https://medium.com/@kojott/teaching-an-ai-to-trade-system-prompt-engineering-and-performance-monitoring-9d55258cca06)
- Claude Code pattern: a scheduled routine or cron run where Claude researches → trades on Alpaca paper → writes a journal entry. Guides stress "always start with paper". — [MindStudio](https://www.mindstudio.ai/blog/build-ai-trading-agent-claude-code-alpaca); [MindStudio routines](https://www.mindstudio.ai/blog/how-to-build-ai-trading-agent-claude-code-routines)
- Guardrail pattern: the model's decision passes through "a hard risk layer the model can't override". — [mejba.me](https://www.mejba.me/blog/claude-ai-automate-stock-trading)
  - MCP listings warn the server can place real trades, so users should review each proposed trade before approving it. — [playbooks](https://playbooks.com/mcp/tedlikeskix-alpaca-trading)
- One open PR in a small repo adds slippage modelling and "offline point-in-time LLM signal eval". This shows practitioners retrofitting cost and look-ahead controls. — [GitHub biswajeetdev/ai-trader PR #2](https://github.com/biswajeetdev/ai-trader/pull/2)

### Inferences
These points are assembled from the patterns above and are not quoted from one source.
- Typical repo layout:
  - `agents/`: one prompt or module per role
  - `dataflows/` or `tools/`: yfinance, Finnhub, Alpha Vantage, Reddit or news APIs
  - `graph.py`: orchestration
  - `backtester.py`
  - `config`: LLM provider and model, tickers, risk limits
  - `.env`: API keys
  - a broker adapter, usually alpaca-py
- Representative prompt contract:
  - The system prompt sets the role ("You are a risk-averse portfolio manager…") and the constraints (maximum position % and leverage, allowed tickers, no shorting).
  - It supplies the data snapshot plus current positions and cash.
  - It demands a strict JSON schema, for example `{"ticker","action":"BUY|SELL|HOLD","quantity","confidence","stop_loss","reasoning"}`.
  - Code then validates the schema, clips sizes to limits, checks buying power and market hours, logs the rationale, and only then calls `submit_order`.
- Common extra guardrails:
  - kill switch or daily loss limit
  - maximum orders per day, to stop the overtrading Alpha Arena exposed
  - whitelist of symbols
  - paper or live flag in the environment
  - human approval for live orders
  - trade journal for review

### Gaps
- I could not read the actual prompt files in TradingAgents or ai-hedge-fund, or nof1's published system prompt, so the example prompt contract is a synthesis, not a quote.

## 3. Benchmarks and live competitions: how did Claude rank?

### Takeaway
Across live competitions from 2025-2026, most frontier models lost money or trailed buy-and-hold. Claude has never won.
- In Alpha Arena Season 1 (crypto, Oct-Nov 2025), Claude Sonnet 4.5 placed about 3rd of 6 but still lost roughly 30-42%. Chinese models Qwen3 Max (+22%) and DeepSeek were the only profitable entrants.
- In Season 1.5 (US stocks, Nov-Dec 2025), Claude Sonnet 4.5 was among the worst, at about -32% to -35%, while a mystery Grok 4.20 won.
- In HKU's live FX test (Apr-Jul 2026), Claude again recorded "substantial losses".
- Academic benchmarks (StockBench, FINSABER) find that most agents fail to beat buy-and-hold, especially in down markets.
- Agent Market Arena finds that agent design matters more than which model is used.

### Cited Findings
**Alpha Arena (Nof1), Season 1: 18 Oct-3 Nov 2025**
- Six models, $10k real money each, trading crypto perpetuals.
- Final balances:

  | Place | Model | Final balance | Return |
  |---|---|---|---|
  | 1 | Qwen3 Max | $12,231 | about +22% |
  | 2 | DeepSeek (V3.1) | $10,489 | about +5% |
  | 3 | Claude Sonnet 4.5 | $5,799 | about -42% |
  | Last | GPT-5 | $4,126 | about -59% |

  — [iweaver](https://www.iweaver.ai/blog/alpha-arena-ai-trading-season-1-results/); [gncrypto](https://www.gncrypto.news/news/qwen-wins-alpha-arena-season-1-with-22-percent-returns/); [SCMP](https://www.scmp.com/tech/tech-trends/article/3331425/alibabas-ai-model-outperforms-us-rivals-crypto-trading-showdown); [forklog](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/)
- Conflict: other coverage gives Claude about -30.8%, not -42%. RootData says "all four major [US] models incurred losses exceeding 30%". — [RootData](https://www.rootdata.com/news/412456)
- Gemini 2.5 Pro and GPT-5 were reported down more than 60% mid-contest. — [iweaver live](https://www.iweaver.ai/blog/alpha-arena-ai-trader-showdown/)
- Claude ran a "100% long book… without hedging or stop-loss discipline". Nof1's founder described a clear bullish bias. — [buildix](https://www.buildix.trade/blog/nof1-alpha-arena-lessons-ai-trading-byok-strategy-advisor-2026); [upscale.trade](https://upscale.trade/blog/ai-trading-alpha-arena)
- Chinese models outperformed Western models. — [bitcoin.com](https://news.bitcoin.com/alpha-arena-ai-trading-experiment-sees-china-outperform-western-models-so-far/)

**Alpha Arena, Season 1.5: about Nov-3 Dec 2025**
- Eight models traded US stock tokens (TSLA, NVDA, MSFT, AMZN, Nasdaq-100) on trade.xyz across four parallel competition modes, with "full autonomy".
- The winner was a "Mystery Model", later revealed as Grok 4.20, at +12.11% aggregate return (about $4,844 profit across the modes). — [gncrypto](https://www.gncrypto.news/news/mystery-model-alpha-arena-season-1-5-winner/); [aihola](https://aihola.com/article/grok-wins-alpha-arena-trading); [aibase](https://news.aibase.com/news/23442)
- One summary gives GPT-5.1 at -3.4% and Gemini 3.0 at -5.7%. Forklog ranks GPT-5.1 2nd and Gemini 3 3rd. — [aibase](https://news.aibase.com/news/23442); [forklog](https://forklog.com/en/ai-model-grok-4-2-triumphs-in-trading-tournament/)
- Leaderboard snapshots in early December show different numbers:

  | Model | ~6 Dec | 9 Dec |
  |---|---|---|
  | Grok 4.20 | +22.38% | 22.27% |
  | GPT-5.1 | -2.29% | not given |
  | Gemini 3 Pro | -25.74% | not given |
  | Claude Sonnet 4.5 | -35.08% | -32.44% |
  | Grok 4 | -53.39% | not given |

  Another update said every model except Grok 4.20 was at a loss. — [bitcoinethereumnews](https://bitcoinethereumnews.com/tech/grok-4-20-leads-alpha-arena-season-1-5-with-22-38-return-on-trade-xyz/); [bitget](https://www.bitget.com/news/detail/12560605099629); [weex](https://www.weex.com/news/detail/alpha-arena-15-season-update-grok-420-maintains-lead-all-other-ai-models-remain-at-a-loss-262786)
- One headline said "all eight major models post losses in overtrading frenzy". — [BigGo Finance](https://finance.biggo.com/news/5BSX_Z0BaoGGrU-ID27J)

**Alpha Arena Season 2**
- As of 6 Aug 2026 there was no public Season 2 roster or results. The nof1.ai leaderboard is an archive whose equity series ends on 12 Dec 2025. — [traderank.ai](https://www.traderank.ai/blog/alpha-arena-alternatives-2026)

**StockBench (arXiv 2510.02209, Oct 2025)**
- Contamination-free benchmark: daily trading of DJIA large caps over several months in 2025, using prices, fundamentals and news.
- Models tested: GPT-5, Claude-4, Qwen3, Kimi-K2, GLM-4.5 and others.
- Results:
  - "Most agents did not beat a simple buy-and-hold baseline."
  - They struggled in the Jan-Apr 2025 downturn.
  - Most beat the baseline in the rising May-Aug 2025 period, which the authors read as a bullish bias.
- No transaction costs or slippage were modelled. — [arXiv abs](https://arxiv.org/abs/2510.02209v1); [liner review](https://liner.com/ko/review/stockbench-can-llm-agents-trade-stocks-profitably-in-realworld-markets)

**Agent Market Arena / "When Agents Trade" (arXiv 2510.11695, Oct 2025)**
- A live, lifelong benchmark covering crypto and stocks, running for about two months at writing.
- Agents "can trade profitably in real-time, often outperforming simple Buy & Hold".
- "Agent frameworks display markedly distinct behavioral patterns… whereas model backbones contribute less to outcome variation."
- Best pairings included TradeAgent with Gemini-2.0-flash. DeepFundAgent returned +8.61% cumulative on TSLA and +9.45% on BMRN. — [emergentmind](https://www.emergentmind.com/papers/2510.11695); [themoonlight](https://www.themoonlight.io/en/review/when-agents-trade-live-multi-market-trading-benchmark-for-llm-agents)

**HKU Business School "Agentic Trader": live FX, ten models, from April 2026 (press release 14 Jul 2026)**
- Kimi K2.5 managed risk best and had the strongest six-week return. Other HKU pages instead name Qwen as the leader, at nearly +10%.
- Gemini 3.1 Pro Preview and DeepSeek V3.2 used high leverage and had larger drawdowns.
- GPT-5.4 kept exposure low.
- MiniMax and Claude "recorded more substantial losses". — [HKU press release](https://www.hku.hk/press/press-releases/detail/29241.html); [HKUBS report](https://www.hkubs.hku.hk/aimodelrankings_en/report/En_Agentic%20Trader%20Short%20Report.pdf); [HKU LEAD](https://lead.hku.hk/en/article/2026/07/testing-ai-in-the-real-world-hku-business-school-released-ai-agents-trading-performance/)

**Third-party crypto arenas (2026)**
- TradeRank reports Gemini leading average return at 2.89% across 9 seasons, with GPT and Claude weaker. — [traderank compare, Sep 2026](https://www.traderank.ai/compare/claude-vs-gpt-vs-grok-vs-gemini-for-trading)
- Another Claude vs GPT vs Grok live comparison. — [strategyarena](https://strategyarena.io/en/blog/quelle-ia-utiliser-pour-trader)

**Production fleets**
- A six-month, population-scale study of LLM trading agents in production (arXiv 2609.05663, 2026) exists. I could not read its findings. — [arXiv 2609.05663](https://arxiv.org/pdf/2609.05663)

### Inferences
- Claude's record is consistent across sources: a long-only, bullish-biased style that loses heavily in volatile or falling markets. It placed mid-pack among losers in Alpha Arena S1, near the bottom in S1.5, and among the losers at HKU.
- Rankings flip between seasons. Qwen and DeepSeek won S1, Grok 4.20 won S1.5, and Kimi or Qwen led HKU FX. With two-to-six-week windows and roughly one account per model, results are dominated by noise and leverage choices. They are not reliable evidence of model skill.
- The AMA finding that agent design and risk style matter more than the model fits this.

### Gaps
- Exact Alpha Arena S1 finals for Gemini 2.5 Pro and Grok 4: commonly cited at about -57% and about -45%, but not confirmed here.
- Claude's specific StockBench metrics (return, Sortino, drawdown) were not retrieved.
- I found no InvestorBench or FinBen trading results in search. FinBen is mainly a broad financial NLP benchmark, and InvestorBench is a backtest-based investing benchmark; neither was verified here.
- I found no live result for Claude Opus 4.x or newer models; competitions mostly used Sonnet 4.5.

## 4. Academic findings: look-ahead bias, overfitting, survival after costs

### Takeaway
The literature is increasingly sceptical. Backtested LLM "alpha" is heavily inflated by memorisation. "Profit Mirage" finds Sharpe ratios drop about 51-62% after the model's knowledge cutoff. Over long horizons and broad universes, the advantages largely disappear (FINSABER). Many headline studies also ignore transaction costs and slippage.

### Cited Findings
- **Profit Mirage (arXiv 2510.07920):** audits five LLM trading-agent frameworks and finds about 51-62% Sharpe decay past the model's knowledge cutoff. "Dazzling back-tested returns evaporate once the model's knowledge window ends." — cited in [HindsightBench arXiv 2607.18867](https://arxiv.org/html/2607.18867)
- **Look-Ahead-Bench (arXiv 2601.13770, Jan 2026):** measures look-ahead bias through alpha decay across regimes. Standard LLMs such as Llama 3.1 and DeepSeek 3.2 show significant look-ahead bias; point-in-time models show less. — [alphaxiv](https://www.alphaxiv.org/abs/2601.13770)
- **"Evaluating LLMs in Finance Requires Explicit Bias Consideration" (arXiv 2602.14233):** defines "time travel" as a model backtested on dates before its training cutoff drawing on knowledge of later events, and flags retrieval-based leakage as a second source. — [arXiv 2602.14233](https://arxiv.org/pdf/2602.14233)
- **HindsightBench (arXiv 2607.18867, Jul 2026):** a black-box audit protocol for "parametric hindsight" in time-indexed LLM decisions. — [arXiv](https://arxiv.org/html/2607.18867)
- **FINSABER (Li, Kim, Cucuringu, Ma; arXiv 2505.07078; v5 Feb 2026):**
  - Tests LLM timing strategies over more than 20 years and more than 100 stocks.
  - The advantages reported in earlier studies "shrink considerably" over longer horizons and broader universes.
  - LLM strategies are too conservative in bull markets, trailing passive, and too aggressive in bear markets, taking large losses.
  - The authors recommend regime-aware risk management over added architectural complexity.

  — [arXiv v5](https://arxiv.org/html/2505.07078v5); [arXiv abs](https://arxiv.org/abs/2505.07078)
- **StockBench** does not model trading costs, slippage or liquidity. — [liner review](https://liner.com/ko/review/stockbench-can-llm-agents-trade-stocks-profitably-in-realworld-markets)
- **Practitioner view:** "LLM Trading Strategies: Why Real Backtests Are Worse" (Jul 2026). — [Jiri Pik](https://jiripik.com/2026/07/11/llm-designing-trading-strategies/)
  - Look-ahead bias makes broken bots "look like holy grails". — [DataDrivenInvestor](https://datadriveninvestor.com/articles/backtesting-lies-how-look-ahead-bias-makes-broken-trading-bots-look-like-holy-grails)
- **Mitigations recommended across sources:**
  - Evaluate only on dates after the model's training cutoff; live or forward testing is the gold standard, as in AI-Trader, AMA and StockBench.
  - Use point-in-time data.
  - Anonymise tickers and dates.
  - Model slippage and fees.

  — [HindsightBench](https://arxiv.org/html/2607.18867); [hyper.ai AI-Trader](https://hyper.ai/en/papers/2512.10971)
- **Live trading costs:** Alpha Arena S1.5 coverage attributes losses partly to overtrading. Frequent trades on leveraged perpetuals pay fees and funding that erode returns. — [BigGo Finance](https://finance.biggo.com/news/5BSX_Z0BaoGGrU-ID27J)

### Inferences
- Any backtest of TradingAgents, ai-hedge-fund or similar that covers a period before the LLM's cutoff should be treated as an upper bound, not evidence of edge.
- The only credible evidence comes from forward or live tests. Those mostly show losses or results near buy-and-hold before costs, so no robust evidence was found that LLM alpha survives costs.

### Gaps
- I could not confirm the original arXiv ID or details of "The Memorization Problem" paper (LLMs recall pre-cutoff financial data even when told not to).
- I found no rigorous study isolating after-cost alpha for LLM agents over long live periods.

## 5. Running costs: API tokens and data

### Takeaway
Claude API list prices are roughly $3/$15 per million input/output tokens for Sonnet 4.6, $5/$25 for current Opus and $1/$5 for Haiku 4.5. The Batch API costs about half and suits once-a-day runs. My estimate, assembled from those prices: a daily multi-agent run over a handful of tickers costs single-digit dollars per day on Sonnet, while an Alpha-Arena-style loop every few minutes costs tens of dollars per day. Market data can be free (Alpaca basic or IEX, yfinance) or a paid subscription.

### Cited Findings
- Sonnet 4.6 costs $3 per million input tokens and $15 per million output. — [finout](https://finout.io/blog/anthropic-api-pricing); [pricepertoken](https://pricepertoken.com/pricing-page/model/anthropic-claude-sonnet-4.6)
- Opus 4.6 and later cost $5 / $25. Legacy Opus 4 / 4.1 cost $15 / $75. — [metacto](https://metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration); [doit](https://www.doit.com/blog/anthropic-api-pricing)
- Haiku 4.5 costs $1 / $5 (one source says $0.80 / $4). — [finout](https://finout.io/blog/anthropic-api-pricing)
- Batch processing is about 50% off, for example Sonnet 4.6 at $1.50 / $7.50. — [finout](https://finout.io/blog/anthropic-api-pricing)
- One unconfirmed source lists "Sonnet 5" at $2 / $10. Verify on Anthropic's pricing page. — [pasqualepillitteri](https://pasqualepillitteri.it/en/news/13165/claude-anthropic-complete-guide-models-pricing)
- Alpaca paper trading is free with a simulated $100K account. The MCP server is open source. — [Alpaca MCP](https://alpaca.markets/mcp-server)

### Inferences
These are my own estimates from list prices, not sourced numbers.
- **TradingAgents-style daily run** (about 10-15 LLM calls per ticker, about 150-250k input and 15-25k output tokens per ticker):
  - about $0.70-$1.10 per ticker per day on Sonnet 4.6
  - so about $7-11 per day for 10 tickers, or about $150-240 per month over 21 trading days
  - about half that via Batch or prompt caching
  - about 3x less on Haiku
- **Alpha-Arena-style loop** (a call every 2-3 minutes, 24/7 crypto, about 10k input tokens per call): about 500-700 calls a day, or 5-7M input tokens. That is about $15-25 per day on Sonnet before output tokens, and about $25-40 on Opus.
- **Claude Code on a subscription plan** (Pro/Max) can make a once-a-day routine roughly fixed-cost instead of per-token, within plan usage limits.

### Gaps
- I did not retrieve Anthropic's official pricing page or Alpaca's market-data pricing page. Alpaca's paid "Algo Trader Plus" tier is commonly cited at about $99/month but was not verified.
- I found no other data vendors' prices (Polygon, Financial Modeling Prep, Finnhub, news APIs).
- I found no published per-run token measurements for TradingAgents or ai-hedge-fund.
