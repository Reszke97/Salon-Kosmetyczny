from rest_framework.permissions import (
    IsAuthenticated,  
    BasePermission, 
    AllowAny
)
from rest_framework.views import APIView
from ..models import *
from ..serializers import *
from ..auth.auth_backend import CheckIfPasswordWasChanged
from .utils.non_working_days import NonWorkingDays
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
import datetime as dt
import calendar

class Holidays(APIView):
    # permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get_holidays(self, year):
        return NonWorkingDays(year).non_working_days

    def get(self, request):
        non_working_days = self.get_holidays(request.query_params.get("year"))
        return Response(data=non_working_days, status=status.HTTP_200_OK)
    
class HolidaysForThreeYears(APIView):
    def get(self, request):
        non_working_days_current_year = NonWorkingDays(request.query_params.get("year")).non_working_days_with_year
        non_working_days_prev_year = NonWorkingDays(str(int(request.query_params.get("year")) - 1)).non_working_days_with_year
        non_working_days_next_year = NonWorkingDays(str(int(request.query_params.get("year")) +1)).non_working_days_with_year
        non_working_days = non_working_days_prev_year + non_working_days_current_year + non_working_days_next_year
        return Response(data=non_working_days, status=status.HTTP_200_OK)

class GetMonthDays(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]
    def __init__(self):
        self.monthly_calendar = {
            "days": {
                "Poniedziałek": [],
                "Wtorek": [],
                "Środa": [],
                "Czwartek": [],
                "Piątek": [],
                "Sobota": [],
                "Niedziela": []
            },
            "day_count": 0,
            "dayOfMonth": 0,
            "week":0,
            "year":0,
            "next_month_days": 0,
            "last_month_days": 0,
            "current_month_days": 0,
            "week_start": "",
            "week_end":""
        }
    
    def assignBaseData(self, month = None, year = None, dayOfMonth = None):
        date_now = dt.datetime.now()
        self.today = date_now.day
        self.dayOfMonth = int(dayOfMonth) if dayOfMonth else self.today
        self.month = int(month) if month else date_now.month
        self.year = int(year) if year else date_now.year
        self.week = (
            dt.datetime(month = self.month, day = self.dayOfMonth, year = self.year).isocalendar().week 
            if dayOfMonth and month and year
            else date_now.isocalendar().week
        )
        self.monthly_calendar["month"] = {
            "number": self.month,
            "name": self.get_month_name(self.month)
        }
        self.monthly_calendar["year"] = self.year
        self.always_day_one = 1
        self.last_day_current_month = calendar.monthrange(self.year, self.month)
        self.first_week_day_current_month = dt.datetime(self.year,self.month,self.always_day_one).weekday()
        self.last_month = self.month - 1 if self.month > 1 else 12
        self.last_year = self.year - 1
        self.next_year = self.year + 1

        if self.last_month < 12:
            self.last_month_last_day = (
                calendar.monthrange(self.year, self.last_month)[1] - (self.first_week_day_current_month - 1) 
            )
            self.last_month_days = calendar.monthrange(self.year, self.last_month)[1]
        else:
            self.last_month_last_day = (
                calendar.monthrange(self.last_year, self.last_month)[1] - (self.first_week_day_current_month - 1)
            )
            self.last_month_days = calendar.monthrange(self.last_year, self.last_month)[1]

        if self.month < 12:
            self.next_month = self.month + 1
            self.next_month_days = calendar.monthrange(self.year, self.next_month)[1]
        else:
            self.next_month = 1
            self.next_month_days = calendar.monthrange(self.next_year, self.next_month)[1]

        self.first_week_day_next_month = dt.datetime(
            self.next_year if self.month == 12 else self.year,
            self.next_month,
            self.always_day_one
        ).weekday()
    
    def getDay(self,day):
        return {
            0: 'Poniedziałek',
            1: 'Wtorek',
            2: 'Środa',
            3: 'Czwartek',
            4: 'Piątek',
            5: 'Sobota',
            6: 'Niedziela',
        }[day]

    def get_month_name(self, month):
        return {
            1: 'Styczeń',
            2: 'Luty',
            3: 'Marzec',
            4: 'Kwiecień',
            5: 'Maj',
            6: 'Czerwiec',
            7: 'Lipiec',
            8: 'Sierpień',
            9: 'Wrzesień',
            10: 'Październik',
            11: 'Listopad',
            12: 'Grudzień',
        }[month]

    def assign_days(self, next_day, day_number, month):
        dayOfMonth = {
            "week_day": self.getDay(next_day),
            "day_number": day_number,
        }
        self.monthly_calendar["days"][dayOfMonth["week_day"]].append(
            {
                "number": dayOfMonth["day_number"],
                "month": month,
                "month_in_words": self.get_month_name(month),
                "holiday": self.non_working_days.checkForHoliday(day_number, month)
            }
        )
        self.monthly_calendar["day_count"] += 1
        return({
            "next_day": next_day + 1 if next_day < 6 else 0,
            "day_number": day_number + 1
        })
    
    def get_days(
        self, action_type = "current", 
        month = None, year = None, calendar_type = "monthly", dayOfMonth = None,
        week = None
    ):
        self.assignBaseData(month, year, dayOfMonth)
        day_info = {}
        if calendar_type == "monthly":
            if action_type == "next":
                day_info["next_day"] = self.first_week_day_next_month
                day_info["day_number"] = 1
                while self.monthly_calendar["day_count"] < 42:
                    day_info = self.assign_days(day_info["next_day"], day_info["day_number"], self.next_month)
            elif action_type == "prev":
                day_info["next_day"] = 0
                day_info["day_number"] = self.last_month_last_day
                while day_info["next_day"] < self.first_week_day_current_month:
                    day_info = self.assign_days(day_info["next_day"], day_info["day_number"], self.last_month)
            else:
                day_info["next_day"] = self.first_week_day_current_month
                day_info["day_number"] = 1
                while day_info["day_number"] <= self.last_day_current_month[1]:
                    day_info = self.assign_days(day_info["next_day"], day_info["day_number"], self.month)
                    
        elif calendar_type == "weekly":
            year = self.year
            if self.month == 1 and self.week >= 52:
                year -= 1
            if self.month == 12 and self.week == 1:
                year += 1
            given_year_week = str(year) + '-' + 'W' + str(self.week)
            date = dt.datetime.strptime(given_year_week + '-1', "%G-W%V-%u")
            ## zwraca pierwszy dzień tygodnia na podstawie podanych danych
            day_info["next_day"] = 0
            day_info["day_number"] = date.day
            month_days = self.last_day_current_month[1]
            if self.month > date.month:
                month_days = self.last_month_days

            month = date.month
            week_start_month = date.month
            week_start_year = date.year
            week_end_year = date.year
            while self.monthly_calendar["day_count"] < 7:
                if day_info["day_number"] > month_days:
                    month += 1
                    if month > 12:
                        week_end_year = date.year + 1
                        month = 1
                    day_info["day_number"] = 1
                day_info = self.assign_days(day_info["next_day"], day_info["day_number"], month)
            self.monthly_calendar["week_start"] = str(date.day) + ' ' + self.get_month_name(week_start_month) + ' ' + str(week_start_year)
            self.monthly_calendar["week_end"] = str(day_info["day_number"] - 1) + ' ' + self.get_month_name(month) + ' ' + str(week_end_year)
            
        # elif calendar_type == "daily":



    def get(self, request, *args, **kwargs):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        dayOfMonth = request.query_params.get("dayOfMonth")
        self.non_working_days  = NonWorkingDays(year)

        if request.query_params.get("calendarType") == "weekly":
            self.get_days(calendar_type = "weekly", year = year, dayOfMonth = dayOfMonth, month = month)
        elif request.query_params.get("calendarType") == "monthly":
            self.get_days("prev", month, year)
            self.get_days("current", month, year)
            self.get_days("next", month, year)
            
        # elif request.query_params.get("daily"):
        self.monthly_calendar["week"] = self.week
        self.monthly_calendar["dayOfMonth"] = self.dayOfMonth
        self.monthly_calendar["year"] = self.year
        self.monthly_calendar["next_month_days"] = self.next_month_days
        self.monthly_calendar["last_month_days"] = self.last_month_days
        self.monthly_calendar["current_month_days"] = self.last_day_current_month[1]    
        return Response(self.monthly_calendar)


