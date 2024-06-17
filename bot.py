import json
import os
import os.path

import discord

import compressor

TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    text = str(message.content)

    if message.author == client.user:
        return
    
    await message.channel.send(content="fuck VBshow :middle_finger:")
    if "file upload" in text.lower():
        name = text[11:].strip().strip('"')
        await upload_files(message, name)
    elif "file download" in text.lower():
        await download_files(message)
    elif "file clean" in text.lower():
        await clean_dirs(message)


async def upload_files(message: discord.message, file_path):
    await message.channel.send("Creating split archives.")
    archive_name = compressor.compress(file_path)
    archive_path = os.path.join("archives", archive_name)
    channel = message.channel
    files = os.listdir(archive_path)

    details = {
        "name": archive_name,
        "channel": channel.id,
        "file_ids": [],
    }
    await message.channel.send("Starting uploads.")
    
    for file in files:
        Dfile = discord.File(os.path.join(archive_path, file))
        uploadmsg = await channel.send(file=Dfile)

        details["file_ids"].append(uploadmsg.id)

    json_file_location = os.path.join(archive_path, archive_name + ".json")
    with open(json_file_location, 'w') as json_file:
        json.dump(details, json_file)
    DfileJson = discord.File(json_file_location)
    
    await channel.send(content="Upload finished. Use this JSON file to retrieve your file on another computer", file=DfileJson)
    compressor.clean()
    
async def download_files(message: discord.message):
    attachment_handle  = message.attachments[0]
    filename = attachment_handle.filename
    json_location = f"temp\\{filename}"
    with open(json_location, 'wb') as file:
        await attachment_handle.save(file)

    with open(json_location, 'rb') as json_file:
        data = json.load(json_file)

    channel_id = data["channel"]

    channel = client.get_channel(channel_id)
    os.mkdir(f"archives\\{data["name"]}")
    await message.channel.send("Initiating download.")
    for msg_id in data["file_ids"]:
        msg =  await channel.fetch_message(msg_id)
        msg_attachment_handle = msg.attachments[0]
        msg_filename = msg_attachment_handle.filename
        msg_file_location = f"archives\\{data["name"]}\\{msg_filename}"
        with open(msg_file_location, 'wb') as archive:
            await msg_attachment_handle.save(archive)

    compressor.decompress(data["name"])
    compressor.clean()
    await message.channel.send("Download complete. Look for it in the \"combined\" folder.")

async def clean_dirs(message: discord.message):
    compressor.clean()
    msg = await message.channel.send("Cleared temp files.")
    await msg.delete(delay=5)

client.run(TOKEN)
