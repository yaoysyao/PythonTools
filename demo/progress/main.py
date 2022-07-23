from time import sleep

from yaoysTools.progress.bar import *

bar = Bar('Bar', max=200, check_tty=False, color='green')
for i in range(200):
    # Do some work
    sleep(0.01)
    bar.next()
bar.finish()

# not use finish()
with Bar('Processing', max=200, check_tty=False) as bar:
    for i in range(200):
        # Do some work
        bar.next()

bar2 = ChargingBar('ChargingBar', max=200, check_tty=False, color='green')
for i in range(200):
    # Do some work
    sleep(0.01)
    bar2.next()
bar2.finish()

bar3 = FillingSquaresBar('FillingSquaresBar', max=200, check_tty=False, color='green')
for i in range(200):
    # Do some work
    sleep(0.01)
    bar3.next()
bar3.finish()

bar4 = FillingCirclesBar('FillingCirclesBar', max=200, check_tty=False, color='green')
for i in range(200):
    # Do some work
    sleep(0.01)
    bar4.next()
bar4.finish()

bar5 = IncrementalBar('IncrementalBar', max=200, check_tty=False, color='green')
for i in range(200):
    # Do some work
    sleep(0.01)
    bar5.next()
bar5.finish()

bar6 = PixelBar('PixelBar', max=200, check_tty=False, color='green')
for i in range(200):
    # Do some work
    sleep(0.01)
    bar6.next()
bar6.finish()

bar7 = ShadyBar('ShadyBar', max=200, check_tty=False, color='green')
for i in range(200):
    # Do some work
    sleep(0.01)
    bar7.next()
bar7.finish()

from yaoysTools.progress.spinner import Spinner

# 不确定长度的用spinner
spinner = Spinner('Loading ', check_tty=False)
state = 'loading'
while state != 'FINISHED':
    # Do some work
    spinner.next()
