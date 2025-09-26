from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from curso.views import CursoViewSet
from disciplina.views import DisciplinaViewSet
from perfis.views import PerfilViewSet

router = DefaultRouter()
router.register(r'cursos',CursoViewSet)
router.register(r'perfis',PerfilViewSet)
router.register(r'disciplinas',DisciplinaViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
