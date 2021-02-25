# Создать объект менеджера контекста который будет переходить по заданному юрл,
# при этом отловить requests.exceptions.ConnectionError. в теле менеджера записать html файл и закрыть его
import requests
import pytest

class MyUrlContextManager():
    def __init__(self, url, exception=None):
        self.url = url
        self.exception = exception or Exception
        self.file = open("test.html", mode="w", encoding="UTF8")

    def __enter__(self):
        try:
            re = requests.get(self.url, timeout=3)
        except self.exception:
            if self.exception == Exception:
                raise
            raise self.exception()
        if re.status_code == 200:
            # with open("test.html", mode="w", encoding="UTF8") as file:
            data = re.text
            self.file.write(data)
            return data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


if __name__ == "__main__":
    with MyUrlContextManager("https://1habr.com/ru/company/lamoda/blog/432656/") as c:
        print(c)
