# L.Finesse Humxn

Software engineer. Python primary, JavaScript secondary. These days I point that at AI systems: LangGraph agent orchestration, retrieval pipelines, and multi-provider LLM routing, plus the full-stack product around them.

Most of what I get called for is the same problem. A team bought or built an AI feature, it demoed beautifully, and it does not survive contact with real users. That is rarely a model problem. It is state, retries, fallback, and deciding what the system is allowed to do when it is unsure.

**What I work on**
- Agent orchestration and state management with LangGraph, including real human-in-the-loop interrupts
- Retrieval over public records, where the data decides and the model explains
- Multi-provider LLM routing and graceful degradation
- The boring parts: tests, citations on every number, claims that match the shipped defaults

**Shipped and running**
- **MCGrantz**: grant winnability scored against USASpending award history and IRS 990-PF filings. FastAPI, Postgres, Claude. [Live](https://grants.millennialscreatives.com)
- **MCStanding**: data-broker compliance across 11 regimes with no backend, so regulated data never leaves the browser. React, 304 tests. [Live](https://mcstanding.millennialscreatives.com)
- **HumxnMed**: patient health briefings behind a LangGraph guardrail that routes crisis input out before generation. [Live](https://humxnmed.millennialscreatives.com)
- **MCProof**: Section 508 and security scanning that drafts the VPAT/ACR. [Live](https://mcproof.millennialscreatives.com)

**Open source.** Small, complete, tested tools built on patterns I run in production:

- **[failclosed-guardrail](https://github.com/finessehumxn/failclosed-guardrail)**: a LangGraph safety guardrail that fails closed. Crisis input exits before generation, the human-in-the-loop step is a real interrupt, and CI fails if any crisis case leaves the safety routes. 130 tests.
- **[llm-failover](https://github.com/finessehumxn/llm-failover)**: multi-provider LLM routing with retries, per-provider circuit breakers and a deadline. Falling back never hides a revoked key. Zero required dependencies, 100 tests.
- **[award-odds](https://github.com/finessehumxn/award-odds)**: a CLI that shows who actually won a federal grant program, using public USASpending data. Transparent rules, no LLM in the scoring path.

The product source is private because it is commercial. The design reasoning is public in **[ai-engineering-portfolio](https://github.com/finessehumxn/ai-engineering-portfolio)**. Earlier experiments: [emosafe-ai](https://github.com/finessehumxn/emosafe-ai), [ai-failure-analysis](https://github.com/finessehumxn/ai-failure-analysis).

**Where**
Founder and AI and software engineer at Millennials Creatives.

**Also**
Executive Director of Finesse Our Minds, a youth mental health nonprofit offering free peer support from people who get it. Years of that work taught me the thing I design around: detection is the easy part. What happens in the moments after the signal fires is where systems fail.

[finessehumxn.com/work](https://finessehumxn.com/work) · [LinkedIn](https://linkedin.com/in/lfinesseskills) · finessehumxn@gmail.com
