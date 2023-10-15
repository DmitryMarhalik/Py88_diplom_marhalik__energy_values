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


def transformation_evop_lst_dishes(evop_list):
    res_list, finlist = [], []
    for elem in evop_list:
        off = ',г'
        push = '. '
        delete_letters = 'кКал'
        table_trslt = str.maketrans(off, push, delete_letters)
        # The third parameter in the mapping table describes characters
        # that you want to remove from the string:
        # txt = "Good night Sam!"
        # x = "mSa"
        # y = "eJo"
        # z = "odnght"
        # mytable = str.maketrans(x, y, z)
        # print(txt.translate(mytable))  ----> G i Joe!
        elem = elem.translate(table_trslt)
        res_list.append(elem)
    res_list = [res_list[i:i + 4] for i in range(0, len(res_list), 4)]
    return res_list


def make_dict_dishes(names, values):
    evop = transformation_evop_lst_dishes(values)
    dict_dishes = dict(zip(names, evop))
    return dict_dishes
