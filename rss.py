import discord
import discord.ext import commands
from bs4 import BeautifulSoup
import lxml
import requests
import re
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
url = 'https://store.steampowered.com/feeds/news/app/2073850/?cc=US&l=english&snr=1_2108_9__2107' 


def get_html_and_parse(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        entries = soup.find_all("item")

        if entries:
            latest_entry = entries[0]
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
    print(shift)
    print(title_cur)
    return shift, title_cur

get_html_and_parse(url)
