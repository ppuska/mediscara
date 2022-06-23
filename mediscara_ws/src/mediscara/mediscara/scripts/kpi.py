"""Module for managing KPI"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import ClassVar


class KPI:
    """Class for tracking and managing KPIs"""

    def __init__(self, quota: int = 60):
        self.__availability = KPI.Availability()
        self.__quality = KPI.Quality(quota)
        self.__performance = KPI.Performance(quota)

    def __repr__(self) -> str:
        return f"""KPI:
        {self.availability}
        {self.quality}
        {self.performance}"""

    @property
    def availability(self):
        """Returns the availability member of the class

        Returns:
            KPI.Availability: Availability
        """
        return self.__availability

    @property
    def quality(self):
        """Returns the quality member of the class

        Returns:
            KPI.Quality: Quality
        """
        return self.__quality

    @property
    def performance(self):
        """Returns the performance member of the class

        Returns:
            KPI.Performance: Performance
        """
        return self.__performance

    @dataclass
    class Availability:
        """Dataclass to manage and store the availability KPI value"""

        format = "%H:%M:%S"
        __planned_start: ClassVar[datetime] = datetime.strptime("08:00:00", format)
        __planned_end: ClassVar[datetime] = datetime.strptime("10:00:00", format)  # todo set to 16:00:00
        __actual_start: datetime = field(default=None)
        __actual_end: datetime = field(default=None)

        def __repr__(self):
            return f"Availability: {self.actual_duration=} / {self.__planned_end - self.__planned_start=} = {self.calculate()}"

        def start_now(self):
            """Sets the actual start time to the current time"""
            self.__actual_start = datetime.now()

        def end_now(self):
            """Sets the actual end time to the current time"""
            self.__actual_end = datetime.now()

        def calculate(self):
            """Calculates the Availabilty KPI

            Returns:
                float: Availability KPI
            """
            planned_duration = self.__planned_end - self.__planned_start

            return self.actual_duration / planned_duration

        # region PROPERTIES

        @property
        def actual_start(self):
            """Returns the actual start value in a None safe way

            Returns:
                str: the actual start value as a formatted string
            """
            if self.__actual_start is None:
                return "Not set yet"

            return self.__actual_start.strftime(self.format)

        @property
        def actual_end(self):
            """Returns the actual end value as a formatted string

            Returns:
                str: The actual end time as a formatted string
            """
            if self.__actual_end is None:
                return "Not set yet"
            else:
                return self.__actual_end

        @property
        def planned_start(self):
            """Returns the planned start time

            Returns:
                datetime: The planned start time
            """
            return self.__planned_start

        @property
        def planned_end(self):
            """Returns the planned end time

            Returns:
                datetim: The planned end time
            """
            return self.__planned_end

        @property
        def actual_duration(self) -> timedelta:
            """Returns the actual duration (A_curM in the documenatation)"""
            if self.__actual_start is None:
                return timedelta(0)

            start = self.__actual_start

            if self.__actual_end is None:
                end = datetime.now()

            else:
                end = self.__actual_end

            return end - start

        # endregion

    @dataclass
    class Quality:
        """Class for calculating and storing quality KPI data

        Reference quality is defined as
        """

        __product_count: int = field(default=0)
        __error_count: int = field(default=0)

        def __repr__(self):
            return f"Quality: ({self.product_count} - {self.error_count}) / {self.product_count} = {self.calculate()}"

        def calculate(self):
            """Calculates the Quality KPI number

            Returns:
                float: the Quality KPI
            """
            if self.product_count == 0:
                return 0

            if self.error_count > self.product_count:
                return 0

            return (self.product_count - self.error_count) / self.product_count

        @property
        def product_count(self):
            """Product count getter

            Returns:
                int: product count
            """
            return self.__product_count

        @product_count.setter
        def product_count(self, value: int):
            """Product count setter

            Args:
                value (int): the value to be set
            """
            self.__product_count = value

        @property
        def error_count(self):
            """Error count getter

            Returns:
                int: the number of errors
            """
            return self.__error_count

        @error_count.setter
        def error_count(self, value: int):
            """Error count setter

            Args:
                value (int): the number of errors to be set
            """
            self.__error_count = value

    @dataclass
    class Performance:
        """Class for calculating and storing performance KPIs

        Performance is calculated as {products manufactured} / {manufacturing time}
        Reference performance is 60 [-] / 10 [h]
        Actual performance is calculated as {actual products made} / A_curM - {time paused}
            - where A_curM is the actual working time (see Availability class)

        The performance KPI is calculated like this:
            - P_M = {Actual performance} / {Reference performance}

        To simplify code performance will be calculated as
            - {manufacturing time} / {products manufactured}
        and the performance KPI will be calculated as
            - 1 / P_M = 1 / ({Actual performance} / {Reference performance})
        """

        __product_quota: int

        __work_period: ClassVar[timedelta] = timedelta(hours=10)
        __reference_performance: timedelta = field(init=False)

        __paused: timedelta = field(default=timedelta(0))
        __pause_timer: ClassVar[datetime] = None

        __product_count: int = field(default=0)

        def __post_init__(self):
            self.__reference_performance = self.__product_quota / self.__work_period.total_seconds()

        def __repr__(self):
            return f"Performance: {self.paused=} {self.product_count=}"

        def calculate(self, a_cur_m: timedelta):
            """Calculates the Performace KPI based on the input and stored data

            Args:
                a_cur_m (timedelta): The current availability time delta (A_cur_m in the docs)

            Returns:
                float: The performance KPI
            """

            manuf_time = (a_cur_m - self.paused).total_seconds()  # in seconds as float

            if manuf_time == 0:
                return 0.0

            actual_performance = self.product_count / (a_cur_m - self.paused).total_seconds()

            kpi = actual_performance / self.__reference_performance

            return kpi

        def pause_start(self):
            """Starts the pause timer"""
            self.__pause_timer = datetime.now()

        def pause_end(self):
            """Ends the pause timer"""
            if self.__pause_timer is None:
                return

            self.paused += datetime.now() - self.__pause_timer
            self.__pause_timer = None

        @property
        def paused(self):
            """Returns whether the Performance counting is currently paused or not"""
            return self.__paused

        @paused.setter
        def paused(self, value: timedelta):
            self.__paused = value

        @property
        def product_count(self):
            """Returns the current product count"""
            return self.__product_count

        @product_count.setter
        def product_count(self, value: int):
            """Sets the current product count

            Args:
                value (int): The current product count
            """
            self.__product_count = value
