import arcade
import csv
import arcade.gui
import pandas as pd
from arcade.gui import UIManager
import random
import arcade.key
import pkg_resources.py2_warn

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Jeopardy Total"


def split(string, size):
    if string is None:
        return " "
    splits = string.split()
    if len(splits) <= size:
        return string
    elif len(splits) <= size * 2:
        string = ""
        for x in splits[:size:]:
            string += x + " "
        string += "\n"
        for x in splits[size::]:
            string += x + " "
        return string
    elif len(splits) <= size * 3:
        string = ""
        for x in splits[:size:]:
            string += x + " "
        string += "\n"
        for x in splits[size:size * 2:]:
            string += x + " "
        string += "\n"
        for x in splits[size * 2::]:
            string += x + " "
        return string
    elif len(splits) <= size * 4:
        string = ""
        for x in splits[:size:]:
            string += x + " "
        string += "\n"
        for x in splits[size:size * 2:]:
            string += x + " "
        string += "\n"
        for x in splits[size * 2:size * 3:]:
            string += x + " "
        string += "\n"
        for x in splits[size * 3::]:
            string += x + " "
        return string
    string = ""
    for x in splits[:size:]:
        string += x + " "
    string += "\n"
    for x in splits[size:size * 2:]:
        string += x + " "
    string += "\n"
    for x in splits[size * 2:size * 3:]:
        string += x + " "
    string += "\n"
    for x in splits[size * 3:size * 4:]:
        string += x + " "
    for x in splits[size * 4::]:
        string += x + " "
    return string


def randq():
    return random.randint(0, 377094)


class CorrectButton(arcade.gui.UIFlatButton):
    def __init__(self, center_x, center_y, questions_correct, value, earnings):
        super().__init__(
            'Correct',
            center_x=center_x,
            center_y=center_y,
            width=250
        )
        self.earnings = earnings
        self.value = value
        self.questions_correct = questions_correct

    def on_click(self):
        self.questions_correct += 1
        self.earnings = self.earnings + self.value


class SaveButton(arcade.gui.UIFlatButton):
    def __init__(self, center_x, center_y, value, category, question, correct_answer, user_answer):
        super().__init__(
            'Save Q ',
            center_x=center_x,
            center_y=center_y,
            width=100
        )
        self.value = value
        self.category = category,
        self.question = question,
        self.correct_answer = correct_answer,
        self.user_answer = user_answer,

    def on_click(self):
        row = [self.category, self.value, self.question, self.correct_answer, self.user_answer]
        with open('saved_questions.csv', 'a') as fd:
            writer = csv.writer(fd)
            writer.writerow(row)


class IncorrectButton(arcade.gui.UIFlatButton):
    def __init__(self, center_x, center_y, questions_incorrect, value, earnings):
        super().__init__(
            'Incorrect',
            center_x=center_x,
            center_y=center_y,
            width=250
        )
        self.earnings = earnings
        self.value = value
        self.questions_incorrect = questions_incorrect

    def on_click(self):
        self.questions_incorrect += 1
        self.earnings = self.earnings - self.value


class TitleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        # play intro song
        self.title_sound = arcade.load_sound("intro.wav")
        # arcade.play_sound(self.title_sound)

    def setup(self):
        self.background = arcade.load_texture("background.png")

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        arcade.draw_text("Welcome! Click to begin", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100,
                         arcade.color.DARK_TANGERINE, font_size=60, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        arcade.stop_sound(self.title_sound)
        game_view = QuestionView(0, 0, 0, 0)
        game_view.setup()
        self.window.show_view(game_view)


class QuestionView(arcade.View):

    def __init__(self, questions_correct, questions_incorrect, question_count, earnings, bank=None):
        super().__init__()
        self.question_count = question_count + 1
        self.questions_correct = questions_correct
        self.questions_incorrect = questions_incorrect
        self.earnings = earnings

        if bank is None:
            self.bank = pd.read_csv('final_jeopardy_data.csv')
        else:
            self.bank = bank

        number = randq()
        self.question = self.bank['clue'].values[number]
        self.question = split(self.question, 9)
        self.answer = self.bank['answer'].values[number]
        self.answer = split(self.answer, 3)
        self.category = self.bank['category'].values[number]
        self.value = self.bank['value'].values[number]
        self.input = None
        self.ui_manager = UIManager(self.window)

    def setup(self):
        self.ui_manager.purge_ui_elements()
        ui_input_box = arcade.gui.UIInputBox(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT - 400,
            width=300
        )
        ui_input_box.text = 'X'
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.input = ui_input_box
        self.ui_manager.add_ui_element(self.input)

        save_button = SaveButton(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT - 450,
            value=self.value,
            category=self.category,
            question=self.question,
            correct_answer=self.answer,
            user_answer=self.input.text
        )
        self.ui_manager.add_ui_element(save_button)

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        start_y = SCREEN_HEIGHT - 100
        start_x = SCREEN_WIDTH / 2

        arcade.draw_text("$" + str(self.earnings),
                         start_x, start_y + 50, arcade.color.DARK_TANGERINE, font_size=20, align="center",
                         anchor_x="center")
        arcade.draw_text(self.category,
                         start_x, start_y, arcade.color.DARK_TANGERINE, font_size=40, align="center",
                         anchor_x="center")
        start_y = start_y - 50
        arcade.draw_text("$" + str(self.value),
                         start_x, start_y, arcade.color.DARK_TANGERINE, font_size=20, align="center",
                         anchor_x="center")
        start_y = start_y - 100
        arcade.draw_text(self.question,
                         start_x, start_y, arcade.color.DARK_TANGERINE, font_size=20, align="center",
                         anchor_x="center")
        start_y = 20
        start_x = 10
        arcade.draw_text("Questions Correct: " + str(self.questions_correct),
                         start_x, start_y, arcade.color.WHITE, font_size=25, align="left")
        arcade.draw_text("Questions Incorrect: " + str(self.questions_incorrect),
                         SCREEN_WIDTH - 300, start_y, arcade.color.WHITE, font_size=25, align="left")
        start_y = 70
        start_x = SCREEN_WIDTH / 2
        arcade.draw_text("Questions Seen: " + str(self.question_count),
                         start_x, start_y, arcade.color.WHITE, font_size=25, align="center", anchor_x='center')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            game_view = AnswerView(self.questions_correct, self.questions_incorrect, self.question_count,
                                   self.input.text, self.answer, self.earnings, self.value, self.bank, self.category, self.question)
            self.ui_manager.purge_ui_elements()
            game_view.setup()
            self.window.show_view(game_view)


class AnswerView(arcade.View):

    def __init__(self, questions_correct, questions_incorrect, question_count, user_answer, correct_answer, earnings,
                 value, bank, category, question):
        super().__init__()
        self.category = category
        self.question = question
        self.question_count = question_count
        self.questions_correct = questions_correct
        self.questions_incorrect = questions_incorrect
        self.earnings = earnings
        self.bank = bank
        self.user_answer = user_answer
        self.correct_answer = correct_answer
        self.value = value
        self.incorrect = None
        self.correct = None
        self.ui_manager = UIManager(self.window)

    def setup(self):
        self.incorrect = IncorrectButton(
            center_x=int(4 * SCREEN_WIDTH / 5),
            center_y=100,
            questions_incorrect=self.questions_incorrect,
            value=self.value,
            earnings=self.earnings
        )
        self.ui_manager.add_ui_element(self.incorrect)
        self.correct = CorrectButton(
            center_x=int(SCREEN_WIDTH / 5),
            center_y=100,
            questions_correct=self.questions_correct,
            value=self.value,
            earnings=self.earnings
        )
        self.ui_manager.add_ui_element(self.correct)
        save_button = SaveButton(
            center_x=int(SCREEN_WIDTH / 2),
            center_y=SCREEN_HEIGHT - 450,
            value=self.value,
            category=self.category,
            question=self.question,
            correct_answer=self.correct_answer,
            user_answer=self.user_answer
        )
        self.ui_manager.add_ui_element(save_button)

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        start_y = SCREEN_HEIGHT / 2
        start_x = SCREEN_WIDTH / 5

        arcade.draw_text("Correct Answer",
                         start_x, 700, arcade.color.DARK_TANGERINE, font_size=40, align="center",
                         anchor_x="center")

        arcade.draw_text(str(self.correct_answer),
                         start_x, start_y, arcade.color.DARK_TANGERINE, font_size=25, align="center",
                         anchor_x="center")

        start_y = SCREEN_HEIGHT / 2
        start_x = 4 * SCREEN_WIDTH / 5

        arcade.draw_text("User Answer",
                         start_x, 700, arcade.color.DARK_TANGERINE, font_size=40, align="center",
                         anchor_x="center")
        answer = split(str(self.user_answer), 3)
        try:
            arcade.draw_text(answer, start_x, start_y, arcade.color.DARK_TANGERINE, font_size=25, align="center",
                             anchor_x="center")
        except:
            arcade.draw_text('None', start_x, start_y, arcade.color.DARK_TANGERINE, font_size=25, align="center",
                             anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            self.ui_manager.purge_ui_elements()
            if not self.earnings == self.correct.earnings:
                self.earnings = self.correct.earnings
            else:
                self.earnings = self.incorrect.earnings
            game_view = QuestionView(self.correct.questions_correct, self.incorrect.questions_incorrect,
                                     self.question_count,
                                     self.earnings, self.bank)
            game_view.setup()
            self.window.show_view(game_view)


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = TitleView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
