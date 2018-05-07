from django.conf.urls import url, include

from .api import StartupViewSet, NaiveBayesViewSet

urlpatterns = [
    url(r'^startup/', include(StartupViewSet.get_router(), namespace='startup')),
    url(r'^naive_bayes/', include(NaiveBayesViewSet.get_router(), namespace='naive bayes api'))
]