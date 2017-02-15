# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from dgr.sitecontent.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of dgr.sitecontent into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if dgr.sitecontent is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.dgrroductInstalled('dgr.sitecontent'))

    def test_uninstall(self):
        """Test if dgr.sitecontent is cleanly uninstalled."""
        self.installer.uninstallProducts(['dgr.sitecontent'])
        self.assertFalse(self.installer.dgrroductInstalled('dgr.sitecontent'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IDgrSitecontentLayer is registered."""
        from dgr.sitecontent.interfaces import IDgrSitecontentLayer
        from plone.browserlayer import utils
        self.failUnless(IDgrSitecontentLayer in utils.registered_layers())
