from bs4 import BeautifulSoup

class TxtFormatter:
    @classmethod    
    def txtDescrFormat(self, html):
        if html is None:
            return None
        soup = BeautifulSoup(html, features="html.parser")
        txt = soup.get_text('\n')
        return txt
