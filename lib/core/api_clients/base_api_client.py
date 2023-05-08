from requests import Session


class BaseAPIClient:

    def __init__(self, url):
        self.url = url[:-1] if url.endswith('/') else url
        self.session = Session()

    @staticmethod
    def _check_status_code(actual, expected):
        assert actual == expected, f'An unexpected status code has been returned: {actual}\n' \
                                   f'Expected status is {expected}'

    @staticmethod
    def _convert_response(response, to_json=True):
        if to_json:
            return response.json()
        return response

    def _check_status_and_convert(self, response, expected_status=200, to_json=True):
        self._check_status_code(
            actual=response.status_code,
            expected=expected_status,
        )
        return self._convert_response(response, to_json=to_json)

    def _request_delete(self, url, expected_status=204, to_json=False, **kwargs):
        return self._check_status_and_convert(
            response=self.session.delete(url=url, **kwargs),
            expected_status=expected_status,
            to_json=to_json,
        )

    def _request_get(self, url, expected_status=200, to_json=True, **kwargs):
        return self._check_status_and_convert(
            response=self.session.get(url=url, **kwargs),
            expected_status=expected_status,
            to_json=to_json,
        )

    def _request_patch(self, url, expected_status=200, to_json=True, **kwargs):
        return self._check_status_and_convert(
            response=self.session.patch(url=url, **kwargs),
            expected_status=expected_status,
            to_json=to_json,
        )

    def _request_post(self, url, expected_status=200, to_json=True, **kwargs):
        return self._check_status_and_convert(
            response=self.session.post(url=url, **kwargs),
            expected_status=expected_status,
            to_json=to_json,
        )

    def _request_put(self, url, expected_status=200, to_json=True, **kwargs):
        return self._check_status_and_convert(
            response=self.session.put(url=url, **kwargs),
            expected_status=expected_status,
            to_json=to_json,
        )
