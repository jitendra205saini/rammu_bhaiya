import os
import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """Aap "Rammu Bhai" ho — gaming server ke Ram bhakt Bot Bhaiya. Creator: hunternumber01.

=== SABSE ZAROORI NIYAM ===
- HAMESHA CHHOTA jawab do — max 3-4 lines. Kabhi bhi lamba paragraph mat likho.
- Jis user ne message kiya hai, uska naam + "ji" lagao. Jaise "hunternumber01 ji" ya "[username] ji". Kabhi sirf "aap ji" mat likho — naam zaroor lo.
- Hinglish mein baat karo (Hindi+English mix), casual gaming style.

=== GAMING KNOWLEDGE ===
GTA 6 (Vice City, Jason+Lucia, 2025-26), BGMI/PUBG, Valorant, CS:GO, Minecraft, Fortnite — sab jaante ho.
Kabhi "noob" mat kaho — "practice karo, pro ban jaoge" kaho.

=== PERSONALITY ===
- Gaali mile toh: "Ram Ram [naam] ji! Aapki gaali prasad lagti hai 🙏 Agli game mein clutch maaro!"
- Game haarne par: "Gita kehti hai [naam] ji — karm karo, phal ki chinta nahi. Next game better hoga!"
- Greeting (Hi/Hello/Hey/Ram Ram/Jai Shree Ram aaye): "Jai Shree Ram [naam] ji! 🙏 Kya game kheloge aaj?"
- Koi "Jai Shree Ram" bole: "Jai Shree Ram [naam] ji! 🙏" se jawab do
- Koi bye/alvida/jaa raha hoon bole: "Jai Shree Ram [naam] ji! 🙏 Dobara aana, bye byeee!"
- Creator puchha: "hunternumber01 ji ne banaya hai mujhe! Jai Shree Ram! 🙏"
- BAAKI saari normal baaton mein "Jai Shree Ram" MAT likho — sirf upar wale cases mein likhna hai."""

groq_client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Conversation history per channel (in-memory)
conversation_history = defaultdict(list)
MAX_HISTORY = 10


@bot.event
async def on_ready():
    print(f"Jai Shree Ram! {bot.user} Discord par aa gaya hai! 🙏")
    await bot.change_presence(
        activity=discord.Game(name="GTA 6 ka wait | Jai Shree Ram 🙏")
    )


@bot.event
async def on_message(message):
    print(f"[MSG] {message.author}: {message.content[:50]}")
    if message.author == bot.user:
        return

    should_respond = False
    content = message.content

    # Bot user mention ya bot ki role mention — dono pe respond karo
    bot_role_mentioned = (
        message.guild is not None and
        any(role in message.role_mentions for role in message.guild.me.roles)
    )

    if bot.user.mentioned_in(message) or bot_role_mentioned:
        should_respond = True
        content = content.replace(f"<@{bot.user.id}>", "").strip()
        content = content.replace(f"<@!{bot.user.id}>", "").strip()
        for role in message.role_mentions:
            content = content.replace(f"<@&{role.id}>", "").strip()
        print(f"[MENTION] {message.author}: '{content}'")
        if not content:
            content = "Jai Shree Ram! Kaise ho aap?"

    if should_respond:
        async with message.channel.typing():
            channel_id = str(message.channel.id)

            # Add to conversation history
            conversation_history[channel_id].append({
                "role": "user",
                "content": f"{message.author.display_name}: {content}"
            })

            # Keep only last MAX_HISTORY messages
            if len(conversation_history[channel_id]) > MAX_HISTORY:
                conversation_history[channel_id] = conversation_history[channel_id][-MAX_HISTORY:]

            try:
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *conversation_history[channel_id]
                    ],
                    max_tokens=180,
                    temperature=0.85
                )

                reply = response.choices[0].message.content

                # Add bot reply to history
                conversation_history[channel_id].append({
                    "role": "assistant",
                    "content": reply
                })

                # Discord 2000 char limit — split if needed
                if len(reply) > 2000:
                    for i in range(0, len(reply), 2000):
                        await message.reply(reply[i:i+2000])
                else:
                    await message.reply(reply)

            except Exception as e:
                print(f"Error: {e}")
                await message.reply(
                    "Ram Ram! 🙏 Thodi takleef aa gayi server mein. "
                    "Hanuman ji se madad maang raha hoon, thoda ruko! Jai Shree Ram!"
                )

    await bot.process_commands(message)


@bot.command(name="clear")
async def clear_history(ctx):
    """Conversation history clear karo"""
    channel_id = str(ctx.channel.id)
    conversation_history[channel_id] = []
    await ctx.send(
        "Ram Ram! 🙏 Conversation history saaf ho gayi! "
        "Naya game, naya din, naya jazbaa! Jai Shree Ram! 🚩"
    )


@bot.command(name="ramram")
async def ramram(ctx):
    """Rammu Bhai se greeting lo"""
    await ctx.send(
        f"Jai Shree Ram! 🙏 {ctx.author.mention} bhai!\n"
        "Main Rammu Bhai hoon — aapka gaming partner aur Ram ka chhota sa sevak!\n"
        "Kya aaj koi game kheloge? GTA 6 ki khabar sunni hai? Batao! 🎮\n"
        "**Jai Bajrangbali! 🚩**"
    )


@bot.command(name="gta6")
async def gta6_info(ctx):
    """GTA 6 ki latest info"""
    await ctx.send(
        "🎮 **GTA 6 — Rammu Bhai ki Report!**\n\n"
        "🗺️ **Map:** Vice City (Miami inspired) — bahut bada map aane wala hai!\n"
        "👥 **Characters:** Jason aur Lucia — pehli baar female protagonist!\n"
        "📅 **Release:** 2025-26 ki khabar hai, par Ram ji chahein toh jaldi aaye!\n"
        "💰 **Price:** Probably $70+ hoga — save karo abhi se!\n\n"
        "Tab tak GTA 5 Online mein practice karo bhai! 😄\n"
        "**Jai Shree Ram! 🙏**"
    )


bot.run(DISCORD_TOKEN)
