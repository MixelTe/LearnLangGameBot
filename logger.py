from datetime import datetime, timedelta
import logging


def custom_time(*args):
    utc_dt = datetime.utcnow()
    utc_dt += timedelta(hours=3)
    return utc_dt.timetuple()


def set_logging():
    logging.basicConfig(
        level=logging.ERROR,
        filename="log.log",
        format="[%(asctime)s] %(levelname)s in %(module)s (%(name)s): %(message)s",
        encoding="utf-8"
    )
    logging.Formatter.converter = custom_time
