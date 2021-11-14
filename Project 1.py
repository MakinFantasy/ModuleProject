import requests
from pprint import pprint
import datetime

class VkUpload:
    def __init__(self):
        self.token = 'AQAAAAAZJUXrAADLW-qtmvkOBUvjvOye265SgRU'
        date = datetime.datetime.now().strftime("%d-%b-%Y %H-%M-%S")
        self.path = f'Backup_{date}'

    def get_photos(self):
        url = 'http://api.vk.com/method/photos.get'
        params = {
            'owner_id': '552934290',
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131',
            'album_id': 'profile',
            'extended': '1',
            'count': '5'
        }
        response = requests.get(url, params=params)
        data_vk = response.json()
        pprint(data_vk)
        return

    def create_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content_Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {
            'path': 'netology/photos'
        }
        requests.put(url, headers=headers, params=params )


    def upload_photos(self, file_path: str):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content_Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {
            'path': file_path,
            'overwrite':'true'
        }

        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        pprint(data)
        return data




a = VkUpload()
a.create_folder()
