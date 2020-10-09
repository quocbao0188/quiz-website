from import_export import resources
from .models import Question

class QuizResource(resources.ModelResource):
    
    class Meta:
        model = Question
        # fields = ('catago__title',)