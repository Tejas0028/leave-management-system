from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LeaveForm
from .models import LeaveRequest


@login_required
def apply_leave(request):

    form = LeaveForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.status = LeaveRequest.Status.PENDING
            leave.save()

            return redirect("my_leaves")

    return render(request, "apply_leave.html", {
        "form": form
    })


@login_required
def my_leaves(request):
    leaves = LeaveRequest.objects.filter(
        employee=request.user
    ).order_by("-id")

    return render(request, "my_leaves.html", {
        "leaves": leaves
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest


@login_required
def manage_leaves(request):
    if request.user.role != 2:
        return redirect("dashboard")

    leaves = LeaveRequest.objects.all().order_by("-id")

    return render(request, "manage_leaves.html", {
        "leaves": leaves
    })


@login_required
def update_leave_status(request, pk):

    if request.user.role != 2:
        return redirect("dashboard")

    leave = get_object_or_404(LeaveRequest, id=pk)

    if request.method == "POST":
        action = request.POST.get("action")
        remarks = request.POST.get("remarks")

        if action == "approve":
            leave.status = LeaveRequest.Status.APPROVED
        elif action == "reject":
            leave.status = LeaveRequest.Status.REJECTED

        leave.manager_remarks = remarks
        leave.save()

    return redirect("manage_leaves")