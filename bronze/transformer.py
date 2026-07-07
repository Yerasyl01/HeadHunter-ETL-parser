from models.types import Vacancy

class VacancyTransformer:
    def transform(self, vacancy: Vacancy) -> Vacancy:
        return vacancy.copy()
