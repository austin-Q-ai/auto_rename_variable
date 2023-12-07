import string
from parser.changeVar import changeVar
from parser.parse import parse


def check_variable(methodStr, variable):
    new_method = changeVar(methodStr, 'app', variable)
    try:
        parse(new_method)
        return True
    except:
        return False

def filter_result(predictions, methodStr, top_nums):
    special_characters = set(string.punctuation)

    # Filtering out single-character words
    words = list(set([word for sublist in predictions for word in sublist]))

    filtered_words = [word for word in words if not any(char in special_characters for char in word)]
    print(filtered_words)
    vaild_variables = [word for word in filtered_words if check_variable(methodStr, word)]
    print(vaild_variables)
    default_value = 0


    # Create a new dictionary with keys from the list and all values set to the default value
    rank_dict = {key: default_value for key in vaild_variables}

    for ele in predictions:
        for i, var in enumerate(ele):
            if var in vaild_variables:
                rank_dict[var] += top_nums - i

    print(rank_dict)
    return dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))


methodStr = '''
def create_app(handler: Handler, key: bytes, max_age: Optional[int]=None) -> web.Application:
    middleware = session_middleware(NaClCookieStorage(key, max_age=max_age))
    app = web.Application(middlewares=[middleware])
    app.router.add_route('GET', '/', handler)
    return app
'''

# print(check_variable(methodStr, 'return'))
predictions = [['handler', 'def', 'return', ')', 'appl??ication'], ['products', 'p', 'server', 'c', ')'], ['handler', '.', ')', 'route', 'app']]
print(filter_result(predictions, methodStr, 5))