"""
sipd_bot package initializer.

This module defines the main `SIPDBot` class by combining the base
functionality and mixin classes for modular actions such as login and
interactions with the SIPD-RI web application.

Classes:
    SIPDBot: The unified bot class composed of base and mixin components.
"""

from .base import SIPDBotBase
from .login import LoginMixin
from .utils import UtilsMixin
from .aklap_jurnal_umum import AklapJurnalUmumMixin
from .aklap_posting_jurnal import AklapPostingJurnalMixin
from .aklap_lampiran import AklapLampiranMixin


class SIPDBot(
    SIPDBotBase,
    LoginMixin,
    UtilsMixin,
    AklapJurnalUmumMixin,
    AklapPostingJurnalMixin,
    AklapLampiranMixin,
):
    """
    The main SIPDBot class combining all mixins.
    """
