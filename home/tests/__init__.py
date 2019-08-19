"""
LetLive Wep Application Tests
=============================

Tests for the LetLive web application.

Has tests for the modules below:

* Models:

  * home.models.userModel.AppUsers

* Views:

  * home.views.authView
"""
from .tests import AppClientTestCase
from .userTests import AppUsersTests
from .authTests import AuthTests
from .userPermission import UserPermissionTests
