from rest_framework.routers import DefaultRouter

from api_.tag import TagViewSet

# 创建API路由对象
router = DefaultRouter()

# 向路由注册Viewset(接口)
router.register(r'tag', TagViewSet)
