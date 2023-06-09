
from django.urls import path

from . import views
from .views import (
    faculty,
    utils,
    cafedra,
    directions,
    groups,
    plan,
)

urlpatterns = [
    path('', views.base, name='base'),
    path('auth/login', views.login_view, name='login'),

    # yordamchi funksiyalar
    path('utils/check_username', utils.check_username, name='d_check_username'),
    path('utils/get_sciense_list/<int:direction_id>/<int:semestr_id>', view=plan.get_sciense_list, name='d_get_sciense_list'),

    # Fakultetlar
    path('faculty/all', faculty.faculty_all, name='d_faculty_all'),
    path('faculty/detail/<int:pk>', faculty.faculty_detail, name='d_faculty_detail'),
    path('faculty/change/<int:pk>', faculty.change_faculty, name='d_change_faculty'),
    path('faculty/delete/<int:pk>', faculty.delete_faculty, name='d_delete_faculty'),
    path('faculty/change-manager/<int:pk>', faculty.change_manager, name='d_change_manager'),
    path('faculty/add', faculty.add_faculty, name='d_add_faculty'),


    # Kafedralar
    path('cafedra/all', cafedra.all_cafedra, name='d_all_cafedra'),
    path('cafedra/detail/<int:pk>', cafedra.detail_cafedra, name='d_detail_cafedra'),
    path('cafedra/add', cafedra.add_cafedra, name='d_add_cafedra'),
    path('cafedra/change-name/<int:pk>', cafedra.change_name_cafedra, name='d_change_name_cafedra'),
    path('cafedra/delete/<int:pk>', cafedra.delete_cafedra, name='d_delete_cafedra'),
    path('cafedra/change-manager/<int:pk>', cafedra.change_manager_cafedra, name='d_change_manager_cafedra'),
    path('cafedra/change-faculty/<int:pk>', cafedra.change_faculty_cafedra, name='d_change_faculty_cafedra'),

    # directions
    path('direction/all', directions.all_direction, name='d_all_direction'),
    path('direction/detail/<int:pk>', directions.detail_direction, name='d_detail_direction'),
    path('direction/add', directions.add_direction, name='d_add_direction'),
    path('direction/delete/<int:pk>', directions.delete_direction, name='d_delete_direction'),
    path('direction/change/<int:pk>', directions.change_direction, name='d_change_direction'),
    path('direction/add-group/<int:pk>', directions.add_group_for_direction, name='d_add_group_for_direction'),

    # groups
    path('groups/all', groups.groups_all, name='d_groups_all'),
    path('groups/detail/<int:pk>', groups.detail_group, name='d_detail_group'),
    path('groups/delete/<int:pk>', groups.delete_group, name='d_delete_group'),
    path('groups/change/<int:pk>', groups.change_group, name='d_change_group'),
    
    # plan
    path('plan/init/<int:direction_id>/semestr/<int:semestr_id>', plan.plan_init, name='d_plan_init'),
    path('plan/save/<int:direction_id>/semestr/<int:semestr_id>', plan.save_plan, name='d_save_plan'),
    path('plan/delete/<int:pk>', plan.delete_plan_row, name='d_delete_plan_row'),
    path('plan/change/<int:direction_id>/semestr/<int:semestr_id>/<int:pk>', plan.save_plan, name='d_change_plan'),
]   
