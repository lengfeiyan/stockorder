# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from .apps import StockConfig
#import xlrd, xlwt, sys, os, datetime
#sys.path.insert(0, StockConfig.TSL_PATH)
#import TSLPy3
#if TSLPy3.Logined():
#    pass
#else:
#    result = TSLPy3.DefaultConnectAndLogin(StockConfig.TSL_LOGIN_NAME)
#    print(result[0])

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^market_info$', views.marketInfo, name='marketInfo'),
    url(r'^section_info_home$', views.sectionInfoHomepage, name='sectionInfoHomepage'),
    url(r'^left$', views.left, name='left'),
    #url(r'^kline$', views.kline, name='kline'),
    url(r'^stock_list_ajax$', views.stockListAjax, name='stockListAjax'),
    url(r'^stock_info_ajax$', views.stockInfoAjax, name='stockInfoAjax'),
    url(r'^stock_section_list$', views.stockSectionList, name='stockSectionList'),
    url(r'^section_list$', views.sectionList, name='sectionList'),
    url(r'^section_add$', views.addSection, name='addSection'),
    url(r'^section_edit$', views.editSection, name='editSection'),
    url(r'^section_delete$', views.deleteSection, name='deleteSection'),
    url(r'^stock_add$', views.addStock, name='addStock'),
    url(r'^stock_delete$', views.addStock, name='deleteStock'),
    url(r'^section_merge$', views.mergeSection, name='mergeSection'),
    url(r'^section_market_info$', views.sectionMarketInfo, name='sectionMarketInfo'),
    url(r'^stock_info$', views.stockInfo, name='stockInfo'),
    url(r'^section_info$', views.sectionInfo, name='sectionInfo'),
    url(r'^batch_import$', views.batchImport, name='batchImport'),
    url(r'^news$', views.newsList, name='newsList'),
    url(r'^news_stat$', views.newsStat, name='newsStat'),
    url(r'^add_comment$', views.addComment, name='addComment'),
    url(r'^like_comment$', views.likeComment, name='likeComment'),
    url(r'^syn2tysoft$', views.synToTysoft, name='synToTysoft'),
    url(r'^stock_watch_list$', views.stockWatchList, name='stockWatchList'),
    url(r'^stock_watch_add$', views.addStockWatch, name='addStockWatch'),
    url(r'^stock_watch_edit$', views.editStockWatch, name='editStockWatch'),
    url(r'^stock_watch_del$', views.deleteStockWatch, name='deleteStockWatch'),
    url(r'^set_important_stock$', views.setImportantStock, name='setImportantStock'),
    url(r'^get_stock_id$', views.getStockId, name='getStockId'),
    url(r'^export_news$', views.exportNews, name='exportNews'),
    url(r'^load_stock_id$', views.loadStockId, name='loadStockId'),
    url(r'^load_stock_info$', views.loadInfo, name='loadInfo'),
    url(r'^kline_mode_filter$', views.showKLineModeFilter, name='showKLineModeFilter'),
    url(r'^mins$', views.minsLine, name='minsLine'),
    url(r'^minskline$', views.minsKLine, name='minsKLine'),
    url(r'^days$', views.daysLine, name='daysLine'),
    url(r'^lines$', views.showLines, name='showLines'),
]
