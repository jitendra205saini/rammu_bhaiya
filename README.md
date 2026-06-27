# 🚩 Rammu Bhai — Discord Gaming Bot

**Rammu Bhai** ek Hindi/Hinglish gaming Discord bot hai jo Groq AI (LLaMA) use karta hai.  
Creator: **hunternumber01** | Powered by: **Groq API** + **discord.py**

---

## 🔄 Bot Ka Working Flowchart

```mermaid
flowchart TD
    A([🚀 Bot Start]) --> B{Env Vars\nCheck}
    B -->|DISCORD_TOKEN\nya GROQ_API_KEY\nMissing| C([❌ ERROR + Exit])
    B -->|✅ Dono milgaye| D[Discord se Connect karo]
    D --> E[Presence set karo\n'GTA 6 ka wait 🙏']
    E --> F([⏳ Message ka wait...])

    F --> G[📩 Message aaya]
    G --> H{Bot ka khud\nka message?}
    H -->|Haan| F
    H -->|Nahi| I{Bot mention\nya Role mention?}

    I -->|Nahi| J[process_commands\nchalaao]
    J --> F

    I -->|Haan| K[Mention tags\nsaaf karo]
    K --> L{Content\nkhaali hai?}
    L -->|Haan| M[Default:\nJai Shree Ram! 🙏]
    L -->|Nahi| N{500+ channels\ntrack ho rahe?}
    M --> N

    N -->|Haan| O[Sabse purana\nchannel hatao]
    O --> P[History mein\nuser message add karo]
    N -->|Nahi| P

    P --> Q[Sirf last 5\nmessages rakho]
    Q --> R[🤖 Groq API Call\nllama-3.1-8b-instant\nmax 100 tokens]

    R --> S{API\nResponse?}
    S -->|❌ Error| T[Error message\nDiscord pe bhejo]
    T --> F

    S -->|✅ Reply mila| U{Reply\n2000 chars\nse zyada?}
    U -->|Haan| V[Parts mein\ntod ke bhejo]
    U -->|Nahi| W[Seedha reply\nkaro]

    V --> X[Reply ko history\nmein save karo]
    W --> X
    X --> F

    style A fill:#4CAF50,color:#fff
    style C fill:#f44336,color:#fff
    style F fill:#2196F3,color:#fff
    style R fill:#FF9800,color:#fff
    style T fill:#f44336,color:#fff
```

---

## ⚡ Commands

| Command | Kaam |
|---------|------|
| `@Rammu Bhai <message>` | Bot se baat karo |
| `!clear` | Is channel ki history saaf karo |
| `!ramram` | Rammu Bhai se greeting lo |
| `!gta6` | GTA 6 ki latest info |

---

## 🛠️ Setup

### 1. Environment Variables (Railway Dashboard mein set karo)
```
DISCORD_TOKEN=your_discord_bot_token
GROQ_API_KEY=your_groq_api_key
```

### 2. Discord Developer Portal
- **MESSAGE CONTENT INTENT** enable karo (Privileged Gateway Intents)

### 3. Groq API
- Free account: [console.groq.com](https://console.groq.com)
- Model: `llama-3.3-70b-versatile`

---

## 📦 Dependencies

```
discord.py==2.3.2
groq==0.11.0
httpx==0.27.2
python-dotenv==1.0.1
audioop-lts==0.2.1
```

---

## 🚀 Railway Deployment

- `Procfile` mein `worker: python bot.py` — koi web server nahi chahiye
- Railway pe push karo → automatic redeploy hoga

**Jai Shree Ram! 🙏**
