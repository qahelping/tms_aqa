from pytest import fixture
from requests import Session

from lib.core.base_test import BaseTest


class BaseAPITest(BaseTest):

    session = None  # This is needed only to disable PyCharm weak warning

    @property
    # This property have to be redefined in children classes
    def api_url(self):
        return None

    @fixture(autouse=True)
    # This fixture could be redefined in children classes to extend session set up
    def create_session(self):
        self.session = Session()
        yield
        self.session.close()

    @staticmethod
    def _check_status_code(actual, expected):
        assert actual == expected, f'A request has returned unexpected status code: {actual}\n' \
                                   f'Expected status is {expected}'

    @staticmethod
    def _convert_response(response, raw=True, to_list=False):
        if raw:
            return response
        elif to_list:
            return response.json()['value']
        return response.json()

    def _check_status_and_convert(self, response, expected_status=200, raw=True, to_list=False):
        self._check_status_code(
            actual=response.status_code,
            expected=expected_status,
        )
        return self._convert_response(response, raw=raw, to_list=to_list)

    def _request_delete(self, url, expected_status=204, raw=True, to_list=False):
        return self._check_status_and_convert(
            response=self.session.delete(url=url),
            expected_status=expected_status,
            raw=raw,
            to_list=to_list,
        )

    def _request_get(self, url, expected_status=200, raw=False, to_list=False):
        return self._check_status_and_convert(
            response=self.session.get(url=url),
            expected_status=expected_status,
            raw=raw,
            to_list=to_list,
        )

    def _request_patch(self, url, data=None, json=None, expected_status=200, raw=False, to_list=False):
        return self._check_status_and_convert(
            response=self.session.patch(
                url=url,
                data=data,
                json=json,
            ),
            expected_status=expected_status,
            raw=raw,
            to_list=to_list,
        )

    def _request_post(self, url, data=None, json=None, expected_status=200, raw=False, to_list=False):
        return self._check_status_and_convert(
            response=self.session.post(
                url=url,
                data=data,
                json=json,
            ),
            expected_status=expected_status,
            raw=raw,
            to_list=to_list,
        )

    def _request_put(self, url, data=None, json=None, expected_status=200, raw=False, to_list=False):
        return self._check_status_and_convert(
            response=self.session.put(
                url=url,
                data=data,
                json=json,
            ),
            expected_status=expected_status,
            raw=raw,
            to_list=to_list,
        )
