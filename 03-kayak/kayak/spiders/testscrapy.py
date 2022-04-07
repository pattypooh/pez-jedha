import scrapy
print('OK')
text = ''
#text=' 23 exp\u00e9riences v\u00e9cues '
print(text.strip().split(' ')[0])
print(f'text:{text.strip().split(" ")[0]}$')

cities = [1, 2, 3]
urls = ['url1', 'url2', 'url3']


class UnObjet():
    def __init__(self,att1, att2):
        self.att1 = att1
        self.att2 = att2

def parsear (self):
    for i, url in enumerate(urls):
        yield UnObjet('att1', 'att2')

