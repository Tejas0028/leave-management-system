from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import LeaveCreateSerializer,LeaveListSerializer, ManagerLeaveSerializer
from leaves.models import LeaveRequest
from accounts.models import User


class ApplyLeaveApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = LeaveCreateSerializer(data=request.data)

        if serializers.is_valid():
            leave = LeaveRequest.objects.create(
                employee = request.user,
                status = LeaveRequest.Status.PENDING,
                **serializers.validated_data
            )

            return Response({
                "message" : "Leave applied successfully",
                "id" : leave.id
            },status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

class MyLeaveAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaves = LeaveRequest.objects.filter(employee=request.user).order_by("-created_at")
        serializer = LeaveListSerializer(leaves, many=True)
        return Response(serializer.data)
    

class PendingLeavesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Roles.MANAGER:
            return Response({"error" : "Only manager allowed"},status=status.HTTP_403_FORBIDDEN)
        
        leaves = LeaveRequest.objects.filter(status=LeaveRequest.Status.PENDING).order_by("-created_at")
        serializer = ManagerLeaveSerializer(leaves,many=True)
        return Response(serializer.data)
    

class LeaveActionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != User.Roles.MANAGER:
            return Response({"error" : "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        action = request.data.get("action")
        remarks = request.data.get("remarks" , " ")

        try:
            leave = LeaveRequest.objects.get(id=pk)
        except LeaveRequest.DoesNotExist:
            return Response({"error" : "Leave not found"},status=status.HTTP_404_NOT_FOUND)
        
        if leave.status != LeaveRequest.Status.PENDING:
            return Response({"error" : "Already processed"},status=status.HTTP_404_NOT_FOUND)
        
        if action == "approve":
            leave.status = LeaveRequest.Status.APPROVED

        elif action == "reject":
            leave.status = LeaveRequest.Status.REJECTED

        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        
        leave.manager = request.user
        leave.manager_remarks = remarks
        leave.save()

        return Response({"message" : f"Leave {action}d successfully"})