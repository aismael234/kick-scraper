import pandas as pd
import ast

def main():
    # INSERT CHANNEL NAME
    channel = ""
    
    df = pd.read_csv('copy.csv', names=['id', 'title', 'thumbnail_url', 'privacy', 'date_created', '', 'creator', 'channel'])
    df = df.drop('', axis=1)
    df = df.drop('privacy', axis=1)
    df = df[['id', 'title', 'creator', 'channel', 'date_created', 'thumbnail_url']]
    df.insert(0,'link', [f'=HYPERLINK("https://kick.com/{channel}?clip={x}", "Link")' for x in df['id']])
    df['creator'] = [str(ast.literal_eval(x)['username']) for x in df['creator']]
    df['channel'] = [str(ast.literal_eval(x)['username']) for x in df['channel']]
    df.to_csv('links.csv', mode='w', header=not pd.io.common.file_exists('links.csv'), index=True)

if __name__ == "__main__":
    main()