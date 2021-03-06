import requests
import time
import json

VICTIM_ID = 18689304
TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'


def get_victim_groups():

    params = {
        'access_token': TOKEN,
        'user_id': VICTIM_ID,
        'extended': 0,
        'count': 1000,
        'fields': 'members_count',
        'v': '5.73'
    }

    response = requests.get('https://api.vk.com/method/groups.get', params)
    print('-')
    victim_groups_set = set(response.json()['response']['items'])

    return victim_groups_set


def get_victim_friends():

    params = {
        'access_token': TOKEN,
        'user_id': VICTIM_ID,
        'v': '5.73'
    }

    response = requests.get('https://api.vk.com/method/friends.get', params)
    print('-')
    victim_friends_list = response.json()['response']['items']

    return victim_friends_list


def is_valid_friend(victim_friends_list):

    temp_victim_friends_list = ', '.join([str(i) for i in victim_friends_list])

    params = {
        'user_ids': temp_victim_friends_list,
        'v': '5.73'
    }

    response = requests.post('https://api.vk.com/method/users.get', params)
    print('-')
    # Used post because of error 414 
    friends_info = response.json()['response']
    invalid_set_of_friends = set()
    victim_friends_set = set(victim_friends_list)
    for i in friends_info:
        for keys in i.keys():
            if 'deactivated' in keys:
                invalid_set_of_friends.add(i['id'])

    valid_set_of_friends = victim_friends_set.difference(invalid_set_of_friends)
    valid_list_of_friends = list(valid_set_of_friends)

    return valid_list_of_friends


def get_friends_groups(valid_list_of_friends):

    main_list_friends_groups = []
    i = 1
    for friend in valid_list_of_friends:

        params = {
            'access_token': TOKEN,
            'user_id': friend,
            'extended': 0,
            'v': '5.73',
            'count': 1000
        }

        response = requests.get('https://api.vk.com/method/groups.get', params)
        print('-')
        time.sleep(0.5)
        try:
            friend_groups_set = set(response.json()['response']['items'])
            main_list_friends_groups.append(friend_groups_set)
            print('Remained friends {}'.format(len(valid_list_of_friends)-i))
            i += 1
        except KeyError:
            continue

    return main_list_friends_groups


def get_unique_groups(victim_groups_set, main_list_friends_groups):

    unique_groups = victim_groups_set.difference(*main_list_friends_groups)

    return unique_groups


def get_group_description(unique_groups):

    list_of_group_description = []
    i = 0
    for user_id in unique_groups:
        params = {
            'group_ids': user_id,
            'fields': 'members_count',
            'v': '5.73'
        }

        unused_keys = ['is_closed', 'photo_100', 'photo_200', 'photo_50', 'screen_name', 'type']

        response = requests.get('https://api.vk.com/method/groups.getById', params)
        groups_description = response.json()['response'][i]
        for key in unused_keys:
            del groups_description[key]

        list_of_group_description.append(groups_description)

    i += 1
    return list_of_group_description


def write_groups_to_json(list_of_group_description):
    with open('groups.json', 'w', encoding='UTF-16') as f:
        json.dump(list_of_group_description, f, indent=2, ensure_ascii=False)
        text = json.dumps(list_of_group_description, indent=2, ensure_ascii=False)
        print(text)


def main():
    result_get_victim_groups = get_victim_groups(TOKEN, VICTIM_ID)
    result_get_victim_friends = get_victim_friends(TOKEN, VICTIM_ID)
    result_is_valid_friend = is_valid_friend(result_get_victim_friends)
    result_get_friends_groups = get_friends_groups(TOKEN, result_is_valid_friend)
    result_get_unique_groups = get_unique_groups(result_get_victim_groups, result_get_friends_groups)
    result_get_group_description = get_group_description(result_get_unique_groups)
    write_groups_to_json(result_get_group_description)


main()





