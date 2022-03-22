# CCF Rec-Paper DB

[![license-MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/tmylla/CCF-Rec-Paper-DB/blob/main/LICENSE)

CCF推荐期刊/会议历年发表的论文数据库，包含数据库构建、数据库检索、数据库更新功能。

# 目录

- [CCF Rec-Paper DB](#CCF Rec-Paper DB)
- [目录](#目录)
- [项目介绍](#项目介绍)
- [目录结构](#目录结构)
- [安装说明](#安装说明)
- [使用说明](#使用说明)
- [鸣谢](#鸣谢)
- [版权信息](#版权信息)

# 项目简介

## CCF推荐会议与期刊（2019版）

- 根据研究领域将期刊/会议细分为10类

  > 1-计算机体系结构/并行与分布计算/存储系统；    6-计算机科学理论
  > 2-计算机网络；														 7-计算机图形学与多媒体
  > 3-网络与信息安全；												 8-人工智能
  > 4-软件工程/系统软件/程序设计语言；				   9-人机交互与普适计算
  > 5-数据库/数据挖掘/内容检索；							  10-交叉/综合/新兴

- 共计612个期刊/会议，其中20个期刊/会议有单独`url`，其余均可在`dblp`数据库检索。

  ```python
  no_dblp = ['Performance Evaluation: An International Journal', 'JETTA', 'JGC', 'HOT CHIPS', 'TOPS', 'CLSR', 'IFIP WG 11.9', 'HotSec', 'QRS', 'JGITM', 'JASA', 'CAVW', 'JSLHR', 'IET-CVI', 'IET Signal Processing', 'CollaborateCom', 'Cognition', 'IET Intelligent Transport Systems', 'CogSci', 'ISMB']
  ```

## 项目介绍

该项目的主要目的是：**在调研某个领域的顶刊/顶会文章时，不再“一个个期刊，一场场会议，一年又一年的重复性关键词查找”，只需“领域类别、关键词、A/B/C等级（可选）、最近n年（可选）”就可即时返回CCF推荐期刊/会议的相关论文**。

`./src/main.py`搜集整理CCF推荐期刊/会议发表的论文，`./paper_db`存储抓取到的论文数据，`./src/search_db.py`根据自定义选项对论文数据库进行检索。

![Conference](https://gitee.com/misite_J/blog-img/raw/master/img/Conference.png)

![Journal](https://gitee.com/misite_J/blog-img/raw/master/img/Journal.png)

论文数据库

- 每个会议/期刊单独存储为一个`.json`文件，依类别保存在`./paper_db/{no.}`文件夹
- 期刊/会议的数据类型略有不同，如上图所示，`.json`示例可见[期刊](https://raw.githubusercontent.com/tmylla/CCF-Rec-Paper-DB/main/paper_db/3/TDSC.json)/[会议](https://raw.githubusercontent.com/tmylla/CCF-Rec-Paper-DB/main/paper_db/3/DIMVA.json)

数据库构建

- 当前已构建类别“3-网络与信息安全”和“8-人工智能”历年论文数据库，其余类别后续上传或用户自行构建，构建流程可见[使用说明](#使用说明)部分
- 由于612个期刊/会议中大多数均可在`bdlp`数据库检索，`./src/parse_html.py`目前仅提供了`bdlp`的解析，对其余20个期刊/会议，暂需自行到对应网站查找，后续有时间会补充对`no_bdlp`期刊/论文的解析；
- 数据库的更新（*TODO*）

数据库检索

- 输入“领域类别、关键词、A/B/C等级（可选）、最近n年（可选）”，返回“所选领域近n年A/B/C期刊和会议发表论文的标题包含关键词（可多个）的论文标题列表”

- 借助[dblp-api](https://github.com/alumik/dblp-api)检索特定论文的详细信息

  ```json
  {
      'Query': 'Anomaly Detection in Streams with Extreme Value Theory',
      'Title': 'Anomaly Detection in Streams with Extreme Value Theory.',
      'Year': '2017',
      'Venue': 'KDD',
      'CCF Class': 'A',
      'DOI': '10.1145/3097983.3098144',
      'URL': 'https://doi.org/10.1145/3097983.3098144',
      'BibTeX': 'https://dblp.org/rec/conf/kdd/SifferFTL17?view=bibtex'
  }
  ```

  

# 目录结构

```shell
CCF Rec-Paper DB
├─ dblp  # 开源项目dblp_api，用于根据标题检索详细信息
│    ├─ __init__.py
│    ├─ api.py
│    └─ data
│           └─ ccf_catalog.csv
├─ paper_db  # 论文数据库
│    ├─ 3  # 领域类别
│    │    ├─ ACISP.json  # 一会/一刊一文件
│    │    ├─ ...
│    ├─ 8
│    │    ├─ AAAI.json
│    │    ├─ ...
│    └─ ccf_catalog.csv
├─ pic
│    ├─ Conference.png
│    └─ Journal.png
└─ src
│    ├─ __init__.py
│    ├─ db_search.py  # 数据库检索
│    ├─ main.py  # 数据库构建
│    ├─ parse_html.py
│    ├─ stat_info.py
│    └─ utils.py
├─ requirements.txt
├─ LICENSE
├─ README.md
```



# 安装说明

1. `git clone git@github.com:tmylla/CCF-Rec-Paper-DB.git`
2. 解压缩

## 环境依赖

> pip install -r requirements.txt

- beautifulsoup4==4.10.0
- pandas==1.3.5
- requests==2.26.0
- tqdm==4.62.3

# 使用说明

功能1：数据库构建（面向开发者）

- src：`python main.py`
- input：CCF期刊/会议类别，范围1-10
- output：无，指定类别下的期刊/会议论文存储到`.json`文件，内容包含录用数量，论文名称等信息

**功能2：数据库检索（面向使用者）**

使用时首先查看`paper_db`是否存在相应类别数据库，如果存在，直接检索；否则，先构建数据库，然后检索。

- src：`python db_search.py`
- input：no - 期刊/会议对应类别、rank - 期刊/会议检索等级，形如'A/B/C'，year - 查找近n年的论文，0表示全部年份、key_words（可选） - 关键词，多个可用';'划分，可以不输入
- output：list(papers) - 类别{no}近{year}年的{rank}期刊/会议发表的{len(papers)}篇论文标题；list(key_papers) - 其中标题含关键字{key_words}的{len(key_papers)}篇论文标题

功能3：数据库更新（面向开发者）

- src：*TODO*
- input：会议/期刊名称，年份
- output：无（相应数据库数据增加）



# 鸣谢

该项目参考了[alumik](https://github.com/alumik)的[dblp-api](https://github.com/alumik/dblp-api)

# 版权信息

该项目签署了MIT 授权许可，详情请参阅 [LICENSE](https://github.com/tmylla/CCF-Rec-Paper-DB/blob/main/LICENSE)

# TODO

- [ ] `no_dblp`数据库解析
- [ ] 数据库更新
- [ ] 类别3/8之外其他类别数据库扩充