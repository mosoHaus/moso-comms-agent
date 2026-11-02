# Barebone AI (barebone.ai): AI stock research app

Research note: the agent's network blocked direct page fetches (apps.apple.com, linkup.so, caplight.com), so every finding below comes from search-engine snippets and summaries of the cited pages, not from reading the full pages. Many sources are Barebone's own marketing pages, and they are labelled as such. Researched 2 November 2026.

## 1. Which company/product is it (website, founders, launch, funding)?

### Takeaway
The product exists. It is called "Barebone - AI Finance Research" / "Barebone - AI Stock Research", website barebone.ai, published by Barebone Group Holdings Limited and reported as based in San Francisco. It is a mobile-first AI "investment research agent" for retail investors, and it is clearly the best match for "Barebone AI". No other finance product with a similar name turned up (searches for "barebone.ai" otherwise returned barebone PC hardware, BackboneAI, BareAI and so on). Founders are described but not named. No funding has been disclosed.

### Cited Findings
- Official site title: "Barebone AI — AI Investment Agent & Stock Research App". — [barebone.ai](https://barebone.ai/)
- iOS app ID 6737490098. The listing name appears as both "Barebone - AI Finance Research" and "Barebone - AI Stock Research". — [App Store (US)](https://apps.apple.com/us/app/-/id6737490098); [App Store (HK)](https://apps.apple.com/hk/app/barebone-ai-stock-research/id6737490098?l=en-GB)
- Android app ID `com.briiantam.bareboneai`. — [Google Play](https://play.google.com/store/apps/details?id=com.briiantam.bareboneai&hl=en_US)
- iOS developer: Barebone Group Holdings Limited. Contact emails seen: brian@barebone.ai and team@barebone.ai. — [App Store listing via search](https://apps.apple.com/app/id6737490098); [apppricinglab](https://apppricinglab.com/app/apple/6737490098)
- AppBrain lists the Google Play developer as "Barebone AI", with roughly 10,000+ installs and updates through July 2026. — [AppBrain](https://www.appbrain.com/dev/Barebone+AI/)
- Caplight: private company, HQ San Francisco, founded 2025, described as an "AI-powered mobile platform for investment research, stock analysis, and portfolio monitoring". Funding round information "not publicly available", no known investors. — [Caplight](https://www.caplight.com/company/barebone)
- Founders, according to the company itself: a former Goldman Sachs investment banker and a former Hanson Robotics engineer who worked on Sophia the Robot. The App Store listing says the app was "built by ex-Goldman Sachs bankers". — [Barebone AI Review (company page)](https://barebone.ai/resources/barebone-ai-review); [App Store](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098)
- Hanson Robotics is a Hong Kong company founded in 2007 by David Hanson, best known for the robot Sophia. — [Wikipedia](https://en.wikipedia.org/wiki/Hanson_Robotics)
- Company claim: "Top 10 in Google Play Finance within 60 days of launch". — [barebone.ai review page](https://barebone.ai/resources/barebone-ai-review)
- A Linkup (web-search API vendor) case study dated 22 January 2026 profiles Barebone as a customer. — [Linkup blog](https://www.linkup.so/blog/user-story-barebone-linkup); [Linkup case study](https://www.linkup.so/case-studies/user-story-barebone-linkup)

### Inferences
- The Android package name "briiantam" plus the brian@barebone.ai contact suggests a founder or developer called Brian Tam. A direct search for "Barebone AI Brian Tam" returned nothing, so this is unconfirmed.
- "Holdings Limited" and the Hanson Robotics (Hong Kong) link hint at a Hong Kong or Asia connection, even though Caplight says San Francisco. Unconfirmed.
- An iOS app ID in the 6737xxxxxx range usually means the app was first registered around late 2024. Caplight's "founded 2025" may be the year of the company or public launch. The exact launch date is unconfirmed.
- Early-stage, probably bootstrapped or seed-funded. With no disclosed raise, this is a small team.

### Gaps
- Founders' names, LinkedIn profiles and exact launch date. Crunchbase, LinkedIn and the full App Store page could not be fetched.
- Any funding or investors.
- The Instagram account itself (handle, follower count, post style). No search result surfaced Barebone's Instagram, TikTok or X presence. The "strong, polished Instagram" description from the user could not be verified.

## 2. What it does: features, data sources, AI models, signals, portfolio, trading

### Takeaway
It is an AI chat/agent research app. You ask plain-English questions about stocks and get back synthesised research: fundamentals, technicals, sentiment, news, insider trades, Congress trades and hedge-fund 13F filings. It has a "viral narrative" detection angle drawn from social media. Portfolio connections are read-only. It does not execute trades and says it gives no personal advice. The underlying LLM (Claude, GPT or other) is not disclosed. Linkup supplies web-search grounding.

### Cited Findings
- Listed features: "Live Search • Market Sentiment • Financial Data • Value Investor Mode • Technical Analysis • Industry & Asset Comparisons", plus AI-curated news, stock comparisons and industry trends. — [apppricinglab](https://apppricinglab.com/app/apple/6737490098); [App Store](https://apps.apple.com/app/id6737490098)
- Described as an "agentic AI investment research terminal built for retail investors" and "professional-grade investment research through AI agents". — [appshunter](https://appshunter.io/ios/app/barebone-ai-stock-research/id6737490098)
- "20+ specialized research skills" covering fundamentals, technicals, sentiment, insider and Congress trades, and earnings. — [barebone.ai review page](https://barebone.ai/resources/barebone-ai-review); [mwm.ai](https://mwm.ai/apps/barebone-ai-finance-research/6737490098)
- Tracks Congressional stock trades, corporate insider transactions and hedge-fund 13F filings. Returns a synthesised answer to a plain-English question "in under a minute". — [agent-finder.co](https://agent-finder.co/reviews/barebone-ai)
- Portfolio connections are read-only and encrypted. No trade execution, no personalised investment advice. — [agent-finder.co](https://agent-finder.co/reviews/barebone-ai); [mwm.ai](https://mwm.ai/apps/barebone-ai-finance-research/6737490098)
- Core positioning per Linkup: "a mobile-first investment AI agent that focuses on one thing: detecting emerging, viral narratives early on social media, and turning that into actionable investment research". It aggregates what investors discuss across social channels, communities and news. Examples cited: high-bandwidth memory "weeks ahead of mainstream coverage" and the Sydney Sweeney / American Eagle campaign. — [Linkup case study](https://www.linkup.so/case-studies/user-story-barebone-linkup)
- Data: Barebone runs "its own proprietary systems for large-scale data collection and aggregation" and uses Linkup's search API in the backend to validate information. This serves both the consumer app and Barebone's own internal fund. — [Linkup case study](https://www.linkup.so/case-studies/user-story-barebone-linkup)
- Company claim: "Every figure the AI cites is checked against the underlying financial data before it reaches your screen." — [barebone.ai vs ChatGPT (company page)](https://barebone.ai/compare/barebone-ai-vs-chatgpt)
- Company-acknowledged limits: no trade execution, no desktop terminal. — [barebone.ai review page](https://barebone.ai/resources/barebone-ai-review)

### Inferences
- In practice this is a wrapper around a frontier LLM with financial-data APIs, a web-search API (Linkup) and pre-built prompt "skills" layered on top. The value is convenience and packaging, not proprietary intelligence.
- No buy/sell signal service was found, but "actionable investment research" and the internal fund suggest the outputs lean towards trade ideas.

### Gaps
- Which LLM(s) it uses. No source names Claude, GPT, Gemini or another model.
- Market-data vendor (prices, fundamentals) and how fresh the data is.
- Whether explicit buy/sell ratings or price targets are shown.

## 3. UI/UX and platforms

### Takeaway
Mobile only: iOS and Android, no desktop/web terminal according to the company. It uses a chat/agent interface with a news feed. No detailed screenshot descriptions could be retrieved.

### Cited Findings
- Available on iOS and Android. — [App Store](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098); [Google Play](https://play.google.com/store/apps/details?id=com.briiantam.bareboneai&hl=en_US)
- "No desktop terminal". — [barebone.ai review page](https://barebone.ai/resources/barebone-ai-review)
- Users ask questions in plain English and get a synthesised answer. — [agent-finder.co](https://agent-finder.co/reviews/barebone-ai)
- A user asked for more customisation of the news feed, and the developer replied that it is working on it. — [App Store reviews (via search)](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098?see-all=reviews&platform=iphone)
- A video review exists on Quasa ("Wall Street Research for Everyone"), in English and Spanish versions. Content not retrieved. — [Quasa](https://quasa.io/video/barebone-ai-review-on-quasa-wall-street-research-for-everyone)

### Gaps
- Screenshot or onboarding details, whether a web app exists at barebone.ai, and the iPad version. Full store pages could not be fetched.

## 4. Pricing tiers and free plan

### Takeaway
Free to download, with a limited free tier. Paid tiers are "Plus" and "Pro", sold through App Store / Google Play subscriptions. Prices vary by region and snapshot. US listings show roughly US$15/month (Plus), US$29/month or US$7.99/week (Pro), and annual plans from about US$139 to US$349, with a 7-day trial on the annual plan.

### Cited Findings
- US App Store in-app purchases: Barebone Pro (Monthly) US$29.00; Pro (Weekly) US$7.99; Barebone Plus (Monthly) US$15.00; annual plans listed between US$139 and US$349. — [App Store (US)](https://apps.apple.com/us/app/-/id6737490098)
- Another snapshot: Pro US$29/month or US$209/year, Plus US$15/month. — [App Store](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098)
- Annual plan US$174.99 with a 7-day free trial. — [appshunter / Linkup-related search summary](https://appshunter.io/ios/app/barebone-ai-stock-research/id6737490098)
- Luxembourg store: Pro (Monthly) €35.00. — [App Store (LU)](https://apps.apple.com/lu/app/barebone-ai-finance-research/id6737490098)
- Agent-Finder (August 2026): the website lists no public pricing tiers, which it calls "pricing opacity". — [agent-finder.co](https://agent-finder.co/reviews/barebone-ai)
- Company site: "free to start", with Pro for unlimited research. — [barebone.ai](https://barebone.ai/resources/best-free-stock-research-apps)
- A German comparison (August 2026) rates its mobile AI explanations as only "partially free". — [uamr.de](https://www.uamr.de/?p=28926)

### Inferences
- A weekly US$7.99 plan works out to about US$415/year. This is a common subscription-app tactic, so annual billing is far cheaper. In AUD, Pro monthly is likely around A$45 (not confirmed from the AU store).
- Pro at about US$29/month costs more than ChatGPT Plus or Claude Pro (about US$20/month each).

### Gaps
- Australian App Store prices (AUD). Exactly what the free tier allows (query caps and so on).

## 5. Reviews and sentiment

### Takeaway
Small but mostly positive app-store sentiment: about 4.5 stars from around 82 to 102 ratings on iOS. The company claims 4.8. There are a few negative reviews, including one calling it a "scam". No Reddit, Product Hunt or Trustpilot presence was found. Almost all "best AI investing apps" rankings that feature it are written by Barebone itself (SEO content).

### Cited Findings
- iOS: 4.5/5 from 82 reviews (one snapshot). Another aggregator shows 102 ratings and 40 written reviews, and a Finance top-grossing rank of about #101. — [appshunter](https://appshunter.io/ios/app/barebone-ai-stock-research/id6737490098); [appshunter reviews](https://appshunter.io/ios/app/barebone-ai-stock-research/id6737490098/reviews)
- Company claims 4.8/5 on the App Store. — [barebone.ai review page](https://barebone.ai/resources/barebone-ai-review) (conflicts with the 4.5 aggregator figure)
- Positive reviews: "AI summaries save so much time especially when comparing multiple tickers"; "fundamentals + technical analysis combo works well"; "free account is useful"; "very informative and well built". — [App Store reviews](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098?see-all=reviews&platform=iphone)
- Negative reviews: one called it "functionally great" but "half-baked". One alleged "scam" (single, unverified). — [App Store / appshunter via search](https://appshunter.io/ios/app/barebone-ai-stock-research/id6737490098/reviews)
- Independent review (Agent-Finder, 7/10): "a strong pick for retail investors who want faster research without becoming a spreadsheet analyst", but "unpublished pricing and thin public documentation mean cautious buyers should ask for a trial before committing". — [agent-finder.co](https://agent-finder.co/reviews/barebone-ai)
- A third-party legitimacy check scored it 60/100 ("legitimate, with a few gaps"). — [search summary of app aggregators](https://appshunter.io/ios/app/barebone-ai-stock-research/id6737490098) (exact source page unclear, low confidence)
- The German comparison lists Barebone AI among 2026's leading apps alongside WallStreetZen and Morningstar. — [uamr.de](https://www.uamr.de/?p=28926) (low-authority site)
- barebone.ai publishes many "Best AI investing apps / We tested 10", "vs ChatGPT", "vs TradingView", "vs Robinhood Cortex" and "Yahoo Finance alternatives" pages that rank itself first. — [barebone.ai best AI investing apps](https://barebone.ai/resources/best-ai-investing-apps); [vs TradingView](https://barebone.ai/compare/barebone-ai-vs-tradingview); [vs Robinhood Cortex](https://barebone.ai/compare/barebone-ai-vs-robinhood-cortex)
- Searches found no Reddit threads or Product Hunt listing. — (searches run 2 Nov 2026; negative result)

### Inferences
- A sample of about 100 ratings is too small to judge quality. The self-ranking SEO pages mean many "reviews" found online are the company's own marketing.

### Gaps
- Trustpilot, YouTube creator reviews, X sentiment, and Google Play rating/review counts were not retrieved.

## 6. Red flags: performance claims, disclaimers, licensing, finfluencer tactics

### Takeaway
The main red flag is an unaudited, self-reported "77% returns" claim for Barebone's internal fund, made in a vendor case study. Running an internal fund alongside a consumer research app also raises a potential conflict of interest. The app disclaims advice ("informational tool"). No evidence was found of SEC/FINRA registration or an Australian AFSL. The company's own SEO content ranks itself first in "we tested" lists.

### Cited Findings
- "Barebone's internal fund, powered by these AI agents, is up 77% over the last year". Linkup's headline promotes "77% returns in 2025". — [Linkup case study](https://www.linkup.so/case-studies/user-story-barebone-linkup); [Linkup blog](https://www.linkup.so/blog/user-story-barebone-linkup)
- The same AI systems support "both Barebone's consumer app and their own internal fund operations". — [Linkup case study](https://www.linkup.so/case-studies/user-story-barebone-linkup)
- Disclaimer: the app "is an informational tool and does not provide investment, financial, or legal advice", "not an investment advisory tool", "does not execute trades". The App Store listing notes AI output can contain errors. — [apppricinglab](https://apppricinglab.com/app/apple/6737490098); [App Store](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098)
- No source confirms registration with the SEC, FINRA, ASIC or any other regulator. — (searches run; negative result)
- Background: the SEC has brought "AI washing" enforcement cases against firms that overstate their AI use. — [RegCompliance Watch](https://www.regcompliancewatch.com/sec-enforcement-director-grewal-addresses-ai-washing-cases/)
- The company's marketing pages cite a study finding that 35% of ChatGPT finance answers were wrong or misleading. These pages favour Barebone. — [barebone.ai vs ChatGPT](https://barebone.ai/compare/barebone-ai-vs-chatgpt)
- "Built by ex-Goldman Sachs bankers" is used as a credibility signal. — [App Store](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098)

### Inferences
- The 77% figure covers one year (2025) with no audit, no benchmark comparison, no fund size and no fund name. Treat it as marketing. A 77% single-year return during a strong AI-stock rally says little about skill.
- Weekly subscription pricing, "ex-Goldman" credentials, a self-reported star rating higher than aggregators show, and self-ranking "we tested" articles are typical growth-marketing tactics for consumer fintech. If the Instagram presence is polished and viral, it fits this pattern. That is not evidence of fraud, but it is a reason for scepticism.
- Under Australian law, general information tools with a "general advice" or "not advice" disclaimer often operate without an AFSL. Anything that becomes personalised advice would need one. Barebone appears to sit in the "general information" category.

### Gaps
- Regulatory status in any jurisdiction (no ASIC Professional Register or SEC IAPD check could be completed).
- Details of the internal fund (legal entity, AUM, whether outside investors are involved).

## 7. Is it available in Australia?

### Takeaway
Probably yes. The iOS app appears in multiple regional App Stores (US, HK, Luxembourg) and on Google Play, so an Australian listing is likely, but it was not directly confirmed. ASX coverage is unknown. The smart-money features (Congress trades, 13F, US insider filings) are US-centric.

### Cited Findings
- Listings exist in the US, Hong Kong and Luxembourg App Stores. — [US](https://apps.apple.com/us/app/-/id6737490098); [HK](https://apps.apple.com/hk/app/barebone-ai-stock-research/id6737490098?l=en-GB); [LU](https://apps.apple.com/lu/app/barebone-ai-finance-research/id6737490098)
- No source mentions ASX coverage. — (search run; negative result)

### Inferences
- The core data features (Congress trades, 13F filings, US insider Form 4) only apply to US-listed stocks, so for an Australian investor focused on the ASX the distinctive features add little.

### Gaps
- Confirmation of the AU App Store listing and AUD pricing, and whether ASX tickers are supported. Suggest the user searches "Barebone" in the AU App Store and tests a ticker such as BHP.AX on the free tier, or emails team@barebone.ai.

## 8. Verdict: value over free tools?

### Takeaway
For a non-technical Australian retail investor, Barebone offers modest convenience: one mobile app that bundles US fundamentals, technicals, news sentiment and US "smart money" tracking into plain-English answers. It is not a proven edge. Most of the same research can be done free or more cheaply with ChatGPT/Claude (with web search), Simply Wall St (strong on ASX), Yahoo Finance, TradingView, and free Congress/insider trackers. The free tier is worth a try. Paying about US$29/month (about A$45) is hard to justify, especially for ASX-focused investing, and the 77% fund claim should be ignored.

### Cited Findings
- Independent reviewer: good for "faster research without becoming a spreadsheet analyst", 7/10, ask for a trial. — [agent-finder.co](https://agent-finder.co/reviews/barebone-ai)
- The company itself positions ChatGPT as "better for learning than for market-specific analysis" and claims verified figures and live data as its advantage. — [barebone.ai vs ChatGPT](https://barebone.ai/compare/barebone-ai-vs-chatgpt)
- Pro costs US$29/month. — [App Store (US)](https://apps.apple.com/us/app/-/id6737490098)
- A user found it saves time comparing multiple tickers. — [App Store reviews](https://apps.apple.com/us/app/barebone-ai-stock-research/id6737490098?see-all=reviews&platform=iphone)

### Inferences
- Real but narrow value-add: (1) a ready-made finance "skills" layer, so the user doesn't need to write good prompts; (2) structured US smart-money data (Congress, insider, 13F) in one place; (3) a social-narrative or trend feed. Items 1 and 3 are partly reproducible with Claude or ChatGPT web search. Item 2 is available free on sites such as Quiver Quantitative, OpenInsider and Capitol Trades (not researched here, general knowledge).
- Risks: an unknown underlying model, a small young company with undisclosed funding (continuity risk), possible conflict with the internal fund, US-centric data, and no regulatory status.
- Recommendation for the user: use the free tier only, test it on two or three ASX and US stocks against Simply Wall St or Yahoo Finance and a direct Claude query, avoid weekly plans, and do not treat outputs as advice.

### Gaps
- No hands-on test was possible. No independent accuracy benchmark of Barebone's outputs exists.
