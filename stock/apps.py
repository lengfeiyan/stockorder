from django.apps import AppConfig


class StockConfig(AppConfig):
    name = 'stock'
    # 天软安装路径
    TSL_PATH = r'C:\Program Files\Tinysoft\Analyse.NET'
    # 天软登录配置名
    TSL_LOGIN_NAME = 'jyu'
    # 分页大小
    PAGE_SIZE = 10

    DEFAULT_NDAYS = 40

    STOCK_LIST_TYPE = ['all','auction', 'amountRate', 'occupationRate', 'turnoverRate', 'ndaysLimitUp', 'firstLimitUp',
                        'increaseFastWithAmount', 'longTopShadow', 'longBottomShadow', 'maClose' , 'short', 'longHedging',
                        'through3lines', 'breakThrough3lines', 'reopenAbnormal', 'devourLine', 'breakthroughLine',
                        'sectionList','singleStock','hasLimitUp','strongWash','IslandReversal']

    MODE_NAME_DICT = {'increaseFastWithAmount':'带量急拉',
                      'longTopShadow':'上长影',
                      'longBottomShadow':'下长影',
                      'maClose':'均线粘合' ,
                      'longHedging':'多头',
                      'short':'空头',
                      'through3lines':'穿3线',
                      'breakThrough3lines':'破后穿3线',
                      'reopenAbnormal':'复牌异动',
                      'devourLine':'吞噬线',
                      'breakthroughLine':'贯穿线',
                      'hasLimitUp':'区间有板',
                      'strongWash':'昨日强洗',
                      'IslandReversal':'岛转'
                      }