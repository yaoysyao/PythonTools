# Python工具类

## 简介

此工具类致力于封装一些常用的python代码，目前支持log日志，progress进度条，mysql数据库操作，雪花算法唯一id，时间工具类等方法

## 使用说明

### 安装

```
pip install yaoys-python-tool
```

## 更多例子请查看demo文件夹下相关代码

### log日志

```python
# log日志demo
from yaoysTools.log.logutil import getLogger, log_info, MY_LOG_INFO

# 说明：如果设置保存日志到日志文件，则必须设置日志文件路径，此时 save_log2_file=True， log_path='../log'
# 封装了log_info，log_error,log_warn,log_debug等方法
# 日志颜色将根据不同的日志等级设置为不同的颜色
logger = getLogger('test', log_path='../log', log_level=MY_LOG_INFO, save_log2_file=True)
log_info('test', my_logger=logger)
# 运行结果如下：
[2022 - 07 - 23 13: 31:25, 05
8] [log_name: test] [INFO][filename:some_thing_test.py][func_name:非方法调用(Not
function)] [15 line] - message: test
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
# 自定义logger时，同样的如果需要将进度保存到日志中，必须设置 is_save_log=True，并且设置log日志的路径，必须设置is_only_file=True，否则会在控制台输出进度
# logger = getLogger(self.message, log_level=MY_LOG_INFO, log_path=self.log_path, is_only_file=True)
# 如果采用默认的logger，则不需要设置my_logger=logger

# 以下为显示进度时间样式
PROGRESS_ELAPSED = 'elapsed'  # 正向时间增加，只显示秒数
PROGRESS_ELAPSED_TD = 'elapsed_td'  # 正向时间增加，显示时，分，秒
PROGRESS_ETA = 'eta'  # 倒序时间减少，elapsed的逆序
PROGRESS_ETA_TD = 'eta_td'  # elapsed_td的逆序
默认显示时间，时间格式为：elapsed_td，如果需要不显示时间, 设置： need_show_time = False
bar = definitionProgressBar(progress_type=PROGRESS_TYPE_PIXELBAR,
                            count=100, is_save_log=True, log_path='../log', my_logger=logger, need_show_time=True,
                            show_time_type=PROGRESS_ELAPSED_TD).get_progress()
for i in range(100):
    # Do some work
    sleep(0.01)
    bar.next()
bar.finish()
# 控制台运行结果：
Progress |  ################################| 100/100  100.00% 0:00:11 
# log日志输出进度如下：
[2022-08-26 21:08:38,976][log_name:Progress][INFO][filename:E:\MyJob\PyCharm\PythonTools\yaoysTools\progress\__init__.py][func_name:writeln][131 line]-message:Progress |################################| 100/100  100.00% 0:00:11
```



