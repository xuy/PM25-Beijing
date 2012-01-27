from pm25_beijing.items import Pm25BeijingItem
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from datetime import datetime
from os import path as p
from os import mkdir

class Pm25Spider(BaseSpider):
    name = "pm25_beijing"
    allowed_domains = ["zx.bjmemc.com.cn"]
    start_urls = [ "http://zx.bjmemc.com.cn/Charts/PM25.aspx", ]
    def parse(self, response):
        folder = p.abspath(p.join(p.split(__file__)[0], 'raw'))
        items = []
        timestamp = str(datetime.utcnow())
        hxs = HtmlXPathSelector(response)
        tds = hxs.select('//td/text()')
        values = []
        for td in tds:
            if td.extract().strip():
                values.append(td.extract().strip())
        for i in xrange(len(values)/2):
            item = Pm25BeijingItem()
            item['hour'] = values[2*i]
            item['saturation'] = values[2*i+1]
            item['timestamp'] = timestamp
            items.append(item)
        if not p.exists(folder):
            mkdir(folder)
        filename = p.join(folder, "PM25_html_" + timestamp + ".html")
        open(filename, 'wb').write(response.body)
        return items
        