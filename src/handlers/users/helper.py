def get_text(file_name):
    with open(f'texts/{file_name}', 'r', encoding='UTF-8') as file:
        return file.read()


def get_photo(file_name):
    return open(f'photo/{file_name}', 'rb')