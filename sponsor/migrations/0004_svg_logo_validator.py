from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0003_auto_20210906_0915"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sponsor",
            name="logo",
            field=models.FileField(
                blank=True,
                help_text="Make sure logo is not bigger than 200 pixels wide. Accepted formats: PNG, JPG, GIF, WebP, SVG.",
                null=True,
                upload_to="event/sponsors/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["png", "jpg", "jpeg", "gif", "webp", "svg"]
                    )
                ],
            ),
        ),
    ]