from datetime import datetime
from datetime import date


def get_datetime(raw_date):
    try:
        datetime_object = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        try:
            datetime_object = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%f")
        except:
            try:
                datetime_object = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S")
            except:
                try:
                    datetime_object = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                except:
                    try:
                        datetime_object = datetime.strptime(
                            raw_date, "%Y-%m-%dT%H:%M:%S-%f:%f"
                        )
                    except:
                        datetime_object = datetime(2011, 11, 4, 0, 0)
    return datetime_object
