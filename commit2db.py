import pymysql.cursors


class MysqlConnection():
  def __init__(self):
    self.mysql_conn = self.get_conn()
    self.cursor = self.mysql_conn.cursor()
    self.player_id = 0
  
  def get_conn(self):
    mysql_conn = pymysql.connect(
      host='127.0.0.1',
      user='root',
      password='root',
      port=3306,
      db='nba_patricks_draft',
      charset='utf8mb4',
      cursorclass=pymysql.cursors.DictCursor
    )
    return mysql_conn
  
  def save_to_db(self, player_info: dict, career_data: dict, college_data: dict):
    self.player_id = player_info.get('ID', '')
    self.save_player_info(player_info)
    self.save_career_data(career_data)
    self.save_player_college(college_data)
    self.mysql_conn.commit()
  
  def save_player_college(self, college_data: dict):
    sql = "insert into player_college VALUE (%s,%s,%s,%s,%s,%s,%s,%s)"
    self.cursor.execute(sql, (
      self.player_id, college_data.get('FG', 0), college_data.get('3P', 0), college_data.get('FT', 0),
      college_data.get('MP', 0), college_data.get('PTS', 0), college_data.get('TRB', 0), college_data.get('AST', 0)
    ))
  
  def save_career_data(self, career_data: dict):
    sql = "insert into player_career values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    self.cursor.execute(sql, (
      self.player_id, career_data.get('G', 0), career_data.get('PTS', 0), career_data.get('TRB', 0),
      career_data.get('AST', 0),
      career_data.get('FG', 0), career_data.get('FG3', 0), career_data.get('FT', 0), career_data.get('eFG', 0),
      career_data.get('PER', 0), career_data.get('WS', 0)
    ))
  
  def save_player_info(self, player_info: dict):
    sql = "insert into player_info(ID,name,weight,height,position,shoots,born,college,nba_debut,draft_year,team)" \
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    self.cursor.execute(sql, (
      self.player_id, player_info.get('name', ''), player_info.get('weight', 0), player_info.get('height', 0),
      player_info.get('position', ''), player_info.get('shoots', ''), player_info.get('born', ''),
      player_info.get('college', ''),
      player_info.get('nba_debut', ''), player_info.get('draft_year', 0), player_info.get('team', ''),
    ))
