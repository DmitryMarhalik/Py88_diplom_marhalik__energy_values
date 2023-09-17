def transformation_list(list_products):
    res_list = []
    for elem in list_products:
        if ',' in elem and '-' in elem and elem[0].isdigit():
            elem = elem.replace(',', '.')
            lst = elem.split('-')
            lst = [float(k) for k in lst]
            num = round(((min(lst) + max(lst)) / 2), 2)
            res_list.append(num)
        elif '-' in elem and elem[0].isdigit() and ',' not in elem:
            lst = elem.split('-')
            lst = [int(k) for k in lst]
            num = round(((min(lst) + max(lst)) / 2), 2)
            res_list.append(num)
        elif ',' in elem and elem[0].isdigit():
            elem = elem.replace(',', '.')
            res_list.append(elem)
        elif '-' in elem and len(elem) == 1:
            elem = elem.replace('-', '0')
            res_list.append(elem)
        else:
            res_list.append(elem)
    print(res_list)
    return [res_list[i:i + 5] for i in range(0, len(res_list), 5)]


# names = legumes[0::5]
# proteins = legumes[1::5]
# fats = legumes[2::5]
# carbohydrates = legumes[3::5]
# kcal = legumes[4::5]
