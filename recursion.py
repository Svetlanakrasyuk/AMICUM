import json
with open('new_test_hw.json') as json_file:
    data = json.load(json_file)
data = [data]

result_tuple = []


def json_to_tuple(d, result_tuple):
    for i in d:
        # Если в словаре есть ключ children то передаем значения ключа функции рекусивно
        if 'children' in i:
            if i.get('title', False) and i.get('id', False):
                result_tuple.append((i['title'], i['id']))
            json_to_tuple(i['children'], result_tuple)
        else:
            # Добавляем данные в список
            result_tuple.append((i['title'], i['id']))
    return tuple(result_tuple)


result = json_to_tuple(data, result_tuple)
print(result)
