# Python工具类

## 简介

此工具类致力于封装一些常用的python代码，目前支持log日志，progress进度条，mysql数据库操作，雪花算法唯一id，时间工具类等方法

## 使用说明

### log日志

```python
# log日志demo
from yaoysTools.log.logutil import getLogger, log_info, MY_LOG_INFO
# 说明：如果设置保存日志到日志文件，则必须设置日志文件路径，此时 save_log2_file=True， log_path='../log'
# 封装了log_info，log_error,log_warn,log_debug等方法
#日志颜色将根据不同的日志等级设置为不同的颜色
logger = getLogger('test', log_path='../log', log_level=MY_LOG_INFO, save_log2_file=True)
log_info('test', my_logger=logger)
# 运行结果如下：
[2022-07-23 13:31:25,058] [log_name:test] [INFO] [filename:some_thing_test.py] [func_name:非方法调用(Not function)] [15 line] -message:test
# 可在log文件中查看到相关日志
```

### progress 进度条

```python
# 进度条demo
# 进度条工具整合了第三方的工具，代码地址：https://github.com/verigak/progress.git
# 针对以上源码进行了封装，修改，增加将进度保存到日志文件中
from time import sleep
from yaoysTools.progress.progressUtil import PROGRESS_TYPE_PIXELBAR, definitionProgressBar
# 进度条可选择的样式有多种，如果不知道具体的总的长度，可以使用spinner，原作者提供了多种spinner
PROGRESS_TYPE_BAR = 'Bar'
PROGRESS_TYPE_CHARGING_BAR = 'ChargingBar'
PROGRESS_TYPE_FILLINGSQUARESBAR = 'FillingSquaresBar'
PROGRESS_TYPE_FILLINGCIRCLESBAR = 'FillingCirclesBar'
PROGRESS_TYPE_INCREMENTALBAR = 'IncrementalBar'
PROGRESS_TYPE_PIXELBAR = 'PixelBar'
PROGRESS_TYPE_SHADYBAR = 'ShadyBar'
PROGRESS_TYPE_SPINNER = 'Spinner'
PROGRESS_TYPE_PIESPINNER = 'PieSpinner'
PROGRESS_TYPE_MOONSPINNER = 'MoonSpinner'
PROGRESS_TYPE_LINESPINNER = 'LineSpinner'
PROGRESS_TYPE_PIXELSPINNER = 'PixelSpinner'
# 注意，如果需要将进度保存到日志中，必须设置 is_save_log=True，并且设置log日志的路径
# 你还可以自己定义自己的logger.如果不定义，将采用默认的logger,自定义logger使用的方法是log日志中的getLogger
#自定义logger时，同样的如果需要将进度保存到日志中，必须设置 is_save_log=True，并且设置log日志的路径，必须设置is_only_file=True，否则会在控制台输出进度
# logger = getLogger(self.message, log_level=MY_LOG_INFO, log_path=self.log_path, is_only_file=True)
# 如果采用默认的logger，则不需要设置my_logger=logger
bar = definitionProgressBar(progress_type=PROGRESS_TYPE_PIXELBAR,
                            count=100, is_save_log=True, log_path='../log',my_logger=logger).get_progress()
for i in range(100):
    # Do some work
    sleep(0.01)
    bar.next()
bar.finish()
# 控制台运行结果：
Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿| 100/100
# log日志输出进度如下：
```

