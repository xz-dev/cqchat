import urwid
try:
    from .ui import ui_widget
except ModuleNotFoundError:
    from ui import ui_widget


class TreeBrowser:
    def __init__(self, data=None):
        self.__init_ui_data()
        self.topnode = ui_widget.NParentNode(data)
        self.listbox = urwid.TreeListBox(urwid.TreeWalker(self.topnode))
        self.listbox.offset_rows = 1
        self.header = urwid.Text("联系人")
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(self.header, 'head'))

    def __init_ui_data(self):
        self.palette = [
            ('body', 'black', 'light gray'),
            ('focus', 'light gray', 'dark blue', 'standout'),
            ('head', 'yellow', 'black', 'standout'),
            ('foot', 'light gray', 'black'),
            ('key', 'light cyan', 'black', 'underline'),
            ('title', 'white', 'black', 'bold'),
            ('flag', 'dark gray', 'light gray'),
            ('error', 'dark red', 'light gray'),
        ]

    def main(self):
        """Run the program."""

        self.loop = urwid.MainLoop(
            self.view, self.palette, unhandled_input=self.unhandled_input)
        self.loop.run()

    def unhandled_input(self, k):
        if k in ('q', 'Q'):
            raise urwid.ExitMainLoop()


def get_contact_tree(data):
    from .chat.chat_object import ChatObject
    ChatObject = ChatObject(data)
    friend_list_object = ChatObject.ChatList.FriendListObject()
    tmp_dict = dict()
    friend_list_info = friend_list_object.info()
    for i in friend_list_info:
        category = i['category']
        markname = i['markname']
        if not markname:
            markname = i['name']
        if category in tmp_dict:
            tmp_dict[category].append({'name': markname})
        else:
            tmp_dict[category] = [
                {
                    'name': markname
                },
            ]
    retval = {
        'name':
        "friend",
        'children': [{
            'name': i,
            'children': tmp_dict[i]
        } for i in tmp_dict.keys()]
    }
    return retval


def main(data):
    sample = get_contact_tree(data)
    TreeBrowser(sample).main()


if __name__ == "__main__":
    main(None)
