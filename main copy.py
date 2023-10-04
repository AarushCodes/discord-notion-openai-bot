
chatgptKey = 'YOUR CHATGPTKEY'
discordtoken = 'YOUR DISCORD TOKEN'
import discord
import os
import re
import openai
import requests
from datetime import datetime, timezone
from notionapi import notion
NOTION_TOKEN = "YOUR NOTION TOKEN"
DATABASE_ID = "YOUR DATABASE ID"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}



openai.api_key = (chatgptKey)

def createpage(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res


#idea = 'example idea'
#desc= 'example_description'

NotionforIdea = notion(DATABASE_ID,NOTION_TOKEN)


def askgpt(query: str):
    response = openai.ChatCompletion.create(
    model="text-davinci-003",
    messages=[
        {
        "role": "user",
        "content": f"{query}"
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content.startswith('are you alive'):
            await message.channel.send('yes i am')
        
        channel = message.channel
        msg = message.content

        if 'idea:' and '.description:' in msg.replace(' ', '').lower() and message.author != self.user:
            pattern = re.compile(r'idea: |\. description:', re.IGNORECASE)
            splittedmsg = pattern.split(msg)
            print(*splittedmsg, sep='\n')
            idea = splittedmsg[1]
            #idea = str(idea[1])
            desc = str(splittedmsg[2])
            try:
                aiquery = f'Can you tell me how to execute this idea: {idea}. The description of this idea is : {desc}'
                aiaskedresult = askgpt(aiquery)
            except Exception as e:
                aiaskedresult = 'Not asked to ai due to error(check your openai API balance)'

            print(f'idea is : {idea} and description is {desc}')
            statuscode = NotionforIdea.addnewidea(idea,desc,aiaskedresult=aiaskedresult)
            if statuscode == 200:
                await channel.send(f'''idea and description sent to notion
AI suggestions: {aiaskedresult}''')
            else:
                await channel.send(f'some error happened. the response code was {statuscode}')
        
        elif 'idea:' in msg.lower().replace(' ', '') and message.author != self.user:
            pattern = re.compile(r'idea:', re.IGNORECASE)
            splittedmsg = pattern.split(msg)
            idea = splittedmsg[1].strip()
            #print(*splittedmsg, sep='\n')
            try:
                aiquery = f'can you tell me how to execute this idea: {idea}'
                aiaskedresult = askgpt(aiquery)
            except Exception as e:
                aiaskedresult = 'Not asked to ai due to error(check your openai API balance)'
            statuscode = NotionforIdea.addnewidea(idea,aiaskedresult=aiaskedresult)
            if statuscode == 200:
                await channel.send(f'''idea sent to notion
AI suggestions: {aiaskedresult}''')
            else:
                await channel.send(f'some error happened. the response code was {statuscode}')
            print(statuscode)
            
        #if 'ask to ai:' in msg:
            #aiquery = msg.replace('ask to ai:', '')
            #await channel.send(askgpt(aiquery))

        #if (message.author != self.user):
            #await channel.send('I am alive! sewyy')

        if '/help' in msg:
            await channel.send('''To send idea to notion and get AI suggestions use idea: {your idea}
If you want to give description of the idea then you can add fullstop then space then description:{your description}
Example: Idea: Example idea. description: example description
(this is not case sensitive)''')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discordtoken)

'''try:
                aiquery = f'can you tell me how to execute this idea: {idea}'
                aiaskedresult = askgpt(aiquery)
            except Exception as e:
                aiaskedresult = 'Not asked to ai due to error(check your openai API balance)'''