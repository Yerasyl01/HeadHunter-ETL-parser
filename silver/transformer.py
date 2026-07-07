import polars as pl

VACANCY_COLUMNS = {
    "vacancy_id": pl.col("vacancyId"),
    "title": pl.col("name"),
    "published_at": pl.col("publicationTime").struct.field("$").str.to_datetime("%Y-%m-%dT%H:%M:%S%.f%:z"),
    "responses_count": pl.col("totalResponsesCount"),
}
COMPANY_COLUMNS = {
    "company_id": pl.col("company").struct.field("id"),
    "company_name": pl.col("company").struct.field("name"),
    "company_site": pl.col("company").struct.field("companySiteUrl"),
    "company_trusted": pl.col("company").struct.field("@trusted"),
    "company_accredited_it": pl.col("company").struct.field("accreditedITEmployer"),
}
COMPENSATION_COLUMNS = {
    "salary_from": pl.col("compensation").struct.field("from"),
    "salary_to": pl.col("compensation").struct.field("to"),
    "salary_currency": pl.col("compensation").struct.field("currencyCode"),
    "salary_gross": pl.col("compensation").struct.field("gross"),
    "salary_mode": pl.col("compensation").struct.field("mode"),
    "salary_frequency": pl.col("compensation").struct.field("frequency"),
}
LOCATION_COLUMNS = {
    "area_id": pl.col("area").struct.field("@id"),
    "area_name": pl.col("area").struct.field("name"),
    "city": pl.col("address").struct.field("city"),
    "street": pl.col("address").struct.field("street"),
    "building": pl.col("address").struct.field("building"),
    "latitude": pl.col("address").struct.field("marker").struct.field("@lat"),
    "longitude": pl.col("address").struct.field("marker").struct.field("@lng"),
}
EMPLOYMENT_COLUMNS = {
    "work_schedule": pl.col("@workSchedule"),
    "work_schedule_by_days": pl.col("workScheduleByDays").list.first().struct.field("workScheduleByDaysElement"),
    "working_hours": pl.col("workingHours").list.first().struct.field("workingHoursElement"),
    "work_experience": pl.col("workExperience"),
    "employment_form": pl.col("employmentForm"),
    "premium": pl.col("vacancyProperties").struct.field("calculatedStates").struct.field("HH").struct.field("premium"),
}

class HHVacancyTransformer:
    def transform(self, bronze: pl.DataFrame) -> pl.DataFrame:
        return bronze.select(
            **VACANCY_COLUMNS,
            **COMPANY_COLUMNS,
            **COMPENSATION_COLUMNS,
            **LOCATION_COLUMNS,
            **EMPLOYMENT_COLUMNS,
        )
