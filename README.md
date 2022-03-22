# CCF Rec-Paper DB

[![license-MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/AlumiK/dblp-api/blob/main/LICENSE)

A helper package to get information of scholarly articles from [DBLP](https://dblp.uni-trier.de/) using its public API.



[TOC]

# 项目简介

功能1：数据库构建
    输入：会议/期刊名称（必选）
    输出：录用数量，论文名称等信息
    
功能2：数据库检索
    输入：关键词，年份（默认所有年份）
    输入：精简模式（标题），
    
功能3：数据库更新
    输入：会议名称，年份
    输入：无（数据库数据增加）
    

- 一个会议/期刊存一个数据库
- 使用时首先检索是有存在查询数据库，如果存在，直接检索；否则，先抓取数据库，然后检索
- 数据库的更新（手动）



# 目录结构



# 安装说明



# 使用说明

## Usage

```python
import dblp

queries = [...]

# verbose > 0: Print out search results for each query.
results = dblp.search(queries, verbose=1)
```

## Examples



```python
import dblp

queries = [
    'Anomaly Detection in Streams with Extreme Value Theory',
    'Intelligent Detection of Large-Scale KPI Streams Anomaly Based on Transfer Learning',
]

results = dblp.search(queries)
```

The results will be:

```python
[
    {
        'Query': 'Anomaly Detection in Streams with Extreme Value Theory',
        'Title': 'Anomaly Detection in Streams with Extreme Value Theory.',
        'Year': '2017',
        'Venue': 'KDD',
        'CCF Class': 'A',
        'DOI': '10.1145/3097983.3098144',
        'URL': 'https://doi.org/10.1145/3097983.3098144',
        'BibTeX': 'https://dblp.org/rec/conf/kdd/SifferFTL17?view=bibtex'
    },
    {
        'Query': 'Intelligent Detection of Large-Scale KPI Streams Anomaly Based on Transfer Learning',
        'Title': 'N/A',
        'Year': 'N/A',
        'Venue': 'N/A',
        'CCF Class': 'N/A',
        'DOI': 'N/A',
        'URL': 'N/A',
        'BibTeX': 'N/A'
    }
]
```







# 鸣谢

该项目参考了[alumik](https://github.com/alumik)的[dblp-api](https://github.com/alumik/dblp-api)

# 版权信息

该项目签署了MIT 授权许可，详情请参阅 [LICENSE]()