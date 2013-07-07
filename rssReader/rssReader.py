# -*- coding: utf-8 -*-
'''
Created on 2013-6-17

@author: hai
'''
from __future__ import with_statement
from globals import *
import sys, os
import datatable
from datatable import Post, Feed
from htmlentitydefs import name2codepoint as n2cp
import re
import operator
from PyQt4 import QtGui, QtCore, QtWebKit
from ui.Ui_about import Ui_Dialog as UI_AboutDialog
from ui.Ui_filterwidget import Ui_Form as UI_FilterWidget
from ui.Ui_searchwidget import Ui_Form as UI_SearchWidget
from ui.Ui_main import Ui_MainWindow

import sqlalchemy as sql
import elixir

from postmodel import PostModel


class FilterWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Set up the UI from designer
        self.ui = UI_FilterWidget()
        self.ui.setupUi(self)


class SearchWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Set up the UI from designer
        self.ui = UI_SearchWidget()
        self.ui.setupUi(self)


class AboutDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        # Set up the UI from designer
        self.ui = UI_AboutDialog()
        self.ui.setupUi(self)


class TrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self):
        QtGui.QSystemTrayIcon.__init__(self, QtGui.QIcon(":/urssus.svg"))

    def updateIcon(self):

        uc = root_feed.unreadCount()
        self.setToolTip('%d unread posts' % uc)
        if uc:
            self.setIcon(QtGui.QIcon(':/urssus-unread.svg'))
        else:
            self.setIcon(QtGui.QIcon(':/urssus.svg'))


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Internal indexes
        self.combinedView = False
        self.showingFolder = False
        self.pendingFeedUpdates = {}

        # Set up the UI from designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # add widgets to status bar
        self.progress = QtGui.QProgressBar()
        self.progress.setFixedWidth(120)
        self.ui.statusBar.addPermanentWidget(self.progress)

        # Article filter fields
        self.filterWidget = FilterWidget()
        self.ui.filterBar.addWidget(self.filterWidget)
        QtCore.QObject.connect(self.filterWidget.ui.filter, QtCore.SIGNAL("returnPressed()"), self.filterPosts)
        QtCore.QObject.connect(self.filterWidget.ui.clear, QtCore.SIGNAL("clicked()"), self.unFilterPosts)
        QtCore.QObject.connect(self.filterWidget.ui.statusCombo, QtCore.SIGNAL("currentIndexChanged(int)"),
                               self.filterPostsByStatus)
        self.statusFilter = None
        self.textFilter = ''
        # Make status filter persistent
        self.filterWidget.ui.statusCombo.setCurrentIndex(config.getValue('ui', 'statusFilter', 0))

        # Search widget
        self.ui.searchBar.hide()
        self.searchWidget = SearchWidget()
        self.ui.searchBar.addWidget(self.searchWidget)
        QtCore.QObject.connect(self.searchWidget.ui.next, QtCore.SIGNAL("clicked()"), self.findText)
        QtCore.QObject.connect(self.searchWidget.ui.previous, QtCore.SIGNAL("clicked()"), self.findTextReverse)
        QtCore.QObject.connect(self.searchWidget.ui.close, QtCore.SIGNAL("clicked()"), self.ui.searchBar.hide)
        QtCore.QObject.connect(self.searchWidget.ui.close, QtCore.SIGNAL("clicked()"), self.ui.view.setFocus)
        # Completion with history
        self.searchHistory = []
        self.filterHistory = []

        # Set some properties of the Web view
        page = self.ui.view.page()
        if not config.getValue('options', 'followLinksInUrssus', False):
            page.setLinkDelegationPolicy(page.DelegateAllLinks)
        self.ui.view.setFocus(QtCore.Qt.TabFocusReason)
        QtWebKit.QWebSettings.globalSettings().setUserStyleSheetUrl(QtCore.QUrl(cssFile))
        QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        QtWebKit.QWebSettings.globalSettings().setWebGraphic(QtWebKit.QWebSettings.MissingImageGraphic,
                                                             QtGui.QPixmap(':/file_broken.svg').scaledToHeight(24))
        copy_action = self.ui.view.page().action(QtWebKit.QWebPage.Copy)
        self.ui.view.page().action(QtWebKit.QWebPage.OpenLinkInNewWindow).setVisible(False)
        copy_action.setIcon(QtGui.QIcon(':/editcopy.svg'))
        self.ui.menu_Edit.insertAction(self.ui.actionFind, copy_action)
        self.ui.menu_Edit.insertSeparator(self.ui.actionFind)
        self.ui.view.setFocus(QtCore.Qt.TabFocusReason)

        # Set sorting for post list
        column, order = config.getValue('ui', 'postSorting', [2, QtCore.Qt.DescendingOrder])
        order = [QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder][order]
        self.ui.posts.sortByColumn(column, order)
        # Set custom context menu hook in post list header
        header = self.ui.posts.header()
        header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(header, QtCore.SIGNAL("customContextMenuRequested(const QPoint)"),
                               self.postHeaderContextMenu)
        QtCore.QObject.connect(header, QtCore.SIGNAL("sectionMoved ( int, int, int)"), self.savePostColumnPosition)

        # Timer to trigger status bar updates
        self.statusTimer = QtCore.QTimer()
        self.statusTimer.setSingleShot(True)
        QtCore.QObject.connect(self.statusTimer, QtCore.SIGNAL("timeout()"), self.updateStatusBar)
        self.statusTimer.start(1000)

        #����  preferences
        self.loadPreferences()

        # Tray icon
        self.tray = TrayIcon()
        self.tray.show()
        self.notifiedFeed = None
        QtCore.QObject.connect(self.tray, QtCore.SIGNAL("messageClicked()"), self.notificationClicked)
        QtCore.QObject.connect(self.tray, QtCore.SIGNAL("activated( QSystemTrayIcon::ActivationReason)"),
                               self.trayActivated)
        self.tray.updateIcon()
        self.setWindowIcon(self.tray.icon())
        traymenu = QtGui.QMenu(self)
        traymenu.addAction(self.ui.actionFetch_All_Feeds)
        traymenu.addSeparator()
        traymenu.addAction(self.ui.actionQuit)
        self.tray.setContextMenu(traymenu)

        # ������action��ӵ�������ڣ��Ա������ش���ʱ���ܹ���
        # the menu bar is hidden (tricky!)
        for action in self.ui.menuBar.actions():
            self.addAction(action)

        self.showOnlyUnread = False

        self.initTree()
        if self.showOnlyUnread:
            self.ui.actionShow_Only_Unread_Feeds.setChecked(self.showOnlyUnread)
            self.on_actionShow_Only_Unread_Feeds_triggered(self.showOnlyUnread)

        self.feedStatusTimer = QtCore.QTimer()
        self.feedStatusTimer.setSingleShot(True)
        QtCore.QObject.connect(self.feedStatusTimer, QtCore.SIGNAL("timeout()"), self.updateFeedStatus)
        self.feedStatusTimer.start(3000)
        # Start the background feedupdater
        feedUpdateQueue.put([1])

    def initTree(self):
        """
        init the tree


        """
        self.setEnabled(False)
        self.ui.feedTree.initTree()
        self.fixFeedListUI()
        self.setEnabled(True)
        self.filterWidget.setEnabled(True)
        self.searchWidget.setEnabled(True)

    def fixFeedListUI(self):
       # 中文测试
        header = self.ui.feedTree.header()
        header.setStretchLastSection(False)
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Fixed)
        header.resizeSection(1, header.fontMetrics().width(' Unread ') + 4)


    def filterPosts(self):
        pass

    def unFilterPosts(self):
        pass

    def filterPostsByStatus(self):
        pass

    def findText(self):
        pass

    def findTextReverse(self):
        pass

    def postHeaderContextMenu(self):
        pass

    def savePostColumnPosition(self):
        pass


    def notificationClicked(self):
        pass

    def trayActivated(self):
        pass

    def loadPreferences(self):
        pass

    def on_feedTree_itemClicked(self, item, column=None):
        if not item:
            return
        feed = item.feed
        self.open_feed2(item)
        if not self.combinedView:
            self.ui.view.setHtml(renderTemplate('feed.tmpl', feed=feed))

    def on_feedTree_itemExpanded(self, item):
        feed = item.feed
        try:
            feed.is_open = True
            elixir.session.commit()
        except:
            elixir.session.rollback()

    def on_feedTree_itemCollapsed(self, item):
        feed = item.feed
        try:
            feed.is_open = False
            elixir.session.commit()
        except:
            elixir.session.rollback()

    def on_actionShow_Only_Unread_Feeds_triggered(self, checked=None):
        if checked == None: return
        self.showOnlyUnread = checked
        config.setValue('ui', 'showOnlyUnreadFeeds', checked)
        for feed in Feed.query.filter(Feed.xmlUrl != None):
            if feed.unreadCount() == 0:
                self.queueFeedUpdate(feed)

    def queueFeedUpdate(self, feed, parents=True):
        feedStatusQueue.put([1, feed.id])
        if parents:
            p = feed.parent
            while p:
                feedStatusQueue.put([1, p.id])
                p = p.parent


    def on_actionAbout_uRSSus_triggered(self, i=None):
        if i == None: return
        AboutDialog(self).exec_()

    def updateTree(self, feed):
        self.initTree()
        item = self.ui.feedTree.itemFromFeed(feed)
        self.ui.feedTree.setCurrentItem(item)
        self.open_feed2(item)

    def updatePostList(self):
        # This may call updateFeedItem, so avoid loops
        QtCore.QObject.disconnect(self.ui.posts.model(), QtCore.SIGNAL("modelReset()"), self.updateListedFeedItem)
        cp = self.ui.posts.model().postFromIndex(self.ui.posts.currentIndex())
        self.ui.posts.model().initData(update=True)
        if cp:
            idx = self.ui.posts.model().indexFromPost(cp)
            self.ui.posts.setCurrentIndex(idx)
            self.ui.posts.scrollTo(idx, self.ui.posts.EnsureVisible)
        else:
            self.ui.posts.scrollToTop()
        QtCore.QObject.connect(self.ui.posts.model(), QtCore.SIGNAL("modelReset()"), self.updateListedFeedItem)

    def updatePostItem(self, post):
        self.ui.posts.model().updateItem(post)

    def updateFeedItem(self, feed):

        info("Updating item for feed %d" % feed.id)

        item = self.ui.feedTree.itemFromFeed(feed)

        if not item:
            return # Weird, but a feed was added behind our backs or something
        unreadCount = feed.unreadCount()
        # If we are updating the current feed, update the post list, too
        if self.ui.posts.model() and self.ui.posts.model().feed_id == feed.id:
            self.updatePostList()

        if self.showOnlyUnread:
            if unreadCount == 0 and feed != self.currentFeed() and feed.xmlUrl:
            # Hide feeds with no unread items
                item.setHidden(True)
            else:
                item.setHidden(False)
        else:
            if item.parent() and item.parent().isHidden():
                item.parent().setHidden(False)
        if feed.updating:
            item.setForeground(0, QtGui.QColor("darkgrey"))
            item.setForeground(1, QtGui.QColor("darkgrey"))
        else:
            item.setForeground(0, QtGui.QColor("black"))
            item.setForeground(1, QtGui.QColor("black"))
        self.ui.feedTree.update(self.ui.feedTree.indexFromItem(item, 0))
        self.ui.feedTree.update(self.ui.feedTree.indexFromItem(item, 1))

        if feed == root_feed:
            # And set the unread count in the "unread items" item
            unread_feed.curUnread = -1
            self.updateFeedItem(unread_feed)
            # And set the systray tooltip to the unread count on root_feed
            self.tray.updateIcon()
            self.setWindowIcon(self.tray.icon())

            self.updateFeedItem(starred_feed)


    def updateFeedStatus(self):
        info("updateFeedStatus queue length: %d" % len(self.pendingFeedUpdates))
        try:
            while not feedStatusQueue.empty():
                # The idea: this function should never fail.
                # But, if we do, we keep our last attempted update in
                # memory, and we'll restart it the next try.
                data = feedStatusQueue.get()
                [action, id] = data[:2]
                debug("updateFeedStatus: %d %d" % (action, id))

                # FIXME: make this more elegant
                # These are not really feed updates
                if action in [4, 5, 6]:
                    if action == 4:     # Add new feed
                        self.addFeed(id)
                    elif action == 5:     #OPML to import
                    #                    importOPML(id, root_feed)
                        self.initTree()
                    elif action == 6:     #Just pop
                        self.show()
                        self.raise_()
                    else:
                        error("id %s not in the tree" % id)
                # We collapse all updates for a feed, and keep the last one
                else:
                    self.pendingFeedUpdates[id] = data

            for id in self.pendingFeedUpdates:
                if not self.pendingFeedUpdates[id]: continue
                [action, id] = self.pendingFeedUpdates[id]
                feed = Feed.get_by(id=id)
                if not feed: # Maybe it got deleted while queued
                    self.pendingFeedUpdates[id] = None
                    continue
                if action == 0: # Mark as updating
                    self.updateFeedItem(feed)
                else: # Mark as finished updating
                    # Force recount after update
                    feed.curUnread = -1
                    feed.unreadCount()
                    self.updateFeedItem(feed)
                    if feed.notify and len(data) > 2: # Systray notification
                        self.notifiedFeed = feed
                        self.tray.showMessage("New Articles", "%d new articles in %s" % (data[2], feed.text))
                        # We got this far, that means it's not pending anymore!
                    self.pendingFeedUpdates[id] = None
                    # We got this far, that means nothing is pending anymore!
            self.pendingFeedUpdates = {}
        except:
        # FIXME: handle errors better
        #             traceback.print_exc(10)
            error("FIX error handling in updateFeedStatus already!")
        self.feedStatusTimer.start(2000)

    def updateStatusBar(self):
        if not statusQueue.empty():
            msg = statusQueue.get()
            self.statusBar().showMessage(msg)
        else:
            self.statusBar().showMessage("")
        if statusQueue.empty():
            self.statusTimer.start(1000)
        else:
            self.statusTimer.start(100)

    def updateListedFeedItem(self):
        '''This connects to the post list model's reset signal, so we can update
        the feed item when the model data changes'''
        feed = Feed.get_by(id=self.ui.posts.model().feed_id)
        self.queueFeedUpdate(feed)

    def loadPostColumnPosition(self):
        positions = config.getValue('ui', 'postColumnPosition', [0, 1, 2, 3, 4])
        colPos = zip([0, 1, 2, 3, 4], positions)
        colPos.sort(key=operator.itemgetter(1))
        header = self.ui.posts.header()
        # Gack!
        for logical, visual in colPos:
            header.moveSection(header.visualIndex(logical), visual)


    def fixPostListUI(self):
        # Fixes for post list UI
        widths = config.getValue('ui', 'postColumnWidths', [])
        header = self.ui.posts.header()
        header.setStretchLastSection(False)
        header.setResizeMode(0, QtGui.QHeaderView.Fixed)
        header.resizeSection(0, 24)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Fixed)
        header.resizeSection(2, header.fontMetrics().width(' 88/88/8888 8888:88:88 ') + 4)
        header.setResizeMode(3, QtGui.QHeaderView.Interactive)
        if widths:
            header.resizeSection(3, widths[3])
        self.loadPostColumnPosition()
        starred, feed, date = config.getValue('ui', 'visiblePostColumns', [True, False, True])
        self.ui.actionShowStarredColumn.setChecked(starred)
        self.ui.actionShowFeedColumn.setChecked(feed)
        self.ui.actionShowDateColumn.setChecked(date)
        if starred:
            header.showSection(0)
        else:
            header.hideSection(0)

        if feed:
            header.showSection(3)
        else:
            header.hideSection(3)

        if date:
            header.showSection(2)
        else:
            header.hideSection(2)

    def on_posts_clicked(self, index):
        post = self.ui.posts.model().postFromIndex(index)
        if post: #post may go away if you changed feeds very quickly
            if post.feed.loadFull and post.link:
                # If I pass post.link, it crashes if I click something else quickly
                self.ui.statusBar.showMessage("Opening %s" % post.link)
                self.ui.view.setUrl(QtCore.QUrl(QtCore.QString(post.link)))
            else:
                showFeed = self.showingFolder or config.getValue('ui', 'alwaysShowFeed', False) == True
                if not self.showingFolder:
                    post.content = decode_htmlentities(post.content)
                self.ui.view.setHtml(renderTemplate('post.tmpl', post=post, showFeed=showFeed))
            QtGui.QApplication.instance().processEvents(QtCore.QEventLoop.ExcludeUserInputEvents, 1000)
            upUnread = False
            upImportant = False
            upFeed = False
            try:
                if index.column() == 0: # Star icon
                    post.important = not post.important
                    upImportant = True
                if post.unread:
                    post.unread = False
                    post.feed.curUnread -= 1
                    upUnread = True
                    upFeed = True
                elixir.session.commit()
            except:
                elixir.session.rollback()

            if upUnread or upImportant:
                self.updatePostItem(post)
            if upFeed:
                self.queueFeedUpdate(post.feed)


    def on_posts_doubleClicked(self, index=None):
        if index == None: return
        item = self.ui.posts.model().itemFromIndex(index)
        if item:
            post = self.ui.posts.model().postFromIndex(index)
            if post and post.link:
                debug("Opening %s" % post.link)
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(post.link))


    def open_feed2(self, item):
        if not item: return
        feed = item.feed
        unreadCount = feed.unreadCount()

        if feed.xmlUrl:
            self.showingFolder = False
        else:
            self.showingFolder = True

        self.ui.feedTree.setCurrentFeed(feed)
        # Scroll the feeds view so this feed is visible
        self.ui.feedTree.scrollToItem(item)

        # Update window title
        if feed.title:
            self.setWindowTitle("%s - newsCollect" % feed.title)
        elif feed.text:
            self.setWindowTitle("%s - newsCollect" % feed.text)
        else:
            self.setWindowTitle("newsCollect")

        actions = [self.ui.actionNext_Article,
                   self.ui.actionNext_Unread_Article,
                   self.ui.actionPrevious_Article,
                   self.ui.actionPrevious_Unread_Article,
                   self.ui.actionMark_as_Read,
                   self.ui.actionMark_as_Unread,
                   self.ui.actionMark_as_Important,
                   self.ui.actionDelete_Article,
                   self.ui.actionOpen_in_Browser,
                   self.ui.actionRemove_Important_Mark,
        ]

        if self.combinedView: # CombinedView / FancyView
        # Lose the model in self.ui.posts
            self.ui.posts.setModel(None)

            info("Opening combined")
            if feed.xmlUrl: # A regular feed
                self.posts = Post.query.filter(Post.feed == feed)
                showFeedInPosts = True
            else: # A folder
                self.posts = feed.allPostsQuery()
                showFeedInPosts = False
                # Filter by text according to the contents of self.textFilter
            if self.textFilter:
                self.posts = self.posts.filter(sql.or_(Post.title.like('%%%s%%' % self.textFilter),
                                                       Post.content.like('%%%s%%' % self.textFilter),
                                                       Post.tags.like('%%%s%%' % self.textFilter)))
            if self.statusFilter:
                self.posts = self.posts.filter(self.statusFilter == True)
                # FIXME: find a way to add sorting to the UI for this (not very important)
            self.posts = self.posts.order_by(sql.desc(Post.date)).all()
            self.ui.view.setHtml(renderTemplate(self.combinedTemplate, posts=self.posts, showFeed=showFeedInPosts))
            for action in actions:
                action.setEnabled(False)
        else: # StandardView / Widescreen View
            info("Opening in standard view")
            # FIXME: There must be a better place to call this
            #           self.savePostSectionSizes()

            model = self.ui.posts.model()

            # Remember current post
            if self.ui.posts.model():
                post = self.ui.posts.model().postFromIndex(self.ui.posts.currentIndex())
            else:
                post = None

            # The == are weird because sqlalchemy reimplementes the == operator for
            # model.statusFilter
            if model and model.feed_id == feed.id and \
                            str(model.textFilter) == str(self.textFilter) and \
                            str(model.statusFilter) == str(self.statusFilter):
                self.ui.posts.model().initData(update=True)
            else:
                self.ui.posts.setModel(PostModel(self.ui.posts, feed, self.textFilter, self.statusFilter))
                QtCore.QObject.connect(self.ui.posts.model(), QtCore.SIGNAL("modelReset()"), self.updateListedFeedItem)
                QtCore.QObject.connect(self.ui.posts.model(), QtCore.SIGNAL("dropped(PyQt_PyObject)"), self.updateTree)
                header = self.ui.posts.header()
                # Don't show feed column yet
                header.hideSection(3)
            self.fixPostListUI()

            # Try to scroll to the same post or to the top

            self.updatePostList()

            for action in actions:
                action.setEnabled(True)
                # TODO: move substitute_entity and decode_htmlentities to utils module
def substitute_entity(match):
    ent = match.group(2)
    if match.group(1) == "#":
        return unichr(int(ent))
    else:
        cp = n2cp.get(ent)
        if cp:
            return unichr(cp)
        else:
            return match.group()


def decode_htmlentities(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute_entity, string)[0]


def main():
    global root_feed, unread_feed, starred_feed
    root_feed = datatable.root_feed
    unread_feed = datatable.unread_feed
    starred_feed = datatable.starred_feed
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    pass
