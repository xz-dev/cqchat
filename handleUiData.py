from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


def handleSearchOutput(single_search_info_dict, is_child):
    """
    处理搜索结果输出格式
    """
    search_contact_text = None
    search_chat_object_name = None
    tmp_search_text_list = single_search_info_dict['search_text_list']
    tmp_chat_object_info = single_search_info_dict['search_dict']
    if tmp_chat_object_info['markname']:
        search_chat_object_name = tmp_chat_object_info['markname']
    else:
        search_chat_object_name = tmp_chat_object_info['name']
        # 确定显示的昵称
    for search_text in tmp_search_text_list:
        if not search_contact_text:
            search_contact_text = search_chat_object_name
        if search_text != search_chat_object_name:
            if not is_child:
                search_contact_text = search_contact_text + '\n' + search_text
            elif is_child:
                search_contact_text = search_contact_text + '\n\b' + search_text
    newItem = QtWidgets.QListWidgetItem()
    newItem.setText(search_contact_text)
    chat_object_info_dict = dict()
    chat_object_info_dict['id'] = tmp_chat_object_info['id']
    chat_object_info_dict['chat_type'] = single_search_info_dict['search_type']
    chat_object_info_dict['chat_info_dict'] = tmp_chat_object_info
    return newItem, chat_object_info_dict
    self.search_contact_result_dict[repr(
        newItem)] = chat_object_info_dict
    self.searchContactList.insertItem(0, newItem)

