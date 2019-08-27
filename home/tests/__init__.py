"""
LetLive Wep Application Tests
=============================

Tests for the LetLive web application.

Has tests for the modules below:

* Models:

  * home.models.userModel

* Views:

  * home.views.registrationView
  * home.views.profileView
  * home.views.userView
"""
from .authTests import AuthTests
from .userTests import AppUsersTests
from .userClientTests import UserClientTests

