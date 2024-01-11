from django.shortcuts import render,redirect,HttpResponseRedirect
# from django.core.mail import EmailMessage #envoi mail
# from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from .models import Etudiant,Enseignant,Matiere,Departement,Utilisateur
from .forms import EtudiantForm,EnseignantForm,MatiereForm,DepartementForm,UtilisateurForm

# Create your views here.
# def envoyer_mail(request):
#     if request.method == 'POST':
#         sujet = request.POST.get('sujet')
#         msg = request.POST.get('msg')
#         mail = [request.POST.get('mail')]
#         em = "tolnophilippe2002@gmail.com"

#         msg = EmailMessage(
#                 sujet,
#                 msg,
#                 em,
#                 mail,
#         )
#         msg.send()

#         return render('G_P16:index')
        

# def envoyer_mail(request):
#      if request.method == 'POST':
#         sujet = request.POST.get('sujet')
#         message = request.POST.get('msg')
#         emetteur = request.POST.get('mail')
#         destinataires = 'tolnophilippe2002@gmail.com'

#         send_mail(sujet, message, emetteur, [destinataires])

#         return redirect('G_P16:index')

# views.py

# from django.core.mail import send_mail
# from django.shortcuts import render

# def envoyer_email(request):
#     send_mail(
#         'Sujet de l\'e-mail',
#         'Corps de l\'e-mail.',
#         'expediteur@example.com',
#         ['destinataire@example.com'],
#         fail_silently=False,
#     )
#     return render(request, 'template.html')

# def supprEtu(request,matricule):
#     ma_session = request.session.get('user_login')
#     if ma_session is not None:
        
#         asuppr = Etudiant.objects.get(pk = matricule)
#         asuppr.delete()

#         return redirect('G_P16:menu')
#     else:
#         return render(request, 'G_P16/index.html')

def index(request):
    NbreEns = len(Enseignant.objects.all())
    NbreEtu = len(Etudiant.objects.all())
    NbreDep = len(Departement.objects.all())

    return render(request,'G_P16/index.html',{'NbreEns':NbreEns,'NbreEtu':NbreEtu,'NbreDep':NbreDep})

def presentation(request):
    return render(request,'G_P16/presentation.html')
    

def departement(request):
    return render(request,'G_P16/departement.html')
    

def connexion(request):
    if request.method == 'POST':
        login = request.POST.get('login').upper()
        passe = request.POST.get('passe')
        if Utilisateur.objects.filter(Login = login).exists():
            passeEncoder = Utilisateur.objects.get(Login = login).Password
            passeVerifier = check_password(passe,passeEncoder)
            if passeVerifier:
                request.session['user_login'] = login
                droit = Utilisateur.objects.get(Login = login).Droit
                depart = Utilisateur.objects.get(Login = login).Departement
                request.session['user_droit'] = droit

                if droit == "admin":
                    return redirect('G_P16:dep')
                else:
                    return redirect('G_P16:menu')
            else:
                messages.error(request,"Mot de passe ou login incorrect !")
        else:
            messages.error(request,"Mot de passe ou login incorrect !")

    return render(request, 'G_P16/connexion.html')

def deconnexion(request):
    NbreEns = len(Enseignant.objects.all())
    NbreEtu = len(Etudiant.objects.all())
    NbreDep = len(Departement.objects.all())

    request.session.flush()
    ma_session = request.session.get('user_login')
    mon_droit = request.session.get('user_droit')

    if ma_session is None:
        return render(request, 'G_P16/index.html',{'NbreEns':NbreEns,'NbreDep':NbreDep,'NbreEtu':NbreEtu})


def menu(request):
    ma_session = request.session.get('user_login')
    mon_droit = request.session.get('user_droit')

    if ma_session is not None:
        depart = Utilisateur.objects.get(Login = ma_session).Departement

        mes_etuds = Etudiant.objects.filter(Departement = depart)
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_etuds = Etudiant.objects.filter(Matricule__icontains = recherche)

        if request.method == 'POST':

            form = EtudiantForm(request.POST)
            matricule = request.POST.get('Matricule')
            tel = request.POST.get('telephone')

            if Etudiant.objects.filter(Matricule = matricule).exists():
                messages.error(request,"Ce matricule existe déjà !")
            elif Etudiant.objects.filter(telephone = tel).exists():
                messages.error(request,"Ce tel existe déjà !")
            else:
            
                if form.is_valid():
                
                    mat = form.cleaned_data['Matricule']
                    nom = form.cleaned_data['Nom']
                    prenom = form.cleaned_data['Prenom']
                    tel = form.cleaned_data['telephone']
                    enreg = Etudiant(Matricule = mat,Nom = nom,Prenom = prenom,telephone = tel,Departement = depart)
                    enreg.save()
                    form = EtudiantForm()
                else:
                    form = EtudiantForm()
        else:
            form = EtudiantForm()
        return render(request, 'G_P16/menu.html',{'form':form,'mes_etuds':mes_etuds,'ma_session':ma_session,'user':user})
    else:
        return render(request, 'G_P16/index.html')

