from django.urls import path

from .views import CellViewSet, SheetList

urlpatterns = [
    path(
        "v1/<str:sheet_id>/<str:cell_id>/",
        CellViewSet.as_view({"get": "retrieve", "post": "update", "delete": "delete"}),
        name="cell-detail",
    ),
    path("v1/<str:sheet_id>/", SheetList.as_view({"get": "get", "delete": "delete"}), name="sheet-list"),
]
