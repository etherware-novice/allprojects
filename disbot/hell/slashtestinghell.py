app_id = 860551486148050985
token = "ODYwNTUxNDg2MTQ4MDUwOTg1.YN85Bg.4_h0yJJ5NiXUcd8-PaUgMkzXPxI"

from discord.ext.commands import bot
import requests
from discord_slash import SlashCommand 
app = Quart(__name__)


url = f"https://discord.com/api/v8/applications/{app_id}/guilds/825807971917365269/commands"

json = {
    "name": "tester",
    "description": "this is so much heck i have never used json aaa",
    "options": [
        {
            "name": "opt",
            "description": "idk",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "0",
                    "value": "0"
                },
                {
                    "name": "1",
                    "value": "1"
                },
                {
                    "name": "2",
                    "value": "2"
                }
            ]
        },
        {
            "name": "string",
            "description": "idk",
            "type": 5,
            "required": False
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": f"Bot {token}"
}



r = requests.post(url, headers=headers, json=json)
print(r.status_code)
r.raise_for_status()


app.run()