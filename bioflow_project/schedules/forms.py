from django import forms
from .models import Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = [
            'equipment',
            'start_datetime',
            'end_datetime',
            'purpose',
            'notes'
        ]

        widgets = {
            'start_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'end_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'purpose': forms.Textarea(
                attrs={'rows': 3}
            ),
            'notes': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        equipment = cleaned_data.get('equipment')
        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('end_datetime')

        if equipment and start and end:

            if end <= start:
                raise forms.ValidationError(
                    'O horário final deve ser maior que o inicial.'
                )

            conflicts = Schedule.objects.filter(
                equipment=equipment,
                status__in=['pending', 'confirmed'],
                start_datetime__lt=end,
                end_datetime__gt=start,
            )

            if self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            if conflicts.exists():
                raise forms.ValidationError(
                    'Já existe um agendamento nesse horário.'
                )

        return cleaned_data
