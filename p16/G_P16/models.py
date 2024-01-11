from django.db import models

# Create your models here.

class Departement(models.Model):

	NomDepartement = models.CharField(max_length = 50,verbose_name = 'Département')

	class Meta:

		verbose_name = 'Département'
		verbose_name_plural = 'Départements'
		ordering = ['-NomDepartement']

	def __str__(self):
		return self.NomDepartement

class Etudiant(models.Model):

	Matricule = models.CharField(max_length = 20,verbose_name = 'Matricule')
	Nom = models.CharField(max_length = 50,verbose_name = 'Nom')
	Prenom = models.CharField(max_length = 50,verbose_name = 'Prénom')
	telephone = models.CharField(max_length = 20,verbose_name = 'Telephone')
	Departement = models.ForeignKey(Departement,on_delete = models.CASCADE,verbose_name = 'Département')

	class Meta:

		ordering = ['-Matricule']
		verbose_name = 'Etudiant'
		verbose_name_plural = 'Etudiants'

	def __str__(self):
		return self.Matricule

class Enseignant(models.Model):

	choix = {
		('titulaire','Titulaire'),
		('missionnaire','Missionnaire'),
		('vacataire','Vacataire'),
	}

	Matricule = models.CharField(max_length = 5,verbose_name = 'Matricule')
	Nom = models.CharField(max_length = 50,verbose_name = 'Nom')
	Prenom = models.CharField(max_length = 50,verbose_name = 'Prénom')
	telephone = models.CharField(max_length = 20,verbose_name = 'Telephone')
	Mail = models.CharField(max_length = 100,verbose_name = 'Email')
	Statut = models.CharField(max_length = 15,verbose_name = 'Statut',choices = choix)
	Departement = models.ForeignKey(Departement,on_delete = models.CASCADE,verbose_name = 'Département')

	class Meta:

		ordering = ['-Matricule']
		verbose_name = 'Enseignant'
		verbose_name_plural = 'Enseignants'

	def __str__(self):
		return self.Matricule

class Matiere(models.Model):

	Libelle = models.CharField(max_length = 100,verbose_name ='Matière')
	semestre = models.IntegerField(verbose_name = 'Semestre')
	Enseignant = models.CharField(max_length = 5,verbose_name ='Enseignant')
	Departement = models.ForeignKey(Departement,on_delete = models.CASCADE,verbose_name = 'Département')

	class Meta:

		ordering = ['-Libelle']
		verbose_name = 'Matière'
		verbose_name_plural = 'Matières'

	def __str__(self):
		return self.Libelle

# class Dispenser(models.Model):

# 	Departement = models.ForeignKey(Departement,on_delete = models.DO_NOTHING,verbose_name = 'Département')
# 	Matiere = models.ForeignKey(Matiere,on_delete = models.DO_NOTHING,verbose_name = 'Matière')

class Utilisateur(models.Model):

	choix = {
		('admin','Admin'),
		('second','Second'),
	}

	Login = models.CharField(max_length = 50,verbose_name = 'Login')
	Departement = models.ForeignKey(Departement,on_delete = models.CASCADE,verbose_name = 'Département')
	Password = models.CharField(max_length = 100,verbose_name = 'mot de passe')
	Droit = models.CharField(choices = choix,max_length = 20,verbose_name = 'Droit')

	class Meta:

		ordering = ['-Login']
		verbose_name = 'Utilisateur'
		verbose_name_plural = 'Utilisateurs'

	def __str__(self):
		return self.Login