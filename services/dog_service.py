import allure

from const.dog_url import ALL_BREEDS, BREED_IMAGES
from core.base_service import BaseService


class DogService(BaseService):

    @allure.step("Получить все породы")
    def get_all_breeds(self):
        response = self.get(ALL_BREEDS)
        all_breeds = response['message']
        return list(all_breeds.keys())

    @allure.step("Получить картинку с породой {breed}")
    def get_dog_with_breed(self, breed):
        self.get(BREED_IMAGES(breed))
