import os
import requests
import settings,socket



def analiz_func(name_vol, volume):
    print(name_vol, volume, type(volume))

def print_ip():
    print('IP:',socket.gethostbyname(socket.gethostname()))

def get_files(m_DIR_NAME: str, ext=('pdf', 'jpg', 'png')):
    files = []
    with os.scandir(m_DIR_NAME) as listFiles:
        for file in listFiles:
            if os.path.isdir(file.path):
                m_files = get_files(file.path, ext)
                files = files + m_files
            else:
                if file.name[-3:] in ext:
                    files.append(file.path)
    return files


def mk_dir(m_path: str, current: True):
    """

    :param m_path: путь, директорория
    :param current: добавить относительный путь
    :return: Истина, Ложь
    """

    result = False

    if os.path.exists(m_path):
        result = True
    else:
        path = ''
        if current:
            path = os.getcwd()

        try:
            os.makedirs(path + m_path)
            result = True
        except OSError:
            print("Создать директорию %s не удалось" % m_path)

    return result


def post_obj(obj):
    # ниже код если нужно разделять временный путь к источникам
    # if obj.del_path_half == '':
    data_set = {"file": obj.filename,
                "source": obj.textField,
                "data_source": obj.word_locathions,
                "short": obj.short}

    # post запрос на загрузку файлов
    url = settings.URL_1C_API + 'files/load_post'

    if settings.DEBUG:
        print('url:', url)

    resp = requests.post(url, auth=(settings.LOGIN_1C, settings.PASSWORD_1C), json=data_set)

    if settings.DEBUG:
        print('resp:', resp)
        print('resp.text:', resp.text)


def _request_api_get(filtr_val=None):
    # post запрос на загрузку файлов
    # пример
    # http://localhost/analitic/hs/files/inf/doc02733320201030114838.pdf

    url = settings.URL_1C_API + 'files/inf/' + filtr_val

    if settings.DEBUG:
        print(url)

    resp = requests.get(url, auth=(settings.LOGIN_1C, settings.PASSWORD_1C))

    return resp.json()


def request_api_1c(param: str):
    url = settings.URL_1C_API + param
    if settings.DEBUG:
        print('DEBUG',url)
    
    req = requests.get(url, auth=(settings.LOGIN_1C, settings.PASSWORD_1C))


    return req.json()


class TestObj:
    filename = r'\\scan\net\Сканер\1C\doc02733320201030114838.pdf'
    short = 'short_name'
    del_path_half = r'\\scan\net\Сканер\1C'
    word_locathions = [{
        "x": 1580,
        "y": 313,
        "w": 23,
        "h": 156,
        "conf": 95,
        "word": "Счет-фактура",
        "sheets": 1},
        {"x": 1585,
         "y": 478,
         "w": 18,
         "h": 23,
         "conf": 90,
         "word": "№",
         "sheets": 1
         }]
    textField = """Прежде всего, внедрение современных методик однозначно определяет каждого участника как способного 
    учётом сложившейся международной обстановки, базовый вектор развития в значительной степени обусловливает 
    важность благоприятных перспектив. """


def test_request():
    """
    Тестирование апи запросов на базе произвользого объекта
    :return:
    """
    a = TestObj
    post_obj(a)


def test_getFiles(dir_path: str):
    get_files(dir_path)


if __name__ == "__main__":
    print('sub function')

    test_request()
