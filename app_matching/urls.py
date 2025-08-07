from django.urls import path
from app_matching.views.matching_group_list_view import MatchingGroupListView
from app_matching.views.matching_group_create_view import MatchingGroupCreateView
from app_matching.views.matching_group_update_view import MatchingGroupUpdateView
from app_matching.views.matching_pre_confirm import MatchingPreConfirmView
from app_matching.views.matching_method_hybrid import MatchingMethodHybridView
from app_matching.views.matching_method_auto import MatchingMethodAutoView
from app_matching.views.matching_method_manual import MatchingMethodManualView
from app_matching.views.matching_result_views import MatchingResultListView, MatchingResultDetailView

app_name = 'app_matching'

urlpatterns = [
    path('', MatchingGroupListView.as_view(), name='list'),
    path('create/', MatchingGroupCreateView.as_view(), name='create'),
    path('<int:group_id>/detail/', MatchingGroupUpdateView.as_view(), name='detail'),
    path('pp/<int:group_id>/p/confirm/', MatchingPreConfirmView.as_view(), name='pre_confirm'),
    path('pp/<int:group_id>/m/hybrid/', MatchingMethodHybridView.as_view(), name='matching_method_hybrid'),
    path('pp/<int:group_id>/m/auto/', MatchingMethodAutoView.as_view(), name='matching_method_auto'),
    path('pp/<int:group_id>/m/manual/', MatchingMethodManualView.as_view(), name='matching_method_manual'),
    path('result/', MatchingResultListView.as_view(), name='result_list'),
    path('result/<int:result_id>/detail/', MatchingResultDetailView.as_view(), name='result_detail'),
]