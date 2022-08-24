from django.urls import path

from . import views

"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Here at first the app name is declared to find the right app and the all urls of the template are
added to connect with the view of the app.
"""

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]