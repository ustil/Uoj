from django.db import models
from DjangoUeditor.models import UEditorField
from account.models import User


class Notice(models.Model):
    title = models.CharField(max_length=100)
    description = UEditorField('description', height=100,
                               width=200, default=u'', blank=True,
                               imagePath="uploads/images/",
                               toolbars='besttome', filePath='uploads/files/')
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    class Meta:
        db_table = "Notice"

    def __str__(self):
        return self.title
