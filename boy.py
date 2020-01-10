import json
import discord
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import requests
from io import BytesIO

with open("auth.json") as f:
    auth_dict = json.load(f)

token = auth_dict['token']
client = discord.Client()
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    if message.content.startswith('*replace friend '):
        await parse_friend_message(message.content.replace("*replace friend", ""), message)

async def parse_friend_message(command, message):
    #Verify users in command (*new friend andtrue clam)
    #Create image

    friends = command.split()

    if len(friends) != 2:
        await message.channel.send("Specify 2 friends, my guy")
        return

    author_name = message.author.name
    new_friend_name = friends[1]
    old_friend_name = friends[0]

    #print([user.name for user in message.channel.members])
    channel_user_names = [user.name for user in message.channel.members]
    
    #Check if we have both friends in the channel
    if new_friend_name not in channel_user_names:
        await message.channel.send("There is no user " + str(new_friend_name) + ", and they call me the bot.")
        return 
    
    
    if old_friend_name not in channel_user_names:
        await message.channel.send("There is no user " + str(old_friend_name) + ", and they call me the bot.")
        return 

    

    #Get avatar imgs and size them
    size = 128, 128

    #author
    author_avatar_url = message.author.avatar_url
    response = requests.get(author_avatar_url)
    author_avatar = Image.open(BytesIO(response.content))
    author_avatar = author_avatar.resize(size)

    #new friend
    new_friend_avatar_url = next((user.avatar_url for user in message.channel.members if user.name == new_friend_name), None)
    response = requests.get(new_friend_avatar_url)
    new_friend_avatar = Image.open(BytesIO(response.content))
    new_friend_avatar = new_friend_avatar.resize(size)

    #old friend
    old_friend_avatar_url = next((user.avatar_url for user in message.channel.members if user.name == old_friend_name), None)
    response = requests.get(old_friend_avatar_url)
    old_friend_avatar = Image.open(BytesIO(response.content))
    old_friend_avatar = old_friend_avatar.resize(size)


    background = Image.open("bestfriend-original.jpg", "r")


    #place author friend image
    background.paste(author_avatar, (120, 70))

    #place new friend image
    background.paste(new_friend_avatar, (425, 120))

    #place old friend image
    background.paste(old_friend_avatar, (10, 300))
    background.paste(old_friend_avatar, (525, 330))

    #draw text
    #Create new image with text on it with white background, then paste that image to the final product
    old_friend_font = ImageFont.truetype("arial.ttf", 44)
    new_friend_font = ImageFont.truetype("arial.ttf", 34)

    text_img = Image.new("RGBA", (220, 65), "white")
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((10, 5), old_friend_name, (0, 0, 0), font=old_friend_font)

    background.paste(text_img, (455, 5))


    text_img = Image.new("RGBA", (150, 50), "white")
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((10, 5), new_friend_name, (0, 0, 0), font=new_friend_font)

    background.paste(text_img, (255, 140))

    file_name = "out.png"
    background.save(file_name)

    upload_file = discord.File(file_name)
    await message.channel.send(file=upload_file)
    
    



client.run(token)

