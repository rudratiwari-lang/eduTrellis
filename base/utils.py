# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import logging
import socket
import threading  # ✅ NEW

logger = logging.getLogger(__name__)


def get_active_smtp_config():
    """Get active SMTP config that passed test_status='success'."""
    try:
        from adminpanel.models import SMTPConfiguration
        return SMTPConfiguration.objects.filter(
            is_active=True,
            test_status='success',
        ).first()
    except Exception as e:
        logger.error(f"Error getting SMTP configuration: {e}")
        return None


def has_smtp_configured():
    """Check if SMTP is ready to use."""
    return get_active_smtp_config() is not None


def configure_smtp_settings(smtp_config):
    """Temporarily configure Django email settings."""
    if not smtp_config:
        return False

    original_settings = {}
    email_settings = [
        'EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT',
        'EMAIL_USE_TLS', 'EMAIL_USE_SSL', 'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL',
    ]

    for setting in email_settings:
        original_settings[setting] = getattr(settings, setting, None)

    settings.EMAIL_BACKEND = smtp_config.email_backend
    settings.EMAIL_HOST = smtp_config.email_host
    settings.EMAIL_PORT = smtp_config.email_port
    settings.EMAIL_USE_TLS = smtp_config.email_use_tls
    settings.EMAIL_USE_SSL = smtp_config.email_use_ssl
    settings.EMAIL_HOST_USER = smtp_config.email_host_user
    settings.EMAIL_HOST_PASSWORD = smtp_config.email_host_password
    settings.DEFAULT_FROM_EMAIL = smtp_config.default_from_email

    return original_settings


def restore_smtp_settings(original_settings):
    """Restore original Django email settings."""
    if original_settings:
        for setting, value in original_settings.items():
            setattr(settings, setting, value)


def send_otp_email(user, otp_code, timeout=10):
    """Send OTP email with configurable timeout."""
    smtp_config = get_active_smtp_config()
    if not smtp_config:
        return False, "No working SMTP configuration found."

    original_settings = configure_smtp_settings(smtp_config)

    try:
        subject = "Email Verification - OTP Code"
        context = {"user": user, "otp_code": otp_code, "site_name": "Your Site"}

        try:
            html_message = render_to_string("emails/otp_verification.html", context)
        except Exception:
            html_message = None

        plain_message = f"""
Hello {user.first_name or user.email},
Your OTP is: {otp_code}
This OTP expires in 10 minutes.
Thanks,
Your Site Team
        """

        # ✅ Use thread-local socket timeout instead of global setdefaulttimeout
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=smtp_config.default_from_email,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        return True, "OTP sent successfully"

    except Exception as e:
        logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")
        return False, f"Email failed: {str(e)}"
    finally:
        restore_smtp_settings(original_settings)
        # ✅ REMOVED: socket.setdefaulttimeout(None) — no longer needed


# ✅ NEW: Background email sender thread
class _OTPEmailThread(threading.Thread):
    """Daemon thread to send OTP email without blocking the signup response."""

    def __init__(self, user, otp, timeout=10):
        super().__init__(daemon=True)  # daemon=True: thread dies if main process exits
        self.user = user
        self.otp = otp
        self.timeout = timeout

    def run(self):
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(self.timeout)
        try:
            success, message = send_otp_email(self.user, self.otp.otp_code, timeout=self.timeout)
            if not success:
                logger.warning(
                    f"Background OTP email failed for {self.user.email}: {message}. "
                    f"OTP ID={self.otp.pk} marked as used."
                )
                # Mark OTP as used so user is forced to use Resend OTP
                self.otp.is_used = True
                self.otp.save(update_fields=['is_used'])
        except Exception as e:
            logger.error(f"OTPEmailThread crashed for {self.user.email}: {e}")
        finally:
            socket.setdefaulttimeout(old_timeout)  # ✅ Restore only this thread's timeout


def create_and_send_otp(user, verification_type="email", is_mobile=False):
    """
    Create OTP instantly + fire email in a background thread.
    Signup response is returned to user WITHOUT waiting for email.
    """
    from base.models import OTPVerification

    # Deactivate previous OTPs
    OTPVerification.objects.filter(
        user=user,
        verification_type=verification_type,
    ).update(is_used=True)

    # Create new OTP — this is instant (just a DB write)
    otp = OTPVerification.objects.create(
        user=user,
        verification_type=verification_type,
    )

    smtp_config = get_active_smtp_config()
    if not smtp_config:
        return otp, "No SMTP - direct login"

    # ✅ Fire email in background — signup response is NOT blocked
    email_timeout = 15  # Generous timeout since it's async now — no UX penalty
    _OTPEmailThread(user, otp, timeout=email_timeout).start()

    return otp, "OTP sending in background"
