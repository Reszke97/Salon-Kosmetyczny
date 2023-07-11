import calendar
class NonWorkingDays:
    def __init__(self, year):
        self.easter_dates = [
            "2000-04-23",   "2025-04-20",   "2050-04-10",   "2075-04-07",
            "2001-04-15",   "2026-04-05",   "2051-04-02",   "2076-04-19",
            "2002-03-31",   "2027-03-28",   "2052-04-21",   "2077-04-11",
            "2003-04-20",   "2028-04-16",   "2053-04-06",   "2078-04-03",
            "2004-04-11",   "2029-04-01",   "2054-03-29",   "2079-04-23",
            "2005-03-27",   "2030-04-21",   "2055-04-18",   "2080-04-07",
            "2006-04-16",   "2031-04-13",   "2056-04-02",   "2081-03-30",
            "2007-04-08",   "2032-03-28",   "2057-04-22",   "2082-04-19",
            "2008-03-23",   "2033-04-17",   "2058-04-14",   "2083-04-04",
            "2009-04-12",   "2034-04-09",   "2059-03-30",   "2084-03-26",
            "2010-04-04",   "2035-03-25",   "2060-04-18",   "2085-04-15",
            "2011-04-24",   "2036-04-13",   "2061-04-10",   "2086-03-31",
            "2012-04-08",   "2037-04-05",   "2062-03-26",   "2087-04-20",
            "2013-03-31",   "2038-04-25",   "2063-04-15",   "2088-04-11",
            "2014-04-20",   "2039-04-10",   "2064-04-06",   "2089-04-03",
            "2015-04-05",   "2040-04-01",   "2065-03-29",   "2090-04-16",
            "2016-03-27",   "2041-04-21",   "2066-04-11",   "2091-04-08",
            "2017-04-16",   "2042-04-06",   "2067-04-03",   "2092-03-30",
            "2018-04-01",   "2043-03-29",   "2068-04-22",   "2093-04-12",
            "2019-04-21",   "2044-04-17",   "2069-04-14",   "2094-04-04",
            "2020-04-12",   "2045-04-09",   "2070-03-30",   "2095-04-24",
            "2021-04-04",   "2046-03-25",   "2071-04-19",   "2096-04-15",
            "2022-04-17",   "2047-04-14",   "2072-04-10",   "2097-03-31",
            "2023-04-09",   "2048-04-05",   "2073-03-26",   "2098-04-20",
            "2024-03-31",   "2049-04-18",   "2074-04-15",   "2099-04-12",
        ]
        self.non_working_days = [
            "01-01",
            "01-06",
            "05-01",
            "05-03",
            "08-15",
            "11-01",
            "11-11",
            "12-25",
            "12-26"
        ]
        self.non_working_days_with_year = []
        self.getMovableHolidays(year)
        self.append_year()

    def append_year(self):
        for date in self.non_working_days:
            self.non_working_days_with_year.append(str(self.year) + '-' + date)
    
    def getMovableHolidays(self, year):
        self.year = year
        self.month = None
        self.getEaster()
        self.getCorpusChristiDay()

    def getEaster(self):
        for easter in self.easter_dates:
            split_easter_date = easter.split('-')
            if(str(split_easter_date[0]) == str(self.year)):
                _easter = split_easter_date[1] + '-' + split_easter_date[2]
                self.month = int(split_easter_date[1]) if split_easter_date[1][0] != "0" else int(split_easter_date[1][1])
                month_of_easter = self.month
                self.day = int(split_easter_date[2]) if split_easter_date[2][0] != "0" else int(split_easter_date[2][1])
                day_of_easter = self.day
                self.non_working_days.append(_easter)
                month_days = calendar.monthrange(int(self.year), int(self.month))[1]
                if int(self.day) == int(month_days):
                    self.month += 1
                    self.day = "01"
                    self.month = '0' + str(self.month) if self.month < 10 else str(self.month)
                    self.non_working_days.append(self.month + '-' + self.day)
                else:
                    self.day += 1
                    self.day = '0' + str(self.day) if self.day < 10 else str(self.day)
                    self.month = '0' + str(self.month) if self.month < 10 else str(self.month)
                    self.non_working_days.append(str(self.month) + '-' + self.day)
                self.month = month_of_easter
                self.day = day_of_easter
                break
    # Boże ciało + 60 dni od wielkanocy zawsze
    def getCorpusChristiDay(self):
        self.year = int(self.year)
        days_left = 60
        month_days = calendar.monthrange(int(self.year), int(self.month))[1]
        while days_left > 0:
            if self.day == month_days:
                self.month += 1
                self.day = 1
                month_days = calendar.monthrange(int(self.year), int(self.month))[1]
            else:
                self.day += 1
            days_left -= 1
        if int(self.month) < 10:
            self.month = "0" + str(self.month)
        if int(self.day) < 10:
            self.day = "0" + str(self.day)
        self.non_working_days.append(str(self.month) + '-' + str(self.day))

    def checkForHoliday(self, day, month):
        for non_working_day in self.non_working_days:
            _non_working_day = non_working_day.split('-')
            if _non_working_day[1] == day and _non_working_day[0] == month:
                return True
        return False