from ast import Or
from rest_framework.permissions import (
    IsAuthenticated,  
    BasePermission, 
    AllowAny
)
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .auth_views import CheckIfPasswordWasChanged
import datetime as dt
import calendar
from .easter_dates import easter_dates
from .non_working_days import non_working_days

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
            "day_count": 0
        }
    
    def assignBaseData(self, month = None, year = None):
        self.month = int(month) if month else dt.datetime.now().month
        self.monthly_calendar["month"] = {
            "number": self.month,
            "name": self.get_month_name(self.month)
        }
        self.year = int(year) if year else dt.datetime.now().year
        self.monthly_calendar["year"] = self.year
        self.today = dt.datetime.now().day
        self.always_day_one = 1
        self.last_day_current_month = calendar.monthrange(self.year, self.month)
        self.first_week_day_current_month = dt.datetime(self.year,self.month,self.always_day_one).weekday()
        self.last_month = self.month - 1 if self.month > 1 else 12
        self.last_year = self.year - 1
        self.last_month_last_day = (
                calendar.monthrange(self.year, self.last_month)[1] 
                - (self.first_week_day_current_month - 1) 
            if self.last_month < 12
            else 
                calendar.monthrange(self.last_year, self.last_month)[1] 
                - (self.first_week_day_current_month - 1)
        )
        self.next_year = self.year + 1
        self.next_month = self.month + 1 if self.month < 12 else 1
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
        day = {
            "week_day": self.getDay(next_day),
            "day_number": day_number,
        }
        self.monthly_calendar["days"][day["week_day"]].append(
            {
                "number": day["day_number"],
                "month": month,
                "month_in_words": self.get_month_name(month),
            }
        )
        self.monthly_calendar["day_count"] += 1
        return({
            "next_day": next_day + 1 if next_day < 6 else 0,
            "day_number": day_number + 1
        })
    
    def get_days(self, month_type, month = None, year = None):
        self.assignBaseData(month, year)
        day_info = {}
        if month_type == "next":
            day_info["next_day"] = self.first_week_day_next_month
            day_info["day_number"] = 1
            while self.monthly_calendar["day_count"] < 42:
                day_info = self.assign_days(day_info["next_day"], day_info["day_number"], self.next_month)
        elif month_type == "prev":
            day_info["next_day"] = 0
            day_info["day_number"] = self.last_month_last_day
            while day_info["next_day"] < self.first_week_day_current_month:
                day_info = self.assign_days(day_info["next_day"], day_info["day_number"], self.last_month)
        else:
            day_info["next_day"] = self.first_week_day_current_month
            day_info["day_number"] = 1
            while day_info["day_number"] <= self.last_day_current_month[1]:
                day_info = self.assign_days(day_info["next_day"], day_info["day_number"], self.month)

    def get(self, request, *args, **kwargs):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        self.get_days("prev", month, year)
        self.get_days("current", month, year)
        self.get_days("next", month, year)
        return Response(self.monthly_calendar)


