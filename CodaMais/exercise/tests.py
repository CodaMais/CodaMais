from django.test import TestCase
from exercise.form import  ExerciseForm


class TestExerciseRegistration(TestCase):
    title = 'Basic Exercise'
    category = 1
    text = 'Text Basic Exercise.'
    score = 10
    image = None
    deprecated = 0
    input_exercise = 'Input Basic Exercise.'
    output_exercise = 'Output Basic Exercise.'
    form_valid = {}

    def setup(self):
        self.form_valid = {'title' : self.title,
                     'category' : self.category,
                     'text' : self.text,
                     'score' : self.score,
                     'image' : self.image,
                     'deprecated' : self.deprecated,
                     'input_exercise' : self.input_exercise,
                     'output_exercise' : self.output_exercise}

    def test_ExerciseForm_valid(self):
        exercise_form = ExerciseForm(self.form_valid)
        self.assertTrue(exercise_form.is_valid)
