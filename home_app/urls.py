from django.urls import path

from . import views

urlpatterns = [
    path('' , views.index ,name = 'index' ),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('patients/' , views.patients, name = 'patients' ),
    path('reservations/' , views.reservations, name = 'reservations'),
    path('records/' , views.records, name = 'records' ),
    path('add_patient/' , views.add_patient, name = 'add_patient'),
    path('add_reservation/' , views.add_reservation, name = 'add_reservation'),
    path('add_record/' , views.add_record, name = 'add_record'),
    path('delete_patient/<int:id>' , views.deletePatient, name = 'deletePatient'),
    path('delete_reserv/<int:id>' , views.deleteReserv, name = 'deleteReserv'),
    path('delete_record/<int:id>' , views.deleteRecord, name = 'deleteRecord'),
    
    path('patients/edit_patient/<int:pk>' , views.edit_patient, name = 'edit_patient'),
    path('patient/<int:pk>' , views.patient_details, name = 'patient_details'),

    path('reserv/edit_reserv/<int:pk>' , views.edit_reserv, name = 'edit_reserv'),
    path('reserv/<int:pk>' , views.reserv_details, name = 'reserv_details'),

    path('record/edit_record/<int:pk>' , views.edit_record, name = 'edit_record'),
    path('record/<int:pk>' , views.record_details, name = 'record_details'),
    
    path('searchPatients/', views.searchPatients, name = 'searchPatients'),
    path('searchReservations/', views.searchReservations, name = 'searchReservations'),
    path('searchRecords/', views.searchRecords, name = 'searchRecords'),
]