# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from nope.accounts.models import User
#
#
# @receiver(post_save, sender=User)
# def after_create_user(sender, instance, created, **kwargs):
#     """Reward"""
#     if created:
#         instance.set_password(instance.username[-8:] or '12345678')
#         instance.save()
