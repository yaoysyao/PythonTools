from time import sleep

from yaoysTools.progress.progressUtil import PROGRESS_TYPE_PIXELBAR, PROGRESS_TYPE_SPINNER, definitionProgress

'''
以下样式的进度条可选
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
'''
bar = definitionProgress(progress_type=PROGRESS_TYPE_PIXELBAR, count=100, is_save_log=True, log_path='../../demo/log').get_progress()
for i in range(100):
    # Do some work
    sleep(0.01)
    bar.next()
bar.finish()

# 不确定长度的用spinner,spinner进度条不会保存到log日志
spinner = definitionProgress(progress_type=PROGRESS_TYPE_SPINNER).get_progress()
state = 'loading'
count = 0
while state != 'FINISHED':
    # Do some work
    spinner.next()
    count = count + 1
    sleep(0.01)
    if count > 100:
        state = 'FINISHED'

print(count)
