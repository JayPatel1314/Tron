import os
import time
import shutil
import urllib

from requests import post

from pyrogram import Client
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"carbon" : (
		"carbon",
		{
		"carbon [text]" : "Get a carbon image with written text on it.",
		"carblist" : "Get list of carbon colour codes."
		}
		)
	}
)





colour_code = {
	"aqua": "rgba(0, 255, 255, 100)",
	"red": "rgba(255, 0, 0, 100)",
	"blue": "rgba(0, 0, 255, 100)",
	"green": "rgba(0, 255, 0, 100)",
	"yellow": "rgba(255, 255, 0, 100)",
	"gold": "rgba(255, 215, 0, 100)",
	"orange": "rgba(255, 165, 0, 100)",
	"purple": "rgba(41, 5, 68, 100)",
	"black": "rgba(0, 0, 0, 100)",
	"white": "rgba(255, 255, 255, 100)",
	"lime": "rgba(0, 255, 0, 100)",
	"silver": "rgba(192, 192, 192, 100)",
	"maroon": "rgba(128, 0, 0, 100)",
	"olive": "rgba(128, 128, 0, 100)",
	"teal": "rgba(0, 128, 128, 100)",
	"navy": "rgba(0, 128, 128, 100)",
	"chocolate": "rgba(210, 105, 30, 100)",
}




@app.on_message(gen(["carbon", "carb"], allow = ["sudo"]))
async def carb_api(_, m: Message):
	cmd = m.command
	if app.long(m) < 2:
		return await app.send_edit(m, f"Usage:\n\n`{app.PREFIX}carbon [colour] [text]`\n`{app.PREFIX}carbon [text]`\n\n**Note:** Default colour is aqua", delme=4)

	elif app.textlen(m) <= 4096:
		try:
			m = await app.send_edit(m, "creating carbon . . .", mono=True)
			if cmd[1] in colour_code:
				text = m.text.split(None, 2)[2]
				colour = cmd[1]
			else:
				text = m.text.split(None, 1)[1]
				colour= "aqua"
			await create_carbon(m, text=text, colour=colour)
		except Exception as e:
			await app.error(m, e)
	elif app.textlen(m) > 4096:
		await app.send_edit(m, "The text is too long !", delme=2)




@app.on_message(gen("carblist", allow = ["sudo"]))
async def colour_list(_, m: Message):
	clist = [f"`{x}`" for x in list(colour_code.keys())]
	await app.send_edit(m, "**colour code:\n\n" + "\n".join(clist))




async def create_carbon(m: Message, text, colour):
	reply = m.reply_to_message
	json = {"backgroundColor": f"{colour_code.get(colour)}",
		"theme": "Dracula",
		"exportSize": "4x",}
	json["code"] = urllib.parse.quote(text)
	json["language"] = "Auto"
	ApiUrl = "http://carbonnowsh.herokuapp.com"
	text = post(ApiUrl, json=json, stream=True)
	filename = "carbon_image.png"
	if text.status_code == 200:
		text.raw.decode_content = True
		with open(filename, "wb") as f:
			shutil.copyfileobj(text.raw, f)
			f.close()
		reply_msg_id = reply.message_id if reply else None
		await app.send_document(
			m.chat.id,
			filename,
			caption=f"**Carbon Made by:** {app.UserMention()}",
			reply_to_message_id=reply_msg_id,
		)
		await m.delete()
		if os.path.exists(f"./{filename}"):
			os.remove(filename)
	else:
		await app.send_edit(m, "Image Couldn't be retreived.", delme=4, mono=True)
