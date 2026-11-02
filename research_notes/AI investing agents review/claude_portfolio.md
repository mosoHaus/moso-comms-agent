# "Claude Portfolio" and similar "I gave an AI $X to trade" experiments (as of Nov 2026)

Research note: in this session WebFetch was blocked for every host tried (explainx.ai, joinautopilot.com, instagram.com, ai-street.co, financemagnates.com, finance.yahoo.com), and GitHub API access to third-party repos was not enabled. Everything below comes from search-engine snippets and summaries, not full-page reads. Treat details that appear in only one source as lower confidence.

## 1. Who runs "Claude Portfolio"? Money, start date, assets

### Takeaway
"The Claude Portfolio" (Instagram @theclaudeportfolio, X @theaiportfolios) is not Anthropic's. AI Finance Labs runs it. That outfit was founded by University of Florida finance professor Alejandro Lopez-Lira, and it publishes the portfolio as a copy-tradable strategy on the Autopilot app. It started on March 3, 2026 with a $50,000 account and holds US equities picked from the Russell 1000.

### Cited Findings
- Instagram handle: @theclaudeportfolio. The bio says it is not affiliated with Anthropic and calls itself a public project to see which LLM outperforms the market. The bio also cites "$150M invested via Grok, Chat, & Claude." — [Instagram](https://www.instagram.com/theclaudeportfolio/)
- X handle: @theaiportfolios, display name "The Claude Portfolio." It cites "$200M invested alongside Grok, Chat, & Claude" on Autopilot and says viewing the current weights is always free. — [X @theaiportfolios](https://x.com/theaiportfolios?lang=en)
- Launch post: "The Claude Autonomous Agents have officially arrived. So we're setting them up with a brand new $50,000 portfolio to see how well they do at investing in stocks. Can they outperform Buffett?" — [X status 2039006300441620782](https://x.com/theaiportfolios/status/2039006300441620782)
- Start date March 3, 2026, $50,000 account. — [explainx.ai](https://explainx.ai/blog/claude-portfolio-autopilot-ai-trading-experiment-august-2026)
- Operator: AI Finance Labs, founded by Alejandro Lopez-Lira, a University of Florida finance professor. The same team runs ChatGPT, Grok and DeepSeek portfolios, seven AI portfolios in all. — [Finance Magnates](https://www.financemagnates.com/forex/retail-investors-put-27-million-into-claude-trading-portfolio-after-19-gain/); [TradingView mirror](https://www.tradingview.com/news/financemagnates:7f04e00bf094b:0-retail-investors-put-27-million-into-claude-trading-portfolio-after-19-gain/); [FXBrokerTrust](https://www.fxbrokertrust.com/insights/claude-portfolio-gains-19-draws-27m-in-retail-copytrading-funds)
- Lopez-Lira is a UF Warrington faculty member and an academic researcher on LLMs and stock prediction (book, papers). — [UF Warrington directory](https://warrington.ufl.edu/directory/jose-alejandro-lopez-lira-y-ramirez/); [UF news on book](https://warrington.ufl.edu/news/market-speculators-get-an-edge-through-finance-professors-new-book/); [X @alejandroll10](https://x.com/alejandroll10)
- Universe: Russell 1000 stocks, which means US large and mid caps. Final portfolio of 15 positions. — [X @CodeByPoonam summarising the launch thread](https://x.com/CodeByPoonam/status/2039048654368227408?lang=en)
- Example holdings coverage: in April 2026 the Motley Fool wrote about the Claude agent buying "2 trillion-dollar AI stocks" before the Iran ceasefire. — [Motley Fool](https://www.fool.com/investing/2026/04/13/a-claude-agent-bought-these-2-trillion-dollar-arti/)
- Copied money: about $27M copying the Claude portfolio (Aug 2026). One summary says the Autopilot page showed "$49.5 million currently invested." Across all seven AI portfolios, nearly 52,000 investors had allocated about $200M by July. — [Finance Magnates](https://www.financemagnates.com/forex/retail-investors-put-27-million-into-claude-trading-portfolio-after-19-gain/); [AI Street](https://www.ai-street.co/p/how-ai-runs-200-million-in-portfolios); [Autopilot landing page](https://www.joinautopilot.com/landing/5/950048)
- The same group earlier ran a "World War III portfolio" and a Grok portfolio on Autopilot. Autopilot's co-founder said users increasingly want to copy AI-run portfolios. (One source credits a "Wharton professor." That conflicts with the UF affiliation in the other sources and may be an error.) — [MarketScreener](https://ae.marketscreener.com/news/can-chatgpt-and-grok-beat-the-market-ce7e5cdfd081fe24); [Business Insider JP](https://www.businessinsider.jp/article/2607-best-ai-for-trading-stocks-deepseek-claude-chatgpt-grok/)

### Inferences
- The copied-money figures disagree ($150M vs $200M across all AI portfolios, $27M vs $49.5M for Claude). The likely reason is that they are snapshots taken at different times. All of them come from the operator or Autopilot.
- @pelositracker, Autopilot's flagship congressional-trade account, promoted the launch ([X](https://x.com/pelositracker/status/2039008637113528569)). That fits the Claude Portfolio being part of Autopilot's marketing ecosystem rather than a standalone hobby project. I did not confirm Autopilot's ownership of @pelositracker.
- No standalone newsletter or website was found. The "linked site" is in effect the Autopilot portfolio page.

### Gaps
- The full current holdings list and the exact asset mix (any ETFs or cash) could not be read because the Autopilot page was unreachable.
- No TikTok, YouTube or Substack presence was confirmed for this account.
- No evidence that it holds crypto. The universe described is Russell 1000 only.

## 2. Setup: broker, automation, Claude product, scheduling

### Takeaway
The operator says this is a multi-agent pipeline built with Claude Code (Opus 4.6) that screens stocks, debates them and picks 15 positions, rebalanced daily, with results posted at 5PM. Execution and copying happen through Autopilot. The marketing claim of "zero human override" conflicts with press reports that humans set the strategy and risk rules and control the process.

### Cited Findings
- Pipeline as described in the launch-thread summary: screen every Russell 1000 stock → top 50 go forward → 30 agents run in parallel (15 argue buy, 15 argue sell) → 15 more agents model bull, base and bear scenarios with price targets → an "Agent of Agents" picks 15 final positions → mandate is to beat SPY, with no sector above 35% → "zero human approval needed" → rebalances daily → results at 5PM every day. — [X @CodeByPoonam](https://x.com/CodeByPoonam/status/2039048654368227408?lang=en)
- Agents download and analyse financials, news and analyst data to score stocks, and run internal bull/bear debates before building probability-weighted models. — [Linas Beliūnas fintech newsletter](https://linas.substack.com/p/weeklyfintechpulse393); [DEV Community](https://dev.to/o96a/claude-is-running-a-50k-portfolio-with-zero-human-override-the-implications-go-beyond-finance-440)
- Product and model: "a Claude Code agent running Opus 4.6," given a single instruction, operating "under human-set rules." The same write-up says "Claude manages it" is "more complicated than it sounds," that the autonomy claim is "partially true," and that the operator has acknowledged this. — [explainx.ai](https://explainx.ai/blog/claude-portfolio-autopilot-ai-trading-experiment-august-2026)
- Conflicting framing: Finance Magnates reports that Claude "does not manage the portfolio independently. It is used for research and to generate investment ideas, while Lopez-Lira and his team set the strategy and risk parameters and control the entire investment process." — [Finance Magnates](https://www.financemagnates.com/forex/retail-investors-put-27-million-into-claude-trading-portfolio-after-19-gain/)
- Distribution: followers copy the trades through Autopilot, a third-party copy-trading app that charges a $99 annual subscription. Autopilot's most-copied portfolio is the Pelosi tracker, and one review notes about a 2-week average delay on that one. — [Business Insider JP / MarketScreener summary](https://ae.marketscreener.com/news/can-chatgpt-and-grok-beat-the-market-ce7e5cdfd081fe24); [The College Investor review](https://thecollegeinvestor.com/59796/autopilot-review/); [CoolCuration review](https://coolcuration.com/autopilot-app-review-uk)
- A Chinese-language X article analyses the Claude Portfolio's "quant engine and stock-selection logic." — [X @polymaster article](https://x.com/polymaster/article/2086263653771473079)

### Inferences
- The likely architecture is a scheduled (daily) Claude Code / Agent SDK run that fans out subagents, produces target weights, and then has the portfolio rebalanced on Autopilot, which mirrors the weights into followers' linked brokerage accounts. I found no source naming the broker that holds the operator's own $50K account, or saying whether orders go out by API or by hand.
- The honest reading of the "who trades" question: Claude generates the picks and weights inside rules the humans wrote (universe, 15 names, 35% sector cap, daily cadence). Humans keep control of the process. "Zero human override" is marketing language.

### Gaps
- The broker for the master account, the order-execution method, and the cron or scheduler details are not published in any source found.
- Whether Autopilot followers' trades lag the master portfolio, and by how much. Lag is documented for the Pelosi portfolio but not for the Claude one.

## 3. Prompts, rules, data sources

### Takeaway
No full system prompt is published. The publicly stated rules are: Russell 1000 universe, top-50 shortlist, 15 final positions, no sector above 35%, beat SPY, daily rebalance. The inputs are financials, news and analyst data.

### Cited Findings
- Rules: beat SPY, no sector above 35%, 15 positions, daily rebalance. — [X @CodeByPoonam](https://x.com/CodeByPoonam/status/2039048654368227408?lang=en)
- Inputs: financials, news, analyst data. — [Linas newsletter](https://linas.substack.com/p/weeklyfintechpulse393)
- Single instruction to the agent, plus human-set rules. — [explainx.ai](https://explainx.ai/blog/claude-portfolio-autopilot-ai-trading-experiment-august-2026)

### Inferences
- A replicable approximation: a Claude Code skill or Agent SDK script with a fixed universe, structured bull/bear subagents, a synthesis agent that outputs JSON weights, and hard-coded risk constraints validated in code before any order is placed.

### Gaps
- No published prompt text, data vendor (for example FMP, Polygon or EDGAR), or position-sizing or stop-loss rules.

## 4. Code: public GitHub repo?

### Takeaway
The Claude Portfolio has no public repo. Open-source analogues exist, mostly running Claude Code with the Alpaca MCP server, and nearly all of them are paper-trading only.

### Cited Findings
- No repo for Claude Portfolio was found in any source.
- Alpaca's official MCP server lets an LLM trade stocks, ETFs, crypto and options in plain English. Most Claude Code trading projects connect to it. — [alpacahq/alpaca-mcp-server](https://github.com/alpacahq/alpaca-mcp-server)
- satyamdas03/alpaca-trading-agent: "24/7 Autonomous AI Trading Agent — Claude Code + Alpaca MCP + Gmail notifications," fundamentals-driven swing trading, paper trading only. — [GitHub](https://github.com/satyamdas03/alpaca-trading-agent)
- Guide: building a 24/7 trading agent with Claude Code Routines (scheduled runs). — [MindStudio](https://www.mindstudio.ai/blog/how-to-build-ai-trading-agent-claude-code-routines)
- Alzarak/trading-bot: a Claude Code plugin for day trading on the Alpaca API. — [GitHub](https://github.com/Alzarak/trading-bot)
- himanshu2394i/Alpaca: Claude judges options entries, deterministic risk gates have the final veto, paper/hackathon only. — [GitHub](https://github.com/himanshu2394i/Alpaca)
- tatsuyawwp/ai-trading-bot-experiment: AI-built paper bots on Alpaca, documented honestly with "a negative-expectancy result" and "no track record of profitability." — [GitHub](https://github.com/tatsuyawwp/ai-trading-bot-experiment)
- AlexTSung/ai-trading-agent: paper only, with Robinhood real money listed as a future phase. — [GitHub](https://github.com/AlexTSung/ai-trading-agent)
- OpenTrade-Agent: a macOS app that routes orders through a Robinhood MCP, under a source-available Elastic License 2.0. — [GitHub wiki](https://github.com/MariusOTB/OpenTrade-Agent/wiki)
- Hummingbot "Condor": an open-source harness for trading agents (crypto). Not related to Condor Capital. — [Hummingbot](https://hummingbot.org/blog/introducing-condor-the-open-source-harness-for-trading-agents/)
- Nathan Smith's ChatGPT micro-cap repo (LuckyOne7777/ChatGPT-Micro-Cap-Experiment) keeps trade logs, prompts, daily CSVs of PnL and equity, and benchmark comparisons. Forks exist, for example ranjith-gampa. — [Mean Match summary](https://meanmatch.substack.com/p/luckyone7777chatgpt-micro-cap-experiment); [fork](https://github.com/ranjith-gampa/ChatGPT-Micro-Cap-Experiment)

### Inferences
- Common pattern for replication: Claude Code or the Agent SDK, the Alpaca MCP (paper account first), a scheduler (Claude Code routines, cron or GitHub Actions), deterministic risk checks in code, and notifications by email or Slack.

### Gaps
- Could not read repo internals because GitHub API access was not enabled this session.

## 5. Performance and verification

### Takeaway
The Claude Portfolio reports +19.04% vs +12.24% for the S&P 500 from March 3 to early August 2026, about five months. It is self-reported, not audited, and short. The same operator's other AI portfolios report bigger numbers, which also fit cherry-picking of the best-performing "AI" brands.

### Cited Findings
- +19.04% since March 3 vs +12.24% for the S&P 500 (August update). The account says every position and trade is public. — [X @theaiportfolios](https://x.com/theaiportfolios?lang=en); [Finance Magnates](https://www.financemagnates.com/forex/retail-investors-put-27-million-into-claude-trading-portfolio-after-19-gain/)
- Viral amplification: "Five months later it's up 19% versus 12% for the S&P. $27 million is now copying." — [X @VaibhavSisinty](https://x.com/VaibhavSisinty/status/2084950050103603664)
- Sister portfolios: the DeepSeek portfolio reported +76% (May) vs +27% for the S&P over the same period. A later interview gives +56% over a year vs +16% for the S&P. ChatGPT beat the S&P but trailed Grok and DeepSeek. DeepSeek was also beating Claude, though Claude had a shorter history. — [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/ai-model-best-stock-trader-091501419.html)
- Earlier figures: ChatGPT portfolio +78% since launch, Grok +54%. — [Business Insider JP](https://www.businessinsider.jp/article/2607-best-ai-for-trading-stocks-deepseek-claude-chatgpt-grok/)
- A review of Autopilot found headline returns "shrank considerably" once trade timing and delays were counted. — [CoolCuration](https://coolcuration.com/autopilot-app-review-uk)
- The search summaries flagged that no independent audit was found. — [explainx.ai](https://explainx.ai/blog/claude-portfolio-autopilot-ai-trading-experiment-august-2026)
- A separate report surfaced in search (not verified) that Claude Opus 4.6 trailed the S&P 500 across three runs. — [mentioned via AAII / search summary](https://www.aaii.com/investingideas/article/551045-brokerage-ai-agents-arent-ready-for-long-term-investors)

### Inferences
- About 7 percentage points of outperformance in five months, with 15 concentrated large-cap names during an AI-led rally, is consistent with simple tech/AI overweighting (beta and sector tilt) rather than proven skill.
- Survivorship and multiple-testing: the operator runs 7 AI portfolios. Whichever one is ahead gets the headline, and losing variants can be quietly de-emphasised.
- The verification standard is Autopilot's displayed track record plus posts. No broker statements, no GIPS-style audit, and no risk-adjusted metrics (Sharpe, drawdown) were found.

### Gaps
- Performance from August to November 2026 not found.
- Drawdown, turnover and transaction-cost data not found.

## 6. Monetisation and red flags

### Takeaway
The money is made through the Autopilot copy-trading funnel, at $99/yr per subscriber according to reviews. Viewing the weights is free, but auto-mirroring needs Autopilot. No course or paid newsletter from the Claude Portfolio itself was found.

### Cited Findings
- "Viewing the current weights is always free." The Autopilot page invites people to copy. — [X @theaiportfolios](https://x.com/theaiportfolios?lang=en); [Autopilot landing](https://www.joinautopilot.com/landing/5/950048)
- Autopilot costs $99/year. It also hosts the Pelosi/"Pelosi+" congressional portfolios. Its co-founder cited more than $55M copying congressional trades. — [MarketScreener/BI](https://ae.marketscreener.com/news/can-chatgpt-and-grok-beat-the-market-ce7e5cdfd081fe24); [Yahoo SG](https://sg.news.yahoo.com/traders-invested-55-million-using-193917633.html); [Finviz](https://finviz.com/news/335508/exclusive-from-2-million-to-13-billion-autopilots-focus-on-pelosi-and-other-politicians-is-paying-off)
- One repost of the account's claims carried a "post is from a suspended account" note. — [explainx.ai via search summary](https://explainx.ai/blog/claude-portfolio-autopilot-ai-trading-experiment-august-2026)
- AAII (Oct 2026): brokerage AI agents "aren't ready for long-term investors." Start small and be careful with instructions. — [AAII](https://www.aaii.com/investingideas/article/551045-brokerage-ai-agents-arent-ready-for-long-term-investors)
- Unrelated Gumroad "Claude prompt guide" products show up near searches for this account. These are separate sellers. — [Gumroad](https://moelueker.gumroad.com/l/ClaudePromptGuide)

### Inferences
- Red flags: (1) the name uses the Claude brand without Anthropic involvement; (2) the "zero human override" framing contradicts the operator's own press statements; (3) returns are self-reported over a short window; (4) the AUM numbers are inconsistent; (5) the incentive is to drive Autopilot subscriptions. It is a legitimate public experiment by a credentialed academic, but the marketing overstates autonomy and proof of edge.

### Gaps
- Whether AI Finance Labs gets revenue share from Autopilot is not disclosed in any source found.

## 7. Similar experiments and how they compare

### Takeaway
Most "I gave an AI $X" experiments are tiny, short, and end flat or negative once they run long enough. The best-documented one (Nathan Smith's ChatGPT micro-cap) went viral at +23.8% after four weeks and finished six months at -17% vs +11.7% for the S&P.

### Cited Findings
- **Nathan Smith, ChatGPT micro-cap (Jun 27 to Dec 27, 2025):** $100 of real money, GPT-4o, US micro-caps under $300M, full shares only, weekly picks, stop-losses. Smith executed the trades by hand. Week 4: +23.8% vs Russell 2000 +3.9% and XBI +3.5%. — [Decrypt](https://decrypt.co/332826/high-school-students-chatgpt-trading-bot); [Benzinga](https://www.benzinga.com/markets/equities/25/08/46783783/redditors-100-chatgpt-day-trading-experiment-trounces-two-benchmark-indexes-with-24-returns-here)
- Final (Week 26): $82.88 vs $111.68 for $100 in the S&P 500 over the same window. Max drawdown -50.33% (2025-11-06). Negative Sharpe. — [Substack Week 26](https://nathanbsmith729.substack.com/p/chatgpts-micro-cap-portfolio-week-e93)
- Smith said his value was insight into LLM behaviour with irreversible consequences. Next planned: a new-IPO experiment. — [Substack report](https://nathanbsmith729.substack.com/p/report-and-project-news)
- **Condor Capital Wealth Management:** $500 real money each to Claude, ChatGPT and Gemini agents (plus Qwen, Kimi, Seed), told to maximise intraday gains and end each day in cash. The Claude agent traded via Robinhood. One summary says Claude profited, Gemini roughly broke even, and ChatGPT lost over about 3 days. Others ended in the roughly $500-$800 range. More trading correlated with worse results. — [codedtrip](https://codedtrip.com/en/blog/ai-agents-invest-500-in-stocks); [Bizportal](https://www.bizportal.co.il/capitalmarket/news/article/20044109)
- **nof1 Alpha Arena (crypto, Oct to Nov 2025):** $10K real money per model on Hyperliquid. Claude Sonnet 4.5 was briefly near the top early, and made 38 trades vs 238 for Gemini. Qwen3-Max won Season 1 with +22.32%. More than half the models finished in the red. ChatGPT reportedly lost 63%. nof1 called it exploratory. Season 1.5 was won by Grok 4.20. — [Decrypt](https://decrypt.co/345006/ai-crypto-trading-showdown-deepseek-grok-winning-gemini-implodes); [Benzinga](https://fr.benzinga.com/quote/cryptocurrency/25/11/48651974/chatgpt-lost-63-trying-to-trade-crypto-but-one-china-ai-made-a-healthy-profit); [Forklog S1](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/); [Forklog S1.5](https://forklog.com/en/news/ai-model-grok-4-2-triumphs-in-trading-tournament)
- **Individual Claude experiments:** "I gave Claude ₹5000 to day trade" (Groww, 5x margin, short trades, poor results). — [Substack](https://sganesh17.substack.com/p/i-gave-claude-5000-to-day-trade-and). "I gave Claude Code 100k" on Medium was paper money, one month, mixed, and the author admits it is not trustworthy yet. — [Medium](https://medium.com/@jakenesler/i-gave-claude-code-100k-to-trade-with-in-the-last-month-and-beat-the-market-ece3fd6dcebc). There is also a YouTube video "I Gave Claude Code $10,000 to Trade Stocks" with no verifiable results. — [YouTube](https://www.youtube.com/watch?v=osZBKQV9v3c)
- r/AI_Agents: a developer's 30-day lessons from letting an AI agent manage a live micro-portfolio. — [AI Weekly](https://aiweekly.co/node/2533)
- Related non-trading example: Anthropic's Project Vend, where Claude ran an office shop and lost money. — [PromptHub](https://prompthub.substack.com/p/claude-tried-running-a-vending-machine)

### Inferences
- Pattern: early viral wins regress. Hard-coded risk rules and low turnover help, and Claude's low trade count in Alpha Arena was an advantage. Weekly or daily LLM stock picking has not shown durable alpha in any public, long-running test found.
- Compared with these, the Claude Portfolio is better engineered (multi-agent debate, diversification constraints, large caps) and has a credentialed operator. It is still unaudited and under a year old.

### Gaps
- No verified, long-horizon (12+ month), audited real-money Claude trading track record was found anywhere.
- No relevant r/ClaudeAI or r/algotrading threads surfaced in searches.
