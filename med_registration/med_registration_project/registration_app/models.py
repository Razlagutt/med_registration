from django.db import models


class Specialty(models.Model):
    title = models.CharField(max_length=50, verbose_name='Специальность')

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return self.title


class Doctors(models.Model):
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, verbose_name='ФИО')

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return self.full_name


class Schedule(models.Model):
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, verbose_name='Врач', on_delete=models.CASCADE)
    client = models.CharField(max_length=255, verbose_name='Посетитель')
    pub_date = models.DateTimeField(max_length=15, verbose_name='Дата', blank='True')

    def __str__(self):
        return self.client

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'График'
