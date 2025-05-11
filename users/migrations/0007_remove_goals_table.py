from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userfaceimage_checkincheckout_is_valid_checkin_and_more'),  # Thay thế bằng migration cuối cùng của bạn
    ]

    operations = [
        migrations.DeleteModel(
            name='Goals',
        ),
    ]
