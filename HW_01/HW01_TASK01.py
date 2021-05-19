import requests
import json
from pprint import pprint

# https://api.github.com/users/octocat/repos
user_name = 'nnataljafenka'
main_link = f'https://api.github.com/users/{user_name}/repos'

response = requests.get(main_link)
status_code = response.status_code

if response.ok:
    j_data = response.json()
    # pprint(j_data)
    with open(f'{user_name}.json', 'w', encoding='utf-8') as f:
        json.dump(j_data, f, ensure_ascii=False, indent=4)

else:
    print('Что-то пошло не так!')
