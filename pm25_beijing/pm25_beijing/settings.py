# Scrapy settings for pm25_beijing project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'pm25_beijing'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['pm25_beijing.spiders']
NEWSPIDER_MODULE = 'pm25_beijing.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = ['pm25_beijing.pipelines.ProcessPipeline',
                  'pm25_beijing.pipelines.StorePipeline' ]

