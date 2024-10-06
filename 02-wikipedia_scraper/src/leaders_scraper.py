from bs4 import BeautifulSoup
import requests

def get_text(url,session):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup.prettify()
    return soup

def get_first_paragraph(wikipedia_url, session):
    print(wikipedia_url)
    soup = get_text(wikipedia_url,session)
    paragraphs = soup.find_all("p")
    for paragraph in paragraphs:
        if paragraph.find('b'):
            first_paragraph = paragraph.text
            break
    return first_paragraph

def get_leaders():
    leaders_per_country = {}
    countries_url = 'https://country-leaders.onrender.com/countries'
    leaders_url = 'https://country-leaders.onrender.com/leaders'
    cookie_url = 'https://country-leaders.onrender.com/cookie'
    session = requests.Session()
    cookies = session.get(cookie_url).cookies
    countries = session.get(countries_url, cookies=cookies).json()
    for country in countries:
        res = session.get(leaders_url, cookies=cookies, params={'country': country})
        if res.status_code == 403:
            print(f"Access denied for {country}")
            cookies = session.get(cookie_url).cookies
            res = session.get(leaders_url, cookies=cookies, params={'country': country})
        leaders_per_country[country] = res.json()
        for leader in leaders_per_country[country]:
            try:
                leader['first_paragraph'] = get_first_paragraph(leader['wikipedia_url'],session)
            except:
                continue

    return leaders_per_country

def save(leaders_per_country):
    import json 
    with open('02-wikipedia_scraper\leaders.json', 'w') as outfile :
        json.dump(leaders_per_country, outfile ) 
        
if __name__ == "__main__":
    leaders = get_leaders()
    save(leaders)

