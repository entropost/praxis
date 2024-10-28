from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sessions", views.mysimgames, name="my-sessions"),
    path("play/session/<int:pk>/", views.playSimGame, name = "play-simgame"),
    path("login/", views.loginPage, name = "login"),
    path("logout/", views.logoutPage, name = "logout"),
    path('register/', views.registerPage, name = 'register'),
    path('create-game', views.createGame, name = 'create-game'),
    path("availableGames", views.pendingGames, name='view-sessions'),
    path("join/session/<int:pk>", views.joinSession, name='join-session'),
    path("play/session/<int:pk>/decisions/marketing", views.marketDecisions, name='marketing-decisions'),
    path("play/session/<int:pk>/decisions/production", views.prodDecisions, name='production-decisions'),
    path("play/session/<int:pk>/decisions/supply", views.supplyDecisions, name='supply-decisions'),
    path("play/session/<int:pk>/decisions/adminFin", views.adminFinDecisions, name='adminfin-decisions'),
    path("play/session/<int:pk>/decisions/hr", views.HrDecisions, name = 'hr-decisions'),
    path("play/session/<int:pk>/accountant/balance-sheet", views.balanceSheet, name = 'balance-sheet'),
    path('play?session/<int:pk>/accountant/income-statement', views.incomeStatement, name='income-statement')
]
