# CCF Rec-Paper DB

[![license-MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/tmylla/CCF-Rec-Paper-DB/blob/main/LICENSE)

CCF推荐期刊/会议历年发表的论文数据库，包含数据库构建、数据库检索、数据库更新功能。

# 目录

- [CCF Rec-Paper DB](# CCF Rec-Paper DB)
- [目录](# 目录)
- [项目介绍](# 项目介绍)
- [文件目录](# 文件目录)
- [安装说明](# 安装说明)
- [使用说明](# 使用说明)
- [鸣谢](# 鸣谢)
- [版权信息](# 版权信息)

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



- 一个会议/期刊存一个数据库
- 使用时首先检索是有存在查询数据库，如果存在，直接检索；否则，先抓取数据库，然后检索
- 数据库的更新（手动）



功能1：数据库构建
    输入：会议/期刊名称（必选）
    输出：录用数量，论文名称等信息
    
功能2：数据库检索
    输入：关键词，年份（默认所有年份）
    输入：精简模式（标题），
    
功能3：数据库更新
    输入：会议名称，年份
    输入：无（数据库数据增加）
    

- 



# 文件目录



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

该项目签署了MIT 授权许可，详情请参阅 [LICENSE](https://github.com/tmylla/CCF-Rec-Paper-DB/blob/main/LICENSE)