def transformation_list(refactor_list):
    res_list = []
    for elem in refactor_list:
        if ',' in elem and '-' in elem and elem[0].isdigit():
            elem = elem.replace(',', '.')
            lst = elem.split('-')
            lst = [float(k) for k in lst]
            num = round(((min(lst) + max(lst)) / 2), 2)
            res_list.append(str(num))
        elif 'следы' in elem:
            elem = elem.replace('следы', '0')
            res_list.append(elem)
        elif '-' in elem and elem[0].isdigit() and ',' not in elem:
            lst = elem.split('-')
            lst = [int(k) for k in lst]
            num = round(((min(lst) + max(lst)) / 2), 2)
            res_list.append(str(num))
        elif ',' in elem and elem[0].isdigit():
            elem = elem.replace(',', '.')
            res_list.append(elem)
        elif '-' in elem and len(elem) == 1:
            elem = elem.replace('-', '0')
            res_list.append(elem)
        else:
            res_list.append(elem)
    res_list = [res_list[i:i + 5] for i in range(0, len(res_list), 5)]
    for name in res_list:
        if name[0] == 'Макаронные изделия из муки твердых сортов в/с':
            res_list.remove(name)
            break
    for name in res_list:
        if name[0] == 'Макаронные изделия в/с':
            res_list.remove(name)
            break
    return res_list


def delete_string_xa0xa0(list_products):
    refactor_list = []
    for id, value in enumerate(list_products):
        if '\xa0\xa0' in value:
            correct_word = refactor_list[id - 5].split()[0]
            value = value.replace('\xa0\xa0', correct_word)
            refactor_list.append(value)
        else:
            refactor_list.append(value)
    return refactor_list


def transformation_evop_dishes(evop_list):
    res_list, finlist = [], []
    for elem in evop_list:
        elem = elem.translate(str.maketrans({',': '.', 'г': ''}))
        res_list.append(elem)
    for i in res_list:
        if 'кКал' in i:
            i = i.replace('кКал', '')
            finlist.append(i)
        else:
            finlist.append(i)
    finlist=[finlist[i:i + 4] for i in range(0, len(finlist), 4)]
    return finlist