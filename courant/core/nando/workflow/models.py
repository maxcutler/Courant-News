from django.db import models

from courant.core.staff.models import Staffer

class Workflow(models.Model):
	name = models.CharField(max_length=255)

class WorkflowStatus(models.Model):
	workflow = models.ForeignKey(Workflow)
	
	name = models.CharField(max_length=255)
	abbreviation = models.CharField(max_length=5)
	published = models.BooleanField()
	
	order = models.PositiveIntegerField()
	
	owners = models.ManyToManyField(Staffer)
	
	class Meta:
		verbose_name_plural = "Workflow Statuses"

class WorkflowMixin(models.Model):

	workflow_status = models.ForeignKey(WorkflowStatus, null=True)
	
	class Meta:
		abstract = True