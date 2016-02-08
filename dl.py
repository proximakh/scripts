#-*- coding: cp949 -*-

import urllib
import re
import os

# ������ ���� (������ �ٲ�� ���ο� ������ ����� �߰��ؾ� ��)
tribe_map = {
"���̼�":"T", "������":"T", "�赵��":"T", "������":"T",
"����":"T", "���ر�":"T", "����":"T", "�����":"T",
"������":"T", "���¾�":"T", "�����":"T", "Ȳ�Լ�":"T",
"������":"T", "�ڱ���":"T", "���缱":"T", "������":"T",
"������":"T", "�̽���":"T", "������":"T", "������":"T",
"�̿���":"Z", "����":"Z", "������":"Z", "�̿���":"Z",
"�ڷɿ�":"Z", "�̿���":"Z", "������":"Z", "Ȳ��ȣ":"Z",
"�����":"Z", "�̽���":"Z", "������":"Z", "���¼�":"Z",
"������":"Z", "������":"Z", "���μ�":"Z", "�̿�ǥ":"Z",
"�̺���":"Z", "�̵���":"Z", "������":"Z", "�ڼ�ȣ":"Z",
"���ö":"Z", "������":"Z",
"�ּ���":"P", "������":"P", "����ȣ":"P", "��뿱":"P",
"�Ȼ��":"P", "������":"P", "������":"P", "�鵿��":"P",
"������":"P", "������":"P", "�赵��":"P", "������":"P",
"�����":"P", "�����":"P", "�赵��":"P", "�ּ���":"P",
"������":"P", "�ۺ���":"P",
}

flags = re.MULTILINE | re.DOTALL | re.LOCALE

url_list_page = "http://afbbs.afreeca.com:8080/app/list_ucc_bbs.cgi?nStationNo=9521573&szBbsType=&szBjId=afgsl&nBbsNo=17669292&nPageNo=2&nRowNum=200&szOrderType=title_no&szBjId=afgsl&nBbsNo=17669292&szSkin=business&nRowNum=1000"
list_exp = re.compile('<a href="([^"]*)".*��ü���� / ([^/]*)')

url_item_page = "http://d-c.kr/af_Movie/info.php?"
item_exp = re.compile('([^\s]*)\s*vs\s*([^\s]*)\s*([0-9]*)[^0-9\s]* ([0-9]*)[^0-9\s]*')
season_exp = re.compile('[^A-Za-z]*([A-Za-z])\s*[^A-Za-z0-9]*([0-9])\s*([0-9]*)')

# url_list_page ���� "��ü����" �׸� URL ��������
body_list_page = urllib.urlopen(url_list_page)
objs = list_exp.findall(body_list_page.read(), flags)

# "��ü����" �׸� URL����
for matched in objs:
  params = matched[0].split("?")[1]

  # url_item_page �� URL�� �����ָ� ����URL, �������� ���� ����
  d = urllib.urlopen(url_item_page + params).read().decode('utf-8').encode('euc-kr').split("|")
  mv_url = d[0]     # ����URL
  mv_title = d[2]   # ��������
  m = mv_title.split("/")
  info0 = item_exp.search(m[1].strip()).groups()
  info1 = season_exp.search(m[2].strip()).groups()

  year = int(info1[2])          # �⵵
  season_no = int(info1[1])     # �����ȣ
  code = info1[0]               # �ڵ�S or �ڵ�A
  no_of_players = int(info0[2]) # �����
  game_no = int(info0[3])       # ���° ��������
  player_names = (info0[0] + tribe_map[info0[0]], info0[1] + tribe_map[info0[1]])   # (������+������, ������+������) tuple

  # ������ ���ϸ�
  # GSL_2016S1_CodeA_60��_29���_�̽���T_vs_�ۺ���P.mp4
  save_filename = "GSL_%dS%d_Code%s_%02d��_%02d���_%s_vs_%s.mp4" % (year, season_no, code, no_of_players, game_no, player_names[0], player_names[1])

  print save_filename

  # �̹� �����ϸ� �ٽ� ���� ����
  if os.path.isfile(save_filename):
    print "already exists. passing..."
    continue

  # ����
  sf = open(save_filename, "wb")
  print "saving..."
  data = urllib.urlopen(mv_url)
  sf.write(data.read())
  sf.close()
