from shutil import which  
# Scrapy settings for myproject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "myproject"

SPIDER_MODULES = ["myproject.spiders"]
NEWSPIDER_MODULE = "myproject.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "myproject (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "myproject.middlewares.MyprojectSpiderMiddleware": 543,
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "myproject.middlewares.MyprojectDownloaderMiddleware": 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
    # 'scrapy_selenium.SeleniumMiddleware': 800
    # 'myproject.middlewares.ProxyMiddleware': 100,
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "myproject.pipelines.MyprojectPipeline": 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 连接redis
REDIS_URL = 'redis://:mingri1234@113.45.148.34:6379/3'

# 使用 Scrapy-Redis 的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 使用队列持久化
SCHEDULER_PERSIST = True

# 使用 Scrapy-Redis 去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

CLOSESPIDER_TIMEOUT = 60

# 使用 chrome
# SELENIUM_DRIVER_NAME = 'chrome'  
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver') 

# 连接 splash 浏览器
# SPLASH_URL = 'http://localhost:8050'

# 使用Splash的Http缓存
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# 使用 splash 进行 去重
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'