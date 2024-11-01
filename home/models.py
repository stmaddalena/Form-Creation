from django.db import models


class Answer(models.Model):
    form = models.ForeignKey('Form', on_delete=models.DO_NOTHING)
    question = models.ForeignKey('Question', on_delete=models.DO_NOTHING)
    person_ans = models.ForeignKey('PersonAns', on_delete=models.DO_NOTHING)
    answer = models.CharField(max_length=-1)
    response_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'answer'


class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.DO_NOTHING)
    choice = models.CharField(max_length=-1)

    class Meta:
        db_table = 'choice'


class Country(models.Model):
    code = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        db_table = 'country'


class District(models.Model):
    province = models.ForeignKey('Province', on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        db_table = 'district'


class Form(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    gen_date = models.DateTimeField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    number_responses = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'form'


class Gender(models.Model):
    code = models.CharField(max_length=-1)
    name = models.CharField(max_length=-1)

    class Meta:
        db_table = 'gender'


class PersonAns(models.Model):
    first_name = models.CharField(max_length=-1, blank=True, null=True)
    last_name = models.CharField(max_length=-1, blank=True, null=True)
    email = models.CharField(max_length=-1, blank=True, null=True)
    phone = models.CharField(max_length=-1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, blank=True, null=True)
    province = models.ForeignKey('Province', on_delete=models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, blank=True, null=True)
    subdistrict = models.ForeignKey('Subdistrict', on_delete=models.DO_NOTHING, blank=True, null=True)
    postal_code = models.ForeignKey('PostalCode', on_delete=models.DO_NOTHING, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'person_ans'


class PostalCode(models.Model):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    province = models.ForeignKey('Province', on_delete=models.DO_NOTHING)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=-1)

    class Meta:
        db_table = 'postal_code'


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        db_table = 'province'


class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.DO_NOTHING)
    question_type = models.ForeignKey('QuestionType', on_delete=models.DO_NOTHING)
    question = models.TextField()
    rank = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    choices = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'question'


class QuestionType(models.Model):
    name = models.CharField(max_length=-1)

    class Meta:
        db_table = 'question_type'


class Subdistrict(models.Model):
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        db_table = 'subdistrict'


class User(models.Model):
    first_name = models.CharField(max_length=-1, blank=True, null=True)
    last_name = models.CharField(max_length=-1, blank=True, null=True)
    email = models.CharField(max_length=-1, blank=True, null=True)
    phone = models.CharField(max_length=-1, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, blank=True, null=True)
    subdistrict = models.ForeignKey(Subdistrict, on_delete=models.DO_NOTHING, blank=True, null=True)
    postal_code = models.ForeignKey(PostalCode, on_delete=models.DO_NOTHING, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'user'
