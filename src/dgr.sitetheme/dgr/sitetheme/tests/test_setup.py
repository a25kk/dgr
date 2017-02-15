# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from dgr.buildout.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of dgr.buildout into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if dgr.buildout is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('dgr.buildout'))

    def test_uninstall(self):
        """Test if dgr.buildout is cleanly uninstalled."""
        self.installer.uninstallProducts(['dgr.buildout'])
        self.assertFalse(self.installer.isProductInstalled('dgr.buildout'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IDgrBuildoutLayer is registered."""
        from dgr.buildout.interfaces import IDgrBuildoutLayer
        from plone.browserlayer import utils
        self.failUnless(IDgrBuildoutLayer in utils.registered_layers())
