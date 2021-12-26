from django.core.exceptions import AppRegistryNotReady
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from . models import Employee
from . serializers import EmployeeSerializers
from rest_framework.response import Response
from django.http import HttpResponse


# Create your views here.
class TestAPIView(APIView):
    def get(self, request, pk = None, *args, **kwargs):

        if pk is not None:
            try:
                emp = Employee.objects.get(id = pk)
                serializer = EmployeeSerializers(emp)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return HttpResponse("Employee Not Exist")


        qs = Employee.objects.all()

        serializer = EmployeeSerializers(qs, many = True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pydict = request.data
        print(pydict, type(pydict))

        serializer = EmployeeSerializers(data=pydict)
        if serializer.is_valid():
            serializer.save()
            msg = {'msg': 'Data Added Successfully'}
            return Response(msg)
        
        return Response(serializer.errors)

    def put(self, request, pk, *args, **kwargs):
        pydict = request.data
        # id = self.kwargs.get('pk')

        print(pk, "-----------------", type(pk))
        print('id is ------------------------------>',id)
        emp = Employee.objects.get(id=pk)

        serializer = EmployeeSerializers(emp, data=pydict)
        if serializer.is_valid():
            serializer.save()
            msg = {'msg': 'Complete Data Updated Successfully'}
            return Response(msg)

        return Response(serializer.errors)

    def patch(self, request, pk):
        pydata  = request.data

        print(pk)
        emp = Employee.objects.get(id=pk)

        serializer = EmployeeSerializers(emp, data=pydata, partial = True)
        if serializer.is_valid():
            serializer.save()
            msg = {'msg':'Partial data Updated Successfully'}
            return Response(msg)
        return Response(serializer.errors)

    def delete(self, request, pk):

        print(pk)

        try:
            emp = Employee.objects.get(id = pk)
            emp.delete()
            msg = {'msg':"Employee Deleted Successfully"}
            return Response(msg)
        except Employee.DoesNotExist:
            return HttpResponse("Employee Does Not Exist")        







