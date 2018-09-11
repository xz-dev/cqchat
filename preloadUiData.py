class contactInfo():
    from get import getInfo
    import MainGui

    def __init__(self):
        self.friend_info_dict_list = list()
        self.friendTree = MainGui.friendTree

    def friendInfoTreeWidget(self):
        friend_info_list = getInfo.getFriendInfo()  # 获取好友列表
        if friend_info_list and self.friend_info_dict_list != friend_info_list:
            self.friend_info_dict_list = friend_info_list
            friend_category_list = list(
                set([tmp_dict['category'] for tmp_dict in friend_info_list]))
            self.friendTree.setsortingenabled = True
            self.friendTree_widget_dict.clear()
            self.friendTree.clear()  # 清空联系人列表
            for friend_category in friend_category_list:
                treecategory = QTreeWidgetItem([friend_category])
                for single_friend_info_list in friend_info_list:
                    friend_markname = single_friend_info_list['markname']
                    friend_name = single_friend_info_list['name']
                    if not friend_markname:
                        friend_markname = friend_name
                    if single_friend_info_list['category'] == friend_category:
                        if not friend_markname:
                            friend_markname = friend_name
                        friend_tree_info = QTreeWidgetItem([friend_markname])
                        friend_tree_info.setFlags(
                            Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        self.friendTree_widget_dict[repr(
                            friend_tree_info)] = single_friend_info_list
                        treecategory.addChild(friend_tree_info)
                        treecategory.setExpanded(True)
                        # 自动展开联系人
                        # TODO: 保持联系人展开信息
                treecategory.setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.friendTree.addTopLevelItem(treecategory)
                # 完成分类的联系人绘制
