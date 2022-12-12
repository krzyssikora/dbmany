from django.urls import path, reverse_lazy

from . import views

app_name = 'dbmany'
urlpatterns = [
    path('', views.index, name='all'),
    path('group/<int:pk>', views.GroupDetailView.as_view(), name='group_detail'),
    path('person/<int:pk>', views.PersonDetailView.as_view(), name='person_detail'),
    path('person/create',
         views.PersonCreateView.as_view(success_url=reverse_lazy('dbmany:all')), name='person_create'),
    path('group/create',
         views.GroupCreateView.as_view(success_url=reverse_lazy('dbmany:all')), name='group_create'),
    path('person/<int:pk>/update',
         views.PersonUpdateView.as_view(success_url=reverse_lazy('dbmany:all')), name='person_update'),
    path('person/<int:pk>/delete',
         views.PersonDeleteView.as_view(success_url=reverse_lazy('dbmany:all')), name='person_delete'),
    path('person_picture/<int:pk>', views.stream_file, name='person_picture'),
]