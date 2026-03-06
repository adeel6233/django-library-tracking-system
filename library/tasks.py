from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task(name="check_overdue_loans")
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=timezone.now().date())

    for overdue_loan in overdue_loans:
        send_mail(subject="Reminder for Overdue Loan", 
                  message=f"Hi, {overdue_loan.member.user.username} the book {overdue_loan.book.title}\
                  was overdue on {overdue_loan.due_date}. Please return it ASAP.",
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[overdue_loan.member.user.email],
                  fail_silently=False,
        )

    return f"Emails sent for overdue loans successfully."
