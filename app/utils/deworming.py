from datetime import timedelta


def get_age_in_months(birth_date, reference_date):
    """
    Returns the pet's age in completed months
    on the given reference date.
    """

    if birth_date is None:
        return None

    months = (
        (reference_date.year - birth_date.year) * 12
        + reference_date.month
        - birth_date.month
    )

    if reference_date.day < birth_date.day:
        months -= 1

    return max(months, 0)


def calculate_deworming_schedule(birth_date, date_given):
    """
    Calculates:
    - schedule used
    - age at deworming
    - next due date
    """

    age_months = get_age_in_months(
        birth_date,
        date_given,
    )

    if age_months is None:
        return {
            "schedule_used": "Manual",
            "age_at_deworming": "Unknown",
            "next_due": date_given,
        }

    # Puppies under 3 months
    if age_months < 3:

        next_due = date_given + timedelta(days=14)

        return {
            "schedule_used": "Every 2 Weeks",
            "age_at_deworming": f"{age_months} months",
            "next_due": next_due,
        }

    # Puppies 3–5 months
    if age_months < 6:

        month = date_given.month + 1
        year = date_given.year

        if month > 12:
            month = 1
            year += 1

        try:
            next_due = date_given.replace(
                year=year,
                month=month,
            )
        except ValueError:
            # Handles 31st -> 30th / Feb
            next_due = (
                date_given.replace(day=1, year=year, month=month) + timedelta(days=31)
            ).replace(day=1) - timedelta(days=1)

        return {
            "schedule_used": "Monthly",
            "age_at_deworming": f"{age_months} months",
            "next_due": next_due,
        }

    # 6 months and above

    month = date_given.month + 3
    year = date_given.year

    while month > 12:
        month -= 12
        year += 1

    try:
        next_due = date_given.replace(
            year=year,
            month=month,
        )
    except ValueError:
        next_due = (
            date_given.replace(day=1, year=year, month=month) + timedelta(days=31)
        ).replace(day=1) - timedelta(days=1)

    years = age_months // 12
    remaining = age_months % 12

    if years == 0:
        age_string = f"{remaining} months"

    elif remaining == 0:

        if years == 1:
            age_string = "1 year"
        else:
            age_string = f"{years} years"

    else:

        if years == 1:
            age_string = f"1 year {remaining} months"
        else:
            age_string = f"{years} years {remaining} months"

    return {
        "schedule_used": "Every 3 Months",
        "age_at_deworming": age_string,
        "next_due": next_due,
    }
