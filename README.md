# BOTU - DEVSPHERE DISCORD BOT

![Author](https://img.shields.io/badge/author-samip--regmi-blue)

---

## INSTALLATION

1. **CLONE THE REPO**
   ```bash
   git clone https://github.com/BIC-DevSphere/devsphere-bot.git
   cd devsphere-bot
   ```

2. **USE VIRTUAL ENV (RECOMMENDED)**
    ```bash
    python3 -m venv <envname>
    source <envname>/bin/activate
    ```
3. **INSTALL DEPENDENCIES**
   ```bash
    pip install -r requirements.txt
   ```
4. **CREATE `.env` FILE**
   ```bash
    DISCORD_BOT_TOKEN= 
    GUILD_ID= 
    USER_ID= 
    GEMINI_API_KEY=
   ```
5. **AND U ARE GOOD TO GO**
   ```bash
    python3 server.py
   ```