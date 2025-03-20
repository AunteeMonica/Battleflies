class AdminLogicException(Exception):
    pass

class CatchCooldownIncompleteException(Exception):
    pass

class DailyCooldownIncompleteException(Exception):
    pass

class DailyLogicException(Exception):
    pass

class HigherPageSpecifiedException(Exception):
    pass

class HigherReleaseQuantitySpecifiedException(Exception):
    pass

class ImproperDailyShopItemNumberException(Exception):
    pass

class InventoryLogicException(Exception):
    pass

class LegendaryBattleflyServiceException(Exception):
    """Raised when an issue occurs in the Legendary Battlefly service."""
    pass

class CocoonDoesNotExistException(Exception):
    """Raised when a specified cocoon does not exist."""
    pass

class NotEnoughCocoonQuantityException(Exception):
    """Raised when an Ally does not have enough cocoons."""
    pass

class MiscLogicException(Exception):
    pass

class NoEggCountException(Exception):
    pass

class NotEnoughDailyShopTokensException(Exception):
    pass

class NotEnoughExchangeBattleflyQuantityException(Exception):
    pass

class NotEnoughExchangeBattleflySpecifiedException(Exception):
    pass

class NotEnoughRerollsException(Exception):
    pass

class TheSproutLogicException(Exception):
    pass

class TheSproutSaleAlreadyMadeException(Exception):
    pass

class PageQuantityTooLow(Exception):
    pass

class BattleflyBotAssetsException(Exception):
    pass

class BattleflyBotGeneratorException(Exception):
    pass

class BattleflyBotRatesException(Exception):
    pass

class BattleflyBotStatusException(Exception):
    pass

class BattleflyDoesNotExistException(Exception):
    pass

class ReleaseBattleflyException(Exception):
    pass

class ReleaseQuantityTooLow(Exception):
    pass

class TooManyExchangeBattleflySpecifiedException(Exception):
    pass

class AllyServiceException(Exception):
    pass

class UnavailableBattleflyToTradeException(Exception):
    pass

class UnregisteredAllyException(Exception):
    """Raised when an Ally is not registered."""
    pass
