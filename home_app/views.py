from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import HttpResponse, redirect, render , get_object_or_404,HttpResponseRedirect
from django.contrib import messages
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
ar_num = '۰١٢٣٤٥٦٧٨٩'
en_num = '0123456789'
table = str.maketrans(en_num, ar_num)
# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    value_of_username = request.POST['username']
                    return render(request, 'pages/login.html', {'value' : value_of_username})
            else:
                messages.error(request, 'اسم المستخدم او كلمة المرور غير صحيحة.')
                return redirect('login')
        else:
            messages.error(request, 'قم بأدخال البيانات')
            return redirect('login')
    return render(request, 'pages/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'تم تسجيل خروجك')
    return redirect('login')

@login_required(login_url=('/login/'))
def index(request):
    today = datetime.date.today()
    patients = Patient.objects.all()
    bills = Bill.objects.all()
    appointments = Appointment.objects.all()
    currentMonth = f"{today.year}-{today.month}-1"
    nextMonth = (today.replace(day=27) + datetime.timedelta(days=6)).replace(day=1)
    previousMonth = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    currentMonthPatients = Patient.objects.filter(created_at__lt=nextMonth, created_at__gte=currentMonth)
    previousMonthPatients = Patient.objects.filter(created_at__lt=currentMonth, created_at__gte=previousMonth)
    bills_today = Bill.objects.filter(date=today)
    bills_month = Bill.objects.filter(date__lt=nextMonth, date__gte=currentMonth)
    bills_previousMonth = Bill.objects.filter(date__lt=currentMonth, date__gte=previousMonth)
    billsToday_cost = 0
    bills_cost = 0
    billsMonth_cost = 0
    billsPreviousMonth_cost = 0
    for bill in bills_previousMonth:
        billsPreviousMonth_cost+= bill.amount
    for bill in bills_month:
        billsMonth_cost+= bill.amount
    billsMonthInArabic = f"{billsMonth_cost}".translate(table)
    for bill in bills_today:
        billsToday_cost += bill.amount
    billsTodayCostInArabic = f"{billsToday_cost}".translate(table)
    for bill in bills:
        bills_cost += bill.amount
    billsCostInArabic = f"{bills_cost}".translate(table)
    appointmentsToday = Appointment.objects.filter(date=today)
    appointmentsDone = Appointment.objects.filter(date=today, status='تم')
    appointmentsUnDone = Appointment.objects.filter(date = today, status='لم يتم')
    if previousMonthPatients.count() != 0:
        patientsPercentage = "%.1f" % (((currentMonthPatients.count() - previousMonthPatients.count())/previousMonthPatients.count())*100)
        patientsPercentage = str(patientsPercentage).replace('.0', '')
    else:
        patientsPercentage = 0
    if billsPreviousMonth_cost != 0:
        billsPercentage = "%.1f" % (((billsMonth_cost - billsPreviousMonth_cost)/billsPreviousMonth_cost)*100)
        billsPercentage = str(billsPercentage).replace('.0', '')
    else:
        billsPercentage = 0
    context = {
        'patients_count' : str(patients.count()).translate(table),
        'appointments_count' : str(appointments.count()).translate(table),
        'billsToday_cost' : billsTodayCostInArabic,
        'billsMonth_cost' : billsMonthInArabic,
        'bills_cost' : billsCostInArabic,
        'appointmentsToday' : str(appointmentsToday.count()).translate(table),
        'appointmentsDone' : str(appointmentsDone.count()).translate(table),
        'appointmentsUnDone' : str(appointmentsUnDone.count()).translate(table),
        'currentMonthPatients' : str(currentMonthPatients.count()).translate(table),
        'patientsPercentage' : str(patientsPercentage).translate(table),
        'billsPercentage' : str(billsPercentage).translate(table),
    }
    
    return render(request , 'pages/index.html', context)


def indexDate(request):
        date = request.GET['date']
        
        patients = Patient.objects.filter(created_at=date)
        appointmentsTotal = Appointment.objects.filter(date = date)
        appointmentsDone = Appointment.objects.filter(date = date, status='تم')
        appointmentsUnDone = Appointment.objects.filter(date = date, status='لم يتم')
        bills = Bill.objects.filter(date=date)
        billsAmount = 0
        for bill in bills:
            billsAmount += bill.amount
            
        
        context = {
            'date' : date,
            'bills' : str(bills.count()).translate(table),
            'billsAmount' : str(billsAmount).translate(table),
            'patients' : str(patients.count()).translate(table),
            'appointmentsTotal' : str(appointmentsTotal.count()).translate(table),
            'appointmentsDone' : str(appointmentsDone.count()).translate(table),
            'appointmentsUnDone' : str(appointmentsUnDone.count()).translate(table),
            
        }
        return render(request, 'pages/indexDate.html', context)


@login_required(login_url=('/home_app/login'))
def patients(request):
    patients = Patient.objects.all().order_by('name')
    p = Paginator(patients, 10)
    page = request.GET.get('page', 1)
    p_list = p.get_page(page)
    context = {
        'patients' : patients,
        'p_list' : p_list
    }
    return render(request , 'pages/patients.html',context)

@login_required(login_url=('/home_app/login'))
def patient_details(request, pk):
    patient = Patient.objects.get(id=pk)
    context = {
        'patient' : patient
    }
    return render(request , 'pages/patient.html', context)

@login_required(login_url=('/home_app/login'))
def edit_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    context = {
        'patient' : patient
    }
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient.name = form.cleaned_data['name']
            patient.email = form.cleaned_data['email']
            patient.address = form.cleaned_data['address']
            patient.phone = form.cleaned_data['phone']
            patient.sex = form.cleaned_data['sex']
            patient.bloodgroup = form.cleaned_data['bloodgroup']
            patient.notes = form.cleaned_data['notes']
            patient.age = form.cleaned_data['age']
            patient.save()
            messages.success(request, 'تم التعديل')
            return redirect('patients')
        else:
            messages.error(request, 'فشل التعديل')
            return HttpResponseRedirect(f'{pk}')
    return render(request , 'pages/edit_patient.html', context)

@login_required(login_url=('/home_app/login'))
def add_patient(request):
    patients = Patient.objects.all()
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            for patient in patients:
                if patient.name == name:
                    messages.error(request, 'هذا المريض موجود بالفعل')
                    return redirect('/patients/')
                else:
                    pass
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            sex = form.cleaned_data['sex']
            notes = form.cleaned_data['notes']
            bloodgroup = form.cleaned_data['bloodgroup']
            patient = Patient.objects.create(name=name, age=age, email=email, phone=phone, address=address, sex=sex, notes=notes, bloodgroup=bloodgroup)
            patient.save()
            messages.success(request, 'تم اضافة المريض بنجاح')
            return redirect('/patients/')
        else:
            print(form)
            messages.error(request,'حدث خطأ ولم يتم حفظ البيانات')
            return redirect('add_patient')
    return render(request , 'pages/add_patient.html')

@login_required(login_url=('/home_app/login'))
def reservations(request):
    appointments = Appointment.objects.all().order_by('date')
    p = Paginator(appointments, 10)
    page = request.GET.get('page', 1)
    p_list = p.get_page(page)
    context = {
        'appoins' : appointments,
        'p_list': p_list
    }
    return render(request , 'pages/reservations.html',context)

@login_required(login_url=('/home_app/login'))
def reserv_details(request, pk):
    reserv = Appointment.objects.get(id=pk)
    context = {
        'reserv' : reserv
    }
    return render(request , 'pages/resProfile.html', context)

@login_required(login_url=('/home_app/login'))
def add_reservation(request):

    
    patients = Patient.objects.all().order_by('name')
    context = {
        'patients' : patients,
    }

    if request.method == 'POST' :
        form = ResrevForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            notes = form.cleaned_data['notes']

            appointment = Appointment.objects.create(patient=patient,date=date,time=time,notes=notes)
            appointment.save()
            messages.success(request,"تم اضافة الحجز بنجاح")
            return redirect('/reservations/')
        else:
            print(form)
            messages.error(request,"حدث خطأ ولم يتم حفظ البيانات")
            return redirect('/add_reservation/')

    return render(request , 'pages/add_reservation.html',context)

@login_required(login_url=('/home_app/login'))
def edit_reserv(request, pk):
    reserv = Appointment.objects.get(id=pk)
    context = {
        'reserv' : reserv
    }
    if request.method == 'POST':
        form = ResrevForm(request.POST)
        if form.is_valid():
            reserv.date = form.cleaned_data['date']
            reserv.time = form.cleaned_data['time']
            reserv.notes = form.cleaned_data['notes']
            
            reserv.save()
            messages.success(request, 'تم التعديل')
            return redirect('/reservations/')
        else:
            messages.error(request, 'فشل التعديل')
            return HttpResponseRedirect(f'{pk}')
    return render(request , 'pages/edit_reserv.html', context)

@login_required(login_url=('/home_app/login'))
def records(request):
    records = Bill.objects.all().order_by('date')
    p = Paginator(records, 10)
    page = request.GET.get('page', 1)
    p_list = p.get_page(page)
    context = {
        'records' : records,
        'p_list' : p_list
    }

    return render(request , 'pages/records.html',context)


@login_required(login_url=('/home_app/login'))
def record_details(request, pk):
    record = Bill.objects.get(id = pk)
    context = {
        'record' : record
    }
    return render(request , 'pages/recordProfile.html', context)

@login_required(login_url=('/home_app/login'))
def edit_record(request, pk):
    record = Bill.objects.get(id = pk)
    appointments = Appointment.objects.all().order_by('id').exclude(id = record.appointment.id)
    context = {
        'record' : record,
        'appointments' : appointments
    }
    if request.method == 'POST':
        form = BillForm(request.POST)
        print(form)
        if form.is_valid():
            appointment = form.cleaned_data['appointment']
            amount = form.cleaned_data['amount']
            notes = form.cleaned_data['notes']
            record.appointment = appointment
            record.amount = amount
            record.notes = notes
            record.save()
            messages.success(request, 'تم التعديل')
            return redirect('/records/')
        else:
            messages.error(request, 'فشل التعديل')
            return HttpResponseRedirect(f'{pk}')
    return render(request , 'pages/edit_record.html', context)

@login_required(login_url=('/home_app/login'))
def add_record(request):

    appointments = Appointment.objects.all().order_by('id')
    context = {
        'appointments' : appointments,
    }

    if request.method == 'POST' :
        form = BillForm(request.POST)
        if form.is_valid():
            appointment = form.cleaned_data['appointment']
            amount = form.cleaned_data['amount']
            notes = form.cleaned_data['notes']

            bill= Bill.objects.create(appointment=appointment,amount=amount,notes=notes)
            # bill2 = Bill.objects.get(appointment=appointment)
            app = bill.appointment
            app.status = 'تم'
            bill.save()
            app.save()



            messages.success(request,"تم اضافة السجل بنجاح")
            return redirect('/records/')
        else:
            
            messages.warning(request,"حدث خطأ ولم يتم حفظ البيانات")
            return redirect('/add_record/')

    return render(request , 'pages/add_record.html',context)

@login_required(login_url=('/home_app/login'))
def deletePatient(request,id) :
    patient_clear = get_object_or_404(Patient, id=id)
    patient_clear.delete()
    return redirect('/patients/')

@login_required(login_url=('/home_app/login'))
def deleteReserv(request ,id) :
    reserv_clear = get_object_or_404(Appointment, id=id)
    reserv_clear.delete()
    return redirect('/reservations/')

@login_required(login_url=('/home_app/login'))
def deleteRecord(request ,id) :
    record_clear = get_object_or_404(Bill, id=id)
    record_clear.delete()
    return redirect('/records/')

def searchPatients(request):
    if request.method == 'GET':
        patientsName = request.GET['patientName']
        patients = Patient.objects.filter(name__icontains=patientsName)
        p = Paginator(patients, 10)
        page = request.GET.get('page', 1)
        p_list = p.get_page(page)
        context = {
            'patients' : patients,
            'p_list' : p_list,
            'patientsName' : patientsName
        }
        return render(request, 'pages/searchPatients.html', context)
    
def searchReservations(request):
    if request.method == 'GET':
        reservationsName = request.GET['reservationsName']
        reservations = Appointment.objects.filter(name__icontains=reservationsName)
        p = Paginator(reservations, 10)
        page = request.GET.get('page', 1)
        p_list = p.get_page(page)
        context = {
            'appoins' : reservations,
            'p_list' : p_list,
            'reservationsName' : reservationsName
        }
        return render(request, 'pages/searchReservations.html', context)

def searchRecords(request):
    if request.method == 'GET':
        recordsName = request.GET['recordsName']
        records = Bill.objects.filter(name__icontains=recordsName)
        p = Paginator(records, 10)
        page = request.GET.get('page', 1)
        p_list = p.get_page(page)
        context = {
            'records' : records,
            'p_list' : p_list,
            'recordsName' : recordsName
        }
        return render(request, 'pages/searchRecords.html', context)



def page_not_found(request, exception):
    return render(request, 'pages/404.html')