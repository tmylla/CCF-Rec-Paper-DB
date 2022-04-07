import json
from utils import ccf_filter, ccf_duplicate_abbr
from stat_info import no_dblp
import dblp


class Search_Paper_DB():
    def __init__(self, no, rank='A/B/C', year=0):
        '''
        对CCF推荐期刊/会议数据库Paper_DB的检索
        :param no: 整数型，期刊/会议类别，可选1-10
        :param rank: 字符型，期刊/会议等级，以'/'分隔；默认'A/B/C'全选
        :param year: 整数型，检索最近n年的论文；'0'表示所有年份
        :param key_words: 字符型，检索关键词，以';'分隔，默认为空
        '''
        super(Search_Paper_DB, self).__init__()
        self.no = no
        self.rank = rank
        self.year = year


    def search_papers(self):
        '''
        根据检索条件返回检索条件的论文标题列表
        '''
        venue_list = ccf_filter(self.no, self.rank)

        papers = list()
        for venue in venue_list:
            if venue not in no_dblp:
                with open('../paper_db/{}/{}.json'.format(self.no, venue), 'r', encoding='utf-8') as f:
                    db_info = json.load(f)

                n_years = len(db_info) if self.year==0 else self.year
                for n in range(n_years):
                    if 'count' in list(db_info[n].keys()):  # 期刊
                        papers.extend(db_info[n]['papers'])
                    else:  # 会议
                        for sub_venue in db_info[n]['venues']:
                            papers.extend(sub_venue['papers'])

        return list(set(papers))


    def key_words_search(self, key_words, papers):
        key_papers = list()
        for key_word in key_words.split(';'):
            for paper in papers:
                if key_word.isupper():  # 关键词大写时如KG要准确匹配
                    if key_word.strip() in paper:
                        key_papers.append(paper)
                else:
                    if key_word.strip() in paper.lower():
                        key_papers.append(paper)

        return list(set(key_papers))


    # TODO
    # 通过dblp检索得到论文摘要后，查找关键词时同时检索摘要

if __name__ == '__main__':
    no = int(input("期刊/会议对应类别："))
    rank = input("期刊/会议检索等级，形如'A/B/C'：")
    year = int(input("查找近n年的论文，0表示全部年份："))
    key_words = input("关键词，多个可用';'划分，可以不输入：")

    search_tool = Search_Paper_DB(no, rank, year)
    papers = search_tool.search_papers()
    # print('类别{}近{}年的{}期刊/会议发表论文共{}篇：\n{}'.format(no, year, rank, len(papers), papers))

    if key_words:
        key_papers = search_tool.key_words_search(key_words, papers)
        print('其中标题含关键字‘{}’的论文共{}篇：\n{}'.format(key_words, len(key_papers), key_papers))

    # TODO key_papers -> chosen_paper，UI中点击相应论文标题，dblp.search查找详细信息
    # detail_info = dblp.search(chosen_papers)