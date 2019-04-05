from guesstheword.game import GuessTheWordGame
from guesstheword.examples.judges import Judge
from guesstheword.examples.masks import NoneWordMask
from guesstheword.examples.players import Player, PlayerManager
from guesstheword.examples.restrictions import MaxFailsPlayerRestriction
from guesstheword.examples.vocabularies import RandomVocabulary

from src.client import ConsoleClient


def create_game():
    game = GuessTheWordGame(
        mask=NoneWordMask(),
        vocabulary=RandomVocabulary(),
    )
    return game


def create_player_manager():
    manager = PlayerManager(max_players=2)
    manager.add_player(player=Player(name='Player 1'))
    manager.add_player(player=Player(name='Player 2'))
    return manager


def create_judge():
    restrictions = (MaxFailsPlayerRestriction(),)
    judge = Judge(restrictions=restrictions)
    return judge


def main():

    game = create_game()
    judge = create_judge()
    manager = create_player_manager()

    client = ConsoleClient(
        game=game,
        judge=judge,
        manager=manager
    )
    client.start()


if __name__ == "__main__":
    main()
