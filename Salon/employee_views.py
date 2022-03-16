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
from .views import CheckIfPasswordWasChanged
import datetime as dt
import calendar

class GetMonthDays(APIView):
    permission_classes = [IsAuthenticated, CheckIfPasswordWasChanged]

    def get(self, request, *args, **kwargs):
        month = dt.datetime.now().month
        year = dt.datetime.now().year
        # year = 2022
        # month = 1
        day = 1
        #0 - poniedzialek ... 6 - niedziela
        first_week_day_current_month = dt.datetime(year,month,day).weekday()
        months = {
            "days": {
                "Monday": [],
                "Tuesday": [],
                "Wednesday": [],
                "Thursday": [],
                "Friday": [],
                "Saturday": [],
                "Sunday": []
            }
        }
        last_month = month - 1 if month > 1 else 12
        last_year = year
            
        # monthrange pierwszy parametr to dzień tygodnia, drugi to liczna dni miesiąca


        if(first_week_day_current_month > 0):
            last_month_info = None
            if last_month == 12:
                last_year = last_year - 1
                last_month_info = calendar.monthrange(last_year, last_month)
            else:
                last_month_info = calendar.monthrange(year, last_month)

            last_month_week_day = 0
            last_month_day = last_month_info[1] - (first_week_day_current_month - 1)

            while last_month_week_day < first_week_day_current_month:
                day = {
                    "week_day": getDay(last_month_week_day),
                    "day_number": last_month_day,
                }
                months["days"][day["week_day"]].append(
                    {
                        "number":day["day_number"],
                        "month": last_month
                    }
                )
                last_month_day += 1
                last_month_week_day += 1
        
        last_day_current_month = calendar.monthrange(year, month)
        
        print(months)
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
        }
        return Response(response)

def getDay(day):
    return {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday',
    }[day]