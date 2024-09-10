from django.db import models



# Create your models here.
class pensioner_list(models.Model):
    csv_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    bank = models.CharField(max_length=200,null=True,blank=True)
    add1 = models.CharField(max_length=200,null=True,blank=True)
    add2 = models.CharField(max_length=200,null=True,blank=True)
    birth = models.DateField(max_length=20,null=True,blank=True)
    ptype = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    grouping = models.CharField(max_length=100,null=True,blank=True)
    conmonth = models.CharField(max_length=100,null=True,blank=True)
    readyx = models.CharField(max_length=200,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table = "pensioner_list"
    
class ticket_list(models.Model):
    csv_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    date_issued = models.DateField(max_length=20,null=True,blank=True)
    valid_until = models.DateField(max_length=20,null=True,blank=True)
    endorsed_to = models.CharField(max_length=200,null=True,blank=True)
    relationship = models.CharField(max_length=200,null=True,blank=True)
    ticket_ssp_consult = models.PositiveIntegerField(unique=True, null=True, blank=True, default=None)
    ticket_ssp_lab = models.PositiveIntegerField(unique=True, null=True, blank=True, default=None)
    ticket_family_consult = models.PositiveIntegerField(unique=True, null=True, blank=True, default=None)
    ticket_family_lab = models.PositiveIntegerField(unique=True, null=True, blank=True, default=None)
    checkup_status = models.CharField(max_length=200,default="PENDING CHECKUP")
    checkup_type = models.CharField(max_length=100,null=True,blank=True)
    recepient_type = models.CharField(max_length=100,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)


    
    # def save(self, *args, **kwargs):
    #     if not self.ticket_number:
    #         last_ticket = ticket_list.objects.all().order_by('ticket_number').last()
    #         if last_ticket:
    #             self.ticket_number = last_ticket.ticket_number + 1
    #         else:
    #             self.ticket_number = 10  # starting from 10
    #     super().save(*args, **kwargs)
   

class import_history(models.Model):
    import_date = models.DateField(max_length=20,null=True,blank=True)
    file_name = models.CharField(max_length=200,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)

