from models.hh import HHVacancy

class HHVacancyTransformer:
    def transform(self, vacancy: HHVacancy) -> HHVacancy:
        return vacancy.copy()
