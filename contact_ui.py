import urwid


class ContactView(urwid.WidgetWrap):
    palette = [
        ('header', 'white', 'dark red', 'bold'),
        #  ('line', 'black', 'light gray', 'standout'),
        ('button normal', 'light gray', 'dark blue', 'standout'),
        ('button select', 'white', 'dark green'),
    ]

    def __init__(self):
        self.category_list = list()
        urwid.WidgetWrap.__init__(self, self.main_window())

    def on_mode_button(self, button, state):
        """Notify the controller of a new mode setting."""
        if state:
            print('on')

    def contact_object_button(self, g, l, fn):
        w = urwid.RadioButton(g, l, False, on_state_change=fn)
        w = urwid.AttrMap(w, 'button normal', 'button select')
        return w

    def exit_program(self, w):
        raise urwid.ExitMainLoop()

    def contact_list(self):
        group = list()
        contact_object_buttons = list()
        children_bottons = self.category_list
        for m in children_bottons:
            rb = self.contact_object_button(group, m, self.on_mode_button)
            contact_object_buttons.append(rb)
        goup_list_name = [
            urwid.Text("分组", align="center"),
        ] + contact_object_buttons
        w = urwid.ListBox(urwid.SimpleListWalker(goup_list_name))
        return w

    def main_window(self):
        vline = urwid.AttrWrap(urwid.SolidFill(u'\u2502'), 'line')
        category = self.contact_list()
        w = urwid.Columns([
            ('weight', 1, category),
            ('fixed', 1, vline),
        ],
                          focus_column=0)
        w = urwid.AttrMap(w, 'body')
        return w


class ViewController():
    def __init__(self, ChatObject):
        self.chat_object = ChatObject
        self.view = ContactView()
        friend_list_object = self.chat_object.ChatList.FriendListObject()
        self.view.category_list = friend_list_object.category_list()

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()


def get_contact_info(data):
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
        'name': "friend",
        'children': [{
            'name': i,
            'children': tmp_dict[i]
        } for i in tmp_dict.keys()]
    }
    return retval


def main(data):
    from .wechat.chat.chat_object import ChatObject
    ChatObject = ChatObject(data)
    ViewController(ChatObject).main()


if __name__ == "__main__":
    main(None)
