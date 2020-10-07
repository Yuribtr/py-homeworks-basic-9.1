import requests
import tqdm
import spinner

API_URL = 'https://superheroapi.com/api/'
TOKEN = '2619421814940190'
USER_AGENT = {"User-Agent": "Netology"}

heroes_names = ['Hulk', 'Captain America', 'Thanos', 'Firelord', 'Penance', 'Angel Dust']
# you may leave 1 or more characteristics to compare heroes
characteristics = ['intelligence', 'strength', 'speed', 'durability', 'power', 'combat']


def get_score_by_characteristic(URL, heroes_names, characteristics):
    """
    Function searches heroes at API and gives a score to each one, according
    to given characteristics list
    :param URL: put here full URL to API method
    :param heroes_names: list names of heroes to be searched for
    :param characteristics: list of characteristics by which heroes are compared
    :return: list of found heroes with scores as per requested conditions
    """
    result = []
    print(f'Loading info about {len(heroes_names)} heroes. Pls wait:')
    for hero_name in tqdm.tqdm(heroes_names):
        response = requests.get(API_URL + TOKEN + '/search/' + hero_name, headers=USER_AGENT)
        data = response.json()
        if data['response'] != 'success':
            continue
        for hero in data['results']:
            # strict check if name is exact what we are looking for
            if hero['name'] != hero_name:
                continue
            # let's normalize characteristics and summarize the score
            hero['score'] = 0
            for char in characteristics:
                try:
                    hero['score'] += int(hero['powerstats'][char])
                except ValueError:
                    pass
            result.append(hero)
    return result


with spinner.Spinner():
    heroes = get_score_by_characteristic(API_URL + TOKEN + '/search/', heroes_names, characteristics)

if len(heroes) > 0:
    heroes.sort(key=lambda x: int(x['score']), reverse=True)
    # print(*heroes, sep='\n')
    print(f'SuperHero is: {heroes[0]["name"]} with score: {heroes[0]["score"]}')
