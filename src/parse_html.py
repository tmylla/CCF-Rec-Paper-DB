import json
import re
from tqdm import tqdm
from bs4 import BeautifulSoup
from utils import *

class Parse_HTML(object):
    def __init__(self,name, url, type, no):
        '''
        :param url: C/J's url provided by ccf
        :param type: Journal / Conference
        '''
        super(Parse_HTML, self).__init__()
        self.venue = name
        self.url = url
        self.type = type
        self.no = no
        self.html_doc = FetchUrl(self.url)
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')

    def parse_dblp(self):
        '''
        dblp某一会议/期刊页面为入口，解析当前页面（即历年开会/期刊目录）和下一页面（每一年/刊的收录论文）；
        每一会议/期刊存储为一个json文件；
        '''
        if self.type =='Conference':
            if self.venue in ['CCS', 'AsiaCCS']:
                paper_db = self.dblp_ccs_type()
            else:
                paper_db = self.dblp_conf_frame()
        elif self.type == 'Journal':
            paper_db = self.dblp_jour_frame()
        else:
            logging.info('param type: Journal / Conference')

        with open('../paper_db/{}/{}.json'.format(self.no, self.venue), 'w', encoding='utf-8') as f:
            json.dump(paper_db, f, indent=4)


    def dblp_conf_frame(self):
        # 该函数解析页面格式见'http://dblp.uni-trier.de/db/conf/aaai/'

        # 有的会议近几年的论文发表在期刊上，见‘https://dblp.uni-trier.de/db/conf/fse/index.html’
        # 这些论文需要解析新的journal url
        try:
            h2_1st = self.soup.find_all('h2')[1]  # 第一个会议的h2标签
            jour_info = h2_1st.parent.previous_sibling  # 新的journal url在第一个会议h2标签的前一个兄弟标签
            new_url = jour_info.a['href']
            new_venue = self.venue + ' / ' + jour_info.text

            paper_db = dblp_jour_frame_copy(new_venue, new_url)
        except:
            paper_db = list()


        for yearly_info in self.soup.find_all('h2'):
            # yearly_info example:
            #   <h2 id = "2022"> 36th AAAI / 34nd <a href =
            #   "https://dblp.uni-trier.de/db/conf/iaai/index.html"> IAAI </a> 2022: Virtual Event </h2>
            db_year = dict()
            if yearly_info.attrs:
                db_year['year'] = str(yearly_info.attrs['id'])  # 会议举行年份
                if ': ' in yearly_info.text:
                    db_year['name'] = yearly_info.text.split(': ')[0]
                    db_year['info'] = yearly_info.text.split(': ')[1]
                else:
                    db_year['name'] = yearly_info.text
                    db_year['info'] = ''
                db_year['venues'] = list()

            if db_year:
                paper_db.append(db_year)

        # 获取年度会议（期刊）的子会场（期卷），同时获取跳转下一页面（论文页面）的url
        for sub_venues_yearly in self.soup.find_all('ul',
                                               attrs={'class': 'publ-list'}):  # 所有年份会议的若干子类，如workshop，每一个子类是一个block
            for sub_venue_info in sub_venues_yearly.find_all('li', attrs={'class': "entry editor toc"}):
                db_sub_venue = dict()

                sub_name = sub_venue_info.find('span', attrs={'class': 'title'}).text
                db_sub_venue['sub_name_abbr'] = sub_venue_info['id']
                db_sub_venue['sub_name'] = sub_name
                db_sub_venue['count'] = 0
                db_sub_venue['papers'] = list()

                # 由于html中年度会议与子会场没有上下级（包含）关系，为此需要记录子会场年份，后续根据子会场的年份将子会场信息置于db_year['venues']之内
                pattern = re.compile('(19|20)[0126789][0-9]')
                if re.search(pattern, sub_name):  # sub_name中无年份信息时，将publish_year赋值给conf_year
                    conf_year = re.search(pattern, sub_name).group()
                else:
                    conf_year = sub_venue_info.find('span', attrs={'itemprop': 'datePublished'}).text
                logging.info('{}\t{}'.format(self.venue, conf_year))

                publish_year = sub_venue_info.find('span', attrs={'itemprop': 'datePublished'}).text
                if conf_year != publish_year:
                    logging.info('从标题中正则匹配的年份{}与出版年份{}不匹配，人工核查！'.format(conf_year, publish_year))

                may_contain_new_url = sub_venue_info.find('a', attrs={'class': 'toc-link'}, text='[contents]')
                try:
                    paper_page_url = may_contain_new_url['href']
                except:
                    logging.info('{}-{}没有得到论文页面跳转url！！！'.format(self.venue, conf_year))
                    continue

                try:
                    new_html_doc = FetchUrl(paper_page_url)
                except:
                    logging.info('未能获取链接页面有效内容{}'.format(paper_page_url))
                    continue
                new_soup = BeautifulSoup(new_html_doc, 'html.parser')

                papers_sub_venue = new_soup.find_all('li', attrs={'class': 'entry inproceedings'})
                if not papers_sub_venue:
                    papers_sub_venue = new_soup.find_all('li', attrs={'class': 'entry incollection'})
                db_sub_venue['count'] = len(papers_sub_venue)

                paper_titles = list()
                for paper_info in tqdm(papers_sub_venue):
                    paper_title = paper_info.find('span', attrs={'class': 'title'}).text
                    paper_titles.append(paper_title)

                db_sub_venue['papers'] = paper_titles

                # 根据子会场的年份将子会场信息置于db_year['venues']之内
                for i, db_year in enumerate(paper_db):
                    if db_year['year'] == conf_year:
                        idx = i

                paper_db[idx]['venues'].append(db_sub_venue)

        # 有的会议论文列表两种形式混杂，见‘https://dblp.uni-trier.de/db/conf/ches/index.html’
        # 处理完只有一种形式后，对另一种形式单独处理,判断依据'Proccedings published in' in text
        # 多数会议子会场形式只有一种形式，执行该步骤paper_db不会有任何改变；含两种形式的则会新增数据
        for p_soup in self.soup.find_all('p'):
            if 'Proccedings published in' in p_soup.text:
                db_sub_venue, conf_year = dblp_conf_two_type(p_soup, self.venue)
                for i, db_year in enumerate(paper_db):
                    if db_year['year'] == conf_year:
                        idx = i
                paper_db[idx]['venues'].append(db_sub_venue)

        return paper_db

    def dblp_ccs_type(self):
        # 不同于AAAI中主论坛与workshop在同一层次下，CCS中workshop单独列出在页面顶部，见https://dblp.uni-trier.de/db/conf/ccs/index.html
        # 该函数解析类CCS这样的dblp会议数据。首先获得主框架信息paper_db后，然后将workshop加入对应年份的子会场
        # 已进行统计，在所有CCF推荐会议中，只有CCS这样Orz...
        paper_db = self.dblp_conf_frame()

        workshops_html = self.soup.find('p', text='Workshops:').next_sibling
        workshops = workshops_html.find_all('li', recursive=False)
        for ws in workshops:
            ws_info = ws.text.split(':')[0]
            sub_name_abbr = ws_info.split(' -')[0].strip()
            sub_name = ws_info.split(' -')[1].strip()

            for ws_yearly in ws.find_all('a'):  # 不同年份的workshop html链接
                db_sub_venue = dict()
                db_sub_venue['sub_name_abbr'] = sub_name_abbr
                db_sub_venue['sub_name'] = sub_name
                db_sub_venue['count'] = 0
                db_sub_venue['papers'] = list()

                ws_text = ws_yearly.text  # 举办年份，根据年份将workshop相关信息加入到主框架的paper_db['venue']
                ws_url = ws_yearly['href']

                if re.match('^\d{4}$', ws_text):
                    ws_year = ws_text
                    logging.info('Workshop - {}: {}'.format(sub_name_abbr, ws_year))

                    try:
                        new_html_doc = FetchUrl(ws_url)
                        new_soup = BeautifulSoup(new_html_doc, 'html.parser')
                    except:
                        logging.info("html 解析出错")
                        continue

                    papers_sub_venue = new_soup.find_all('li', attrs={'class': 'entry inproceedings'})
                    db_sub_venue['count'] = len(papers_sub_venue)

                    paper_titles = list()
                    for paper_info in tqdm(papers_sub_venue):
                        paper_title = paper_info.find('span', attrs={'class': 'title'}).text
                        paper_titles.append(paper_title)

                    db_sub_venue['papers'] = paper_titles

                    # 根据子会场的年份将子会场信息置于db_year['venues']之内
                    for i, db_year in enumerate(paper_db):
                        if db_year['year'] == ws_year:
                            idx = i

                    paper_db[idx]['venues'].append(db_sub_venue)

        return paper_db

    def dblp_jour_frame(self):
        paper_db = list()

        main_content = self.soup.find('div', attrs={'id': 'main'})

        volume_block = list()
        for chil in main_content.children:  # 在主页面定位包含含论文页url的block
            if chil.name == 'ul':
                try:
                    tmp = chil.li.a
                    volume_block.append(chil)
                except:
                    continue

        volumes = list()
        for block in volume_block:
            volumes.extend(block.find_all('li'))

        for volume in volumes:
            try:
                db_year = dict()
                db_year['name'] = self.venue

                pattern = re.compile('(19|20)[0126789][0-9]')
                conf_year = re.search(pattern, volume.text).group()

                db_year['year'] = conf_year  # 出版年份
                db_year['info'] = volume.text.strip()  # 该年度出版的卷编号
                db_year['count'] = 0
                db_year['papers'] = list()

                # 获取年度期刊的子卷，同时获取跳转下一页面（论文页面）的url
                vol_url_tags = volume.find_all('a')
                paper_titles = list()
                for a_tag in vol_url_tags:
                    paper_page_url = a_tag['href']

                    new_html_doc = FetchUrl(paper_page_url)
                    new_soup = BeautifulSoup(new_html_doc, 'html.parser')

                    papers_sub_venue = new_soup.find_all('li', attrs={'class': 'entry article'})
                    db_year['count'] += len(papers_sub_venue)

                    logging.info('{}\t{}'.format(self.venue, db_year['year']))
                    for paper_info in tqdm(papers_sub_venue):
                        paper_title = paper_info.find('span', attrs={'class': 'title'}).text
                        paper_titles.append(paper_title)

                db_year['papers'] = paper_titles
                paper_db.append(db_year)
            except:
                pass

        return paper_db

    def parse_specdb(self):
        pass

    def parse_newurl(self):
        pass