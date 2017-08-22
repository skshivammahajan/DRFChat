from experchat.choices import ChoiceEnum


class FeedProviders(int, ChoiceEnum):
    """
    Choices for Provider
    """
    FACEBOOK = 1
    INSTAGRAM = 2
    YOUTUBE = 3
    RSS = 4
    EXPERT_CHAT = 5


class FeedTypes(int, ChoiceEnum):
    """
    Type of the feeds like pages. channels
    """
    USER = 1
    PAGE = 2
    CHANNEL = 3
    FEED = 4
