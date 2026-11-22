# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Abay26/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Abay26/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One page that sums up the world's news of Sunday 22 November 2026: the COP31
draft in Antalya drops any fossil-fuel phase-out as the talks run into
overtime; Taiwan bans short selling to halt a market rout; Hong Kong votes
with a record first-hour turnout; Iran plans rolling blackouts as Bahrain
reports an attack; Trump vows a 10% cap on credit-card rates; the suspect
liquor toll reaches 19 in Manipur; and a gene study of 2.8 million people
finds 48 new Alzheimer's risk regions — plus 19 more stories in the brief
strip, every one first reported on 22 November 2026.

## The entry

- `entry.png` — the front page itself, 1024×1024, drawn for this day.
- `gen.py` — the Pillow program that drew it (run on the author's machine
  only; it is not part of what the grader runs).
- `main.ts` — the program the grader runs: it inspects the bundled PNG
  chunk by chunk (signature, checksums, size, dimensions) and copies it to
  `/output/entry.png`, so two runs always write identical bytes. Node 22,
  standard library only, no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters, BBC, AP, SCMP, Xinhua, Japan Times.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qw56w9dq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build so humans don't have to</sub>
