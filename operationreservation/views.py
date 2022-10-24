from django.http import Http404
from rest_framework import status
from .models import Department, Operation, OpRoom
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import OperationSerializer, DepartmentSerializer, OpRoomSerializer
from .Solver import Solver


# Create your views here.


class OperationsList(APIView):

    def get(self, request):
        operations = Operation.objects.all().order_by('-id')
        get_serializer = OperationSerializer(operations, many=True)
        return Response(get_serializer.data)

    def post(self, request, format=None):
        serializer = OperationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            date = serializer.data['date']
            get_solution(date, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentsList(APIView):

    def get(self, request):
        departments = Department.objects.all()
        get_serializer = DepartmentSerializer(departments, many=True)
        return Response(get_serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpRoomsList(APIView):

    def get(self, request):
        op_rooms = OpRoom.objects.all()
        get_serializer = OpRoomSerializer(op_rooms, many=True)
        return Response(get_serializer.data)

    def post(self, request, format=None):
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationDetial(APIView):

    def get_object(self, pk):
        try:
            return Operation.objects.get(pk=pk)
        except Operation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        operation = self.get_object(pk)
        get_serializer = OperationSerializer(operation)
        return Response(get_serializer.data)

    def delete(self, request, pk):
        operation = self.get_object(pk)
        operation.delete()
        return Response('Operation was deleted!')


class SolverView:
    # departments_info =
    pass


def get_solution(date, data):

    operation_rooms_info = OpRoom.objects.filter(date=date)
    #departments = Department.objects.filter(date=date)
    operations = Operation.objects.filter(date=date)
    solver = Solver()
    added_operations = solver.get_solution(operation_rooms_info, operations)
    if len(added_operations)<1:
        deleted_op = Operation.objects.filter(pk=data['id'])
        try:
            deleted_op.delete()
        except:
            return "There operation couldn't be deleted"
        return Response('Operation was deleted!')
    else:
        Operation.objects.all().delete()
        operations_records = added_operations.to_dict('records')
        model_instances = [Operation(
            doctor_name=record['doctor_name'],
            patient_id=record['patient_id'],
            date=record['date'],
            duration=record['duration'],
            emergency=record['emergency'],
            department_id=record['department_id'],
            room_id=record['room_id'],
        ) for record in operations_records]

        Operation.objects.bulk_create(model_instances)






    """
class ALbumUpdate(UpdateView):
    model = Operation
    fields = ['artist', 'album_title','gener', 'album_logo']


class ALbumDelete(DeleteView):
    model = Operation
    success_url = reverse_lazy('music:index.html')
    
    
    class IndexView(ListView):
    template_name = 'operationreservation/index.html'
    context_object_name = 'operations_list'

    def get_queryset(self):
        return Operation.objects.all()


class DetailView(DetailView):
    model = Operation
    template_name = 'operationreservation/details.html'

class OperationCreate(CreateView):
    model = Operation
    fields = ["date","doctor_name","patient_id", "duration"]
    success_url = "operationreservation:index"
    template_name = "operationreservation/add.html"

"""