def modifierEtud(request, id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        depart = Utilisateur.objects.get(Login = ma_session).Departement

        mes_etuds = Etudiant.objects.filter(Departement = depart)
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_etuds = Etudiant.objects.filter(Matricule__icontains = recherche)
       
        if request.method == 'POST':

            amodifier = Etudiant.objects.get(pk = id)

            matric_Mem = amodifier.Matricule
            tel_Mem = amodifier.telephone
        
            form = EtudiantForm(request.POST, instance = amodifier)
            if form.is_valid():
                matricule = request.POST.get('Matricule')
                tel = request.POST.get('telephone')
                
                if matric_Mem != matricule:
                    if Etudiant.objects.filter(Matricule = matricule).exists():
                        messages.error(request,"Ce matricule existe déjà !")
                    else:
                        if tel_Mem != tel:
                            if Etudiant.objects.filter(telephone = tel).exists():
                                messages.error(request,"Ce tel existe déjà !")
                        else:
                            form.save()
                            form = EtudiantForm()
                            return redirect('G_P16:menu')
                elif tel_Mem != tel:
                    if Etudiant.objects.filter(telephone = tel).exists():
                        messages.error(request,"Ce tel existe déjà !")
                    else:
                        if matric_Mem != matricule:
                            if Etudiant.objects.filter(Matricule = matricule).exists():
                                messages.error(request,"Ce matricule existe déjà !")
                        else:
                            form.save()
                            form = EtudiantForm()
                            return redirect('G_P16:menu')
                elif matric_Mem == matricule and tel_Mem == tel:
                    form.save()
                    form = EtudiantForm()
                    return redirect('G_P16:menu')
            else:
                amodifier =Etudiant.objects.get(pk = id)
                form = EtudiantForm(instance = amodifier)
        else:
            amodifier =Etudiant.objects.get(pk = id)
            form = EtudiantForm(instance = amodifier)
        return render(request, 'G_P16/menu.html',{'form': form,'mes_etuds':mes_etuds,'ma_session':ma_session,'user':user})
    else:
        return render(request, 'G_P16/index.html')


def enseignant(request):
    ma_session = request.session.get('user_login')
    mon_droit = request.session.get('user_droit')

    if ma_session is not None:
        depart = Utilisateur.objects.get(Login = ma_session).Departement

        mes_enseigs = Enseignant.objects.filter(Departement = depart)
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_mats = Enseignant.objects.filter(Matricule__icontains = recherche)

        if request.method == 'POST':
            form = EnseignantForm(request.POST)
            mat = request.POST.get('Matricule')
            tel = request.POST.get('telephone')
            mail = request.POST.get('Mail')

            if Enseignant.objects.filter(Matricule = mat).exists():
                if Enseignant.objects.get(Matricule = mat).Departement == depart:
                    messages.error(request,"Ce Matricule existe déjà !")
                else:
                    messages.error(request,"Ce Matricule existe déjà !")
            elif Enseignant.objects.filter(telephone = tel).exists():
                messages.error(request,"Ce tel existe déjà !")
            elif Enseignant.objects.filter(Mail = mail).exists():
                messages.error(request,"Ce e-mail existe déjà !")
            else:
                if form.is_valid():
                    mat = form.cleaned_data['Matricule']
                    nom = form.cleaned_data['Nom']
                    prenom = form.cleaned_data['Prenom']
                    tel = form.cleaned_data['telephone']
                    mail = form.cleaned_data['Mail']
                    stat = form.cleaned_data['Statut']
                    enreg = Enseignant(Matricule = mat,Nom = nom,Prenom = prenom,telephone = tel,Mail = mail,Statut = stat,Departement = depart)
                    enreg.save()
                    form = EnseignantForm()
                else:
                    form = EnseignantForm()
        else:
            form = EnseignantForm()
        return render(request, 'G_P16/enseignant.html',{'form':form,'mes_enseigs':mes_enseigs,'ma_session':ma_session,'user':user})
    else:
        return render(request, 'G_P16/index.html')

def modifierEns(request, id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        depart = Utilisateur.objects.get(Login = ma_session).Departement

        mes_enseigs = Enseignant.objects.filter(Departement = depart)
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_enseigs = Enseignant.objects.filter(Matricule__icontains = recherche)

        if request.method == 'POST':

            amodifier = Enseignant.objects.get(pk = id)
            mat_Mem = amodifier.Matricule
            tel_Mem = amodifier.telephone 
            mail_Mem = amodifier.Mail
        
            form = EnseignantForm(request.POST, instance = amodifier)

            if form.is_valid():
                matric = request.POST.get('Matricule')
                tel = request.POST.get('telephone')
                mail = request.POST.get('Mail')

                if mat_Mem == matric and tel_Mem == tel and mail_Mem == mail:
                    form.save()
                    modifMat = Matiere.objects.all()
                    for modif in modifMat:
                        if modif.Enseignant == mat_Mem:
                            modif.Enseignant = matric
                            modif.save()
                    form = EnseignantForm()
                    return redirect('G_P16:enseignant')
                elif mat_Mem != matric:
                    if Enseignant.objects.filter(Matricule = matric).exists():
                        if Enseignant.objects.get(Matricule = matric).Departement == depart:
                            messages.error(request,"Ce matricule existe déjà !")
                        else:
                            if tel_Mem != tel:
                                if Enseignant.objects.filter(telephone = tel).exists():
                                    messages.error(request,"Ce tel existe déjà !")
                            elif mail_Mem != mail:
                                if Enseignant.objects.filter(Mail = mail).exists():
                                    messages.error(request,"Ce e-mail existe déjà !")
                            else:
                                form.save()
                                modifMat = Matiere.objects.all()
                                for modif in modifMat:
                                    if modif.Enseignant == mat_Mem:
                                        modif.Enseignant = matric
                                        modif.save()
                                form = EnseignantForm()
                                return redirect('G_P16:enseignant')
                    else:
                        if tel_Mem != tel:
                            if Enseignant.objects.filter(telephone = tel).exists():
                                messages.error(request,"Ce tel existe déjà !")
                        elif mail_Mem != mail:
                            if Enseignant.objects.filter(Mail = mail).exists():
                                messages.error(request,"Ce e-mail existe déjà !")
                        else:
                            form.save()
                            modifMat = Matiere.objects.all()
                            for modif in modifMat:
                                if modif.Enseignant == mat_Mem:
                                    modif.Enseignant = matric
                                    modif.save()
                            form = EnseignantForm()
                            return redirect('G_P16:enseignant')
                elif tel_Mem != tel:
                    if Enseignant.objects.filter(telephone = tel).exists():
                        messages.error(request,"Ce tel existe déjà !")
                    else:
                        if mat_Mem != matric:
                            if Enseignant.objects.filter(Matricule = mat).exists():
                                if Enseignant.objects.get(Matricule = mat).Departement == depart:
                                    messages.error(request,"Ce matricule existe déjà !")
                        elif mail_Mem != mail:
                            if Enseignant.objects.filter(Mail = mail).exists():
                                messages.error(request,"Ce e-mail existe déjà !")
                        else:
                            form.save()
                            modifMat = Matiere.objects.all()
                            for modif in modifMat:
                                if modif.Enseignant == mat_Mem:
                                    modif.Enseignant = matric
                                    modif.save()
                            form = EnseignantForm()
                            return redirect('G_P16:enseignant')
                elif mail_Mem != mail:
                    if Enseignant.objects.filter(Mail = mail).exists():
                        messages.error(request,"Ce mail existe déjà !")
                    else:
                        if mat_Mem != matric:
                            if Enseignant.objects.filter(Matricule = mat).exists():
                                if Enseignant.objects.get(Matricule = mat).Departement == depart:
                                    messages.error(request,"Ce matricule existe déjà !")
                        if tel_Mem != tel:
                            if Enseignant.objects.filter(Mail = mail).exists():
                                messages.error(request,"Ce tel existe déjà !")
                        else:
                            form.save()
                            modifMat = Matiere.objects.all()
                            for modif in modifMat:
                                if modif.Enseignant == mat_Mem:
                                    modif.Enseignant = matric
                                    modif.save()
                            form = EnseignantForm()
                            return redirect('G_P16:enseignant')
                
        else:
            amodifier =Enseignant.objects.get(pk = id)
            form = EnseignantForm(instance = amodifier)
        return render(request, 'G_P16/enseignant.html',{'form': form,'mes_enseigs':mes_enseigs,'ma_session':ma_session,'user':user})
    else:
        return render(request, 'G_P16/index.html')

def supprEns(request,id):
    ma_session = request.session.get('user_login')
    if ma_session is not None:
        
        asuppr = Enseignant.objects.get(pk = id)
        asuppr.delete()

        return redirect('G_P16:enseignant')
    else:
        return render(request, 'G_P16/index.html')
    

def matiere(request):
    ma_session = request.session.get('user_login')
    mon_droit = request.session.get('user_droit')

    if ma_session is not None:
        depart = Utilisateur.objects.get(Login = ma_session).Departement

        mes_mats = Matiere.objects.filter(Departement = depart)
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_mats = Matiere.objects.filter(Libelle__icontains = recherche)

        if request.method == 'POST':
            form = MatiereForm(request.POST)
            mat = request.POST.get('Libelle').upper()
            enseig = request.POST.get('Enseignant').upper()
            sem = request.POST.get('semestre')

            if Matiere.objects.filter(Libelle = mat).exists():
                if Matiere.objects.get(Libelle = mat).Departement == depart:
                    messages.error(request,"Cette matière existe déjà !")
                else:
                    if Enseignant.objects.filter(Matricule = enseig).exists():
                        if Enseignant.objects.get(Matricule = enseig).Departement != depart:
                            messages.error(request,"Ce enseignant n'est pas du département !")
                        else:
                            mat_sem = Matiere.objects.filter(semestre = sem)
                            if len(mat_sem) == 5:
                                messages.error(request,"Ce semestre à déjà 5 matières.")
                            else:
                                if form.is_valid():
                                    mat = form.cleaned_data['Libelle']
                                    sem = form.cleaned_data['semestre']
                                    ensei = form.cleaned_data['Enseignant']
                                    enreg = Matiere(Libelle = mat,semestre = sem,Enseignant = ensei,Departement = depart)
                                    enreg.save()
                                    form = MatiereForm()
                                else:
                                    form = MatiereForm()
                    else:
                        messages.error(request,"Ce enseignant n'est pas du département !")
            else:
                if Enseignant.objects.filter(Matricule = enseig).exists():
                    if Enseignant.objects.get(Matricule = enseig).Departement != depart:
                        messages.error(request,"Ce enseignant n'est pas du département !")
                    else:
                        mat_sem = Matiere.objects.filter(semestre = sem)
                        if len(mat_sem) == 5:
                            messages.error(request,"Ce semestre à déjà 5 matières.")
                        else:
                            if form.is_valid():
                                mat = form.cleaned_data['Libelle']
                                sem = form.cleaned_data['semestre']
                                ensei = form.cleaned_data['Enseignant']
                                enreg = Matiere(Libelle = mat,semestre = sem,Enseignant = ensei,Departement = depart)
                                enreg.save()
                                form = MatiereForm()
                            else:
                                form = MatiereForm()
                else:
                    messages.error(request,"Ce enseignant n'est pas du département !")
        else:
            form = MatiereForm()
        return render(request, 'G_P16/matiere.html',{'form':form,'mes_mats':mes_mats,'ma_session':ma_session,'user':user})
    else:
        return render(request, 'G_P16/index.html')

def modifierMat(request, id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        depart = Utilisateur.objects.get(Login = ma_session).Departement

        mes_mats = Matiere.objects.filter(Departement = depart)
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_mats = Matiere.objects.filter(Libelle__icontains = recherche)
       
        if request.method == 'POST':

            amodifier = Matiere.objects.get(pk = id)

            lib_Mem = amodifier.Libelle.upper()
            ens_Mem = amodifier.Enseignant.upper()
            sem_Mem = amodifier.semestre
        
            form = MatiereForm(request.POST, instance = amodifier)
            if form.is_valid():
                lib = request.POST.get('Libelle').upper()
                ens = request.POST.get('Enseignant').upper()
                sem = int(request.POST.get('semestre'))

                if sem_Mem == sem and lib_Mem == lib and ens_Mem == ens:
                    form.save()
                    form = MatiereForm()
                    return redirect('G_P16:matiere')
                else:
                    if lib_Mem != lib:
                        if Matiere.objects.filter(Libelle = lib.lower()).exists():
                            if Matiere.objects.get(Libelle = lib.lower()).Departement == depart:
                                messages.error(request,'Cette matière existe déjà !')
                        else:
                            if ens_Mem != ens:
                                if Enseignant.objects.filter(Matricule = ens).exists():
                                    if Enseignant.objects.get(Matricule = ens).Departement != depart:
                                        messages.error(request,'Ce enseignant n\'est du département !')
                                else:
                                    messages.error(request,'Ce enseignant n\'est du département !')
                            mat_sem = Matiere.objects.filter(semestre = sem)
                            if len(mat_sem) == 5:
                                messages.error(request,'Ce semestre a 5 matières !')
                            else:
                                form.save()
                                form = MatiereForm()
                                return redirect('G_P16:matiere')
                    if lib_Mem == lib:
                        if ens_Mem != ens:
                            if Enseignant.objects.filter(Matricule = ens).exists():
                                if Enseignant.objects.get(Matricule = ens).Departement != depart:
                                    messages.error(request,'Ce enseignant n\'est du département !')
                                else:
                                    mat_sem = Matiere.objects.filter(semestre = sem)
                                    if len(mat_sem) == 5:
                                        messages.error(request,'Ce semestre a 5 matières !')
                                    else:
                                        form.save()
                                        form = MatiereForm()
                                        return redirect('G_P16:matiere')
                            else:
                                messages.error(request,'Ce enseignant n\'est du département !')
            else:
                amodifier =Matiere.objects.get(pk = id)
                form = MatiereForm(instance = amodifier)
        else:
            amodifier =Matiere.objects.get(pk = id)
            form = MatiereForm(instance = amodifier)
        return render(request, 'G_P16/matiere.html',{'form': form,'mes_mats':mes_mats,'ma_session':ma_session,'user':user})
    else:
        return render(request, 'G_P16/index.html')

def supprMat(request,id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        
        asuppr = Matiere.objects.get(pk = id)
        asuppr.delete()

        return redirect('G_P16:matiere')
    else:
        return render(request, 'G_P16/index.html')

def dep(request):
    
    ma_session = request.session.get('user_login')
    mon_droit = request.session.get('user_droit')

    if ma_session is not None:
        mes_dep = Departement.objects.all()
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_dep = Departement.objects.filter(NomDepartement__icontains = recherche)
        if request.method == 'POST':
            form = DepartementForm(request.POST)
            dep = request.POST.get('NomDepartement')
            if Departement.objects.filter(NomDepartement = dep).exists():
                messages.error(request,"Ce département existe déjà !")
            else:
                if form.is_valid():
                    dep = form.cleaned_data['NomDepartement'].lower()
                    enreg = Departement(NomDepartement = dep)
                    enreg.save()
                    form = DepartementForm()
                    return redirect('G_P16:dep')
                else:
                    form = DepartementForm()
        else:
            form = DepartementForm()
        return render(request, 'G_P16/dep.html',{'form':form,'mes_dep':mes_dep,'ma_session':ma_session,'user':user})
    else:
        return redirect('G_P16:connexion')

def supprDep(request, id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        if request.method == 'POST': # si une requete est envoyé

            asuppr = Departement.objects.get(pk = id) # on selectionne l'user correspondant
            asuppr.delete() # on le supprime
            return redirect('G_P16:dep') # renvoi sur la même page
    else:
        return render(request, 'G_P16/index.html')

def modifierDep(request, id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        mes_dep = Departement.objects.all()
        user = Utilisateur.objects.get(Login = ma_session)

        if request.method == 'POST':

            amodifier = Departement.objects.get(pk = id)
        
            form = DepartementForm(request.POST, instance = amodifier)
            if form.is_valid():
                dep = request.POST.get('NomDepartement').lower()
                
                if Departement.objects.filter(NomDepartement = dep).exists():
                    messages.error(request,"Ce département existe déjà !")
                else:
                    form.save()
                    form = DepartementForm()
                    return redirect('G_P16:dep')
        else:
            amodifier =Departement.objects.get(pk = id)
            form = DepartementForm(instance = amodifier)
        return render(request, 'G_P16/dep.html',{'form': form,'mes_dep':mes_dep,'user':user})
    else:
        return render(request, 'G_P16/index.html')


def utilisateur(request):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        mes_users = Utilisateur.objects.all()
        user = Utilisateur.objects.get(Login = ma_session)

        recherche = request.GET.get('recherche') # recuperer la valeur de l'input du formulaire
        if recherche != '' and recherche is not None:
            mes_users = Utilisateur.objects.filter(Login__icontains = recherche)
        if request.method == 'POST':
            form = UtilisateurForm(request.POST)
            login = request.POST.get('Login')
            if Utilisateur.objects.filter(Login = login).exists():
                messages.error(request,"Ce login existe déjà !")
            else:
                if form.is_valid():
                    login = form.cleaned_data['Login'].upper()
                    dep = form.cleaned_data['Departement']
                    pwd = make_password(form.cleaned_data['Password'])
                    droit = form.cleaned_data['Droit']
                    enreg = Utilisateur(Login = login,Departement = dep,Password = pwd,Droit = droit)
                    enreg.save()
                    form = UtilisateurForm()
                    return redirect('G_P16:utilisateur')
                else:
                    form = UtilisateurForm()
        else:
            form = UtilisateurForm()
        return render(request, 'G_P16/utilisateur.html',{'form':form,'mes_users':mes_users,'ma_session':ma_session,'user':user})
    else:
        return render(request,'G_P16/index.html')

def ChangePwd(request,id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:

        if request.method == 'POST':
            pwdAct = request.POST.get('pwdAct')
            pwdNew = request.POST.get('newPwd')
            pwdconf = request.POST.get('confPwd')

            amodifier = Utilisateur.objects.get(pk = id)
            passeCrypt =amodifier.Password

            passeVerifier = check_password(pwdAct,passeCrypt)

            if not passeVerifier:
                msg = '<h4 style = "color:red;">Entrez le mot de passe actuel</h4>'
                return HttpResponse(msg)
            elif pwdNew != pwdconf:
                msg = '<h4 style = "color:red;">Les mot de passe ne sont pas identiques</h4>'
                return HttpResponse(msg)
            else:
                pwdModif = make_password(pwdNew)
                amodifier.Password = pwdModif
                amodifier.save()
                request.session.flush()
                return redirect('G_P16:connexion')
    else:
        return render(request, 'G_P16/index.html')

def supprUser(request,id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        if request.method == "POST":

            asuppr = Utilisateur.objects.get(pk = id)
            asuppr.delete()
            return redirect('G_P16:utilisateur')
    else:
        return render(request, 'G_P16/index.html')

def modifierUser(request, id):
    ma_session = request.session.get('user_login')

    if ma_session is not None:
        mes_users = Utilisateur.objects.all()
        user = Utilisateur.objects.get(Login = ma_session)

        if request.method == 'POST':

            amodifier = Utilisateur.objects.get(pk = id)
            login_Mem = amodifier.Login
            pwd_Mem = amodifier.Password
            form = UtilisateurForm(request.POST, instance = amodifier)
            if form.is_valid():
                login = request.POST.get('Login').upper()
                pwd = make_password(request.POST.get('Password'))
                
                if login == login_Mem:
                    if pwd_Mem != pwd:
                        form.save()
                        form = UtilisateurForm()
                        return redirect('G_P16:utilisateur')
                    else:
                        messages.error(request,"Les actions sur le mot de passe sont reservées au proprietaire")
                else:
                    if Utilisateur.objects.filter(Login = login).exists():
                        messages.error(request,"Ce login existe déjà !")
                    else:
                        if pwd_Mem != pwd:
                            form.save()
                            form = UtilisateurForm()
                            return redirect('G_P16:utilisateur')
                        else:
                            messages.error(request,"Les actions sur le mot de passe sont reservées au proprietaire")
        else:
            amodifier =Utilisateur.objects.get(pk = id)
            form = UtilisateurForm(instance = amodifier)
        return render(request, 'G_P16/utilisateur.html',{'form': form,'mes_users':mes_users,'user':user})
    else:
        return render(request, 'G_P16/index.html')
