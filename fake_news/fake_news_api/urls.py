from django.conf.urls import url, include

from .api import StartupViewSet, NaiveBayesViewSet, DecisionTreeViewSet

urlpatterns = [
    url(r'^startup/', include(StartupViewSet.get_router(), namespace='startup')),
    url(r'^naive_bayes/', include(NaiveBayesViewSet.get_router(), namespace='naive bayes api')),
    url(r'^decision_tree/', include(DecisionTreeViewSet.get_router(), namespace='decision tree api'))
]