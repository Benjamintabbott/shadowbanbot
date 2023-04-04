from bs4 import BeautifulSoup as BS
from requests_html import AsyncHTMLSession
import re
import time



async def grab(username):
    check = "\u2705"
    exclamation = "\u274c"
    soup = BS()
    s = AsyncHTMLSession()
    url = 'https://shadowban.yuzurisa.com/'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0'}
    r = await s.get(url + username, headers=headers)
    await r.html.arender(sleep=4)
    

    soup = BS(r.html.html, 'html.parser')
    #print(r.html)
    results = soup.find_all('div', class_ = 'task-message')
    scrape_bans = []
    for result in results:
        unreadable = str(result.find('span'))
        readable = re.sub('<[^>]+>', '', unreadable)
        scrape_bans.append(readable)

    #dictionary to return
    bans = {}
    #EXISTS 
    #print(bans[0].split(' ')[1])
    for attempt in range(4):
        if(scrape_bans[0].split(' ')[1] != 'exists.'):
           time.sleep(1)
           await grab(username)

    if(scrape_bans[0].split(' ')[1] != 'exists.'):
        bans['exists'] = False
    else:
        bans['exists'] = True
    
    #SUGGESTION BAN 
    #print(bans[1].split(' ')[0])
    if(scrape_bans[1].split(' ')[0] != 'No'):
        bans['sug_ban'] = " Search suggestion ban!"
        bans['sug_ban_emoji'] = exclamation
        bans['sug_ban_text'] = "\n\U0001F534 Does not populate search suggestions and search results."      
    else:
        bans['sug_ban'] = " No search suggestion ban."
        bans['sug_ban_emoji'] = check
        bans['sug_ban_text'] = ""

    #SEARCH BAN
    #print(bans[2].split(' ')[0])
    if(scrape_bans[2].split(' ')[0] != 'No'):
        bans['s_ban'] = " Search ban!"
        bans['s_ban_emoji'] = exclamation
        bans['s_ban_text'] = "\n\U0001F534 Tweets are hidden from search results entirely, including hashtags."
    else:
        bans['s_ban'] = " No search ban."
        bans['s_ban_emoji'] = check
        bans['s_ban_text'] = ""

    #GHOST BAN
    #print(bans[3].split(' ')[0])
    if(scrape_bans[3].split(' ')[0] != 'No'):
        bans['ghost'] = " Ghost ban!"
        bans['ghost_emoji'] = exclamation
        bans['ghost_text'] = "\n\U0001F534 Found reply tweets completely hidden to the public."
    else:
        bans['ghost'] = " No ghost ban."
        bans['ghost_emoji'] = check
        bans['ghost_text'] = ""

    #DEBOOST BAN
    #print(bans[4].split(' ')[0])
    if(scrape_bans[4].split(' ')[0] != 'No'):
        bans['deboost'] = " Reply deboosting detected!"
        bans['deboost_emoji'] = exclamation
        bans['deboost_text'] = "\n\U0001F534 Found reply tweets hidden behind \"Show more replies\"."
    else:
        bans['deboost'] = " No reply deboosting detected."
        bans['deboost_emoji'] = check
        bans['deboost_text'] = ""

    return(bans)

    
# has multiple bans on account
#grab('multer69')
#grab('asld;kfahsgh9eubgfaib')

# has no bans
#grab('spicycryptocat')