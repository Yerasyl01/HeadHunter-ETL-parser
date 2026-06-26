from db.mongo import mongodb

def create_indexes() -> None:
    mongodb.vacancies.create_index('_id')
    mongodb.vacancies.create_index('published_at')
    mongodb.vacancies.create_index('area.id')
    mongodb.vacancies.create_index('employer.id')
