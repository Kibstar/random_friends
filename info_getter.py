import json, requests, os, bs4, re, random, webbrowser


url = 'https://en.wikipedia.org/wiki/List_of_Friends_episodes'
headers = {'Accept-Language': 'en-UK,en;q=0.8'}


class Friends:

    netflix_url = 'https://www.netflix.com/watch/'
    id = 70273996

    def __init__(self,number,episode,date,title):
        self.title = title
        self.episode = episode # episode number in that season i.e ep.12
        self.number = number # overall episode number i.e ep.134
        self.date = date
        self. netflix_id = (self.id + int(self.number))
        self. link = f'{self.netflix_url}{self.netflix_id}'

    def __str__(self):
        return(f'{self.title}\n'
               f'Episode: {self.number}\n')

def episode_finder(url):
    episode_list =[]
    res = requests.get(url,headers=headers)

    try:
        res.raise_for_status()
    except:
        return('The page could not be loaded')

    soup = bs4.BeautifulSoup(res.text,'html.parser')

    div = soup.find('div',{'class': 'mw-parser-output'})

    rows = div.find_all('tr',{'class':'vevent'})
    counter = 1
    for i in range(len(rows)):

        number = rows[i].contents[0].text
        title = rows[i].contents[2].text
        episode = rows[i].contents[1].text

        try:
            date = rows[i].contents[5].text
        except:
            date = ''

        if len(rows[i - 1].contents[0].text) > 1 and len(number) / 2 == len(rows[i - 1].contents[0].text):
            number = counter
            f = Friends(number+1,episode,date,title)
            episode_list.append(f)
            counter += 1
        if title[0] == '"':
            f = Friends(number,episode,date,title)
            episode_list.append(f)
            counter += 1
    return episode_list



if __name__ == '__main__':
    list = episode_finder(url)

    while True:
        choice = random.choice(list)
        print(choice)
        print('Do you want to watch this episode? Y or N?')
        i = input()
        if i.upper() == 'N':
            command = 'clear'
            os.system(command)
            continue
        elif i.upper() == 'Y':
            webbrowser.open(choice.link, new=2)
            break




