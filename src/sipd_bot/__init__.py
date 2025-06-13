from .base import SIPDBotBase
from .login import LoginMixin


class SIPDBot(SIPDBotBase, LoginMixin):
    """
    The main SIPDBot class combining all mixins.
    """
