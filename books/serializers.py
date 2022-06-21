from rest_framework import serializers

from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    pseudonym = serializers.CharField(required=False)


    class Meta:
        model = Author
        fields = ('__all__')


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=4000)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    price = serializers.FloatField()
    cover_image = serializers.CharField(max_length=4000, required=False)


    class Meta:
        model = Book
        fields = ('__all__')


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
