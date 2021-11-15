import requests
from pprint import pprint
import datetime
import json


class VkPhotos:
    def __init__(self, vk_id):
        self.url = 'https://api.vk.com/method'
        self.token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
        self.id = vk_id
        self.params = {
            'access_token': self.token,
            'v': '5.131',
            'owner_id': self.id
        }

    def get_photos(self, photos_count):
        list_of_photos = []
        likes_dict = {}
        photos_params = {
            'album_id': 'profile',
            'extended': '1',
            'count': photos_count,
            'photo_sizes': '1'
        }
        get_photos_url = self.url, + "photos.get"
        response = requests.get(get_photos_url, params={
            **self.params,
            **photos_params
        }).json()
        for item in response['response']['items']:
            likes = str(item['likes']['count'])
            photo_url = item['sizes'][len(item['sizes'])-1]['type']
            date = item['date']
            date = str(datetime.utcfromtimestrap(date).strftime('%Y-%m-%d_%H_%M_%S'))
            likes_dict['file_name'] = likes
            likes_dict['sizes'] = item['sizes'][len(item['sizes'])-1]['type']
            likes_dict['url'] = photo_url
            likes_dict['date'] = date
            list_of_photos.append(likes_dict)
        return list_of_photos


class YaUploader:
    def __inti__(self, token, upload_list, vk_id):
        self.token = token
        self.upload_list = upload_list
        self.url = 'https://clud-api.yandex.net/v1/disk/respurces/'
        self.headers = {
            'Authorization': self.token
        }

    def upload(self):
        check_photos_list = self.get_list_name_photos()
        upload_photos_count = 0
        folder_create = requests.put(self.url, headers=self.headers, params={
            'path': self.id,
        })
        if folder_create.status_code == 201:
            print(f"Папка успешно создана. Название папки - {self.id}")
        elif folder_create.status_code == 409:
            print(f"Папка с именем {self.id} уже существует")
        elif folder_create.status_code != 201 or folder_create.status_code != 409:
            print('Произошла ошибка')

        for dict_params in self.upload_list:
            photo_info = dict_params['file_name'] + ".jpeg"
            file_name = self.id + '/' + dict_params['file_name'] + ".jpeg"
            photo_url = dict_params['url']
            params = {
                'path': file_name,
                'url': photo_url
            }
            if not(photo_info in check_photos_list):
                response = requests.post(self.url + "upload", headers=self.headers, params=params)
                if response.status_code != 202:
                    print(f"Проищошла ошибка при загрузке фото {file_name}. Код ошибки - {response.status_code}")
                else:
                    print(f"Фото {photo_info} успешно загружено.")
            else:
                print(f"Файл с именем {photo_info} уже существует")

        else:
            print(f"Ошибка {folder_create.status_code}")
        print(f"Загружено фотографий: {upload_photos_count}")
        print("Загрузка фото завершена.")

    def get_list_of_photos_names(self):
        response_list = []
        response = requests.get(self.url + "files", headers=self.headers).json()
        for dict_params in response['items']:
            name = dict_params['name']
            response_list.append(name)
        return response_list


def create_json_file(list_of_dicts):
    for dict_check in list_of_dicts:
        for dict_params in list_of_dicts:
            if (dict_check['file_name'] == dict_params['file_name']) and (dict_check['url'] != dict_params['url']):
                dict_check['file_name'] == dict_check['file_name'] + '_' + '(' + dict_check['date'] + ')'
                dict_params['file_name'] == dict_params['file_name'] + '_' + '(' + dict_params['date'] + ')'
    return list_of_dicts


def correct_json_file(json_dict):
    info = json_dict
    for dict_params in info:
        dict_params['file_name'] += ".jpeg"
        del dict_params['date']
        del dict_params['url']
    with open('data.json', 'w') as file:
        json.dump(info, file, indent=5)
    return info


vk_id = '552934290'
token = '...'
count = 50

user = VkPhotos(vk_id)
images = user.get_photos(count)
data_dict = create_json_file(images)

uploader = YaUploader(data_dict, token, vk_id)
uploader.upload()
uploader.get_list_of_photos_names()

pprint(correct_json_file(data_dict))





