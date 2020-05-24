from bson import ObjectId
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import UserDataBase, FlashCardDatabase
from bson.json_util import dumps
import pymongo
import DBConnection
import classes

kv = Builder.load_file("my.kv")


class WindowManager(ScreenManager):
    pass


sm = WindowManager()
# db_u = UserDataBase("users.txt")
db_f = FlashCardDatabase()
# client = pymongo.MongoClient(
#   "mongodb+srv://Developer:TrustMe99@flipcardsdb-k8zdx.mongodb.net/test?retryWrites=true&w=majority")
# db_u = client["FlipcardsDB"]

mail = ""
flashcard_set = classes.Set("1", "a")
current_sets = {}
# db_x = DBConnection.DBConnection
# db_x.db = client["FlipcardsDB"]

db_x = DBConnection.DBConnection()


class Pop(FloatLayout):
    pass


class Pop1(FloatLayout):
    pass


class Pop2(FloatLayout):
    pass


class Pop3(FloatLayout):
    pass


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    font_size_large = NumericProperty(20)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            x = db_x.add_user(self.namee.text, self.email.text, self.password.text)
            if x == 1:
                self.show_popup2()
                # db_u.add_user(self.email.text, self.password.text, self.namee.text)
                # db_x.add_user(self.namee.text, self.email.text, self.password.text)
                self.reset()
                sm.current = "login"
            elif x == -1:
                self.show_popup3()
                self.reset_pass()
                sm.current = "create"
            elif x == -2:
                self.show_popup4()
                self.reset()
                sm.current = "create"
        else:
            self.reset()
            self.show_popup1()
            sm.current = "create"

    def reset_pass(self):
        self.password.text = ""

    def show_popup1(self):
        show = Pop()
        popupWindow = Popup(title="Error!", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def show_popup2(self):
        show = Pop1()
        popupWindow = Popup(title="Account created!", content=show, size_hint=(None, None), size=(300, 200))
        popupWindow.open()

    def show_popup3(self):
        show = Pop2()
        popupWindow = Popup(title="Error!", content=show, size_hint=(None, None), size=(400, 200))
        popupWindow.open()

    def show_popup4(self):
        show = Pop3()
        popupWindow = Popup(title="Error!", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class HomeScreenWindow(Screen):
    def mySetsButton(self):
        sm.current = "my_sets"

    def available_sets(self):
        sm.current = "home"

    def createFlashcard(self):
        sm.current = "createFlashcard"

    def log_out(self):
        sm.current = "login"

    def create_set(self):
        sm.current = "createSet"

    def searchSet(self):
        sm.current = "searchSet"


class MySetsWindow(Screen):
    email = ObjectProperty(None)

    def available_sets(self):
        sm.current = "home"

    def log_out(self):
        sm.current = "login"

    def username(self):
        # print(self.email)
        return 0

    def mainMenu(self):
        sm.current = "homeScreenWindow"


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        # if db_u.validate(self.email.text, self.password.text):
        x = db_x.user_auth(self.email.text, self.password.text)
        if x == 1:
            global mail
            mail = self.email.text
            HomeWindow.current = self.email.text
            self.reset()
            sm.current = "homeScreenWindow"
        elif x == -1:
            self.reset()
            self.show_popup1()
            sm.current = "login"
        else:
            self.reset()
            self.show_popup2()
            sm.current = "login"

    def show_popup1(self):
        show = P()
        popupWindow = Popup(title="Login error", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def show_popup2(self):
        show = P1()
        popupWindow = Popup(title="Login error", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def back(self):
        sm.current = "login"


class HomeWindow(Screen):
    # layout_content = ObjectProperty(None) is it necessary??

    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.sets = []

    current = ""

    def mainMenu(self):
        sm.current = "homeScreenWindow"

    def log_out(self):
        sm.current = "login"

    def my_sets(self):
        sm.current = "my_sets"

    def on_enter(self, *args):
        for name, desc, auth, size in [x for x in db_f.sets for _ in range(1)]:
            button = Button(text=name + ': ' + ' by ' + auth + ' (' + size + ' flashcards)')
            button.size_hint = (0.8, 0.35)
            button.bind(on_press=self.pressed)
            self.sets.append(button)
            self.ids.grid.add_widget(button)

    def on_leave(self, *args):
        for but in self.sets:
            self.ids.grid.remove_widget(but)

    def pressed(self, instance):
        filename = instance.text.split(':')[0]
        sm.transition.direction = 'left'
        sm.current = 'learning'
        sm.current_screen.ids.set_name.text = filename + '.txt'


class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=(self.pos[0] + self.size[0] * 0.1, self.pos[1] + self.size[1] * 0.1),
                      size=(self.size[0] * 0.8, self.size[1] * 0.8))


class LearningWindow(Screen):

    def __init__(self, **kwargs):
        super(LearningWindow, self).__init__(**kwargs)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.filename = ""
        self.card_labels = []

    def set_file(self, filename):
        self.filename = filename

    def browse_sets(self):
        sm.current = "home"

    def on_enter(self, *args):
        filename = self.ids.set_name.text
        #self.flashcards = db_f.retrieve_set(filename)
        for card in flashcard_set.Flashcards:
            label_term = MyLabel(text=card.Question, halign='center', valign='middle')
            # with label_term.canvas:
            #     Color(0, 1, 0, 0.25)
            #     Rectangle(pos=label_term.pos, size=label_term.size)
            label_def = MyLabel(text=card.Answer, halign='center', valign='middle')
            # with label_term.canvas:
            #     Color(0, 1, 0, 0.25)
            #     Rectangle(pos=label_term.pos, size=label_term.size)
            self.card_labels.append(label_term)
            self.card_labels.append(label_def)
            self.ids.grid.add_widget(label_term)
            self.ids.grid.add_widget(label_def)

    def on_leave(self, *args):
        for label in self.card_labels:
            self.ids.grid.remove_widget(label)

    def pressed(self, instance):
        filename = instance.text.split(':')[0]
        instance.text = 'Opening ' + filename + '.txt'


class CreateSet(Screen):
    description = ObjectProperty(None)

    def log_out(self):
        sm.current = "login"
        self.reset()

    def mainMenu(self):
        sm.current = "homeScreenWindow"
        self.reset()

    def reset(self):
        self.description.text = ""

    def createSet(self):
        global flashcard_set
        flashcard_set = classes.Set(db_x.get_id(mail), self.description.text)
        # print(flashcard_set.ID)
        # print(flashcard_set.Flashcards)
        self.reset()
        sm.current = "createFlashcard"


class CreateFlashcard(Screen):
    front = ObjectProperty(None)
    back = ObjectProperty(None)

    def log_out(self):
        sm.current = "login"

    def mainMenu(self):
        sm.current = "homeScreenWindow"

    def reset(self):
        self.front.text = ""
        self.back.text = ""

    def show_popup1(self):
        show = P2()
        popupWindow = Popup(title="Create flashcard", content=show, size_hint=(None, None), size=(300, 200))
        popupWindow.open()

    '''
    def createFlashcard(self):
        user_id = db_x.get_id(mail)
        db_x.add_flashcard(self.front.text, self.back.text, "5ec10633be0a393195f3866b", "5eb737df92763182cc3c835d")
        self.reset()
        self.show_popup1()
        sm.current = "createFlashcard"
    '''

    def show_popup2(self):
        show = P3()
        popupWindow = Popup(title="Create flashcard", content=show, size_hint=(None, None), size=(300, 200))
        popupWindow.open()

    def addFlashcard(self):
        flashcard = classes.Flashcard(self.front.text, self.back.text, db_x.get_id(mail), flashcard_set.ID)
        flashcard_set.addFlashcard(flashcard)
        # print(flashcard_set.Flashcards)
        self.show_popup2()
        self.reset()

    def uploadSet(self):
        db_x.upload_set(flashcard_set)
        sm.current = "homeScreenWindow"


class SearchSet(Screen):
    keyword = ObjectProperty(None)

    def mainMenu(self):
        sm.current = "homeScreenWindow"
        self.reset()

    def searchSet(self):
        global current_sets
        current_sets = db_x.sets_list_for_selection(self.keyword.text)

        sm.current = "availableSets"
        self.reset()

    def reset(self):
        self.keyword.text = ""


# class AvailableSets(RecycleView):
#     # def mainMenu(self):
#     #     sm.current="homeScreenWindow"
#     def __init__(self, **kwargs):
#         super(AvailableSets, self).__init__(**kwargs)
#         print("im here!!!")
#         self.data = [{'text': cardsset.description} for cardsset in current_sets]
#         # for cardset in current_sets:
#         #     print(cardset.description)
#         # # self.data = [{'text': str(x)} for x in range(10)]
#         # self.data = [{'text': cardsset.description} for cardsset in current_sets]


class AvailableSets(Screen):
    def __init__(self, **kwargs):
        super(AvailableSets, self).__init__(**kwargs)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.sets = []

    def on_enter(self, *args):
        for (key, cardsSet) in current_sets.items():
            button = Button(text=cardsSet.description + " : ID:"+str(cardsSet.ID))
            button.size_hint = (0.8, 0.35)
            button.bind(on_press=self.pressed)
            self.sets.append(button)
            self.ids.grid.add_widget(button)

    def pressed(self, instance):
        setID = instance.text.split(':')[2]
        global flashcard_set
        flashcard_set = current_sets[ObjectId(setID)]
        current_sets.clear()
        sm.current = "learning"

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    '''blablabla'''


# class SelectableLabel(RecycleDataViewBehavior, Label):
#     ''' Add selection support to the Label '''
#     index = None
#     selected = BooleanProperty(False)
#     selectable = BooleanProperty(True)
#
#     def refresh_view_attrs(self, rv, index, data):
#         ''' Catch and handle the view changes '''
#         self.index = index
#         return super(SelectableLabel, self).refresh_view_attrs(
#             rv, index, data)
#
#     def on_touch_down(self, touch):
#         ''' Add selection on touch down '''
#         if super(SelectableLabel, self).on_touch_down(touch):
#             return True
#         if self.collide_point(*touch.pos) and self.selectable:
#             return self.parent.select_with_touch(self.index, touch)
#
#     def apply_selection(self, rv, index, is_selected):
#         ''' Respond to the selection of items in the view. '''
#         self.selected = is_selected
#         if is_selected:
#             print("selection changed to {0}".format(rv.data[index]))
#         else:
#             print("selection removed for {0}".format(rv.data[index]))


class P2(FloatLayout):
    pass


class P(FloatLayout):
    pass


class P1(FloatLayout):
    pass


class P3(FloatLayout):
    pass


screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),
           HomeWindow(name="home"), LearningWindow(name="learning"), MySetsWindow(name="my_sets")
    , HomeScreenWindow(name="homeScreenWindow"), CreateFlashcard(name="createFlashcard"), CreateSet(name="createSet"),
           SearchSet(name="searchSet"), AvailableSets(name="availableSets")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    font_size_large = NumericProperty(20)

    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
