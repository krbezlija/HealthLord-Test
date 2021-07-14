from django.shortcuts import render, redirect
from .models import Delavec, Trgovina
from django.contrib import messages
# Create your views here.

def delavci(request):
	if request.method == "POST" and 'delete' in request.POST:
		itemID = int(request.POST['delete'])
		Delavec.objects.get(id=itemID).delete()
	data = Delavec.objects.all()
	return render(request, 'app/delavci.html', {"data": data})

def trgovine(request):
	if request.method == "POST" and 'delete' in request.POST:
		itemID = int(request.POST['delete'])
		trg = Trgovina.objects.get(id=itemID)
		trg.delete()
		trg.save
	data = Trgovina.objects.all()
	return render(request, 'app/trgovine.html', {"data": data})

def iskanjePoDel(request):
	dataT = Trgovina.objects.all()
	dataD = Delavec.objects.all()
	if 'izberiDelavca' in request.GET and request.GET['izberiDelavca'] not in ['none', '']:
		ime, priimek = request.GET['izberiDelavca'].split(" ")
		idd = Delavec.objects.filter(Ime=ime).filter(Priimek=priimek)
		data = Delavec.objects.get(id=idd[0].id).trgovina.all()
		return render(request, 'app/poDelavc.html', {"dataT": dataT, "dataD": dataD, "data": data, "ime": ime+" "+priimek})
	return render(request, 'app/poDelavc.html', {"dataT": dataT, "dataD": dataD, "ime": None})

def iskanjePoTrg(request):
	dataT = Trgovina.objects.all()
	dataD = Delavec.objects.all()
	if 'izberiTrgovine' in request.GET and request.GET['izberiTrgovine'] not in ['none', '']:
		imeTrgovine= request.GET['izberiTrgovine']
		data = Delavec.objects.filter(trgovina__Ime=imeTrgovine)
		return render(request, 'app/poTrgovin.html', {"dataT": dataT, "dataD": dataD, "data": data, "ime": imeTrgovine})
	return render(request, 'app/poTrgovin.html', {"dataT": dataT, "dataD": dataD, "ime": None})

def noviDelavec(request):
	data = Trgovina.objects.all()
	if request.method == "POST":
		d = request.POST
		if len(Delavec.objects.filter(Ime=d['Ime'],Priimek=d['Priimek'])) == 0:
			novi = Delavec(Ime=d['Ime'],Priimek=d['Priimek'], DatumRojstva=d['RojstniDan'], Spol=d['Spol'])
			novi.save()
			novi.trgovina.add(Trgovina.objects.get(Ime=d['trg']))
			messages.info(request, 'Delavec vspesno dodan')
		else:
			messages.error(request, 'Delavec ze obstaja')
	return render(request, 'app/noviDelavec.html', {"data": data})

def novaTrgovina(request):
	if request.method == "POST":
		imeTrgovine = request.POST['imeT']
		if len(Trgovina.objects.filter(Ime=imeTrgovine)) == 0:
			Trgovina.objects.create(Ime=imeTrgovine)
			messages.success(request, f'Trgovina {imeTrgovine} je bila uspešno dodana')
		else:
			messages.info(request, 'Trgovina ze obstaja')
	return render(request, 'app/novaTrgovina.html', {})


def spremeniD(request):
	if "save" in request.POST:
		d = request.POST
		x = d['RojstniDan']
		itemID = int(d['save'])
		dela = Delavec.objects.get(id=itemID)
		trg = d['trg']
		if len(Delavec.objects.filter(Ime=d['Ime'], Priimek=d['Priimek'], DatumRojstva=x, Spol=d['Spol'])) <= 0 or (len(dela.trgovina.all())>0 and dela.trgovina.all()[0]!=trg) or (len(dela.trgovina.all())==0 and len(trg)>0):
			dela.Ime = d['Ime']
			dela.Priimek = d['Priimek']
			dela.DatumRojstva = x
			dela.Spol = d['Spol']
			dela.trgovina.add(Trgovina.objects.get(Ime=trg))
			dela.save()
			return redirect("/")
		else:
			d = Delavec.objects.get(id=itemID)
			data = Trgovina.objects.all()
			trg = d.trgovina.all()
			if len(trg) != 0:
				x = d.DatumRojstva.strftime("%Y-%m-%d")
				return render(request, 'app/spremeniD.html', {"d" : d, "data": data, "trg": trg[-1].Ime, "x": x })
			return render(request, 'app/spremeniD.html', {"d" : d, "data": data, "trg": "", "x": x })

	else:
		itemID = int(request.POST['spremeni'])
		d = Delavec.objects.get(id=itemID)
		data = Trgovina.objects.all()
		trg = d.trgovina.all()
		x = d.DatumRojstva.strftime("%Y-%m-%d")
		if len(trg) != 0:
			return render(request, 'app/spremeniD.html', {"d" : d, "data": data, "trg": trg[0].Ime, "x": x })
		else:
			return render(request, 'app/spremeniD.html', {"d": d, "data": data, "trg": "", "x": x})
	return render(request, 'app/spremeniD.html', {"d" : d, "data": data, "trg": ""})

def spremeniT(request):
	if "save" in request.POST:
		d = request.POST
		itemID = int(d['save'])
		dela = Trgovina.objects.get(id=itemID)
		if len(Trgovina.objects.filter(Ime=d['imeT'])) <= 0:
			dela.Ime = d['imeT']
			dela.save()
			messages.success(request, f'Trgovina {dela.Ime} je bila uspešno dodana')
			return redirect("/trgovine/")
		else:
			d = Trgovina.objects.get(id=itemID)
			messages.error(request, 'Trgovina ze obstaja')
	else:
		itemID = int(request.POST['spremeni'])
		d = Trgovina.objects.get(id=itemID)
	return render(request, 'app/spremeniT.html', {"t" : d})
