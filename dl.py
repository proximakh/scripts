#-*- coding: cp949 -*-

import urllib
import re
import os

# 종족
tribes = ["T", "Z", "P"]

# 종족별 유저 (관리를 편하게 하기 위해 가나다 순으로 list로 만들어 둠)
tribe_players_map = {
  "T": [ "고병재", "김기용", "김기현", "김도욱", "김지성", "노준규", "박근일", "변현우", "서태희", "윤영서", "이신형", "이재선", "전태양", "정우용", "정지훈", "조성주", "조중혁", "최지성", "한이석", "황규석", ],
  "Z": [ "강동현", "강민수", "고석현", "김민철", "김준혁", "박령우", "박수호", "박진혁", "방태수", "신희범", "어윤수", "이동녕", "이병렬", "이승현", "이영한", "이예훈", "이원주", "이원표", "이제동", "한지원", "현성민", "황강호", ],
  "P": [ "김대엽", "김도경", "김도우", "김명식", "김유진", "김준호", "남기웅", "백동준", "변영봉", "서성민", "송병구", "송현덕", "안상원", "이형섭", "장현우", "조성호", "조지현", "주성욱", "최성일", "한재운", ],
}

# 유저별 종족 (탐색을 빠르게 하기 위해 dictionary로 만들어 둠)
tribe_map = {}

for t in tribes:
  for p in tribe_players_map[t]:
    tribe_map[p] = t


flags = re.MULTILINE | re.DOTALL | re.LOCALE

url_list_page = "http://afbbs.afreeca.com:8080/app/list_ucc_bbs.cgi?nStationNo=9521573&szBbsType=&szBjId=afgsl&nBbsNo=17669292&nPageNo=2&nRowNum=200&szOrderType=title_no&szBjId=afgsl&nBbsNo=17669292&szSkin=business&nRowNum=1000"
list_exp = re.compile('<a href="([^"]*)".*전체보기 / ([^/]*)')

url_item_page = "http://d-c.kr/af_Movie/info.php?"
item_exp = re.compile('([^\s]*)\s*vs\s*([^\s]*)\s*([0-9]*)[^0-9\s]* ([0-9]*)[^0-9\s]*')
season_exp = re.compile('[^A-Za-z]*([A-Za-z])\s*[^A-Za-z0-9]*([0-9])\s*([0-9]*)')

# url_list_page 에서 "전체보기" 항목만 URL 가져오기
body_list_page = urllib.urlopen(url_list_page)
objs = list_exp.findall(body_list_page.read(), flags)

# "전체보기" 항목 URL마다
for matched in objs:
  params = matched[0].split("?")[1]

  # url_item_page 에 URL을 보내주면 영상URL, 영상제목 등이 나옴
  d = urllib.urlopen(url_item_page + params).read().decode('utf-8').encode('euc-kr').split("|")
  mv_url = d[0]     # 영상URL
  mv_title = d[2]   # 영상제목
  m = mv_title.split("/")
  info0 = item_exp.search(m[1].strip()).groups()
  info1 = season_exp.search(m[2].strip()).groups()

  year = int(info1[2])          # 년도
  season_no = int(info1[1])     # 시즌번호
  code = info1[0]               # 코드S or 코드A
  no_of_players = int(info0[2]) # 몇강인지
  game_no = int(info0[3])       # 몇번째 게임인지
  player_names = (info0[0] + tribe_map[info0[0]], info0[1] + tribe_map[info0[1]])   # (선수명+종족명, 선수명+종족명) tuple

  # 저장할 파일명
  # GSL_2016S1_CodeA_60강_29경기_이신형T_vs_송병구P.mp4
  save_filename = "GSL_%dS%d_Code%s_%02d강_%02d경기_%s_vs_%s.mp4" % (year, season_no, code, no_of_players, game_no, player_names[0], player_names[1])

  print save_filename

  # 이미 존재하면 다시 받지 않음
  if os.path.isfile(save_filename):
    print "already exists. passing..."
    continue

  # 저장
  sf = open(save_filename, "wb")
  print "saving..."
  data = urllib.urlopen(mv_url)
  sf.write(data.read())
  sf.close()
