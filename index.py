import requests
import mysql.connector
from bs4 import BeautifulSoup

from youtubesearchpython import VideosSearch
import re
import time
url = 'https://katmoviehd.zip/'

def insert_into_moviedb(data):
    # Connect to MySQL server
    # Replace 'your_username', 'your_password', 'your_host' and 'your_database' with appropriate values
    conn = mysql.connector.connect(
        host='localhost',
        user='anant',
        password='Anants2mi7@',
        database='moviebot'
    )

    # Create cursor object
    cursor = conn.cursor()

    # SQL query to insert data into the 'moviedb' table
    insert_query = """
    INSERT INTO moviedb (postid, movieurl, moviename, posterurl, 720plink, 1080plink)
    VALUES (%(postid)s, %(movieurl)s, %(moviename)s, %(posterurl)s, %(720plink)s, %(1080plink)s)
    """

    # Execute the query with the data
    cursor.execute(insert_query, data)

    # Commit changes
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    print("Data inserted successfully.")

def get_latest_postid():
    # Connect to MySQL server
    # Replace 'your_username', 'your_password', 'your_host' and 'your_database' with appropriate values
    conn = mysql.connector.connect(
        host='localhost',
        user='anant',
        password='Anants2mi7@',
        database='moviebot'
    )

    # Create cursor object
    cursor = conn.cursor()

    # SQL query to fetch the latest postid
    select_query = "SELECT postid FROM moviedb ORDER BY created DESC LIMIT 1"

    # Execute the query
    cursor.execute(select_query)

    # Fetch the result
    latest_postid = cursor.fetchone()[0]

    # Close cursor and connection
    cursor.close()
    conn.close()
    print(latest_postid)
    return latest_postid


def get_post_id():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_post = soup.find('li', class_='post')
    post_id = first_post.get('id')
    latest_post_id = post_id.split('-')[1]
    print(latest_post_id)
    return latest_post_id

def last_post_id():
    last_post_id = get_latest_postid()
    return last_post_id

while True:
        youtube = 'https://www.youtube.com/watch?v='
        oft = 'Official Trailor'
        url = 'https://katmoviehd.zip/'
        Bot_Token = '7078609511:AAEDo1VTWDgrm18v8z94F-a7inpFOaJI3R0'
        Chat_Id = -1001996864308


        if int(last_post_id()) == int(get_post_id()):
            print("no new movie")

        if int(last_post_id()) < int(get_post_id()):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('div', class_='post-content').find('h2').text.strip()
            img_src = soup.find('div', class_='post-thumb').find('img')['src']
            post_link = soup.find('div', class_='post-thumb').find('a')['href']
            response2 = requests.get(post_link)
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            first_post2 = soup2.find('div', class_='entry-content')
            first_post3 = first_post2.find('ul')
            list_items = first_post2.find_all('li')
            movie_details = '\n'.join(f"=> {item.get_text(strip=True)}" for item in list_items)


            print("Post Link:", post_link)
            print("Image Source:", img_src)
            print("Title:", title)
            just_title = title.split(')')
            movie_title = just_title[0].replace('(', '- ')
            videosSearch = VideosSearch(f'{movie_title + oft} ', limit=1)
            vi = videosSearch.result()
            video_id = vi['result'][0]['id']
            print(video_id)

            try:

                response = requests.get(post_link)

                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find the 720p and 1080p download links
                link_720p = soup.find('a', string=lambda text: text and '720p Links' in text)
                #link_1080p = soup.find('a', string=lambda text: text and '1080p Links' in text)

                # Extract href attribute from the links if found
                link_720p_url = link_720p['href'] if link_720p else None






                response = requests.get(link_720p_url)

                # Parse the HTML content
                # Extracting gdriveId using regular expression
                gdriveId_match = re.search(r'gdriveId:"(.*?)"', response.text)

                # Check if match is found

                gdriveId = gdriveId_match.group(1)
                Dwonload720plink = f"https://drive.google.com/uc?export=download&id={gdriveId}"
                print(Dwonload720plink)






                moviedata = {
                    "postid": get_post_id(),
                    "movieurl": post_link,
                    "moviename": movie_title,
                    "posterurl": img_src,
                    "720plink": Dwonload720plink,
                    "1080plink": "Dwonload1080plink"
                }
                insert_into_moviedb(moviedata)
                url = f"https://api.telegram.org/bot{Bot_Token}/sendMessage"
                data = {'chat_id': Chat_Id, 'text': movie_details}
                requests.post(url, data=data)

                url = f"https://api.telegram.org/bot{Bot_Token}/sendPhoto"
                data2 = {'chat_id': Chat_Id, 'photo': img_src, 'caption': movie_title}
                requests.post(url, data=data2)

                url = f"https://api.telegram.org/bot{Bot_Token}/sendMessage"
                data = {'chat_id': Chat_Id, 'text': 'Movie Trailer Link'}
                requests.post(url, data=data)
                url = f"https://api.telegram.org/bot{Bot_Token}/sendMessage"
                data = {'chat_id': Chat_Id, 'text': youtube + video_id}
                requests.post(url, data=data)
                url = f"https://api.telegram.org/bot{Bot_Token}/sendMessage"
                data = {'chat_id': Chat_Id, 'text': Dwonload720plink}
                requests.post(url, data=data)

            except Exception as e:
                print(f"An error occurred: {str(e)}")

        time.sleep(300)
