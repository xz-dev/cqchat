import multiprocessing as mp
from fuzzyfinder import fuzzyfinder


class SearchInfo():
    """
    搜索信息类
    """

    def __init__(self, search_text, search_type_list, all_search_dict_list):
        self.search_text = search_text
        self.search_type_list = search_type_list
        self.all_search_dict_list = all_search_dict_list

    def searchContactObject(self):
        search_type_list = self.search_type_list
        all_search_dict_list = self.all_search_dict_list
        search_result_dict_list = list()
        pool = mp.Pool()
        for search_type, search_dict_list in zip(search_type_list, all_search_dict_list):
            self.search_type = search_type
            search_result_dict_list += pool.map(self.search, search_dict_list)
        search_result_dict_list = [
            i for i in search_result_dict_list if i != None]
        return search_result_dict_list

    def search(self, search_dict):
        # 搜索函数
        search_type = self.search_type
        search_text = self.search_text
        dynamic_loading_list = list()
        search_list = list()
        if search_type == 'friend':
            dynamic_loading_list = ['category', 'client_type',
                                    'name', 'markname', 'state', 'client_type', 'uid']
            search_owner_id = search_dict['id']
            search_group_id = None
        elif search_type in ('group_basis', 'group_all'):
            dynamic_loading_list = ['markname',
                                    'uid', 'owner_uid', 'memo', 'name']
            search_owner_id = search_dict['id']
            search_group_id = search_dict['id']
        for tmp in dynamic_loading_list:
            if tmp in search_dict and search_dict[tmp] != None:
                search_list.append(str(search_dict[tmp]))
        suggestions = fuzzyfinder(search_text, search_list)
        result = list(suggestions)
        if result:
            result_dict = {'search_text_list': result,
                           'search_dict': search_dict,
                           'search_owner_id': search_owner_id,
                           'search_group_id': search_group_id,
                           'search_type': search_type,
                           }
            return result_dict
        else:
            return None

    def groupSearch(self, group_info_dict):
        # 搜索群组信息
        global global_search_text
        search_text = global_search_text
        search_list = list()
        dynamic_loading_list = ['markname', 'uid', 'owner_uid', 'memo', 'name']
        for tmp in dynamic_loading_list:
            if group_info_dict[tmp]:
                search_list.append(group_info_dict[tmp])
                # 搜索群组基础信息
        if 'member' in group_info_dict:
            group_nember_info_dict = group_info_dict['member']
            pool = mp.Pool()
            sear
            groupNumberSearch(group_nember_info_dict)
