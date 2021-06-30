import datetime
from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    """
    Bill 단일 객체에 대한 처리를 수행하는 serializer
    """
    class Meta:
        model = Bill
        fields = [
            "idx",
            "name",
            "birthDate",
            "location",
            "amount",
            "receivedDate",
            "state",
            "signature"]
    
    def validate_name(self, name):
        """
        이름 유효성 검사
        """
        if name == "":
            name= None

        return name

    def validate_birthDate(self, date):
        """
        생년월일 유효성 검사
        1. is Null
        2. 날짜 형식 검사
        """

        if date == "":
            date= None
            return date

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        
        return date

    def validate_location(self, location):
        """
        거주동 유효성 검사
        """
        if location == "":
            location= None

        return location
            
    def validate_receiveDate(self, date):
        """
        수령일 유효성 검사
        1. is Null
        2. 날짜 형식 검사
        """
       
        if date == "":
            date = None
            return date

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError("Incorrect data format, should be YYYY-MM-DD")

        return date


class BillListSerializer(serializers.ListSerializer):
    """
    Bill의 여러 객체에 대한 처리를 한번에 수행하는 serializer
    """
    child = BillSerializer()

    
