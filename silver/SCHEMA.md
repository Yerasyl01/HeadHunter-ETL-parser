# Silver Layer Schema

## Purpose

The Silver layer transforms raw HH vacancy documents stored in MongoDB (Bronze) into a clean, flat, and typed dataset suitable for analytics.

The output is a Polars `DataFrame` written to a Parquet file.

---

## Dataset

One row represents **one vacancy**.

---

## Schema

| Column                  | Type           | Source                                          | Description                                                 |
| ----------------------- | -------------- | ----------------------------------------------- | ----------------------------------------------------------- |
| `vacancy_id`            | `Int64`        | `vacancyId`                                     | Unique vacancy identifier.                                  |
| `title`                 | `String`       | `name`                                          | Vacancy title.                                              |
| `company_id`            | `Int64`        | `company.id`                                    | Employer identifier.                                        |
| `company_name`          | `String`       | `company.name`                                  | Employer name.                                              |
| `company_site`          | `String`       | `company.companySiteUrl`                        | Employer website.                                           |
| `company_trusted`       | `Boolean`      | `company.@trusted`                              | Whether the employer is trusted by HH.                      |
| `company_accredited_it` | `Boolean`      | `company.accreditedITEmployer`                  | Indicates whether the employer is an accredited IT company. |
| `salary_from`           | `Int64`        | `compensation.from`                             | Minimum salary.                                             |
| `salary_to`             | `Int64`        | `compensation.to`                               | Maximum salary.                                             |
| `salary_currency`       | `String`       | `compensation.currencyCode`                     | Salary currency.                                            |
| `salary_gross`          | `Boolean`      | `compensation.gross`                            | `true` if salary is before taxes.                           |
| `salary_mode`           | `String`       | `compensation.mode`                             | Salary period (e.g. `MONTH`).                               |
| `salary_frequency`      | `String`       | `compensation.frequency`                        | Salary payment frequency.                                   |
| `published_at`          | `Datetime`     | `publicationTime.$`                             | Vacancy publication timestamp.                              |
| `area_id`               | `Int64`        | `area.@id`                                      | HH area identifier.                                         |
| `area_name`             | `String`       | `area.name`                                     | Area name.                                                  |
| `city`                  | `String`       | `address.city`                                  | City.                                                       |
| `street`                | `String`       | `address.street`                                | Street.                                                     |
| `building`              | `String`       | `address.building`                              | Building number.                                            |
| `latitude`              | `Float64`      | `address.marker.@lat`                           | Vacancy latitude.                                           |
| `longitude`             | `Float64`      | `address.marker.@lng`                           | Vacancy longitude.                                          |
| `work_schedule`         | `String`       | `@workSchedule`                                 | General work schedule.                                      |
| `work_schedule_by_days` | `List[String]` | `workScheduleByDays`                            | Supported work schedule patterns (e.g. `FIVE_ON_TWO_OFF`).  |
| `working_hours`         | `List[String]` | `workingHours`                                  | Available working-hour options (e.g. `HOURS_8`).            |
| `work_experience`       | `String`       | `workExperience`                                | Required experience level.                                  |
| `employment_form`       | `String`       | `employmentForm`                                | Employment type.                                            |
| `premium`               | `Boolean`      | `vacancyProperties.calculatedStates.HH.premium` | Whether the vacancy has HH Premium status.                  |
| `responses_count` | `Int64`        | `totalResponsesCount`                           | Total number of responses received.                         |

---

## Transformation Rules

* Nested objects are flattened into columns.
* Unnecessary UI and platform metadata are removed.
* Columns are renamed using `snake_case`.
* Datetime values are converted to Polars `Datetime`.
* List-valued fields remain `List[String]`.
* Nullable Bronze fields remain nullable in the Silver dataset.
* The output is written as a Parquet dataset.
