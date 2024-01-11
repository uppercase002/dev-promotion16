from django.urls import path
from . import views

app_name = 'G_P16'

urlpatterns = [
    path('', views.index , name = 'index'),
    # path('envoyer_mail/', views.envoyer_mail, name = 'envoyer_mail'),
    path('presentation/', views.presentation, name = 'presentation'),
    path('departement/', views.departement, name = 'departement'),
    path('connexion/', views.connexion, name = 'connexion'),
    path('deconnexion/', views.deconnexion, name = 'deconnexion'),
    path('menu/', views.menu, name = 'menu'),
    # path('supprEtu/<str:matricule>/', views.supprEtu,name = 'supprEtu'),
    path('modifierEtud/<int:id>/', views.modifierEtud, name = 'modifierEtud'),
    path('enseignant/', views.enseignant, name = 'enseignant'),
    path('supprEns/<int:id>/', views.supprEns, name = 'supprEns'),
    path('modifierEns/<int:id>/', views.modifierEns, name = 'modifierEns'),
    path('matiere/', views.matiere, name = 'matiere'),
    path('modifierMat/<int:id>/', views.modifierMat, name = 'modifierMat'),
    path('supprMat/<int:id>/', views.supprMat, name = 'supprMat'),
    path('dep/', views.dep, name = 'dep'),
    path('utilisateur/', views.utilisateur, name = 'utilisateur'),
    path('ChangePwd/<int:id>/', views.ChangePwd , name = 'ChangePwd'),
    path('supprDep/<int:id>/', views.supprDep, name = 'supprDep'),
    path('modifierDep/<int:id>/', views.modifierDep, name = 'modifierDep'),
    path('supprUser/<int:id>/', views.supprUser, name = 'supprUser'),
    path('modifierUser/<int:id>/', views.modifierUser, name = 'modifierUser'),
]