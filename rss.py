import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import lxml
import requests
import re
import config


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
url = 'https://store.steampowered.com/feeds/news/app/2073850/?cc=US&l=english&snr=1_2108_9__2107' 



@bot.event
async def on_ready():
 print("-"*10)
 print('bot is online')
 channel = bot.get_channel(config.channel_token)




def get_html_and_parse(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        entries = soup.find_all("item")

        if entries:
            latest_entry = entries[1]
            title = latest_entry.find("title")

            description = latest_entry.find("description")

            if title:
                plain_text_desc = title.get_text()

            if description:
                description_text = description.get_text()
                description_soup = BeautifulSoup(description_text, "html.parser")
                plain_text = description_soup.get_text(separator="\n")

                lines = plain_text.split("\n")
                formatted_lines = []
                for line in lines:
                    formatted_lines.append(line)

            else:
                print("No description found in the latest enrty.")
        else:
            print("No entries found in RSS feed")
    else:
        print(f'Failed to fetch the HTML. Status code: {response.status_code}')

    shift = "\n".join(formatted_lines)
    title_cur = plain_text_desc
    return shift, title_cur


@bot.command()
async def recent(ctx, member: discord.Member = None):
    shift, title_cur = get_html_and_parse(url)
    if member == None:
        member = ctx.author

    picture = "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRkMnGJnPhZh-8gG2J1fhvPq4drbYoUy9inp3EyfNm5MZUU93NX"
    embed1 = discord.Embed(title=f"{title_cur}", colour=discord.Colour.red())
    embed1.set_author(name=f"New Update Just Dropped!")
    embed1.set_thumbnail(url=f"{picture}")
    embed1.add_field(name=f"Here's what changed", value=f"{shift}", inline=True)

    embed1.set_footer(
        text="manually triggered",
        icon_url="https://img.icons8.com/color/144/restart--v1.png",
    )
    print('manually triggered')
    await ctx.send(embed=embed1)



if __name__ == "__main__":
    try:
        intents = discord.Intents.all()
        intents.message_content = True
        client = discord.Client(intents=intents)
        bot.run(config.discord_token)

    except SystemExit:
        print('Shutting down')
            
