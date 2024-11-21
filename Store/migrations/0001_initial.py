# Generated by Django 4.2 on 2024-11-21 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField(default=1)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Processing', 'Processing'), ('Failed', 'Failed')], default='Processing', max_length=100)),
                ('payment_method', models.CharField(blank=True, choices=[('Paypal', 'Paypal'), ('Google_Pay', 'Google_Pay'), ('PhonePay', 'PhonePay'), ('RazorPay', 'Razorpay')], default=None, max_length=100, null=True)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, help_text='The original total before', max_digits=12)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Amount your have saved', max_digits=12, null=True)),
                ('order_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=25, prefix='')),
                ('payment_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('coupons', models.ManyToManyField(blank=True, to='Store.coupon')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('vendors', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Order',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, default='product.jpg', null=True, upload_to='images')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Sale Price')),
                ('regular_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Regural Price')),
                ('stock', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Shipping Amount')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Disabled', 'Disabled')], default='Published', max_length=30)),
                ('featured', models.BooleanField(default=False, verbose_name='Marketplace Featured')),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='123456890', length=5, max_length=50, prefix='SKU', unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Store.category')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Products',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Variant Name')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item Title')),
                ('content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item Content')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cariant_items', to='Store.variant')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')], default=None)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='Store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('shipping_service', models.CharField(blank=True, choices=[('BLUEDART', 'Blue Dart'), ('DTDC', 'DTDC'), ('DELHIVERY', 'Delhivery'), ('EKART', 'Ekart Logistics'), ('INDIA_POST', 'India Post'), ('XPRESSBEES', 'XpressBees'), ('E_COM_EXPRESS', 'Ecom Express'), ('FEDEX', 'FedEx')], default=None, max_length=100, null=True)),
                ('tracking_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('qty', models.IntegerField(default=0)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('inital_total', models.DecimalField(decimal_places=2, default=0.0, help_text='The original Amount before', max_digits=12)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Amount Saved', max_digits=12, null=True)),
                ('applied_coupon', models.BooleanField(default=False)),
                ('item_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=25, prefix='')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('coupons', models.ManyToManyField(blank=True, to='Store.coupon')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.product')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_order_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(default='gallery.jpg', upload_to='images')),
                ('gallery_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('cart_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
