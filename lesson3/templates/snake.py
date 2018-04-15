def reverse(x):
    """
    :type x: int
    :rtype: int
    """
    result = 0
    while x != 0:
        temp = result * 10 + x % 10
        print('temp is ' + str(temp))
        print(str(temp / 10))
        if temp // 10 != result:
            print("return")
            return 0
        x //= 10
        print(x)
        result = temp

    return result


if __name__ == '__main__':
    reverse(123)