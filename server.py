# WRITTEN ON AUGUST 26 2025
# SAMIP REGMI
# CODE MODIFIED BY SAMIP REGMI ON AUGUST 27
# VIEW CHANNEL , READ MESSAGE HISTORY , SEND MESSAGES->BOT PERMISSION

import os
import discord
import json
import random
from google import genai
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = genai.Client()

# ENV SHIT
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.environ.get('GUILD_ID'))
USER_ID = int(os.environ.get('USER_ID'))

intents = discord.Intents.default()
# FETCH MEMBERS
intents.members = True
# READ MESSAGE HISTORY
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# USER SESSION
user_sessions = {}
QUESTION_PATH = 'categories/'


def get_categories() -> list:
    CATEGORIES = []
    for folder in os.listdir(QUESTION_PATH):
        if os.path.isdir(os.path.join(QUESTION_PATH, folder)):
            CATEGORIES.append(folder)
    return CATEGORIES

def get_available_question_files(category: str) -> list:
    AVAILABLE_QUESTION_FILES = []
    category_path = os.path.join(QUESTION_PATH, category)
    # print(category_path)
    if not os.path.exists(category_path):
        return AVAILABLE_QUESTION_FILES
    for file in os.listdir(category_path):
        if file.startswith('question_') and file.endswith('.json'):
            AVAILABLE_QUESTION_FILES.append(file)
    return AVAILABLE_QUESTION_FILES



# ------------------------------------------- BI DIRECTIONAL CHATS---------------------------
"""
DONT EXCEED 1800 CHARACTERS
USE MARKDOWN FORMATTING IN YOUR RESPONSES
IN YOUR RESPONSES ALWAYS USE MARKDOWN FORMATTING WHEREVER APPLICABLE
YOU ARE BOTU AI ASSISTANT
YOU ARE AT A COMPUTER SCIENCE COMMUNITY DISCORD SERVER
IF SOME ONE ASKS QUESTION OTHER THAN COMPUTER SCIENCE TOPIC ITSELF TELL IT "I AM SORRY I AM DESIGNED TO ANSWER ONLY COMPUTER SCIENCE RELATED QUESTIONS"
IF SOMEONE ASKS YOU TO TELL A JOKE, STORIES ETC TELL THEM THOSE THINGS WITH A COMPUTER SCIENCE TWIST
TELL THEM MANAGED BY DEVSPHERE 
INITIALIZED BY SAMIP REGMI
"""

# WHEN USER WRITES ASK
# BOTU WILL SAY YOU ARE NOW CONNECTED TO GEMINI
# BOTU WILL ASK FOR YOUR QUERY
# USER WRITES THE QUERY
# BOTU WILL SEND THE QUERY TO GEMINI
# BOTU WILL RETURN THE RESPONSE TO USER
async def send_to_gemini(query):
    system_prompt = (
        "DONT EXCEED 1800 CHARACTERS\n"
        "USE MARKDOWN FORMATTING IN YOUR RESPONSES\n"
        "IN YOUR RESPONSES ALWAYS USE MARKDOWN FORMATTING WHEREVER APPLICABLE\n"
        "YOU ARE BOTU AI ASSISTANT\n"
        "YOU ARE AT A DEVSPHERE A COMPUTER SCIENCE COMMUNITY OF BIRATNAGAR INTERNATIONAL COLLEGE, NEPAL (BIC) IN SHORT\n"
        "IF SOME ONE ASKS QUESTION OTHER THAN COMPUTER SCIENCE TOPIC ITSELF TELL IT \"I AM SORRY I AM DESIGNED TO ANSWER ONLY COMPUTER SCIENCE RELATED QUESTIONS\"\n"
        "IF SOMEONE ASKS YOU TO TELL A JOKE, STORIES ETC TELL THEM THOSE THINGS WITH A COMPUTER SCIENCE TWIST\n"
        "TELL THEM MANAGED BY DEVSPHERE \n"
        "INITIALIZED BY SAMIP REGMI"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = [
            system_prompt,
            query
        ], 
    )
    return response.text


