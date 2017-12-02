from django.db import models
from DjangoUeditor.models import UEditorField
from account.models import User


class Problem(models.Model):
    title = models.CharField(max_length=30)
    description = UEditorField('description',
                               height=100,
                               width=200,
                               default=u'',
                               blank=True,
                               imagePath="uploads/images/",
                               toolbars='besttome',
                               filePath='uploads/files/')
    input_description = models.TextField()
    output_description = models.TextField()
    input = models.TextField()
    output = models.TextField()
    hint = UEditorField('hint',
                        height=100,
                        width=200,
                        default=u'',
                        blank=True,
                        imagePath="uploads/images/",
                        toolbars='besttome',
                        filePath='uploads/files/')
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    time_limit = models.FloatField()
    memory_limit = models.IntegerField()
    visible = models.BooleanField(default=True)
    spj = models.BooleanField(default=False)
    total_submit_number = models.IntegerField(default=0)
    total_accepted_number = models.IntegerField(default=0)
    source = models.CharField(max_length=20, blank=True, null=True)
    difficulty = models.IntegerField(blank=True)
    show_id = models.CharField(max_length=5, blank=True)

    class Meta:
        db_table = "problem"

    def __str__(self):
        return self.title
