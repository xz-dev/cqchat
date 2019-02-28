class SearchObject():
    def __init__(self):
        self.search_dict = {'version': 0,
                            'search': list()}

    def search(self, str_search):
        # 输入搜索文本
        version = self.search_dict['version']
        search_dict_list = self.__split_to_dict(str_search)
        self.search_dict = {'version': version + 1,
                            'search': search_dict_list}

    def __split_to_dict(self, string):
        string_list = [txt.strip() for txt in string.split(',')]
        search_dict_list = [{
            'key': txt_list[0],
            'value': txt_list[1]
        } for txt_list in string_list.split(',', 1)]
        return search_dict_list
