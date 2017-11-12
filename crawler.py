import re
import requests
from bs4 import BeautifulSoup, Comment, Tag
import urllib.parse

from commit2db import MysqlConnection

YEAR_URL = 'https://www.basketball-reference.com/draft/NBA_{year}.html'


def get_player_info(soup: Tag) -> dict:
  meta_soup = soup.find(id='meta')
  player_data = {}
  player_data['name'] = meta_soup.h1.get_text()
  
  all_paragraph = meta_soup.select('div > p')
  
  # The original html is messy, sorry for the regex
  meta_data = meta_soup.get_text().replace('\n', ' ')
  height, weight = re.findall(r'\((\d+)cm.*?(\d+)kg', meta_data)[0]
  player_data['position'] = re.findall(r'Position\:?\s+(\w+\s?\w+)', meta_data)[0]
  player_data['shoots'] = re.findall(r'Shoots\:?\s+(\w+\s?\w+)', meta_data)[0]
  player_data['team'] = re.findall(r'Team\:?\s+(\w+\s?\w+)', meta_data)[0]
  player_data['college'] = re.findall(r'College\:?\s+(\w+\s?\w+)', meta_data)[0]
  player_data['height'] = int(height)
  player_data['weight'] = int(weight)
  
  # some of them just don't have following data,
  # so...
  try:
    player_data['born'] = meta_soup.find(id='necro-birth')['data-birth']
    # Easily broke here, pay attention to index
    player_data['nba_debut'] = all_paragraph[-2].a.get_text()
  except Exception:
    print("Well, well...")
  return player_data


def str2float(string: str, default=None):
  try:
    return float(string)
  except ValueError:
    if default == None:
      return string
    else:
      return default


def get_career_data(soup: Tag) -> dict:
  career_data = soup.find('div', {'class': 'stats_pullout'})
  career_data = career_data.select('div > p')[2:]
  career_data = [str2float(x.get_text(), 0) for x in career_data]
  player_career = {}
  player_career['G'] = career_data[1]
  player_career['PTS'] = career_data[3]
  player_career['TRB'] = career_data[5]
  player_career['AST'] = career_data[7]
  player_career['FG'] = career_data[9]
  player_career['FG3'] = career_data[11]
  player_career['FT'] = career_data[13]
  player_career['eFG'] = career_data[15]
  player_career['PER'] = career_data[17]
  player_career['WS'] = career_data[19]
  return player_career


def get_college_data(soup: Tag) -> dict:
  # I don't understand why they first comment the section
  # then uncomment it in runtime. Reduce rendering time?
  all_comments = soup.findAll(text=lambda x: isinstance(x, Comment))
  comment = list(filter(lambda x: 'College Table' in x, all_comments))[0]
  comment = BeautifulSoup(comment, 'html.parser')
  career_tr = comment.select('tfoot > tr')[0]
  
  def get_each_season(tr_soup: Tag):
    season_data = {}
    season_data['season'] = tr_soup.th.get_text()
    all_td = [str2float(x.get_text()) for x in tr_soup.findAll('td')][-7:]
    all_columns = ['FG', '3P', 'FT', 'MP', 'PTS', 'TRB', 'AST']
    for index, column in enumerate(all_columns):
      season_data[column] = all_td[index]
    return season_data
  
  career_tr = get_each_season(career_tr)
  return career_tr


def get_person(url: str) -> tuple:
  html_page = requests.get(url)
  html_page = html_page.content.decode('utf-8')
  drink_soup = BeautifulSoup(html_page, 'html.parser')
  player_info = get_player_info(drink_soup)
  career_data = get_career_data(drink_soup)
  college_data = get_college_data(drink_soup)
  return player_info, career_data, college_data


def get_person_list_by_year(year: int) -> list:
  url = YEAR_URL.format(year=year)
  year_html = requests.get(url).content.decode('utf-8')
  year_soup = BeautifulSoup(year_html, 'html.parser')
  year_soup = year_soup.find(id='stats')
  player_list = year_soup.select('tbody > tr')
  
  def handle_one_player(player: Tag) -> str:
    try:
      college_name = player.find('td', {'data-stat': 'college_name'}).get_text()
      one_attribute = player.find('td', {'data-stat': 'g'}).get_text()
    except AttributeError:
      return ''
    if not college_name or not one_attribute:
      return ''
    url = player.find('td', {'data-stat': 'player'}).a['href']
    return urllib.parse.urljoin(YEAR_URL, url)
  
  player_list = [handle_one_player(x) for x in player_list]
  return player_list


if __name__ == '__main__':
  # get_person('https://www.basketball-reference.com/players/d/dunnkr01.html')
  mysql = MysqlConnection()
  draft_year = 2016
  current_ID = 0
  person_list = get_person_list_by_year(draft_year)
  person_list = filter(None, person_list)
  for person_url in person_list:
    player_info, career_data, college_data = get_person(person_url)
    player_info['draft_year'] = draft_year
    player_info['ID'] = current_ID
    print(player_info)
    mysql.save_to_db(player_info, career_data, college_data)
    current_ID += 1
