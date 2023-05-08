from datetime import timedelta, datetime


class GetDate:

    @staticmethod
    def convert(datetime_str, old_format, new_format):
        return datetime.strptime(datetime_str, old_format).strftime(new_format)

    @staticmethod
    def datetime(days=0, date_format='%Y-%m-%d %H:%M:%S'):
        return (datetime.now() + timedelta(days)).strftime(date_format)

    @staticmethod
    def date(days=0, date_format='%d.%m.%Y'):
        return GetDate.datetime(days, date_format)
