from constant.errorCodes import ErrorCodes
from discord.ext import commands

class PlayerIDInvalid(commands.CommandError):

    def __init__(self, playerID, *args, **kwargs):
        self.playerID = playerID
        self.message = f"Player ID {playerID} is Invalid. Enter a valid Player ID"
        self.errors = ErrorCodes.InvalidPlayerId
        super().__init__(*args, **kwargs)


class PlayerIdNotFound(commands.CommandError):

    def __init__(self, playerID, *args, **kwargs):
        self.playerID = playerID
        self.message = f"Player ID {playerID} is Invalid Or Not Public. Please make sure player ID is Valid and profile is public"
        self.errors = ErrorCodes.PlayerIdNotFound
        super().__init__(*args, **kwargs)

class MatchIdNotFound(commands.CommandError):

    def __init__(self, matchId, *args, **kwargs):
        self.matchId = matchId
        self.message = f"Match ID {matchId} not found"
        self.errors = ErrorCodes.InvalidMatchId
        super().__init__(*args, **kwargs)