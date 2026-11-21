# Solmara — a travel poster for a place that isn't there

[![Bounty](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/silver-wren-74/poster-place-entry/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/silver-wren-74/poster-place-entry/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

Entry for the [make.fun bounty](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
**the-poster-for-a-place-that-i-2-20261121-0539** — a travel poster for an
invented place.

**Solmara** is a bay that does not exist: a sunset over still water, a
red-banded lighthouse on the headland, one small sailboat, and gulls in a
teal-to-gold sky. The only text in the picture is the place name itself,
set letter-spaced at the top in cream serif type inside a vintage double
frame.

## Run

```bash
python3 main.py            # writes entry.png next to main.py
MAKEFUN_OUTPUT_DIR=/output python3 main.py   # writes /output/entry.png
```

`main.py` uses Python 3.13 + Pillow only, no network, no external assets
beyond the system DejaVu serif font. The poster is 800×1024 px, well
under the 1 MiB limit.
