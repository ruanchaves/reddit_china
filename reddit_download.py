import requests
import argparse
from urllib.parse import urljoin
from urllib.request import urlretrieve
import os
import pandas as pd
from itertools import groupby
import pathlib
from loguru import logger

_default_urls = {
    "submission": "https://files.pushshift.io/reddit/submissions/",
    "comment": "https://files.pushshift.io/reddit/comments/"
}

_SUBMISSION_URL = os.environ.get("SUBMISSION_URL", _default_urls["submission"])
_COMMENT_URL = os.environ.get("COMMENT_URL", _default_urls["comment"])


def url_exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--start_year', action='store', type=int, default=2015)
    parser.add_argument('--end_year', action='store', type=int, default=2021)
    parser.add_argument('--start_month', action='store', type=int, default=1)
    parser.add_argument('--end_month', action='store', type=int, default=12)
    parser.add_argument('-ns', '--no_submission', action='store_true')
    parser.add_argument('-nc', '--no_comment', action='store_true')
    parser.add_argument('--submission_dir', action='store', type=str, default="./submission")
    parser.add_argument('--comment_dir', action='store', type=str, default="./comment")
    parser.add_argument('--extensions', action='store', type=str, default="zst,bz2")
    args = parser.parse_args()
    return args

def generate_date_range(start_year, end_year, start_month, end_month):
    output = pd.date_range(
        start=f"{start_year}-{start_month}-01",
        end=f"{end_year}-{end_month}-01").to_pydatetime().tolist()
    output = [ str(x)[0:7] for x in output ]
    output = [key for key, _group in groupby(output)]
    return output

def get_urls(start_year, end_year, start_month, end_month, submission=True, comment=True, extensions=None):
    submission_urls = []
    comment_urls = []
    submission_filenames = []
    comment_filenames = []
    for date in generate_date_range(
            start_year,
            end_year,
            start_month,
            end_month):
        for extension in extensions:
            if submission:
                submission_urls.append(urljoin(_SUBMISSION_URL, f'RS_{date}.{extension}'))
                submission_filenames.append(f'RS_{date}.{extension}')

        for extension in extensions:
            if comment:
                comment_urls.append(urljoin(_COMMENT_URL, f'RC_{date}.{extension}'))
                comment_filenames.append(f'RC_{date}.{extension}')
    return submission_urls, submission_filenames, comment_urls, comment_filenames

def download_dumps(
    start_year, 
    end_year, 
    start_month, 
    end_month, 
    submission=True, 
    comment=True, 
    extensions=None,
    submission_dir=None,
    comment_dir=None):
    submission_urls, submission_filenames, comment_urls, comment_filenames = get_urls(
            start_year,
            end_year,
            start_month,
            end_month,
            submission=submission,
            comment=comment,
            extensions=extensions)
    
    for url, filename in zip(submission_urls, submission_filenames):
        if url_exists(url):
            logger.debug(f"Downloading {url}.")
            urlretrieve(url, os.path.join(submission_dir, filename))
        else:
            logger.debug(f"{url} does not exist. Skipping.")
    for url, filename in zip(comment_urls, comment_filenames):
        if url_exists(url):
            logger.debug(f"Downloading {url}.")
            urlretrieve(url, os.path.join(comment_dir, filename))    
        else:
            logger.debug(f"{url} does not exist. Skipping.")

def main():
    args = get_args()

    logger.debug(args)

    pathlib.Path(args.submission_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.comment_dir).mkdir(parents=True, exist_ok=True)
    
    extensions = args.extensions.split(",")

    download_dumps(
        args.start_year, 
        args.end_year, 
        args.start_month, 
        args.end_month, 
        submission=not args.no_submission, 
        comment=not args.no_comment, 
        extensions=extensions,
        submission_dir=args.submission_dir,
        comment_dir=args.comment_dir)

if __name__ == '__main__':
    main()