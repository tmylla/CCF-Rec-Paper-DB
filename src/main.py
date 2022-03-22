import dblp
import pandas as pd
import re
import fire
from utils import *
from stat_info import *
from parse_html import Parse_HTML

def paper_details(paper_title:str):
    query = paper_title
    results = dblp.search(query, verbose=1)
    print(results)
    # pd.DataFrame(results).to_csv('output.csv', index=False)


def main(venue:str, no:int):

    parsed = {'venue_name': 'url'}  # 解析过的非dblp数据库的会议/期刊，需手动添加

    ccf_catalog = '../paper_db/ccf_catalog.csv'
    df = pd.read_csv(ccf_catalog)

    venue_info = df.query('abbr=="{}" | name=="{}"'.format(venue, venue))  # 指定会议所在行的信息，type-DataFrame
    paras = list()
    if len(venue_info)>1:  # 名称缩写重名，为此需要找到对应全称并赋值给venue
        for i in range(len(venue_info)):
            name = venue_info.iloc[i]['name']
            url = venue_info.iloc[i]['url']
            type = venue_info.iloc[i]['type']
            paras.append([name, url, type])
    else:
        name = venue
        url = venue_info['url'].to_list()[0]
        type = venue_info['type'].to_list()[0]
        paras.append([name, url, type])

    for para in paras:
        name, url, type = para[0], para[1], para[2]
        if 'http://dblp' in url or 'https://dblp' in url:  # dblp数据库
            Parse_HTML(name, url, type, no).parse_dblp()
        else:
            print(name, url)
            # if url in parsed.values():
            #     Parse_HTML(name, url, type, no).parse_specdb()
            # else:
            #     print("根据url自行解析html，重写arse_HTML(url).parse_newurl()函数。\n"
            #           "重写后将{'conf_name':'url'}添加到字典parsed！")


if __name__ == '__main__':
    # fire.Fire(main)
    set_logger()

    no = 8
    venue_list = ccf_filter(no, rank='A/B/C')

    for venue in venue_list:
        if venue in no_dblp:
            logging.info('"{}" in tmp_no_dblp!!'.format(venue))
        else:
            try:
                main(venue, no)
                logging.info('\n\n')
            except:
                logging.info('"{}" PARSED ERROR!!'.format(venue))



