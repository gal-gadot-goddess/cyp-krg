"""
AI Metadata Generator for cyp-krg via Pollinations AI
Focuses on Crypto, DeFi, Web3, Blockchain Technology, and Tokenomics for @cryptokregg.
Extracts context from visual HTML animations and generates high-converting viral hook titles,
SEO captions, and strictly 5 lowercase hashtags.
"""

import os
import sys
import re
import json
import html
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

def extract_html_context(html_path: Path) -> dict:
    """
    Extracts core crypto/blockchain concepts, headings, equations, and mechanics
    from the visual HTML animation file to provide rich context to the AI.
    """
    if not html_path:
        return {}
    
    path_obj = Path(html_path)
    if not path_obj.exists():
        return {}

    try:
        raw_text = path_obj.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}

    title_match = re.search(r'<title>(.*?)</title>', raw_text, re.IGNORECASE | re.DOTALL)
    page_title = html.unescape(title_match.group(1)).strip() if title_match else ""
    page_title = re.sub(r'^(?:VIZ\s*\d+\s*[·•\-\s—–]*|[·•\-\s—–]+)', '', page_title, flags=re.IGNORECASE).strip()

    # Strip styles & scripts
    clean = re.sub(r'<style.*?</style>', '', raw_text, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<script.*?</script>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = html.unescape(clean)

    lines = [l.strip() for l in clean.splitlines() if l.strip()]

    # UI controls & handles to exclude
    ignore_set = {"@yourhandle", "@cryptokregg", "@kreggscode", "replay", "replayed", "fit", "mute", "unmute", "speed", "1x", "2x", "safe zones", "sound", "music"}
    meaningful_lines = []
    for l in lines:
        if l.lower() in ignore_set:
            continue
        # Skip pure numbers/counters or single symbols
        if len(l) > 3 and not re.match(r'^[0-9\s:.\-→·]+$', l):
            meaningful_lines.append(l)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for m in meaningful_lines:
        m_lower = m.lower()
        if m_lower not in seen:
            seen.add(m_lower)
            deduped.append(m)

    return {
        "page_title": page_title,
        "content_snippets": deduped[:12]
    }

def clean_filename_to_title(filename: str) -> str:
    name = Path(filename).stem
    # Remove leading numbers like VIZ_10_, 01-, etc.
    name = re.sub(r'^(?:VIZ[_-]*\d+[_-]*|\d+[_-]*)', '', name, flags=re.IGNORECASE)
    name = name.replace("_", " ").replace("-", " ")
    return " ".join(name.split())

def clean_hashtags(raw_tags: list, topic: str = "") -> list:
    """
    Ensures strictly at most 5 relevant hashtags, ALL in lowercase small letters.
    """
    clean = []
    for tag in raw_tags:
        if not isinstance(tag, str):
            continue
        t = tag.strip().lower()
        if not t.startswith("#"):
            t = f"#{t}"
        # Keep only alphanumeric and underscore after #
        t = re.sub(r'[^#a-z0-9_]', '', t)
        if len(t) > 2 and t not in clean:
            clean.append(t)

    # Fallback to sensible crypto defaults if too few
    default_fallbacks = [
        "#crypto",
        "#defi",
        "#web3",
        "#blockchain",
        "#ethereum"
    ]
    for d in default_fallbacks:
        d_clean = d.lower()
        if len(clean) >= 5:
            break
        if d_clean not in clean:
            clean.append(d_clean)

    return clean[:5]

def generate_ai_metadata(topic: str, html_file_path: Path = None) -> dict:
    """
    Generates SEO viral title, Instagram caption, Facebook caption, Threads caption,
    and exactly 5 lowercase hashtags from the HTML content and topic name.
    """
    if isinstance(topic, (str, Path)) and (str(topic).endswith(".html") or Path(topic).exists()):
        if not html_file_path:
            html_file_path = Path(topic)
        topic = clean_filename_to_title(str(topic))

    context = extract_html_context(html_file_path) if html_file_path else {}
    snippets = context.get("content_snippets", [])
    display_title = context.get("page_title") or topic

    topic_words = topic.split()
    lead_word = topic_words[0].lower() if topic_words else "crypto"
    fallback_metadata = {
        "title": f"{display_title}: What Actually Happens? ⚡",
        "ig_caption": f"⚡ {display_title} Explained Visually!\n\n"
                      f"Understanding on-chain mechanics is crucial for crypto investors, DeFi users, and Web3 builders.\n\n"
                      + ("\n".join([f"• {s}" for s in snippets[:6]]) if snippets else f"• Deep dive into {topic} smart contract and consensus mechanics.")
                      + f"\n\nWhat's your take on this protocol design? Drop your thoughts below! 👇\n\n"
                      f"Follow @cryptokregg for daily visual breakdowns of Crypto, DeFi & Web3 mechanics.",
        "fb_caption": f"Deep On-Chain Analysis: {display_title}.\n\n"
                      f"In Web3 and DeFi infrastructure, understanding how the underlying protocol functions prevents costly mistakes and reveals true utility.\n\n"
                      + ("\n".join([f"- {s}" for s in snippets[:8]]) if snippets else f"Complete visual overview of {topic}.")
                      + f"\n\nHave you interacted with this on-chain mechanism? Let's discuss in the comments below!",
        "threads_caption": f"{display_title} visualized in under 20s. What's your favorite DeFi innovation? #{lead_word} #crypto #web3",
        "hashtags": clean_hashtags([f"#{lead_word}", "#crypto", "#defi", "#web3", "#blockchain"], topic)
    }

    api_key = os.environ.get("POLLINATIONS_API_KEY", "")
    endpoints = [
        "https://gen.pollinations.ai/v1/chat/completions",
        "https://text.pollinations.ai/openai"
    ]

    context_str = f"Topic: {topic}\n"
    if context.get("page_title"):
        context_str += f"Visual Reel Title: {context['page_title']}\n"
    if snippets:
        context_str += "Key Visual Mechanics & Storyline:\n- " + "\n- ".join(snippets[:10])

    prompt = f"""You are a senior crypto quantitative researcher, Web3 protocol engineer, and viral social media architect managing @cryptokregg.
You create viral, high-retention, educational reels for crypto traders, DeFi enthusiasts, blockchain developers, and Web3 investors.

We are publishing an animated technical concept reel based on this visual blockchain/DeFi animation:
{context_str}

REQUIREMENTS:
1. "title": Viral SEO hook title (max 65 chars) with an emoji. Make it curious, sharp, and high-value (e.g. "How DEXs Set Prices Without Order Books ⚡", "Flash Loans: How to Borrow $10M in 1 Second ⚡", "Bitcoin Transaction: What Actually Happens? ⛓️").
2. "ig_caption": High-retention Instagram caption:
   - First 2 lines: Hook that stops the scroll.
   - Body: Clean bullet points explaining what happens on-chain based on the visual concepts provided.
   - Practical Takeaway: 1-2 sentence real-world DeFi / crypto security or alpha takeaway.
   - Call to Action: Ask a thought-provoking debate question to drive comment engagement.
   - Sign-off: "Follow @cryptokregg for daily visual breakdowns of Crypto, DeFi & Web3 mechanics."
3. "fb_caption": In-depth professional CryptoKregg Facebook post explaining the protocol trade-offs, tokenomics, and security implications.
4. "threads_caption": Short, punchy summary + debate starter (max 280 chars).
5. "hashtags": STRICTLY EXACTLY 5 relevant hashtags, ALL in LOWERCASE small letters only (e.g. ["#crypto", "#defi", "#web3", "#blockchain", "#ethereum"]).

OUTPUT FORMAT:
Return strictly a valid JSON object with keys: "title", "ig_caption", "fb_caption", "threads_caption", "hashtags".
"""

    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": "You are a professional crypto content strategist. You output strictly valid JSON without markdown wrapping."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    for ep in endpoints:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Antigravity-Agent"
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            req = urllib.request.Request(ep, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=25) as resp:
                raw_text = resp.read().decode("utf-8")
                res = json.loads(raw_text)
                content = res.get("choices", [{}])[0].get("message", {}).get("content", "")
                if not content:
                    content = raw_text

                raw_clean = re.sub(r"^```(?:json)?\s*", "", content.strip(), flags=re.MULTILINE)
                raw_clean = re.sub(r"\s*```$", "", raw_clean, flags=re.MULTILINE).strip()
                data = json.loads(raw_clean)

                data["hashtags"] = clean_hashtags(data.get("hashtags", []), topic)
                print(f"✅ Successfully generated viral crypto AI metadata via Pollinations ({ep}).")
                return data
        except Exception as e:
            print(f"⚠️ Notice for Pollinations endpoint {ep}: {e}")

    print("ℹ️ Using curated context-aware fallback metadata.")
    return fallback_metadata

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "VIZ_14_How_a_DEX_Sets_Prices.html"
    p = Path(t)
    if p.exists():
        res = generate_ai_metadata(p.name, html_file_path=p)
    else:
        res = generate_ai_metadata(t)
    print(json.dumps(res, indent=2, ensure_ascii=False))
