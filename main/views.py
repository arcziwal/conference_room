from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Room


class HomePage(View):
    def get(self, request):
        return render(request, 'SITE_TEMPLATE.html')


class AddNewRoom(View):
    def get(self, request):
        cnx = {'return_address': "new/"}
        return render(request, 'new_room_form.html', cnx)

    def post(self, request):
        name = request.POST['name']
        seats = request.POST['seats']
        is_projector = request.POST.get('projector')
        if is_projector == 'on':
            projector = True
        else:
            projector = False
        cnx = self.validation(name, seats)
        if cnx:
            cnx['type_of_operation'] = "add"
            return render(request, 'error_messages.html', cnx)
        else:
            Room.objects.create(name=name, seats=seats, is_projector=projector)
            return render(request, 'SITE_TEMPLATE.html', {'name': name, 'seats': seats})

    @classmethod
    def validation(cls, name, seats):
        cnx = {}
        if not name:
            is_name_filled = False
            cnx['is_name_filled'] = is_name_filled
        elif not seats:
            is_seats_filled = False
            cnx['is_seats_filled'] = is_seats_filled
        else:
            room = Room.objects.filter(name=name)
            if len(room) != 0:
                is_in_db = True
                cnx['is_in_db'] = is_in_db
            else:
                try:
                    if int(seats) < 1:
                        is_num_ok = False
                        cnx['is_num_ok'] = is_num_ok
                except ValueError:
                    is_number = False
                    cnx['is_number'] = is_number
        return cnx


class ShowRooms(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'room_table.html', {'rooms': rooms})


class DeleteRoom(View):
    def get(self, request, **kwargs):
        room_to_del = self.kwargs['room_to_del']
        room_name = Room.objects.get(pk=room_to_del)
        output = f"Czy na pewno chcesz usunąć pokój: {room_name.name}"
        return render(request, 'delete_confirmation.html', {'output': output, 'room': room_to_del})

    def post(self, request, **kwargs):
        decision = request.POST['decision']
        if decision == "tak":
            room_to_del = self.kwargs['room_to_del']
            room = Room.objects.get(pk=room_to_del)
            room.delete()
            return redirect('/rooms')
        elif decision == "nie":
            return redirect('/rooms')


class ModifyRoom(View):
    def get(self, request, **kwargs):
        room_to_mod_id = self.kwargs['room_to_mod']
        room = Room.objects.get(pk=room_to_mod_id)
        text = "Zmień dane w poniższych polach i naciśnij 'prześlij aby zmodyfikować salę"
        cnx = {'modification_text': text, 'room': room, 'return_address': "modify/"}
        return render(request, 'new_room_form.html', cnx)

    def post(self, request, **kwargs):
        room_to_mod_id = self.kwargs['room_to_mod']
        name = request.POST['name']
        seats = request.POST['seats']
        is_projector = request.POST.get('projector')
        room = Room.objects.get(pk=room_to_mod_id)
        if is_projector == 'on':
            projector = True
        else:
            projector = False
        cnx = AddNewRoom.validation(name, seats)
        if 'is_in_db' in cnx:
            if name == room.name:
                del cnx['is_in_db']
        if cnx:
            cnx['return_address'] = "edit"
            cnx['room'] = room.pk
            return render(request, "error_messages.html", cnx)
        else:
            room.name = name
            room.seats = seats
            room.is_projector = projector
            room.save()
            return redirect("/rooms")

