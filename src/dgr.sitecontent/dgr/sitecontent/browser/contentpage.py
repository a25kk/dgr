# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter
from zope.component import getUtility

from dgr.sitecontent.contentpage import IContentPage

from dgr.sitecontent.interfaces import IResponsiveImagesTool

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class ContentPageView(BrowserView):
    """ Folderish content page default view """

    def has_leadimage(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def has_contacts(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.relatedContacts
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def display_gallery(self):
        context = aq_inner(self.context)
        try:
            display = context.displayGallery
        except AttributeError:
            display = None
        if display is not None:
            return display
        return False

    def display_cards(self):
        context = aq_inner(self.context)
        try:
            display = context.displayPreviewCards
        except AttributeError:
            display = None
        if display is not None:
            return display
        return False

    def contained_pages(self):
        context = aq_inner(self.context)
        items = api.content.find(
            context=context,
            depth=1,
            object_provides=IContentPage,
            sort_on='getObjPositionInParent'
        )
        return items

    def has_contained_pages(self):
        return len(self.contained_pages()) > 0

    def rendered_card(self, uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@card-view')()
        return template

    def rendered_gallery(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@gallery-view')()
        return template

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)

    def image_data(self):
        data = {}
        sizes = ['small', 'medium', 'large']
        idx = 0
        for size in sizes:
            idx += 0
            img = self._get_scaled_img(size)
            data[size] = '{0} {1}w'.format(img['url'], img['width'])
        return data

    def _get_scaled_img(self, size):
        context = aq_inner(self.context)
        scales = getMultiAdapter((context, self.request), name='images')
        if size == 'small':
            scale = scales.scale('image', width=300, height=300)
        if size == 'medium':
            scale = scales.scale('image', width=600, height=600)
        else:
            scale = scales.scale('image', width=900, height=900)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item


class CardView(BrowserView):
    """ Embeddable preview card for content pages """

    def has_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def get_image_data(self, uuid):
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)


class CardPreview(BrowserView):
    """Preview embeddable content page preview cards"""

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def rendered_card(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@card-view')()
        return template


class GalleryPreview(BrowserView):
    """Preview embeddable image gallery"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def rendered_gallery(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@gallery-view')()
        return template


class GalleryView(BrowserView):
    """Provide gallery of contained image content"""

    def __call__(self):
        self.has_assets = len(self.contained_images()) > 0
        return self.render()

    def render(self):
        return self.index()

    def has_leadimage(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def leadimage_tag(self):
        context = aq_inner(self.context)
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image', width=900, height=900)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item

    def contained_images(self):
        context = aq_inner(self.context)
        data = context.restrictedTraverse('@@folderListing')(
            portal_type='Image',
            sort_on='getObjPositionInParent')
        return data

    def image_tag(self, image):
        context = image.getObject()
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('image', width=900, height=900)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item

    def _get_scaled_img(self, size):
        context = aq_inner(self.context)
        scales = getMultiAdapter((context, self.request), name='images')
        if size == 'small':
            scale = scales.scale('image', width=300, height=300)
        if size == 'medium':
            scale = scales.scale('image', width=600, height=600)
        else:
            scale = scales.scale('image', width=900, height=900)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        else:
            item['url'] = IMG
            item['width'] = '1px'
            item['height'] = '1px'
        return item
