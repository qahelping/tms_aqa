import os
import subprocess

# TODO: It looks like dependency from monolith, actually, we need to move some constants to core
from lib.monolith.constants import IGNORED_TABLE, TRIGGER_TABLES


# This helper is not used currently
class MySQLHelper:

    '''
    Ещё не реализовано в данном хелпере, но на данный момент уже можно брать готовый дамп с миграцией из артефактов
    соответствующей джобы, и сразу использовать как кэш без дополнительных действий.
    TODO: Research possibility to download and use pre-built database cache
    '''

    def __init__(self, db_config, logger):
        self.config = db_config
        self.log = logger
        # Get base data from config
        self.host = self.config.host
        self.name = self.config.name
        self.user = self.config.user
        # Set params
        self.params = f'-h {self.host} -u {self.user}'
        # Get path and file names from config
        self.cache_path = self.config.cache_path
        self.path = self.config.dumps_path
        self.cache = self.config.files.cache
        self.schema = self.config.files.schema
        self.migrations = self.config.files.migrations
        self.routines = self.config.files.routines
        self.payments_routines = self.config.files.payments_routines

    def create_database(self):
        self.log.info('Create MySQL database if not exists')
        self.run_command(f'mysql {self.params} -e "CREATE DATABASE IF NOT EXISTS {self.name};"')

    def drop_database(self):
        self.log.info('Drop MySQL database if exists')
        self.run_command(f'mysql {self.params} -e "DROP DATABASE IF EXISTS {self.name};"')

    def dump_database(self, full=True, triggersafe=True):
        if os.path.exists(f'{self.path}{self.cache}'):
            os.remove(f'{self.path}{self.cache}')
        tables_to_ignore = [IGNORED_TABLE]
        if triggersafe:
            tables_to_ignore += TRIGGER_TABLES
            tables_to_ignore_str = ' '.join([f'--ignore-table={table}' for table in tables_to_ignore])
            cmd = (f'mysqldump {self.params} '
                   f'--skip-add-locks '
                   f'--compact '
                   f'--skip-create-options '
                   f'--quote-names '
                   f'--skip-triggers '
                   f'--skip-opt '
                   f'--lock_tables=False '
                   f'--extended-insert '
                   f'--no-create-info '
                   f'{tables_to_ignore_str} '
                   f'> {self.cache_path}{self.cache}')
        if full:
            query = ' '.join([f'DELETE FROM {table};' for table in tables_to_ignore])
            self.execute_query(query)
            cmd = (f'mysqldump {self.params} '
                   f'--routines '
                   f'--lock_tables=False '
                   f'--extended-insert '
                   f'{self.name} '
                   f'> {self.cache_path}{self.cache}')
        self.log.info('Dump tables to cache')
        self.run_command(cmd)

    def execute_query(self, query):
        self.run_command(f'mysql {self.params} {self.name} -e "{query}"')

    def load_all_dumps(self):
        if os.path.exists(f'{self.path}{self.cache}'):
            self.log.info('Load MySQL cache')
            self.load_dump(self.cache)
        else:
            self.log.info('Load MySQL dumps')
            self.load_dump(self.schema)
            self.load_dump(self.migrations)
            self.load_dump(self.routines)
            self.load_dump(self.payments_routines)

    def load_dump(self, dump):
        self.run_command(f'mysql {self.params} {self.name} < {self.path}{dump}')

    def reset_database(self):
        self.drop_database()
        self.create_database()

    def run_command(self, cmd):
        self.log.info(f'{cmd}')
        subprocess.call([cmd, ], shell=True)
