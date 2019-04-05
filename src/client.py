from guesstheword.exceptions import ValidationError
from guesstheword.examples.score import MaxScoreFileSaver
from guesstheword.examples.validators import InputLengthValidator


class ConsoleClient:
    """
    Console game client example.
    Read letter from user input and write hidden word to output.

    """
    def __init__(self, game, judge, manager):
        self._game = game
        self._judge = judge
        self._manager = manager

    @staticmethod
    def prepare_word(word):
        """
        Mask word as "_ _ a _ _" where "_" is letter to guess.

        Args:
            word (list): Hidden word as list of letters.

        Returns:
            (str): Masked word for output.

        """
        return ' '.join((m or '_' for m in word))

    def start(self):

        print('Welcome to game Guess the word!')

        while True:

            current_player = self._manager.current_player

            # If game is aborted by judge.
            if self._judge.is_game_over(self._game):
                break

            # If there is not any active player left.
            if not self._manager.active_players_count:
                break

            print('Player "{player.name}" in game. Good luck!'.format(player=current_player))
            print('Hidden word is: {0}'.format(self.prepare_word(self._game.word)))

            letter = input('Enter a letter >>> ').strip()

            validator = InputLengthValidator()
            try:
                validator.validate(letter)
            except ValidationError:
                print(validator.get_message())
                continue

            if letter in self._game.used_letters:
                print('Letter has been chosen before. Please try again.')
                continue

            success = self._game.guess(letter)

            if success:
                current_player.got_it()

                print('Got it!')

                # If game over (all letters are guessed).
                if self._game.is_victory:
                    current_player.win_game()
                    break
            else:
                current_player.missed()

                print('Missed!')

                if not self._judge.is_player_allowed_to_play(current_player):
                    current_player.left_game()

                self._manager.next_player()

        print('Game over!')

        if self._game.is_victory:
            score_saver = MaxScoreFileSaver()
            players_score = self._judge.get_score(current_player)
            score_saver.set_score_and_name(players_score, current_player.name)

            print('Congratulations! Winner is: "{player.name}"'.format(player=current_player))
            print('Winner\'s score is "{0}"'.format(players_score))
            print('Max score is "{0}" ({1})'.format(*score_saver.get_score_and_name()))
        else:
            print('Sorry, no winner for this game. Please try again.')
