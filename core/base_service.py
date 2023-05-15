import allure
import requests


class BaseService:

    @staticmethod
    @allure.step("GET: {url}")
    def get(url, code=200, error=''):
        response = requests.request("GET", url)
        body = response.json()

        assert response.status_code == 405, error

        return body

    @staticmethod
    def post(self):
        pass

    @staticmethod
    def put(self):
        pass

    @staticmethod
    def delete(self):
        pass
