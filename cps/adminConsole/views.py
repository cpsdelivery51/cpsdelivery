from django.shortcuts import render, redirect
from delivery.models import DeliveryRequest, Rider
from .forms import RiderForm, ShopItemForm, RequestStatusUpdateForm, RidersAssignmentForm
from delivery.models import ShopItem
import requests
# Create your views here.

def adminConsole(request):

    return render(request,'html/adminConsole.html')

def requestManagementConsole(request):
    DeliveryRequests = DeliveryRequest.objects.filter(delivered=False).values()
    print(DeliveryRequests)
    context ={
        'DeliveryRequests':DeliveryRequests,

    }
    return render(request,'html/requestsManagementConsole.html',context)

def pastProcessedRequest(request):
    DeliveryRequests = DeliveryRequest.objects.filter(delivered=True).values()
    context ={
        'DeliveryRequests':DeliveryRequests,

    }
    return render(request,'html/pastProcessedRequest.html',context)
def AssignedRiderMsg(instance,rider):
    endPoint = 'https://api.mnotify.com/api/sms/quick'
    apiKey = '	SncBkQH0xepW3ACOlCty3AjUX'
    data = {
    'recipient[]': [str(instance.pickupNumber)],
    'sender': 'CPS',
    'message': f'Your request for CPS deliveries service with ORDER ID: 00{instance.id} has been assigned to rider {rider.name} .Contact him on 0{rider.phone}',
    'schedule_date': '',
    }
    url = endPoint + '?key=' + apiKey
    response = requests.post(url, data)
    data = response.json() 
    print(data,str(instance.pickupNumber))


def managementUpdate(request,unique_id):
    Riders = Rider.objects.all()
    DeliveryRequested = DeliveryRequest.objects.get(unique_id=unique_id)
    RequestStatusUpdateFormUpdater = RequestStatusUpdateForm(instance=DeliveryRequested)
    RidersAssignmentFormUpdater = RidersAssignmentForm(instance=DeliveryRequested)


    
    if request.method == 'POST':
        if 'UdpateAssignment' in request.POST:
            form = RidersAssignmentForm(request.POST,instance=DeliveryRequested)
            rider = request.POST.get('rider')
            AssignedRider = Rider.objects.get(id=rider)
            
            if form.is_valid():
                form.save()
                AssignedRiderMsg(DeliveryRequested,AssignedRider)
                DeliveryRequested.assigned = True
                DeliveryRequested.save()
                print('Done')
            else:
                print('Error')
            return redirect(managementUpdate,unique_id)
        if 'UpdateRequest' in request.POST:
            form = RequestStatusUpdateForm(request.POST,instance=DeliveryRequested)


            if form.is_valid():
                form.save()
                if DeliveryRequested.pickedUp == True:
                    DeliveryRequested.enroute = True
                    DeliveryRequested.save()
                else:
                    DeliveryRequested.enroute = False
                    DeliveryRequested.save()
                if DeliveryRequested.delivered == True:
                    DeliveryRequested.pickedUp = True
                    DeliveryRequested.enroute = True
                    DeliveryRequested.save()
                    
                
            else:
                print('Error')
            return redirect(managementUpdate,unique_id)


    context = {
        'DeliveryRequested':DeliveryRequested,
        'RequestStatusUpdateFormUpdater':RequestStatusUpdateFormUpdater,
        'Riders':Riders,
        'RidersAssignmentFormUpdater':RidersAssignmentFormUpdater,

    }
    return render(request,'html/managementUpdate.html',context)

def riderAddition(request):
    Riders = Rider.objects.all()
    RiderAdditionFormCreator = RiderForm()
    if request.method == 'POST':
        if 'addRider' in request.POST:
            RiderAdditionFormCreator = RiderForm(request.POST)
            if RiderAdditionFormCreator.is_valid():
                RiderAdditionFormCreator.save()
                return redirect(adminConsole)
    context = {
        'RiderAdditionFormCreator':RiderAdditionFormCreator,
        'Riders':Riders,
    }

    return render(request,'html/riderAddition.html',context)

def riderDelete(request,unique_id):
    rider = Rider.objects.get(unique_id=unique_id)
    rider.delete()
    return redirect(riderAddition)

def riderUpdate(request,unique_id):
    rider = Rider.objects.get(unique_id=unique_id)
    DeliveryRequestsUnassigned = DeliveryRequest.objects.filter(assigned=False).values()
    DeliveryRequestsAssigned = DeliveryRequest.objects.filter(assigned=True,rider=rider).values()
    DeliveryRequestsDelivered = DeliveryRequest.objects.filter(delivered=True,rider=rider).values()
    RiderFormUpdate = RiderForm(instance=rider)

    if request.method == 'POST':
        if 'updateRider' in request.POST:
            RiderFormUpdate = RiderForm(request.POST,instance=rider)
            if RiderFormUpdate.is_valid():
                RiderFormUpdate.save()
                return redirect(riderUpdate,unique_id)
        if 'assignRider' in request.POST:
            unique_id_request = request.POST.get('unique_id')
            DeliveryRequested = DeliveryRequest.objects.get(unique_id=unique_id_request)
            DeliveryRequested.rider = rider
            DeliveryRequested.assigned = True
            DeliveryRequested.save()
            AssignedRiderMsg(DeliveryRequested,rider)
            print(DeliveryRequested.rider)
            return redirect(riderUpdate,unique_id)
        if 'unassignRider' in request.POST:
            unique_id_request = request.POST.get('unique_id')
            DeliveryRequested = DeliveryRequest.objects.get(unique_id=unique_id_request)
            DeliveryRequested.rider = None
            DeliveryRequested.assigned = False
            DeliveryRequested.save()
            return redirect(riderUpdate,unique_id)



    context={
        'rider':rider,
        'RiderFormUpdate':RiderFormUpdate,
        'DeliveryRequestsUnassigned':DeliveryRequestsUnassigned,
        'DeliveryRequestsAssigned':DeliveryRequestsAssigned,
        'DeliveryRequestsDelivered':DeliveryRequestsDelivered,
    }

    return render(request,'html/riderUpdate.html',context)

def addShopItem(request):
    ShopItemFormCreator = ShopItemForm()
    ShopItems  = ShopItem.objects.all()
    if request.method == 'POST': 
        if 'addShopItem'  in request.POST:
            form = ShopItemForm(request.POST, request.FILES)  
            if form.is_valid():  
                form.save()
                return redirect(addShopItem)
            else:
                print('Error')
        
    context={
        'ShopItemFormCreator':ShopItemFormCreator,
        'ShopItems':ShopItems,
    }
    return render(request,'html/addShopItem.html',context)