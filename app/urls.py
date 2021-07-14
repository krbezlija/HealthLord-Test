from django.urls import path
from . import views


urlpatterns = [
	path("", views.delavci, name="home"),
	path("trgovine/", views.trgovine, name="trgovine"),
	path("iskanjePoDel/", views.iskanjePoDel, name="iskanjePoDel"),
	path("iskanjePoTrg/", views.iskanjePoTrg, name="iskanjePoTrg"),
	path("novaTrgovina/", views.novaTrgovina, name="novaTrgovina"),
	path("noviDelavec/", views.noviDelavec, name="noviDelavec"),
	path("spremeniD/", views.spremeniD, name="spremeniD"),
	path("spremeniT/", views.spremeniT, name="spremeniT"),
]
