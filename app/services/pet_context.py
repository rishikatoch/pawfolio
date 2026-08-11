from app.models import (
    Pet,
    Vaccination,
    Deworming,
    VetVisit,
    Medication,
    WeightRecord,
)


def build_pet_context(user_id):
    """
    Build a read-only AI context from the current user's
    Pawfolio pet health records.
    """

    pets = Pet.query.filter_by(user_id=user_id).all()

    if not pets:
        return "No pets are currently registered in Pawfolio."

    context = []

    for pet in pets:
        context.append(f"""
PET
Name: {pet.name}
Breed: {pet.breed or "Not provided"}
Gender: {pet.gender or "Not provided"}
Age: {pet.age_display}
""")

        vaccinations = (
            Vaccination.query.filter_by(pet_id=pet.id)
            .order_by(Vaccination.next_due.asc())
            .all()
        )

        if vaccinations:
            context.append("VACCINATIONS")

            for vaccination in vaccinations:
                context.append(
                    f"- {vaccination.vaccine_name}: "
                    f"given {vaccination.date_given}, "
                    f"next due {vaccination.next_due}, "
                    f"status {vaccination.status}"
                )
        else:
            context.append("VACCINATIONS\n- No records")

        dewormings = (
            Deworming.query.filter_by(pet_id=pet.id)
            .order_by(Deworming.next_due.asc())
            .all()
        )

        if dewormings:
            context.append("DEWORMING")

            for deworming in dewormings:
                context.append(
                    f"- {deworming.medicine_name}: "
                    f"given {deworming.date_given}, "
                    f"next due {deworming.next_due}, "
                    f"status {deworming.status}"
                )
        else:
            context.append("DEWORMING\n- No records")

        vet_visits = (
            VetVisit.query.filter_by(pet_id=pet.id)
            .order_by(VetVisit.visit_date.desc())
            .all()
        )

        if vet_visits:
            context.append("VETERINARY VISITS")

            for visit in vet_visits:
                context.append(
                    f"- {visit.visit_date}: "
                    f" {visit.clinic_name}, "
                    f" {visit.veterinarian}; "
                    f"reason: {visit.reason}; "
                    f"diagnosis: {visit.diagnosis or 'Not provided'}; "
                    f"treatment: {visit.treatment or 'Not provided'}"
                )
        else:
            context.append("VETERINARY VISITS\n- No records")

        medications = (
            Medication.query.filter_by(pet_id=pet.id)
            .order_by(Medication.start_date.desc())
            .all()
        )

        if medications:
            context.append("MEDICATIONS")

            for medication in medications:
                context.append(
                    f"- {medication.medicine_name}: "
                    f"dosage {medication.dosage or 'Not provided'}, "
                    f"frequency {medication.frequency}, "
                    f"start {medication.start_date}, "
                    f"end {medication.end_date or 'Ongoing'}, "
                    f"reason {medication.reason or 'Not provided'}"
                )
        else:
            context.append("MEDICATIONS\n- No records")

        weights = (
            WeightRecord.query.filter_by(pet_id=pet.id)
            .order_by(WeightRecord.measurement_date.desc())
            .all()
        )

        if weights:
            context.append("WEIGHT HISTORY")

            for weight in weights:
                context.append(f"- {weight.measurement_date}: " f"{weight.weight} kg")
        else:
            context.append("WEIGHT HISTORY\n- No records")

    return "\n".join(context)
