import tgcrypto
import os
import asyncio

from pyrogram import Client

# guide them 
print("@Tronuserbot Corporation\n\nGet the following values by logging to\nhttps://my.telegram.org\n\nRequired:\n\n1.APP_ID\n2.API_HASH\n3.PHONE NUMBER\n(WITH COUNTRY CODE)\n\n")

# integer only
API_ID = int(input("Enter APP_ID: "))

# string only
API_HASH = input("Enter API HASH: ")

# create a new pyrogram session
with Client(":memory:", api_id=API_ID, api_hash=API_HASH, hide_password=True) as app:
	app.send_message("me", f"This Is Your Tron Userbot • [ `SESSION` ]\n\n```{app.export_session_string()}```\n\n⚠️• Don't share this with anyone !!\n\nCreate Again • [ Press Here](https://replit.com/@beastzx18/Tron-Userbot-Session)", disable_web_page_preview=True,) 
	print("Your String Session Is Successfully Saved In Telegram Saved Messages !! Don't Share It With Anyone!!", Anyone having your session can use your telegram account !)
	
