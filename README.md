# cyp-krg ⚡

Automated daily short-form video generation and multi-platform publishing pipeline for Crypto, DeFi, Web3, and Blockchain technology reels.

## 🚀 Overview
- **Brand**: `@cryptokregg` (Instagram) / `CryptoKregg` (Facebook Page)
- **Content**: Visual technical breakdowns of DEX pricing (AMM / $x \cdot y = k$), Flash Loans, Bitcoin transaction lifecycle, Self-custody vs Exchange custody, Ethereum L1 vs Rollup L2, Zero-Knowledge Proofs, Merkle Trees, tokenomics, and consensus mechanics.
- **Rendering**: Playwright headless browser automation capturing **native Web Audio API synthesized sound effects only** (strictly no background music), high-fidelity 60FPS vertical video (1080x1920), and Frame 0 diagram injection.
- **AI Engine**: Pollinations AI generating viral hooks, curiosity-driven educational captions, and strictly 5 lowercase hashtags.
- **Publishing Schedule**: Runs automatically everyday at 09:00 UTC (14:30 IST) via GitHub Actions, or manually triggered via `workflow_dispatch`.

## 📂 Architecture
```
cyp-krg/
├── .github/workflows/
│   └── automate.yml          # Daily GitHub Actions cron automation
├── html_sources/             # Synced HTML visual animations
├── upload/
│   ├── upload_facebook.py    # Facebook Reels Resumable API
│   ├── upload_instagram.py   # Instagram Reels Resumable API
│   └── upload_threads.py     # Threads API integration
├── converter.py              # Playwright HTML -> 60FPS 1080x1920 MP4 with native Web Audio SFX
├── generate_metadata.py      # Pollinations AI viral metadata engine
├── orchestrator.py           # Weighted LRU candidate selector & pipeline runner
├── publish.py                # Multi-platform social publisher
├── sync_gdrive.py            # Google Drive HTML asset synchronization
├── history.json              # Canonical publishing log & recirculation tracker
├── metadata.json             # Latest generated reel metadata
└── requirements.txt          # Python dependencies
```

## 🛠️ Local Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install --with-deps chromium
```

### 2. Configure environment
Create a `.env` file (do not commit to version control):
```env
GOOGLE_SERVICE_ACCOUNT_KEY={"type": "service_account", ...}
GDRIVE_HTML_FOLDER_ID=1wcWaKj1Nl-SnHArkmhdD_8Ml_-SlV3Bb
POLLINATIONS_API_KEY=your_key
META_LONG_LIVED_ACCESS_TOKEN=your_token
FACEBOOK_PAGE_ID=1024771650710096
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_token
INSTAGRAM_ACCOUNT_ID=17841458665431798
INSTAGRAM_ACCESS_TOKEN=your_page_token
```

### 3. Run Pipeline Locally
```bash
# Render video only (native Web Audio SFX only, skips social media upload)
python orchestrator.py

# Render and publish to Instagram & Facebook
python orchestrator.py --publish
```
