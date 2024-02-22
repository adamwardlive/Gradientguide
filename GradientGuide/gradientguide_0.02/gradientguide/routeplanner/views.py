from django.shortcuts import render, redirect
from .forms import TrainingSessionForm
from .utils import calculate_distance
from .models import TrainingSession


def session_input(request):
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            distance = calculate_distance(session.power, session.duration)
            # Here you would integrate with a mapping API to find suitable routes
            # For now, just redirect to a new page with the calculated distance
            return redirect('session_detail', session_id=session.id)
    else:
        form = TrainingSessionForm()
    return render(request, 'routeplanner/session_input.html', {'form': form})

def session_detail(request, session_id):
    session = TrainingSession.objects.get(id=session_id)
    distance = calculate_distance(session.power, session.duration)
    return render(request, 'routeplanner/session_detail.html', {'session': session, 'distance': distance})
