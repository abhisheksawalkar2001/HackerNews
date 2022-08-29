import requests
import bs4
import pprint

links = []
subtext = []

for page_num in range(1, 20):
    res = requests.get(f'https://news.ycombinator.com/news?p={page_num}')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    links.extend(soup.select('.titlelink'))
    subtext.extend(soup.select('.subtext'))


def sort_stories_by_point(hnlist):
    return sorted(hnlist, key=lambda item: item['point'], reverse=True)


def create_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        link = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            point = int(vote[0].getText().replace('points', ''))
            if point > 99:
                hn.append({'title': title, 'link': link, 'point': point})
    return sort_stories_by_point(hn)


pprint.pprint(create_hn(links, subtext))
