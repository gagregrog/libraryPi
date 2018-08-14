import requests
import json

def get_title_from_isbn(isbn):
    try:
        isbn_f = 'ISBN:{}'.format(isbn)
        r = requests.get('https://openlibrary.org/api/books?bibkeys={}'.format(isbn_f))
        json_string = r.text[18:-1]
        title_url = json.loads(json_string).get(isbn_f).get('info_url')
        title = title_url.split('/')[-1].replace('_', ' ')

        return title

    except Exception as e:
        print('Error fetching title')
