from rest_framework import serializers, viewsets

from art.models import Tag


# 声明 Tag（ORM）模型对象的序列化(将对象转成某种格式(dict)字符串)
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'add_time')


# 声明 Tag数据资源的前端操作
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer