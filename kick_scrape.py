import asyncio
import nodriver as nd
import random
import json
import pandas as pd
import os
import time

cursor_file = 'cursor.txt'
csv_file = 'clips_data.csv'

def append_to_csv(df, file_name):
    try:
        df.to_csv(file_name, mode='a', header=not pd.io.common.file_exists(file_name), index=True)
    except Exception as e:
        print(f"Failed to write to CSV: {e}")
        
def read_cursor():
    if os.path.isfile(cursor_file):
        with open(cursor_file, 'r') as file:
            return file.read().strip()
    return None

def write_cursor(cursor):
    with open(cursor_file, 'w') as file:
        file.write(cursor)
        


async def main():
    # INSERT CHANNEL NAME
    channel = ""
    
    cursor = read_cursor() or '0'
    more_data = True
    base_url = f'https://kick.com/api/v2/channels/{channel}/clips'
    
    if not channel:
        raise ValueError("The 'channel' variable must be set to a valid channel name.")
            
    browser = await nd.start()

    # While there is a valid 'nextCursor' value within the API response
    while more_data:    
        
        print("Current cursor: ", cursor)
        url = f'{base_url}?cursor={cursor}&sort=date&time=all'
        
        page = await browser.get(url)
        body = await page.find_elements_by_text('clips', tag_hint='div')
        
        if page and body:
            
            data = await body[0].get_html()
            if data and data.startswith("<body>"):
                data = data[6:-7]
                data = json.loads(data)
            else:
                raise ValueError("Incorrect data format\n", data)
            
            clips = data.get('clips', [])
            processed_data = [
                {
                    'id': clip.get('id'),
                    'title': clip.get('title'),
                    'creator': clip.get('creator'),
                    'channel': clip.get('channel'),
                    'date_created': clip.get('created_at'),
                    'thumbnail_url': clip.get('thumbnail_url'),
                }
                for clip in clips
            ]

            df = pd.DataFrame(processed_data)
            append_to_csv(df, csv_file)
            
            new_cursor = data.get('nextCursor')
            if new_cursor:
                cursor = new_cursor
                write_cursor(cursor)  # Update the stored cursor
                
            # time.sleep(random.uniform(0, 2))
        else:
            more_data = False

    await page.close()




if __name__ == '__main__':

    # since asyncio.run never worked (for me)
    nd.loop().run_until_complete(main())
