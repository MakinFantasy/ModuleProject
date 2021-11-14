import requests
from pprint import pprint

class VkUpload:
    def __init__(self):
        self.token = 'AQAAAAAZJUXrAADLW-qtmvkOBUvjvOye265SgRU'

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
        data = response.json()
        pprint (data)
        return data



get_photos()
