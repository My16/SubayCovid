from django.db import models

# Create your models here.

class Data(models.Model):
    cfname = models.CharField(max_length=100)
    north_coord = models.FloatField(default=0)
    east_coord = models.FloatField(default=0)
    chances_patient_not_dying = models.FloatField(default=0)
    total_ipcs = models.IntegerField(blank=True, null=True)
    ratio_patients_per_day_and_total_beds = models.FloatField(default=0)
    ratio_staff_not_infected = models.FloatField(default=0)
    ratio_total_staff_members = models.FloatField(default=0)
    kmeans_label = models.IntegerField(blank=True, null=True)
    Image = models.CharField(max_length=1000, null= True)
    total_beds = models.IntegerField(blank=True, null=True)
    tpatient_adm = models.IntegerField(blank=True, null=True)
    total_staff_members = models.IntegerField(blank=True, null=True)
    ambulance = models.IntegerField(blank=True, null=True)

    # city_mun = models.CharField(max_length=100)
    # total_ipcs = models.IntegerField(blank=True, null=True)
    # Percentage_Staff_not_Covid = models.FloatField(default=0)
    # Ratio_Recovered_Patients = models.FloatField(default=0)
    # Ratio_Ambulance_Patients = models.FloatField(default=0)
    # Ratio_Staff_Patients = models.FloatField(default=0)
    # kmeans_label = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.cfname

class Dashboard(models.Model):
    cfname = models.CharField(max_length=100)
    total_covid_patients = models.FloatField(default=0)
    discharged = models.FloatField(default=0)
    conf_died = models.FloatField(default=0)

    def __str__(self):
        return self.cfname