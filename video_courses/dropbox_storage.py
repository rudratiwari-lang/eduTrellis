import os
import dropbox
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from dropbox.files import WriteMode
from django.core.files.base import ContentFile


@deconstructible
class DropboxStorage(Storage):

    def __init__(self):
        self.client = dropbox.Dropbox(
            oauth2_refresh_token=settings.DROPBOX_REFRESH_TOKEN,
            app_key=settings.DROPBOX_APP_KEY,
            app_secret=settings.DROPBOX_APP_SECRET
        )

    # Ensure clean path
    def _clean_path(self, name):
        return f"/{name}".replace("//", "/")

    # 🔥 Upload file (supports large files)
    def _save(self, name, content):
        path = self._clean_path(name)
        file_size = content.size
        CHUNK_SIZE = 4 * 1024 * 1024  # 4MB

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
                offset=content.tell()
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
                        commit
                    )
                else:
                    self.client.files_upload_session_append_v2(
                        content.read(CHUNK_SIZE),
                        cursor
                    )
                    cursor.offset = content.tell()

        return name

    # 🔥 Fix overwrite behavior
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name

    # Check if file exists
    def exists(self, name):
        path = self._clean_path(name)
        try:
            self.client.files_get_metadata(path)
            return True
        except dropbox.exceptions.ApiError:
            return False

    # Open file
    def open(self, name, mode='rb'):
        path = self._clean_path(name)
        metadata, res = self.client.files_download(path)
        return ContentFile(res.content)

    # Generate temporary URL (4 hours)
    def url(self, name):
        path = self._clean_path(name)
        link = self.client.files_get_temporary_link(path)
        return link.link

    # Delete file
    def delete(self, name):
        path = self._clean_path(name)
        try:
            self.client.files_delete_v2(path)
        except dropbox.exceptions.ApiError:
            pass

    # File size (required for some libraries)
    def size(self, name):
        path = self._clean_path(name)
        metadata = self.client.files_get_metadata(path)
        return metadata.size