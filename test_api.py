import allure
import pytest

from services.dog_service import DogService

@allure.story('Dog API')
@allure.title("Получение картинки по породе")
@pytest.mark.regress
def test_api_breed():
    dog_service = DogService()
    all_breeds = dog_service.get_all_breeds()

    dog_service.get_dog_with_breed(all_breeds[0])\



@allure.story('Dog API')
@allure.title("Получение картинки по породе 2")
@pytest.mark.regress
@pytest.mark.skip(reason="Doesn't automated")
def test_api_breed1():
    pass


