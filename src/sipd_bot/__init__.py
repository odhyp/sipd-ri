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
from .aklap_lampiran import AklapLampiranMixin
from .aklap_jurnal_umum import AklapJurnalUmumMixin


class SIPDBot(
    SIPDBotBase, LoginMixin, UtilsMixin, AklapLampiranMixin, AklapJurnalUmumMixin
):
    """
    The main SIPDBot class combining all mixins.
    """
