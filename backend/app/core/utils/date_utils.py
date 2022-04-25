from datetime import date, datetime, timedelta
from pytz import timezone

KST = timezone("Asia/Seoul")


class D:
    def __init__(self, *args):
        self.utc_now = datetime.now()
        self.timedelta = 0  # 한국은 UTC+9

    @classmethod
    def convert_to_kst_tz(cls, value: datetime) -> datetime:
        return value.astimezone(KST)

    @classmethod
    def datetime(cls, diff: int = 0, is_kst_timezone: bool = True) -> datetime:
        if is_kst_timezone:
            dt = cls().utc_now.astimezone(KST)
        else:
            dt = cls().utc_now
        return dt + timedelta(hours=diff)

    @classmethod
    def date(cls, diff: int = 0, is_kst_timezone: bool = True) -> date:
        if is_kst_timezone:
            dt = cls().datetime(diff=diff).astimezone(KST)
        else:
            dt = cls().datetime(diff=diff)
        return dt.date()

    @classmethod
    def date_num(cls, diff: int = 0, is_kst_timezone: bool = True) -> int:
        return int(
            cls.date(diff=diff, is_kst_timezone=is_kst_timezone).strftime("%Y%m%d")
        )

    @classmethod
    def date_str(cls, diff: int = 0, is_kst_timezone: bool = True) -> str:
        return cls.date(diff=diff, is_kst_timezone=is_kst_timezone).strftime("%Y%m%d")

    @classmethod
    def datetime_str(cls, diff: int = 0, is_kst_timezone: bool = True) -> str:
        return cls.datetime(diff=diff, is_kst_timezone=is_kst_timezone).strftime(
            "%Y%m%d %H:%M:%S"
        )

    @classmethod
    def gap_days(
        cls, start_date: str = "2020-01-01", end_date: str = "2020-02-18"
    ) -> int:
        s = datetime.strptime(start_date, "%Y-%m-%d").date()
        e = datetime.strptime(end_date, "%Y-%m-%d").date()
        gap = (e - s).days
        return gap + 1
    
    @classmethod
    def today(cls) -> str:
        # Converting date into YYYY-MM-DD format
        d = datetime.today()
        today = d.strftime('%Y-%m-%d')
        return today
