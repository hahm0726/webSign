import datetime
from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            "idx",
            "name",
            "birthDate",
            "location",
            "amount",
            "receiveDate",
            "state",
            "signature"]

    def validate_birthDate(self, date):
        """
        생년월일 유효성 검사
        """
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        
        return date

            
    def validate_receiveDate(self, date):
        """
        수령일 유효성 검사
        """
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError("Incorrect data format, should be YYYY-MM-DD")

        return date
