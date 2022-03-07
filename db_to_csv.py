import argparse
import pandas as pd
import sqlite3
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', action='store', type=str, default="China, china")
    parser.add_argument('--fields', action='store', type=str, default="body,title,selftext")
    parser.add_argument('--submission_dir', action='store', type=str, default="./submission")
    parser.add_argument('--comment_dir', action='store', type=str, default="./comment")
    parser.add_argument("--submission_output", action='store', type=str, default="./submission.csv")
    parser.add_argument("--comment_output", action='store', type=str, default="./comment.csv")
    parser.add_argument('--database_path', action='store', type=str, default="./data.db")
    args = parser.parse_args()
    return args 

def save_or_append_dataframe(df, filepath):
    if os.path.isfile(filepath):
        df.to_csv(filepath, header=False, index=False, mode = 'a')
    else:
        df.to_csv(filepath, index=False)

def main():
    args = get_args()
    conn = sqlite3.connect(args.database_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA case_sensitive_like = 1;")

    keywords = args.keywords.split(",")
    keywords = [k.strip() for k in keywords]

    fields = args.fields.split(",")
    fields = [f.strip() for f in fields]

    for field in fields:
        for keyword in keywords:
            try:
                df = pd.read_sql(f"SELECT * FROM submission WHERE {field} LIKE '%{keyword}%';", conn)
                save_or_append_dataframe(df, args.submission_output)
            except pd.io.sql.DatabaseError:
                pass

            try:
                df = pd.read_sql(f"SELECT * FROM comment WHERE {field} LIKE '%{keyword}%';", conn)
                save_or_append_dataframe(df, args.comment_output)
            except pd.io.sql.DatabaseError:
                pass

if __name__ == '__main__':
    main()