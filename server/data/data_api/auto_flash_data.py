class AutoFlashData():
    def __init__(self, data):
        self.__data = data
        self.__new_chat_object()

    def __rename_keys(self, in_dict):
        out_dict = dict()
        try:
            out_dict['id'] = in_dict['user_id']
            out_dict['name'] = in_dict['nickname']
            out_dict['remark'] = in_dict['remark']
        except KeyError:
            out_dict['id'] = in_dict['group_id']
            out_dict['name'] = in_dict['group_name']
        return out_dict

    def __new_chat_object(self):
        from ...chat.chat_object import ChatObject
        ChatObject = ChatObject(self.__data)
        friend_list_object = ChatObject.ChatList.FriendListObject()
        group_list_object = ChatObject.ChatList.GroupListObject()
        friend_object_dict = dict()
        group_object_dict = dict()
        friend_object_dict = {
            contact_info_dict['nickname']:
            ChatObject.ChatIndividual.GroupObject(
                self.__rename_keys(contact_info_dict))
            for contact_info_dict in list(group_info
                                          for group_info in friend_list_object.
                                          info.info()['data'])
        }
        group_object_dict = {
            group_info['group_id']: ChatObject.ChatIndividual.GroupObject(
                self.__rename_keys(group_info))
            for group_info in group_list_object.info.info()['data']
        }
        self.__data.ui_data.chat_object = {
            'FriendListObject': friend_list_object,
            'GroupListObject': group_list_object,
            'Friend': friend_object_dict,
            'Group': group_object_dict,
        }
