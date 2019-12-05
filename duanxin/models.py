from django.db import models

# Create your models here.
class Books(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    concern = models.CharField(max_length=50, blank=True, null=True)
    outcount = models.CharField(max_length=50, blank=True, null=True)
    char = models.CharField(max_length=50, blank=True, null=True)
    typeid = models.ForeignKey('Booktype', models.DO_NOTHING, db_column='typeid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'books'


class Booktype(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'booktype'


class Borrowbook(models.Model):
    readerid = models.ForeignKey('Reader', models.DO_NOTHING, db_column='readerid', blank=True, null=True)
    managerid = models.ForeignKey('Manager', models.DO_NOTHING, db_column='managerid', blank=True, null=True)
    borrowdate = models.DateTimeField(db_column='borrowDate', blank=True, null=True)  # Field name made lowercase.
    restoredata = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    bookid = models.ForeignKey(Books, models.DO_NOTHING, db_column='bookid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'borrowbook'


class Manager(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    roleid = models.ForeignKey('Role', models.DO_NOTHING, db_column='roleid', blank=True, null=True)
    dutydate = models.DateTimeField(blank=True, null=True)
    leavedate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'manager'


class Reader(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    roleid = models.ForeignKey('Role', models.DO_NOTHING, db_column='roleid', blank=True, null=True)
    grandid = models.ForeignKey('Readergrade', models.DO_NOTHING, db_column='grandid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'reader'


class Readergrade(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    maxmaney = models.IntegerField(blank=True, null=True)
    dateamount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'readergrade'


class Role(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'role'



