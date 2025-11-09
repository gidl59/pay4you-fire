from datetime import datetime, timedelta

def upload_to_firebase(file_storage, folder="uploads"):
    try:
        client = get_storage_client()
        if not client:
            return None
        bucket = client.bucket(FIREBASE_BUCKET)

        import os, uuid
        ext = os.path.splitext(file_storage.filename or "")[1].lower()
        key = f"{folder}/{datetime.utcnow().strftime('%Y/%m/%d')}/{uuid.uuid4().hex}{ext}"

        blob = bucket.blob(key)
        blob.upload_from_file(file_storage.stream, content_type=file_storage.mimetype)

        # URL firmato (funziona anche con regole restrittive di Firebase Storage)
        url = blob.generate_signed_url(
            expiration=datetime.utcnow() + timedelta(days=3650),
            method="GET"
        )
        return url
    except Exception as e:
        app.logger.exception("Firebase upload failed: %s", e)
        return None