@bot.command(name="ask")
async def ask(ctx):
    await ctx.send(f"NAMASTE {ctx.author.mention},YOU ARE NOW CONENCTED TO BOTU AI\nPLEASE ENTER YOUR QUERY NOW")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', check=check, timeout=30.0)
        query = reply.content
        response = await send_to_gemini(query)
        await ctx.send(f"BOTU AI: {response}")
    except Exception:
        await ctx.send("INVALID INPUT OR TIMEOUT. PLEASE TRY AGAIN.")
        return  

    # user_id = ctx.author.id
    # SESSION XUTYAERA GET MA JANEY
    # user_sessions[user_id] = 'ai'  

@bot.command(name="whoami")
async def whoami(ctx):
    user = ctx.author
    if user.id == USER_ID:
        # await ctx.send(f"**HELLO BOSS**\nGLOBAL ID {user.global_name}\nUSERNAME {user.name}\nDISCRIMINATOR {user.discriminator}\nUSER ID {user.id}")
        await ctx.send(f"**HELLO BOSS**\nGLOBAL ID {user.global_name}\nUSERNAME {user.name}")
    else:
        await ctx.send(f"GLOBAL ID {user.global_name}\nUSERNAME {user.name}\nDISCRIMINATOR {user.discriminator}\nUSER ID {user.id}")


@bot.command(name='leaderboard')
async def leaderboard(ctx):
    try:
        with open('score.json', 'r') as f:
            scores = json.load(f)
            if not scores:
                await ctx.send("NO SCORES RECORDED YET.")
                return

            scores.sort(key=lambda x: x['score'], reverse=True)
            msg = "LEADERBOARD:\n"
            for idx, entry in enumerate(scores, start=1):
                username = entry['username'] 
                msg += f"{idx}. {username} - {entry['score']}\n"

            await ctx.send(msg)
    except FileNotFoundError:
        await ctx.send("NO SCORES RECORDED YET.")
    except Exception as e:
        await ctx.send(f"ERROR LOADING LEADERBOARD: {e}")

# TODO:
# BREAK INTO ATLEAT TWO FUNCTIONS
@bot.command(name="quiz")
async def quiz(ctx):
    score = 0
    categories = get_categories()
    if not categories:
        await ctx.send("NO CATEGORIES AVAILABLE")
        return
    
    msg = "AVAILABLE CATEGORIES:\n"
    for idx, category in enumerate(categories, start=1):
        msg += f"{idx}. {category}\n"
    msg += "PLEASE TYPE THE CATEGORY NUMBER TO SELECT IT"
    await ctx.send(msg)

    # CHECK IF IT IS SAME USER STARTING THE QUIZ AND SAME CHANNEL
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', check=check, timeout=30.0)
        choice = int(reply.content)
    except Exception:
        await ctx.send("INVALID INPUT OR TIMEOUT. PLEASE TRY AGAIN.")
        return
    # BELOW CODE IS FROM MY PROJECT WITH ARYAN REPO: game_juniors
    if choice < 1 or choice > len(categories):
        await ctx.send("INVALID CHOICE. PLEASE TRY AGAIN.")
        return
    category_choice = categories[choice - 1]
    AVAILABLE_QUESTION_FILES = get_available_question_files(category_choice)
    if not AVAILABLE_QUESTION_FILES:
        await ctx.send("NO QUESTIONS AVAILABLE IN THIS CATEGORY")
        return
    RANDOM_QUESTION_FILE = random.choice(AVAILABLE_QUESTION_FILES)

    try:
        with open(os.path.join(QUESTION_PATH, category_choice, RANDOM_QUESTION_FILE), 'r') as f:
            questions = json.load(f)
            random.shuffle(questions)  
            total_questions = len(questions)
            asked_count = 0
            for question in questions:
                asked_count += 1
                await ctx.send(f"QUESTION {asked_count}/{total_questions}:\n{question['question']}")
                for option, answer in question['options'].items():
                    await ctx.send(f"{option}. {answer}")
                await ctx.send("YOUR ANSWER?")

                user_answer = await bot.wait_for('message', check=check, timeout=30.0)
                
                if user_answer.content.lower() == 'exit':
                    await ctx.send("QUIZ ENDED. THANK YOU FOR PARTICIPATING!")
                    return

                if user_answer.content.lower() == question['answer'].lower():
                    await ctx.send("CORRECTOOO")
                    score += 1
                else:
                    await ctx.send(f"WRONG ANSWER. THE CORRECT ANSWER IS {question['answer']} , YOUR ANSWER WAS {user_answer.content}")

            await ctx.send(f"YOUR SCORE IS {score}/{total_questions}")

            try:
                with open('score.json', 'r') as f:
                    scores = json.load(f)
            except FileNotFoundError:
                scores = []
            user_found = False
            for entry in scores:
                # ID > GLOBAL NAME LOL
                if entry['username'] == ctx.author.global_name:
                    entry['score']  = max(entry['score'], score)
                    user_found = True
                    break
            if not user_found:
                scores.append({'username': ctx.author.global_name, 'score': score})
            with open('score.json', 'w') as f:
                json.dump(scores, f, indent=4)
            await ctx.send("YOUR SCORE HAS BEEN RECORDED.")
            return
    except Exception:
        await ctx.send("ERROR LOADING QUESTIONS. PLEASE TRY AGAIN LATER.")
        return

