def normalize(doc: dict) -> dict:
    # ---------- top-level ----------
    doc.setdefault("vacancyId", None)
    doc.setdefault("name", None)
    doc.setdefault("@workSchedule", None)
    doc.setdefault("workExperience", None)
    doc.setdefault("employmentForm", None)
    doc.setdefault("totalResponsesCount", None)

    # ---------- publicationTime ----------
    publication = doc.setdefault("publicationTime", {})
    publication.setdefault("@timestamp", None)
    publication.setdefault("$", None)

    # ---------- company ----------
    company = doc.setdefault("company", {})
    company.setdefault("id", None)
    company.setdefault("name", None)
    company.setdefault("companySiteUrl", None)
    company.setdefault("@trusted", None)
    company.setdefault("accreditedITEmployer", None)

    # ---------- compensation ----------
    compensation = doc.setdefault("compensation", {})
    compensation.setdefault("from", None)
    compensation.setdefault("to", None)
    compensation.setdefault("currencyCode", None)
    compensation.setdefault("gross", None)
    compensation.setdefault("mode", None)
    compensation.setdefault("frequency", None)

    # ---------- area ----------
    area = doc.setdefault("area", {})
    area.setdefault("@id", None)
    area.setdefault("name", None)

    # ---------- address ----------
    address = doc.setdefault("address", {})
    address.setdefault("city", None)
    address.setdefault("street", None)
    address.setdefault("building", None)

    marker = address.setdefault("marker", {})
    marker.setdefault("@lat", None)
    marker.setdefault("@lng", None)

    # ---------- workScheduleByDays ----------
    schedules = doc.setdefault("workScheduleByDays", [])
    if not schedules:
        schedules.append({})
    schedules[0].setdefault("workScheduleByDaysElement", [])

    # ---------- workingHours ----------
    hours = doc.setdefault("workingHours", [])
    if not hours:
        hours.append({})
    hours[0].setdefault("workingHoursElement", [])

    # ---------- vacancyProperties ----------
    vacancy_properties = doc.setdefault("vacancyProperties", {})
    calculated_states = vacancy_properties.setdefault("calculatedStates", {})
    hh = calculated_states.setdefault("HH", {})
    hh.setdefault("premium", None)

    return doc