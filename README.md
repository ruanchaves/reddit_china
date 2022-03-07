# reddit_keywords

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ruanchaves/reddit_keywords/blob/master/reddit.ipynb) 

Extract submissions and comments from Reddit based on keywords. 

<h3> <a href="https://colab.research.google.com/github/ruanchaves/reddit_keywords/blob/master/reddit.ipynb"> Colab notebook </a> </h3>

# Installation

```
pip install pandas loguru requests sqlite3

git clone https://github.com/Paul-E/Pushshift-Importer.git
git clone https://github.com/ruanchaves/reddit_keywords.git

```

# Examples

Extract all submissions and comments with the keyword "China" from 01/2015 to 06/2015.

```
cd reddit_keywords
python reddit_download.py --start_year 2015 --end_year 2015 --start_month 1 --end_month 6
bash build_db.sh
python db_to_csv.py --keywords "China,china" --fields "body,title,selftext"
```

For more details about the options, see also: [Pushshift-Importer](https://github.com/Paul-E/Pushshift-Importer)