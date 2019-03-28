def readtxt():
    data = []
    for line in open('info.txt', 'r', encoding='UTF-8'):
        data.append(line)
    return data

def parseInt(num):
    try:
        return int(num)
    except ValueError:
        result = []
        for c in num:
            if not ('0' <= c <= '9'):
                break
            result.append(c)
        if len(result) == 0:
            return 0
        return int(''.join(result))