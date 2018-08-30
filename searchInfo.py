import multiprocessing as mp
from fuzzyfinder import fuzzyfinder


def search(search_dict):
    # 搜索函数
    global global_search_text
    search_text = global_search_text
    search_list = [search_dict['category'], search_dict['client_type'], search_dict['name'], search_dict['state'], search_dict['client_type']]
    if 'uid' in search_dict and search_dict['uid']:
        chat_object_uid = str(search_dict['uid'])
        search_list.append(chat_object_uid)
    if search_dict['markname']:
        chat_object_markname = search_dict['markname']
        search_list.append(chat_object_markname)
    suggestions = fuzzyfinder(search_text, search_list)
    result = list(suggestions)
    if result:
        return {'search_text_list': result,
                'search_dict': search_dict,
                }
    else:
        return None


def searchContactObject(search_text, search_dict_list):
    global global_search_text
    global_search_text = search_text
    pool = mp.Pool()
    search_result_dict_list = pool.map(search, search_dict_list)
    search_result_dict_list = [i for i in search_result_dict_list if i != None]
    return search_result_dict_list
