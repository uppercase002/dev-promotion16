from django import forms
from .models import Etudiant,Enseignant,Matiere,Departement,Utilisateur

class DepartementForm(forms.ModelForm):

	class Meta:
		model = Departement
		fields = ['NomDepartement']
		labels = {
			'NomDepartement':'Nom département'
		}
		widgets = {
			'NomDepartement':forms.TextInput(attrs = {'class':'form-control'})
		}

class UtilisateurForm(forms.ModelForm):

	class Meta:
		model = Utilisateur
		fields = ['Login','Departement','Password','Droit']
		labels = {
			'Login':'Login',
			'Departement':'Département',
			'Password':'Mot de passe',
			'Droit':'Droit',
		}
		widgets = {
			'Password':forms.PasswordInput(render_value = True,attrs = {'class':'form-control'}),
			'Login':forms.TextInput(attrs = {'class':'form-control'})
		}

class EtudiantForm(forms.ModelForm):

	class Meta:
		model = Etudiant
		fields = ['Matricule','Nom','Prenom','telephone']
		labels = {
			'Matricule':'Matricule',
			'Nom':'Nom',
			'Prenom':'Prénom',
			'telephone':'Telephone'
		}
		widgets = {
			'Matricule':forms.TextInput(attrs = {'class':'form-control'}),
			'Nom':forms.TextInput(attrs = {'class':'form-control'}),
			'Prenom':forms.TextInput(attrs = {'class':'form-control'}),
			'telephone':forms.TextInput(attrs = {'class':'form-control'})
		}

class EnseignantForm(forms.ModelForm):

	class Meta:
		model = Enseignant
		fields = ['Matricule','Nom','Prenom','telephone','Mail','Statut']
		labels = {
			'Matricule':'Matricule',
			'Nom':'Nom',
			'Prenom':'Prénom',
			'telephone':'Telephone',
			'Mail':'E-mail',
			'Statut':'Statut',
		}
		widgets = {

			'Matricule':forms.TextInput(attrs = {'class':'form-control'}),
			'Nom':forms.TextInput(attrs = {'class':'form-control'}),
			'Prenom':forms.TextInput(attrs = {'class':'form-control'}),
			'telephone':forms.TextInput(attrs = {'class':'form-control'}),
			'Mail':forms.EmailInput(attrs = {'class':'form-control'}),
		}

class MatiereForm(forms.ModelForm):

	class Meta:
		model = Matiere
		fields = ['Libelle','semestre','Enseignant']
		labels = {
			'Libelle':'Libellé matière',
			'semestre':'Semestre',
			'Enseignant':'Enseignant'
		}
		widgets = {
			'Libelle':forms.TextInput(attrs = {'class':'form-control'}),
			'semestre':forms.NumberInput(attrs = {'class':'form-control'}),
			'Enseignant':forms.TextInput(attrs = {'class':'form-control'}),
		}
