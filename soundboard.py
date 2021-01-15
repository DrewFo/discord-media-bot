import discord, platform, asyncio, os, glob

client = discord.Client()

def return_file_list():
        file_list = []
        for file in glob.glob("*.mp3"):
            file_list.append(file[:-4])
        return file_list

@client.event
async def on_ready():
    print('Soundboard running on python ' + platform.python_version())
    state = discord.Game("music")
    await client.change_presence(status=discord.Status.dnd, activity=state)

@client.event
async def on_message(message): 

    if message.author == client.user:
        return

    elif "sJoin" in message.clean_content:
        await message.author.voice.channel.connect()

    elif "sLeave" in message.clean_content:
        await message.author.guild.voice_client.disconnect()

    elif "sHelp" in message.clean_content:
        file_list = []
        for file in glob.glob("*.mp3"):
            file_list.append(file[:-4])
        await message.channel.send("\"sJoin\" joins your current vc, \"sLeave\" leaves your current vc.\n" + "type \"s\" and then one of the following keywords directly after:\n" + str(file_list))
        

    elif message.clean_content.startswith("s"):
        if message.clean_content[1:].lower() in return_file_list():
            source = message.clean_content[1:].lower() + ".mp3"
            message.author.guild.voice_client.stop()
            message.author.guild.voice_client.play(await discord.FFmpegOpusAudio.from_probe(source, method='fallback'))
        elif message.clean_content[1:] in return_file_list():
            source = message.clean_content[1:].lower() + ".mp3"
            message.author.guild.voice_client.stop()
            message.author.guild.voice_client.play(await discord.FFmpegOpusAudio.from_probe(source, method='fallback'))

        
client.run('example token')
