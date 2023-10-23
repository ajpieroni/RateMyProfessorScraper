import requests
from bs4 import BeautifulSoup
import csv

# dic of prof names in cs department
professor_names = {
    '897005':'Pankaj K. Agarwal',
    '44522': 'Owen Astrachan',
    '2632142': 'Alberto Bartesaghi',
    '1852935': 'Robert Calderbank',
    '307594': 'Jeffery Chase',
    # '': 'Bhuwan Dhingra',
    '2182858': 'Bruce Randall Donald',
    '398017': 'Robert Duvall',
    # '': 'Pardis Emami-Naeini',
    '2592693': 'Brandon Fain',
    '2474436': 'Rong Ge',
    '2152991': 'Raluca Mihaela Gordan', #only 1 
    '323889': 'Alexander J. Hartemink',
    '986220': 'Alvin R. Lebeck',
    '2768577': 'Matthew Lentz',
    '2340460': 'Ashwin Machanavajjhala',
    '1504148': 'Bruce Maggs',
    '897004': 'Kamesh Munagala',
    '2642236': 'Kartik Nayak',
    '2606531': 'Kate OHanlon',
    '2134556': 'Debmalya Panigrahi',
    '865563': 'Ronald Parr',
    # '': 'Jian Pei',
    # '323870': 'John H. Reif',
    # '': 'Michael Reiter',
    '295867': 'Susan H. Rodger',
    '2671385': 'Benjamin Rossman',
    '2246779': 'Sudeepa Roy',
    '2186716': 'Cynthia D. Rudin',
    # '': 'Tananun Songdechakraiwut',
    # '': 'Alexander Steiger',
    '2335054': 'Kristin V Stephens-Martinez',
    '505273': 'Xiaobai Sun',
    '782570': 'Carlo Tomasi',
    '2617560': 'Yesenia Velasco',
    # '': 'Alicia Nicki Washington',
    '2604031': 'Lisa Wills',
    # '': 'Samuel Joshua Wiseman',
    '1253078': 'Jun Yang',
    '2111078': 'Xiaowei Yang',
    # 'n/A': 'Anru Zhang',
    # 'n/A': 'Danfeng Zhang',
    # 'N/A': 'Danyang Zho',
}

BASE_URL = 'https://www.ratemyprofessors.com/professor/'

# output file
filename = 'comments.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # write headers
    csv_writer.writerow(['Professor Name', 'Rating', 'Class', 'Comment'])
    for professor_id, professor_name in professor_names.items():
        print(f"Processing {professor_name}'s comments...")

        # per prof url
        url = f"{BASE_URL}{professor_id}"
        response = requests.get(url)

        # check if success
        if response.status_code == 200:
            # html
            # !test response html
            # with open('response_content.txt', 'w', encoding='utf-8') as file:
            #     file.write(response.text)   
            soup = BeautifulSoup(response.content, 'html.parser')
            # print(response.content)

            # for each rating
            ratings = soup.find_all('div', class_='Rating__StyledRating-sc-1rhvpxz-1 jcIQzP')
            for rating in ratings:
               
                class_info_div = rating.find('div', class_='RatingHeader__StyledClass-sc-1dlkqw1-3 eXfReS')
                class_info = class_info_div.get_text(strip=True) if class_info_div else 'N/A'

                comment_div = rating.find('div', class_='Comments__StyledComments-dzzyvm-0 gRjWel')
                comment = comment_div.get_text(strip=True) if comment_div else 'N/A'

                rating_div = rating.find('div', class_='RatingValues__RatingContainer-sc-6dc747-1 DObVa')
                rating_value = 'N/A'
                if rating_div:
                    rating_number_div = rating_div.find('div', class_='CardNumRating__StyledCardNumRating-sc-17t4b9u-0 eWZmyX')
                    rating_value = rating_number_div.get_text(strip=True) if rating_number_div else 'N/A'

                # remove the word "Quality"
                rating_value = rating_value.replace("Quality", "").strip()  # stripping extra whitespace after removal

                csv_writer.writerow([professor_name, rating_value, class_info, comment])
        else:
            print(f"Failed to retrieve data for Professor {professor_name}.")

print(f'Data written to {filename}')