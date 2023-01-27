from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

  def create_user(self, userid, user_name, mail, date_of_birth, password, **extra_fields):
    if not mail:
      raise ValueError('must have user email')
    if not userid:
      raise ValueError('must have user userid')
    if not user_name:
      raise ValueError('must have user name')
    if not password:
      raise ValueError('must have password')

    user = self.model(
      mail = self.normalize_email(mail),
      userid = userid,
      user_name = user_name,
      date_of_birth = date_of_birth,
      **extra_fields
    )

    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, userid, mail, password):
    user = self.create_user(
            mail=mail,
            userid=userid,
            user_name = '관리자',
            date_of_birth = '1999-09-09',
    )
    user.is_admin = True
    user.is_superuser = True
    user.set_password(password)
    user.save(using=self._db)
    return user

class Userdata(AbstractBaseUser):

    EXP_CHOICES = (
      ('0', '없음'),
      ('1', '1년이하'),
      ('3', '3년이하'),
      ('5', '5년이하'),
    )

    userid = models.CharField(primary_key=True, max_length=30, null=False, blank=False, unique=True, verbose_name="아이디")
    user_name = models.CharField(max_length=30, blank=False, null=False, unique=False, verbose_name="이름")
    mail = models.CharField(max_length=50, blank=False, null=False, unique=True, verbose_name="이메일")
 
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="생년월일")
    experience = models.CharField(max_length=5, choices=EXP_CHOICES, verbose_name="투자 경험")
    
    now_money = models.BigIntegerField(blank=True, null=True, default=100000000)
    invest_value = models.BigIntegerField(blank=True, null=True, default=0)
    total_money = models.BigIntegerField(blank=True, null=True, default=100000000)
    
    last_login=None
    # password_confirmation = models.CharField(max_length=128)
    # 비밀번호
    password = models.CharField(max_length=128, unique=True, blank=False, null=False, db_column='user_password')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'userid'
    EMAIL_FIELD = 'mail'
    REQUIRED_FIELDS = ['mail', 'user_name', 'password']

    class Meta:
        managed = False
        db_table = 'userdata'


class Macroeconomicindicators(models.Model):
    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return True

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

    @property
    def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin
      
    date_time = models.DateField(blank=True, null=True)
    kospi = models.FloatField(blank=True, null=True)
    america_top_500 = models.FloatField(blank=True, null=True)
    gold = models.FloatField(blank=True, null=True)
    copper = models.FloatField(blank=True, null=True)
    k_gov3 = models.FloatField(blank=True, null=True)
    usd_k = models.FloatField(blank=True, null=True)
    inflation = models.IntegerField(blank=True, null=True)
    treasury_bonds = models.IntegerField(blank=True, null=True)
    tightening = models.IntegerField(blank=True, null=True)
    normality = models.IntegerField(blank=True, null=True)
    powell = models.IntegerField(blank=True, null=True)
    dispute = models.IntegerField(blank=True, null=True)
    japan = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    chairman = models.IntegerField(blank=True, null=True)
    remarks = models.IntegerField(blank=True, null=True)
    thought = models.IntegerField(blank=True, null=True)
    effect = models.IntegerField(blank=True, null=True)
    anxiety = models.IntegerField(blank=True, null=True)
    buying = models.IntegerField(blank=True, null=True)
    volatility = models.IntegerField(blank=True, null=True)
    early_stage = models.IntegerField(blank=True, null=True)
    decline = models.IntegerField(blank=True, null=True)
    learning_result = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'macroeconomicindicators'


class Stockcode(models.Model):
    stock_code = models.CharField(primary_key=True, max_length=7)
    stock_name = models.CharField(max_length=50, blank=True, null=True)
    short_result = models.FloatField(blank=True, null=True)
    long_result = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stockcode'


class Stockdata(models.Model):
    stock_code = models.ForeignKey(Stockcode, models.CASCADE, db_column='stock_code', blank=True, null=True)
    data_time = models.DateField(blank=True, null=True)
    start_open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    end_close = models.FloatField(blank=True, null=True)
    trading_volume = models.FloatField(blank=True, null=True)
    transaction_amount = models.FloatField(blank=True, null=True)
    end_rate_change = models.FloatField(blank=True, null=True)
    institutional_total = models.FloatField(blank=True, null=True)
    other_corporations = models.FloatField(blank=True, null=True)
    individual = models.FloatField(blank=True, null=True)
    foreigner_total = models.FloatField(blank=True, null=True)
    short_selling = models.FloatField(blank=True, null=True)
    short_buying = models.FloatField(blank=True, null=True)
    short_importance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stockdata'


class Userstock(models.Model):
    userid = models.ForeignKey(Userdata, models.CASCADE, db_column='userid', blank=True, null=True)
    stock_code = models.ForeignKey(Stockcode, models.CASCADE, db_column='stock_code', blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    stock_mean_price = models.IntegerField(blank=True, null=True)
    stock_value = models.IntegerField(blank=True, null=True)
    sum_stock_value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userstock'


class Modelresult(models.Model):
    stock_code = models.ForeignKey('Stockcode', models.DO_NOTHING, db_column='stock_code')
    date_time = models.DateField()
    short_pred = models.FloatField(blank=True, null=True)
    long_pred = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modelresult'
