import os
import dropbox
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from dropbox.files import WriteMode

@deconstructible
class DropboxStorage(Storage):

    def __init__(self):
        self.client = dropbox.Dropbox(settings.DROPBOX_ACCESS_TOKEN)

    # 🔥 FIXED: Supports Large File Upload (Chunk Upload)
    def _save(self, name, content):
        path = f"/{name}"
        file_size = content.size
        CHUNK_SIZE = 4 * 1024 * 1024  # 4MB

        # Reset pointer just in case
        content.seek(0)

        if file_size <= CHUNK_SIZE:
            self.client.files_upload(
                content.read(),
                path,
                mode=WriteMode.overwrite
            )
        else:
            upload_session_start_result = self.client.files_upload_session_start(
                content.read(CHUNK_SIZE)
            )

            cursor = dropbox.files.UploadSessionCursor(
                session_id=upload_session_start_result.session_id,
                offset=content.tell(),
            )

            commit = dropbox.files.CommitInfo(
                path=path,
                mode=WriteMode.overwrite
            )

            while content.tell() < file_size:
                if (file_size - content.tell()) <= CHUNK_SIZE:
                    self.client.files_upload_session_finish(
                        content.read(CHUNK_SIZE),
                        cursor,
                        commit,
                    )
                else:
                    self.client.files_upload_session_append_v2(
                        content.read(CHUNK_SIZE),
                        cursor,
                    )
                    cursor.offset = content.tell()

        return name

    # Check if file exists
    def exists(self, name):
        try:
            self.client.files_get_metadata(f"/{name}")
            return True
        except dropbox.exceptions.ApiError:
            return False

    # Open file (Important for MoviePy duration extraction)
    def open(self, name, mode='rb'):
        metadata, res = self.client.files_download(f"/{name}")
        from django.core.files.base import ContentFile
        return ContentFile(res.content)

    # Generate Temporary URL (4 hours validity)
    def url(self, name):
        link = self.client.files_get_temporary_link(f"/{name}")
        return link.link

    # Optional: Delete file
    def delete(self, name):
        try:
            self.client.files_delete_v2(f"/{name}")
        except dropbox.exceptions.ApiError:
            pass