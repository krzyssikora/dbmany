from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import Person, Group
from .owner import OwnerListView, OwnerDetailView,  OwnerDeleteView
from .forms import CreatePersonForm, CreateGroupForm


def index(request):
    person_list = Person.objects.order_by('name')
    group_list = Group.objects.order_by('name')
    context = {
        'person_list': person_list,
        'group_list': group_list,
    }
    return render(request, 'dbmany/index.html', context)


# def person(request, person_id):
#     prsn = get_object_or_404(Person, pk=person_id)
#     return render(request, 'dbmany/person_detail.html', {'person': prsn})


# def group(request, group_id):
#     grp = get_object_or_404(Group, pk=group_id)
#     return render(request, 'dbmany/group_detail.html', {'group': grp})


class PersonListView(OwnerListView):
    model = Person
    # By convention:
    # template_name = "dbmany/person_list.html"


class GroupListView(OwnerListView):
    model = Group


class PersonDetailView(OwnerDetailView):
    model = Person


class GroupDetailView(OwnerDetailView):
    model = Group


# class PersonCreateView(OwnerCreateView):
#     model = Person
#     # List the fields to copy from the Person model to the Person form
#     fields = ['name', 'nationality']

class PersonCreateView(LoginRequiredMixin, View):
    template_name = 'dbmany/person_form.html'
    success_url = reverse_lazy('dbmany:all')

    def get(self, request, pk=None):
        form = CreatePersonForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreatePersonForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        person = form.save(commit=False)
        person.owner = self.request.user
        person.save()
        form.save_m2m()
        return redirect(self.success_url)


class GroupCreateView(LoginRequiredMixin, View):
    template_name = 'dbmany/group_form.html'
    success_url = reverse_lazy('dbmany:all')

    def get(self, request, pk=None):
        form = CreateGroupForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateGroupForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        group = form.save(commit=False)
        group.owner = self.request.user
        group.save()
        return redirect(self.success_url)


class PersonUpdateView(LoginRequiredMixin, View):
    template_name = 'dbmany/person_form.html'
    success_url = reverse_lazy('dbmany:all')

    def get(self, request, pk):
        person = get_object_or_404(Person, id=pk, owner=self.request.user)
        form = CreatePersonForm(instance=person)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        person = get_object_or_404(Person, id=pk, owner=self.request.user)
        form = CreatePersonForm(request.POST, request.FILES or None, instance=person)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        person = form.save(commit=False)
        person.save()
        form.save_m2m()

        return redirect(self.success_url)


class PersonDeleteView(OwnerDeleteView):
    model = Person


def stream_file(request, pk):
    person = get_object_or_404(Person, id=pk)
    response = HttpResponse()
    response['Content-Type'] = person.content_type
    response['Content-Length'] = len(person.picture)
    response.write(person.picture)
    return response
