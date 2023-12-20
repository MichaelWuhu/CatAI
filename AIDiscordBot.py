from dotenv import load_dotenv
import os
import discord
import openai

load_dotenv()
ai_api_key = os.environ.get("AI_API_KEY")
discord_bot_key = os.environ.get("DISCORD_BOT_KEY")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = discord.Client(intents=intents)
openai.api_key = ai_api_key

# conversation = []
conversation=[{"role": "system", "content": "Respond like cat, but still convey the correct information. Don't sound super enthusiastic though so don't use too many exclamation marks."}]

# async function to track which servers bot is in
@bot.event
async def on_ready():
    guild_count = 0

    # print if bot in a guild
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    
    # total guilds bot in
    print("Bot is in " + str(guild_count) + " servers")

# async function to track messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself
    
    # only responds if bot is pinged
    if bot.user.mentioned_in(message):
        user_input = {"role": "user", "content": message.content} # tracks what user says
        conversation.append(user_input) # adds user's message to conversation history
        response = await generate_response(message) # wait for openai to generate response before continuing
        await message.channel.send(response) # sends message

# make the response
async def generate_response(message):
    chat = openai.chat.completions.create(
      model="gpt-3.5-turbo",  
      messages = conversation,
      max_tokens = 3000
    )

    # completion.choices[0].message => returns: ChatCompletionMessage(content='Meow. What can I do for you?', role='assistant', function_call=None, tool_calls=None)
    # 
    # old code that used to work: response = chat.choices[0].message['content']
    # 
    # new code just reference statically:
    response = chat.choices[0].message.content
    
    # print for testing in console
    # print(response)
    
    # add on to conversation (will only remember from when it is online since conversation is reset everytime)
    # to keep conversation from past (even if bot offline) => use database to store previous message history
    conversation.append({"role":"system", "content": response})
    return response

bot.run(discord_bot_key)