@bot.command(name="namaste")
async def namaste(ctx):
    guild = ctx.guild
    # member_count = guild.member_count
    await ctx.send(f"HEY I AM BOTU\nMANAGED BY DEVSPHERE\nINITIALIZED BY <@{USER_ID}>\nI AM SENDING MEMBER DATA TO OUR API ENDPOINT")


# @bot.event
# async def on_message(message):
#     if message.author.bot:
#         return  # IGNORE BOTS

#     user_id = message.author.id
#     session_type = user_sessions.get(user_id)

#     if session_type == 'ai':  
#         query = message.content

#         response = await send_to_gemini(query)  

#         await message.channel.send(f"BOTU AI: {response}")

#         # END SESSION
#         user_sessions.pop(user_id)
    
#     await bot.process_commands(message) # PROCESS OTHER COMMANDS , DONT BLOCK THEM


# ----------------------
# @bot.command(name="sanchai_chau")
# async def sanchai_chau(ctx):
#     guild = ctx.guild
#     await ctx.send(f"EKDAM SANCHAI CHU HAI DHERAI MAYA HAI")

# @bot.command(name="upcoming")
# async def upcoming(ctx):
#     message = (
#         "The Compass is an upcoming event organized by devsphere, the event consists of various activites such as games but the major highlight of it is the panel discussion titled “Demystifying Tech: First Steps Into Web and AI”, with the aim to guide freshers and beginner level students in exploring opportunities and challenges in web development and artificial intelligence. We would be honored to have you join us as a panelist to share your insights and experiences with the students.\n"
#         "**Event Details:**\n"
#         "Topic: Demystifying Tech: First Steps Into Web and AI\n"
#         "Format: Panel Discussion\n"
#         "Date and Time: 27th August 2025 at 10:00 AM\n"
#         "Venue: Biratnagar International College\n"
#         "FORM VARA HAI\n"
#         "## [CLICK HERE](https://docs.google.com/forms/d/e/1FAIpQLSfK_7Qwz-3CwY5HFPjZD0BZTOhUkqJ64NEeGSVAD9Q8FCEJ4g/viewform?pli=1)\n"
#         "## BOTU WILL BE HAPPY IF YOU JOIN US"
#     )
#     await ctx.send(message)

# @bot.command(name="teej")
# async def teej(ctx):
#     embed = discord.Embed(
#         title="HAPPY TEEJ",
#         description="LETS GOOO",
#         color=0xFF69B4  
#     )
#     embed.set_image(url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzI2bWo3bmNzM3J1MWQ0MXZiMHVpbmsyMm0wNW56dHBuNmc1Z3R1eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KQs8OigaWhDP0mYUX8/giphy.gif")
    
#     await ctx.send(embed=embed)

bot.run(DISCORD_BOT_TOKEN)  