```log
[2022-07-23 12:54:51,391] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:
[2022-07-23 12:54:51,418] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⡆                               | 1/100
[2022-07-23 12:54:51,432] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣧                               | 2/100
[2022-07-23 12:54:51,449] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿                               | 3/100
[2022-07-23 12:54:51,479] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⡆                              | 4/100
[2022-07-23 12:54:51,494] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣇                              | 5/100
[2022-07-23 12:54:51,509] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿                              | 6/100
[2022-07-23 12:54:51,525] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⡄                             | 7/100
[2022-07-23 12:54:51,541] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣇                             | 8/100
[2022-07-23 12:54:51,556] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿                             | 9/100
[2022-07-23 12:54:51,573] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⡄                            | 10/100
[2022-07-23 12:54:51,587] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣇                            | 11/100
[2022-07-23 12:54:51,605] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣷                            | 12/100
[2022-07-23 12:54:51,620] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⡄                           | 13/100
[2022-07-23 12:54:51,635] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⡇                           | 14/100
[2022-07-23 12:54:51,653] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣷                           | 15/100
[2022-07-23 12:54:51,666] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿                           | 16/100
[2022-07-23 12:54:51,682] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⡇                          | 17/100
[2022-07-23 12:54:51,698] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣷                          | 18/100
[2022-07-23 12:54:51,714] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿                          | 19/100
[2022-07-23 12:54:51,730] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⡇                         | 20/100
[2022-07-23 12:54:51,744] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣧                         | 21/100
[2022-07-23 12:54:51,760] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿                         | 22/100
[2022-07-23 12:54:51,775] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⡆                        | 23/100
[2022-07-23 12:54:51,792] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣧                        | 24/100
[2022-07-23 12:54:51,809] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿                        | 25/100
[2022-07-23 12:54:51,823] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⡆                       | 26/100
[2022-07-23 12:54:51,839] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣧                       | 27/100
[2022-07-23 12:54:51,857] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿                       | 28/100
[2022-07-23 12:54:51,888] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆                      | 29/100
[2022-07-23 12:54:51,917] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇                      | 30/100
[2022-07-23 12:54:51,932] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                      | 31/100
[2022-07-23 12:54:51,948] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄                     | 32/100
[2022-07-23 12:54:51,963] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇                     | 33/100
[2022-07-23 12:54:51,981] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                     | 34/100
[2022-07-23 12:54:52,009] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄                    | 35/100
[2022-07-23 12:54:52,025] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇                    | 36/100
[2022-07-23 12:54:52,041] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷                    | 37/100
[2022-07-23 12:54:52,055] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄                   | 38/100
[2022-07-23 12:54:52,071] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇                   | 39/100
[2022-07-23 12:54:52,086] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷                   | 40/100
[2022-07-23 12:54:52,102] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                   | 41/100
[2022-07-23 12:54:52,119] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇                  | 42/100
[2022-07-23 12:54:52,135] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷                  | 43/100
[2022-07-23 12:54:52,150] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                  | 44/100
[2022-07-23 12:54:52,165] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇                 | 45/100
[2022-07-23 12:54:52,181] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧                 | 46/100
[2022-07-23 12:54:52,197] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                 | 47/100
[2022-07-23 12:54:52,241] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆                | 48/100
[2022-07-23 12:54:52,260] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧                | 49/100
[2022-07-23 12:54:52,277] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                | 50/100
[2022-07-23 12:54:52,291] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆               | 51/100
[2022-07-23 12:54:52,308] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧               | 52/100
[2022-07-23 12:54:52,328] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿               | 53/100
[2022-07-23 12:54:52,356] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆              | 54/100
[2022-07-23 12:54:52,374] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇              | 55/100
[2022-07-23 12:54:52,402] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿              | 56/100
[2022-07-23 12:54:52,421] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄             | 57/100
[2022-07-23 12:54:52,438] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇             | 58/100
[2022-07-23 12:54:52,463] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿             | 59/100
[2022-07-23 12:54:52,479] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄            | 60/100
[2022-07-23 12:54:52,494] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇            | 61/100
[2022-07-23 12:54:52,511] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷            | 62/100
[2022-07-23 12:54:52,526] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄           | 63/100
[2022-07-23 12:54:52,543] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇           | 64/100
[2022-07-23 12:54:52,558] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷           | 65/100
[2022-07-23 12:54:52,573] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿           | 66/100
[2022-07-23 12:54:52,588] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇          | 67/100
[2022-07-23 12:54:52,604] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷          | 68/100
[2022-07-23 12:54:52,620] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿          | 69/100
[2022-07-23 12:54:52,635] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇         | 70/100
[2022-07-23 12:54:52,654] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧         | 71/100
[2022-07-23 12:54:52,682] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿         | 72/100
[2022-07-23 12:54:52,697] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆        | 73/100
[2022-07-23 12:54:52,714] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧        | 74/100
[2022-07-23 12:54:52,729] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿        | 75/100
[2022-07-23 12:54:52,743] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆       | 76/100
[2022-07-23 12:54:52,758] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧       | 77/100
[2022-07-23 12:54:52,774] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿       | 78/100
[2022-07-23 12:54:52,790] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆      | 79/100
[2022-07-23 12:54:52,806] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇      | 80/100
[2022-07-23 12:54:52,822] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      | 81/100
[2022-07-23 12:54:52,839] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄     | 82/100
[2022-07-23 12:54:52,853] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇     | 83/100
[2022-07-23 12:54:52,870] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿     | 84/100
[2022-07-23 12:54:52,885] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄    | 85/100
[2022-07-23 12:54:52,904] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇    | 86/100
[2022-07-23 12:54:52,932] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷    | 87/100
[2022-07-23 12:54:52,949] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄   | 88/100
[2022-07-23 12:54:52,964] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇   | 89/100
[2022-07-23 12:54:52,979] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷   | 90/100
[2022-07-23 12:54:52,995] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿   | 91/100
[2022-07-23 12:54:53,011] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇  | 92/100
[2022-07-23 12:54:53,026] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷  | 93/100
[2022-07-23 12:54:53,042] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  | 94/100
[2022-07-23 12:54:53,058] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇ | 95/100
[2022-07-23 12:54:53,073] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧ | 96/100
[2022-07-23 12:54:53,089] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ | 97/100
[2022-07-23 12:54:53,107] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆| 98/100
[2022-07-23 12:54:53,121] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧| 99/100
[2022-07-23 12:54:53,137] [log_name:Progress] [INFO] [filename:F:\Myjob\Anaconda\lib\site-packages\yaoysTools\progress\__init__.py] [func_name:writeln] [119 line] -message:Progress |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿| 100/100
```

