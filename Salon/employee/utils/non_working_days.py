import calendar
class NonWorkingDays:
    def __init__(self, year):
        self.easter_dates = [
            "23-4-2000",   "20-4-2025",   "10-4-2050",    "7-4-2075",
            "15-4-2001",    "5-4-2026",    "2-4-2051",   "19-4-2076",
            "31-3-2002",   "28-3-2027",   "21-4-2052",   "11-4-2077",
            "20-4-2003",   "16-4-2028",    "6-4-2053",    "3-4-2078",
            "11-4-2004",    "1-4-2029",   "29-3-2054",   "23-4-2079",
            "27-3-2005",   "21-4-2030",   "18-4-2055",    "7-4-2080",
            "16-4-2006",   "13-4-2031",    "2-4-2056",   "30-3-2081",
            "8-4-2007",   "28-3-2032",    "22-4-2057",   "19-4-2082",
            "23-3-2008",   "17-4-2033",   "14-4-2058",    "4-4-2083",
            "12-4-2009",    "9-4-2034",   "30-3-2059",   "26-3-2084",
            "4-4-2010",   "25-3-2035",   "18-4-2060",   "15-4-2085",
            "24-4-2011",   "13-4-2036",   "10-4-2061",   "31-3-2086",
            "8-4-2012",    "5-4-2037",   "26-3-2062",   "20-4-2087",
            "31-3-2013",   "25-4-2038",   "15-4-2063",   "11-4-2088",
            "20-4-2014",   "10-4-2039",    "6-4-2064",    "3-4-2089",
            "5-4-2015",    "1-4-2040",   "29-3-2065",   "16-4-2090",
            "27-3-2016",   "21-4-2041",   "11-4-2066",    "8-4-2091",
            "16-4-2017",    "6-4-2042",    "3-4-2067",   "30-3-2092",
            "1-4-2018",   "29-3-2043",   "22-4-2068",   "12-4-2093",
            "21-4-2019",   "17-4-2044",   "14-4-2069",    "4-4-2094",
            "12-4-2020",    "9-4-2045",   "30-3-2070",   "24-4-2095",
            "4-4-2021",   "25-3-2046",   "19-4-2071",   "15-4-2096",
            "17-4-2022",   "14-4-2047",   "10-4-2072",   "31-3-2097",
            "9-4-2023",    "5-4-2048",   "26-3-2073",   "20-4-2098",
            "31-3-2024",   "18-4-2049",   "15-4-2074",   "12-4-2099",
        ]
        self.non_working_days = [
            "1-1",
            "6-1",
            "1-5",
            "3-5",
            "15-8",
            "1-11",
            "11-11",
            "25-12",
            "26-12"
        ]
        self.getMovableHolidays(year)

    def getMovableHolidays(self, year):
        self.year = year
        self.getEaster()
        self.getCorpusChristiDay()

    def getEaster(self):
        for easter in self.easter_dates:
            split_easter_date = easter.split('-')
            if(split_easter_date[2] == self.year):
                _easter = split_easter_date[0] + '-' + split_easter_date[1]
                self.month = int(split_easter_date[1])
                self.day = int(split_easter_date[0])
                self.non_working_days.append(_easter)
                break
        easter_month_days = calendar.monthrange(int(self.year), int(self.month))
        if easter_month_days[1] == self.day:
            self.non_working_days.append('1' + '-' + str(self.month+1))
        else:
            self.non_working_days.append(str(self.day+1) + '-' + str(self.month))

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
        self.non_working_days.append(str(self.day) + '-' + str(self.month))
    
    def checkForHoliday(self, day, month):
        for non_working_day in self.non_working_days:
            _non_working_day = non_working_day.split('-')
            if int(_non_working_day[0]) == int(day) and int(_non_working_day[1]) == int(month):
                return True
        return False