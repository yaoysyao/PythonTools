# 判断当前数字是几位
def get_number_len(number):
    count = 0
    while number:
        number = number // 10
        count += 1
    return count
