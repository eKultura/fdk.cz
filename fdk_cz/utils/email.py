"""
Email utilities for FDK.cz
Handles sending emails for project invitations, task notifications, etc.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from django.conf import settings


def send_email(recipient, subject, html_content, text_content=None):
    """
    Send email using SMTP (Seznam.cz)

    Args:
        recipient: Email address of recipient
        subject: Email subject
        html_content: HTML content of email
        text_content: Plain text fallback (optional)
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = os.getenv("FDK_NOREPLY_EMAIL", "noreply@fdk.cz")
        msg['To'] = recipient
        msg['Subject'] = subject

        # Add text/plain part if provided
        if text_content:
            part1 = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(part1)

        # Add HTML part
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part2)

        # Send via SMTP
        with smtplib.SMTP_SSL("smtp.seznam.cz", 465) as smtp:
            smtp.login(
                os.getenv("FDK_NOREPLY_EMAIL"),
                os.getenv("FDK_NOREPLY_PASSWORD")
            )
            smtp.send_message(msg)

        print(f"[✔] Email sent to {recipient}: {subject}")
        return True

    except Exception as e:
        print(f"[✖] Error sending email to {recipient}: {e}")
        return False


def send_project_invitation_email(email, project, role, invited_by):
    """
    Send invitation email to unregistered user

    Args:
        email: Email address of invitee
        project: Project instance
        role: ProjectRole instance
        invited_by: User who sent invitation
    """
    context = {
        'email': email,
        'project': project,
        'role': role,
        'invited_by': invited_by,
        'site_url': os.getenv("SITE_URL", "https://fdk.cz"),
    }

    html_content = render_to_string('emails/project_invitation.html', context)
    text_content = render_to_string('emails/project_invitation.txt', context)

    subject = f"Pozvánka do projektu {project.name} na FDK.cz"

    return send_email(email, subject, html_content, text_content)


def send_project_member_added_email(user, project, role, added_by):
    """
    Send notification to existing user that they were added to project

    Args:
        user: User instance
        project: Project instance
        role: ProjectRole instance
        added_by: User who added them
    """
    context = {
        'user': user,
        'project': project,
        'role': role,
        'added_by': added_by,
        'site_url': os.getenv("SITE_URL", "https://fdk.cz"),
        'project_url': f"{os.getenv('SITE_URL', 'https://fdk.cz')}/projekt/{project.project_id}/",
    }

    html_content = render_to_string('emails/project_member_added.html', context)
    text_content = render_to_string('emails/project_member_added.txt', context)

    subject = f"Byli jste přidáni do projektu {project.name}"

    return send_email(user.email, subject, html_content, text_content)


def send_task_assignment_email(user, task, project, assigned_by):
    """
    Send notification when task is assigned to user

    Args:
        user: User who was assigned the task
        task: ProjectTask instance
        project: Project instance
        assigned_by: User who assigned the task
    """
    # Check if user has notifications enabled
    # TODO: Add notification preferences to user model

    context = {
        'user': user,
        'task': task,
        'project': project,
        'assigned_by': assigned_by,
        'site_url': os.getenv("SITE_URL", "https://fdk.cz"),
        'task_url': f"{os.getenv('SITE_URL', 'https://fdk.cz')}/ukol/{task.task_id}/",
    }

    html_content = render_to_string('emails/task_assigned.html', context)
    text_content = render_to_string('emails/task_assigned.txt', context)

    subject = f"Byl vám přiřazen úkol: {task.title}"

    return send_email(user.email, subject, html_content, text_content)
