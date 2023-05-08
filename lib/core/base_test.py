from pytest import fixture

from lib.core.helpers import Logger


class BaseTest:

    # This is needed only to disable PyCharm warning
    config = None
    log = None

    @fixture(scope='session', autouse=True)
    def prepare_for_test_session(self, pytestconfig):
        # Make some preparations in child class, e.g. warm up some urls related to the system under test
        pass

    @fixture(scope='class', autouse=True)
    def setup_config(self, pytestconfig, request):
        cls = request.node.cls
        cls.config = pytestconfig.conf

    @fixture(scope='class', autouse=True)
    def setup_logger(self, pytestconfig, request, setup_config):
        cls = request.node.cls

        # Configure logger options (if options override config values)
        if pytestconfig.getoption('logfile'):
            cls.config.logger.file = pytestconfig.getoption('logfile')
        if pytestconfig.getoption('logformat'):
            cls.config.logger.format = pytestconfig.getoption('logformat')
        if pytestconfig.getoption('loglevel'):
            cls.config.logger.level = str(pytestconfig.getoption('loglevel')).upper()

        # Get logger
        cls.log = Logger.get(
            name=cls.__name__,
            filename=cls.config.logger.file,
            logformat=cls.config.logger.format,
            loglevel=cls.config.logger.level,
        )
