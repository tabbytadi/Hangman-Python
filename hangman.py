import wx
import random

class HangmanGame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Hang me not", size=(400, 350))
        self.panel = wx.Panel(self)
        self.load_words()
        self.init_ui()
        self.Center()
        self.Show()

    def load_words(self):
        with open("words.txt", "r") as file:
            self.words = file.read().splitlines()

    def init_ui(self):
        self.word = random.choice(self.words)
        self.remaining_attempts = 6
        self.guesses = set(self.word[0] + self.word[-1])

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.word_label = wx.StaticText(self.panel, label=self.get_display_word())
        vbox.Add(self.word_label, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        # Remaining attempts label
        self.remaining_label = wx.StaticText(self.panel, label=f"Remaining attempts: {self.remaining_attempts}")
        vbox.Add(self.remaining_label, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        # Toggle buttons for alphabet
        grid = wx.GridSizer(3, 9, 5, 5)
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in alphabet:
            btn = wx.ToggleButton(self.panel, label=letter)
            btn.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_button)
            grid.Add(btn, 0, wx.EXPAND)
        vbox.Add(grid, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        self.hangman_bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap("hangman0.png", wx.BITMAP_TYPE_ANY))
        vbox.Add(self.hangman_bitmap, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        guess_btn = wx.Button(self.panel, label='Guess')
        guess_btn.Bind(wx.EVT_BUTTON, self.on_guess_button)
        vbox.Add(guess_btn, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        self.panel.SetSizer(vbox)

    def get_display_word(self):
        display_word = self.word[0] + ''.join(
            [char if char in self.guesses or char == self.word[0] or char == self.word[-1] else '_' for char in
             self.word[1:-1]]) + self.word[-1]
        return display_word

    def update_display(self):
        self.word_label.SetLabel(self.get_display_word())
        self.hangman_bitmap.SetBitmap(wx.Bitmap(f"hangman{6 - self.remaining_attempts}.png", wx.BITMAP_TYPE_ANY))
        self.remaining_label.SetLabel(f"Remaining attempts: {self.remaining_attempts}")

    def check_win(self):
        word_set = set(self.word)
        return word_set == self.guesses

    def on_toggle_button(self, event):
        btn = event.GetEventObject()
        letter = btn.GetLabel()

        if letter not in self.guesses:
            if letter in self.word:
                self.guesses.add(letter)
                self.update_display()
                if self.check_win():
                    wx.MessageBox("Congratulations! You guessed the word!", "Hangman Game")
                    self.Close()
            else:
                self.remaining_attempts -= 1
                self.update_display()
                if self.remaining_attempts == 0:
                    wx.MessageBox(f"Sorry, you lost! The word was '{self.word}'", "Hangman Game")
                    self.Close()

    def on_guess_button(self, event):
        pass

if __name__ == '__main__':
    app = wx.App()
    HangmanGame()
    app.MainLoop()
