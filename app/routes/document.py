import os
import uuid

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import DocumentUploadForm
from app.models import Document, Pet

# ==================================================
# Helpers
# ==================================================


def get_pet_or_404(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id,
    ).first_or_404()

    return pet


def get_document_or_404(document_id):

    document = (
        Document.query.join(Pet)
        .filter(
            Document.id == document_id,
            Pet.user_id == current_user.id,
        )
        .first_or_404()
    )

    return document


def upload_folder():

    folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "documents",
    )

    os.makedirs(folder, exist_ok=True)

    return folder


# ==================================================
# Documents
# ==================================================


@app.route("/pets/<int:pet_id>/documents")
@login_required
def documents(pet_id):

    pet = get_pet_or_404(pet_id)

    documents = (
        Document.query.filter_by(
            pet_id=pet.id,
        )
        .order_by(Document.uploaded_at.desc())
        .all()
    )

    return render_template(
        "documents/index.html",
        pet=pet,
        documents=documents,
    )


# ==================================================
# Upload
# ==================================================


@app.route(
    "/pets/<int:pet_id>/documents/add",
    methods=["GET", "POST"],
)
@login_required
def add_document(pet_id):

    pet = get_pet_or_404(pet_id)

    form = DocumentUploadForm()

    if form.validate_on_submit():

        uploaded = form.file.data

        original_filename = secure_filename(uploaded.filename)

        extension = original_filename.rsplit(
            ".",
            1,
        )[-1].lower()

        filename = f"{uuid.uuid4().hex}.{extension}"

        path = os.path.join(
            upload_folder(),
            filename,
        )

        uploaded.save(path)

        document = Document(
            pet_id=pet.id,
            title=form.title.data,
            document_type=form.document_type.data,
            filename=filename,
            original_filename=original_filename,
            file_size=os.path.getsize(path),
            notes=form.notes.data,
        )

        db.session.add(document)

        db.session.commit()

        flash(
            "Document uploaded successfully.",
            "success",
        )

        return redirect(
            url_for(
                "documents",
                pet_id=pet.id,
            )
        )

    return render_template(
        "documents/upload.html",
        pet=pet,
        form=form,
    )


# ==================================================
# Download
# ==================================================


@app.route("/documents/<int:document_id>/download")
@login_required
def download_document(document_id):

    document = get_document_or_404(document_id)

    return send_from_directory(
        upload_folder(),
        document.filename,
        download_name=document.original_filename,
        as_attachment=False,
    )


# ==================================================
# Delete
# ==================================================


@app.route(
    "/documents/<int:document_id>/delete",
    methods=["POST"],
)
@login_required
def delete_document(document_id):

    document = get_document_or_404(document_id)

    path = os.path.join(
        upload_folder(),
        document.filename,
    )

    if os.path.exists(path):

        os.remove(path)

    pet_id = document.pet_id

    db.session.delete(document)

    db.session.commit()

    flash(
        "Document deleted.",
        "success",
    )

    return redirect(
        url_for(
            "documents",
            pet_id=pet_id,
        )
    )
