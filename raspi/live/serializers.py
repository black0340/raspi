from rest_framework import serializers
from .models import SavedImage

class SavedImageSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = SavedImage # 모델 설정
        fields = ('UltraSonic','ImageNumber','CreatedAt') # 필드 설정

