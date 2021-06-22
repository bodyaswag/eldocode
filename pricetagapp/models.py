from django.db import models

# Create your models here.
class Scanaction(models.Model):
	sku = models.IntegerField(blank=True, null=True)
	price = models.IntegerField(blank=True, null=True)
	user_id = models.IntegerField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		managed = False
		db_table = 'scanaction'


class Sku(models.Model):
	sku = models.IntegerField(blank=True, null=True)
	name = models.TextField(blank=True, null=True)
	img_src = models.TextField(blank=True, null=True)
	group_name = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'sku'



class Store(models.Model):
	sku = models.IntegerField(blank=True, null=True)
	cnt = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'store'


class Tasks(models.Model):
	sku = models.IntegerField(blank=True, null=True)
	tasktype = models.TextField(blank=True, null=True)
	task_dt = models.DateField(blank=True, auto_now_add=True)
	task_due_dt = models.DateField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'tasks'


class Users(models.Model):
	id = models.IntegerField(primary_key =True)
	img_src = models.TextField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'users'


class Pricetags(models.Model):
	sku = models.IntegerField(blank=True, null=True)
	price = models.IntegerField(blank=True, null=True)
	timestamp = models.DateField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'pricetags'

class Actualtask(models.Model):
	sku = models.IntegerField(blank=True, null=True)
	tasktype = models.TextField(blank=True, null=True)
	img_src = models.TextField(blank=True, null=True)
	name = models.TextField(blank=True, null=True)
	group_name = models.TextField(blank=True, null=True)
	task_dt = models.DateField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'actualtask'
		#unique_together = ('sku','tasktype')



class Leaderboard(models.Model):
	user_id = models.IntegerField(blank=True, null=True)
	scan_cnt = models.IntegerField(blank=True, null=True)
	place = models.IntegerField(blank=True, null=True)
	img = models.TextField(blank=True, null=True)
	name = models.TextField(blank=True, null=True)
	user_flg = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'leaderboard'