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

    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return True
    
    #### 테스트
    def has_perms(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return True
    ####

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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
    xgb_short_pred = models.FloatField(blank=True, null=True)
    xgb_long_pred = models.FloatField(blank=True, null=True)
    ltms_short_pred = models.FloatField(blank=True, null=True)
    ltms_long_pred = models.FloatField(blank=True, null=True)

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
    xgb_short_result = models.FloatField(blank=True, null=True)
    xgb_long_result = models.FloatField(blank=True, null=True)
    lstm_short_result = models.FloatField(blank=True, null=True)
    lstm_long_result = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modelresult'


class Dictionary(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary'


class Airate(models.Model):
    date_time = models.DateField(primary_key=True)
    synthesis_rate = models.FloatField(blank=True, null=True)
    a000060 = models.FloatField(db_column='A000060', blank=True, null=True)  # Field name made lowercase.
    a000100 = models.FloatField(db_column='A000100', blank=True, null=True)  # Field name made lowercase.
    a000270 = models.FloatField(db_column='A000270', blank=True, null=True)  # Field name made lowercase.
    a000660 = models.FloatField(db_column='A000660', blank=True, null=True)  # Field name made lowercase.
    a000720 = models.FloatField(db_column='A000720', blank=True, null=True)  # Field name made lowercase.
    a000810 = models.FloatField(db_column='A000810', blank=True, null=True)  # Field name made lowercase.
    a003490 = models.FloatField(db_column='A003490', blank=True, null=True)  # Field name made lowercase.
    a003550 = models.FloatField(db_column='A003550', blank=True, null=True)  # Field name made lowercase.
    a003670 = models.FloatField(db_column='A003670', blank=True, null=True)  # Field name made lowercase.
    a004020 = models.FloatField(db_column='A004020', blank=True, null=True)  # Field name made lowercase.
    a004990 = models.FloatField(db_column='A004990', blank=True, null=True)  # Field name made lowercase.
    a005380 = models.FloatField(db_column='A005380', blank=True, null=True)  # Field name made lowercase.
    a005490 = models.FloatField(db_column='A005490', blank=True, null=True)  # Field name made lowercase.
    a005830 = models.FloatField(db_column='A005830', blank=True, null=True)  # Field name made lowercase.
    a005930 = models.FloatField(db_column='A005930', blank=True, null=True)  # Field name made lowercase.
    a005935 = models.FloatField(db_column='A005935', blank=True, null=True)  # Field name made lowercase.
    a005940 = models.FloatField(db_column='A005940', blank=True, null=True)  # Field name made lowercase.
    a006400 = models.FloatField(db_column='A006400', blank=True, null=True)  # Field name made lowercase.
    a006800 = models.FloatField(db_column='A006800', blank=True, null=True)  # Field name made lowercase.
    a007070 = models.FloatField(db_column='A007070', blank=True, null=True)  # Field name made lowercase.
    a008560 = models.FloatField(db_column='A008560', blank=True, null=True)  # Field name made lowercase.
    a008770 = models.FloatField(db_column='A008770', blank=True, null=True)  # Field name made lowercase.
    a009150 = models.FloatField(db_column='A009150', blank=True, null=True)  # Field name made lowercase.
    a009540 = models.FloatField(db_column='A009540', blank=True, null=True)  # Field name made lowercase.
    a009830 = models.FloatField(db_column='A009830', blank=True, null=True)  # Field name made lowercase.
    a010130 = models.FloatField(db_column='A010130', blank=True, null=True)  # Field name made lowercase.
    a010140 = models.FloatField(db_column='A010140', blank=True, null=True)  # Field name made lowercase.
    a010620 = models.FloatField(db_column='A010620', blank=True, null=True)  # Field name made lowercase.
    a010950 = models.FloatField(db_column='A010950', blank=True, null=True)  # Field name made lowercase.
    a011070 = models.FloatField(db_column='A011070', blank=True, null=True)  # Field name made lowercase.
    a011170 = models.FloatField(db_column='A011170', blank=True, null=True)  # Field name made lowercase.
    a011200 = models.FloatField(db_column='A011200', blank=True, null=True)  # Field name made lowercase.
    a011780 = models.FloatField(db_column='A011780', blank=True, null=True)  # Field name made lowercase.
    a011790 = models.FloatField(db_column='A011790', blank=True, null=True)  # Field name made lowercase.
    a012330 = models.FloatField(db_column='A012330', blank=True, null=True)  # Field name made lowercase.
    a012450 = models.FloatField(db_column='A012450', blank=True, null=True)  # Field name made lowercase.
    a015760 = models.FloatField(db_column='A015760', blank=True, null=True)  # Field name made lowercase.
    a016360 = models.FloatField(db_column='A016360', blank=True, null=True)  # Field name made lowercase.
    a017670 = models.FloatField(db_column='A017670', blank=True, null=True)  # Field name made lowercase.
    a018260 = models.FloatField(db_column='A018260', blank=True, null=True)  # Field name made lowercase.
    a018880 = models.FloatField(db_column='A018880', blank=True, null=True)  # Field name made lowercase.
    a021240 = models.FloatField(db_column='A021240', blank=True, null=True)  # Field name made lowercase.
    a024110 = models.FloatField(db_column='A024110', blank=True, null=True)  # Field name made lowercase.
    a028050 = models.FloatField(db_column='A028050', blank=True, null=True)  # Field name made lowercase.
    a028260 = models.FloatField(db_column='A028260', blank=True, null=True)  # Field name made lowercase.
    a028300 = models.FloatField(db_column='A028300', blank=True, null=True)  # Field name made lowercase.
    a029780 = models.FloatField(db_column='A029780', blank=True, null=True)  # Field name made lowercase.
    a030200 = models.FloatField(db_column='A030200', blank=True, null=True)  # Field name made lowercase.
    a032640 = models.FloatField(db_column='A032640', blank=True, null=True)  # Field name made lowercase.
    a032830 = models.FloatField(db_column='A032830', blank=True, null=True)  # Field name made lowercase.
    a033780 = models.FloatField(db_column='A033780', blank=True, null=True)  # Field name made lowercase.
    a034020 = models.FloatField(db_column='A034020', blank=True, null=True)  # Field name made lowercase.
    a034220 = models.FloatField(db_column='A034220', blank=True, null=True)  # Field name made lowercase.
    a034730 = models.FloatField(db_column='A034730', blank=True, null=True)  # Field name made lowercase.
    a035250 = models.FloatField(db_column='A035250', blank=True, null=True)  # Field name made lowercase.
    a035420 = models.FloatField(db_column='A035420', blank=True, null=True)  # Field name made lowercase.
    a035720 = models.FloatField(db_column='A035720', blank=True, null=True)  # Field name made lowercase.
    a036460 = models.FloatField(db_column='A036460', blank=True, null=True)  # Field name made lowercase.
    a036570 = models.FloatField(db_column='A036570', blank=True, null=True)  # Field name made lowercase.
    a047810 = models.FloatField(db_column='A047810', blank=True, null=True)  # Field name made lowercase.
    a051900 = models.FloatField(db_column='A051900', blank=True, null=True)  # Field name made lowercase.
    a051910 = models.FloatField(db_column='A051910', blank=True, null=True)  # Field name made lowercase.
    a055550 = models.FloatField(db_column='A055550', blank=True, null=True)  # Field name made lowercase.
    a066570 = models.FloatField(db_column='A066570', blank=True, null=True)  # Field name made lowercase.
    a066970 = models.FloatField(db_column='A066970', blank=True, null=True)  # Field name made lowercase.
    a068270 = models.FloatField(db_column='A068270', blank=True, null=True)  # Field name made lowercase.
    a071050 = models.FloatField(db_column='A071050', blank=True, null=True)  # Field name made lowercase.
    a078930 = models.FloatField(db_column='A078930', blank=True, null=True)  # Field name made lowercase.
    a086280 = models.FloatField(db_column='A086280', blank=True, null=True)  # Field name made lowercase.
    a086790 = models.FloatField(db_column='A086790', blank=True, null=True)  # Field name made lowercase.
    a088980 = models.FloatField(db_column='A088980', blank=True, null=True)  # Field name made lowercase.
    a090430 = models.FloatField(db_column='A090430', blank=True, null=True)  # Field name made lowercase.
    a091990 = models.FloatField(db_column='A091990', blank=True, null=True)  # Field name made lowercase.
    a096770 = models.FloatField(db_column='A096770', blank=True, null=True)  # Field name made lowercase.
    a097950 = models.FloatField(db_column='A097950', blank=True, null=True)  # Field name made lowercase.
    a105560 = models.FloatField(db_column='A105560', blank=True, null=True)  # Field name made lowercase.
    a128940 = models.FloatField(db_column='A128940', blank=True, null=True)  # Field name made lowercase.
    a137310 = models.FloatField(db_column='A137310', blank=True, null=True)  # Field name made lowercase.
    a138040 = models.FloatField(db_column='A138040', blank=True, null=True)  # Field name made lowercase.
    a161390 = models.FloatField(db_column='A161390', blank=True, null=True)  # Field name made lowercase.
    a207940 = models.FloatField(db_column='A207940', blank=True, null=True)  # Field name made lowercase.
    a241560 = models.FloatField(db_column='A241560', blank=True, null=True)  # Field name made lowercase.
    a247540 = models.FloatField(db_column='A247540', blank=True, null=True)  # Field name made lowercase.
    a251270 = models.FloatField(db_column='A251270', blank=True, null=True)  # Field name made lowercase.
    a259960 = models.FloatField(db_column='A259960', blank=True, null=True)  # Field name made lowercase.
    a267250 = models.FloatField(db_column='A267250', blank=True, null=True)  # Field name made lowercase.
    a271560 = models.FloatField(db_column='A271560', blank=True, null=True)  # Field name made lowercase.
    a282330 = models.FloatField(db_column='A282330', blank=True, null=True)  # Field name made lowercase.
    a293490 = models.FloatField(db_column='A293490', blank=True, null=True)  # Field name made lowercase.
    a302440 = models.FloatField(db_column='A302440', blank=True, null=True)  # Field name made lowercase.
    a316140 = models.FloatField(db_column='A316140', blank=True, null=True)  # Field name made lowercase.
    a323410 = models.FloatField(db_column='A323410', blank=True, null=True)  # Field name made lowercase.
    a326030 = models.FloatField(db_column='A326030', blank=True, null=True)  # Field name made lowercase.
    a329180 = models.FloatField(db_column='A329180', blank=True, null=True)  # Field name made lowercase.
    a352820 = models.FloatField(db_column='A352820', blank=True, null=True)  # Field name made lowercase.
    a361610 = models.FloatField(db_column='A361610', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'airate'
        

class Aifunds(models.Model):
    date_time = models.DateField(primary_key=True)
    a000060 = models.FloatField(db_column='A000060', blank=True, null=True)  # Field name made lowercase.
    a000100 = models.FloatField(db_column='A000100', blank=True, null=True)  # Field name made lowercase.
    a000270 = models.FloatField(db_column='A000270', blank=True, null=True)  # Field name made lowercase.
    a000660 = models.FloatField(db_column='A000660', blank=True, null=True)  # Field name made lowercase.
    a000720 = models.FloatField(db_column='A000720', blank=True, null=True)  # Field name made lowercase.
    a000810 = models.FloatField(db_column='A000810', blank=True, null=True)  # Field name made lowercase.
    a003490 = models.FloatField(db_column='A003490', blank=True, null=True)  # Field name made lowercase.
    a003550 = models.FloatField(db_column='A003550', blank=True, null=True)  # Field name made lowercase.
    a003670 = models.FloatField(db_column='A003670', blank=True, null=True)  # Field name made lowercase.
    a004020 = models.FloatField(db_column='A004020', blank=True, null=True)  # Field name made lowercase.
    a004990 = models.FloatField(db_column='A004990', blank=True, null=True)  # Field name made lowercase.
    a005380 = models.FloatField(db_column='A005380', blank=True, null=True)  # Field name made lowercase.
    a005490 = models.FloatField(db_column='A005490', blank=True, null=True)  # Field name made lowercase.
    a005830 = models.FloatField(db_column='A005830', blank=True, null=True)  # Field name made lowercase.
    a005930 = models.FloatField(db_column='A005930', blank=True, null=True)  # Field name made lowercase.
    a005935 = models.FloatField(db_column='A005935', blank=True, null=True)  # Field name made lowercase.
    a005940 = models.FloatField(db_column='A005940', blank=True, null=True)  # Field name made lowercase.
    a006400 = models.FloatField(db_column='A006400', blank=True, null=True)  # Field name made lowercase.
    a006800 = models.FloatField(db_column='A006800', blank=True, null=True)  # Field name made lowercase.
    a007070 = models.FloatField(db_column='A007070', blank=True, null=True)  # Field name made lowercase.
    a008560 = models.FloatField(db_column='A008560', blank=True, null=True)  # Field name made lowercase.
    a008770 = models.FloatField(db_column='A008770', blank=True, null=True)  # Field name made lowercase.
    a009150 = models.FloatField(db_column='A009150', blank=True, null=True)  # Field name made lowercase.
    a009540 = models.FloatField(db_column='A009540', blank=True, null=True)  # Field name made lowercase.
    a009830 = models.FloatField(db_column='A009830', blank=True, null=True)  # Field name made lowercase.
    a010130 = models.FloatField(db_column='A010130', blank=True, null=True)  # Field name made lowercase.
    a010140 = models.FloatField(db_column='A010140', blank=True, null=True)  # Field name made lowercase.
    a010620 = models.FloatField(db_column='A010620', blank=True, null=True)  # Field name made lowercase.
    a010950 = models.FloatField(db_column='A010950', blank=True, null=True)  # Field name made lowercase.
    a011070 = models.FloatField(db_column='A011070', blank=True, null=True)  # Field name made lowercase.
    a011170 = models.FloatField(db_column='A011170', blank=True, null=True)  # Field name made lowercase.
    a011200 = models.FloatField(db_column='A011200', blank=True, null=True)  # Field name made lowercase.
    a011780 = models.FloatField(db_column='A011780', blank=True, null=True)  # Field name made lowercase.
    a011790 = models.FloatField(db_column='A011790', blank=True, null=True)  # Field name made lowercase.
    a012330 = models.FloatField(db_column='A012330', blank=True, null=True)  # Field name made lowercase.
    a012450 = models.FloatField(db_column='A012450', blank=True, null=True)  # Field name made lowercase.
    a015760 = models.FloatField(db_column='A015760', blank=True, null=True)  # Field name made lowercase.
    a016360 = models.FloatField(db_column='A016360', blank=True, null=True)  # Field name made lowercase.
    a017670 = models.FloatField(db_column='A017670', blank=True, null=True)  # Field name made lowercase.
    a018260 = models.FloatField(db_column='A018260', blank=True, null=True)  # Field name made lowercase.
    a018880 = models.FloatField(db_column='A018880', blank=True, null=True)  # Field name made lowercase.
    a021240 = models.FloatField(db_column='A021240', blank=True, null=True)  # Field name made lowercase.
    a024110 = models.FloatField(db_column='A024110', blank=True, null=True)  # Field name made lowercase.
    a028050 = models.FloatField(db_column='A028050', blank=True, null=True)  # Field name made lowercase.
    a028260 = models.FloatField(db_column='A028260', blank=True, null=True)  # Field name made lowercase.
    a028300 = models.FloatField(db_column='A028300', blank=True, null=True)  # Field name made lowercase.
    a029780 = models.FloatField(db_column='A029780', blank=True, null=True)  # Field name made lowercase.
    a030200 = models.FloatField(db_column='A030200', blank=True, null=True)  # Field name made lowercase.
    a032640 = models.FloatField(db_column='A032640', blank=True, null=True)  # Field name made lowercase.
    a032830 = models.FloatField(db_column='A032830', blank=True, null=True)  # Field name made lowercase.
    a033780 = models.FloatField(db_column='A033780', blank=True, null=True)  # Field name made lowercase.
    a034020 = models.FloatField(db_column='A034020', blank=True, null=True)  # Field name made lowercase.
    a034220 = models.FloatField(db_column='A034220', blank=True, null=True)  # Field name made lowercase.
    a034730 = models.FloatField(db_column='A034730', blank=True, null=True)  # Field name made lowercase.
    a035250 = models.FloatField(db_column='A035250', blank=True, null=True)  # Field name made lowercase.
    a035420 = models.FloatField(db_column='A035420', blank=True, null=True)  # Field name made lowercase.
    a035720 = models.FloatField(db_column='A035720', blank=True, null=True)  # Field name made lowercase.
    a036460 = models.FloatField(db_column='A036460', blank=True, null=True)  # Field name made lowercase.
    a036570 = models.FloatField(db_column='A036570', blank=True, null=True)  # Field name made lowercase.
    a047810 = models.FloatField(db_column='A047810', blank=True, null=True)  # Field name made lowercase.
    a051900 = models.FloatField(db_column='A051900', blank=True, null=True)  # Field name made lowercase.
    a051910 = models.FloatField(db_column='A051910', blank=True, null=True)  # Field name made lowercase.
    a055550 = models.FloatField(db_column='A055550', blank=True, null=True)  # Field name made lowercase.
    a066570 = models.FloatField(db_column='A066570', blank=True, null=True)  # Field name made lowercase.
    a066970 = models.FloatField(db_column='A066970', blank=True, null=True)  # Field name made lowercase.
    a068270 = models.FloatField(db_column='A068270', blank=True, null=True)  # Field name made lowercase.
    a071050 = models.FloatField(db_column='A071050', blank=True, null=True)  # Field name made lowercase.
    a078930 = models.FloatField(db_column='A078930', blank=True, null=True)  # Field name made lowercase.
    a086280 = models.FloatField(db_column='A086280', blank=True, null=True)  # Field name made lowercase.
    a086790 = models.FloatField(db_column='A086790', blank=True, null=True)  # Field name made lowercase.
    a088980 = models.FloatField(db_column='A088980', blank=True, null=True)  # Field name made lowercase.
    a090430 = models.FloatField(db_column='A090430', blank=True, null=True)  # Field name made lowercase.
    a091990 = models.FloatField(db_column='A091990', blank=True, null=True)  # Field name made lowercase.
    a096770 = models.FloatField(db_column='A096770', blank=True, null=True)  # Field name made lowercase.
    a097950 = models.FloatField(db_column='A097950', blank=True, null=True)  # Field name made lowercase.
    a105560 = models.FloatField(db_column='A105560', blank=True, null=True)  # Field name made lowercase.
    a128940 = models.FloatField(db_column='A128940', blank=True, null=True)  # Field name made lowercase.
    a137310 = models.FloatField(db_column='A137310', blank=True, null=True)  # Field name made lowercase.
    a138040 = models.FloatField(db_column='A138040', blank=True, null=True)  # Field name made lowercase.
    a161390 = models.FloatField(db_column='A161390', blank=True, null=True)  # Field name made lowercase.
    a207940 = models.FloatField(db_column='A207940', blank=True, null=True)  # Field name made lowercase.
    a241560 = models.FloatField(db_column='A241560', blank=True, null=True)  # Field name made lowercase.
    a247540 = models.FloatField(db_column='A247540', blank=True, null=True)  # Field name made lowercase.
    a251270 = models.FloatField(db_column='A251270', blank=True, null=True)  # Field name made lowercase.
    a259960 = models.FloatField(db_column='A259960', blank=True, null=True)  # Field name made lowercase.
    a267250 = models.FloatField(db_column='A267250', blank=True, null=True)  # Field name made lowercase.
    a271560 = models.FloatField(db_column='A271560', blank=True, null=True)  # Field name made lowercase.
    a282330 = models.FloatField(db_column='A282330', blank=True, null=True)  # Field name made lowercase.
    a293490 = models.FloatField(db_column='A293490', blank=True, null=True)  # Field name made lowercase.
    a302440 = models.FloatField(db_column='A302440', blank=True, null=True)  # Field name made lowercase.
    a316140 = models.FloatField(db_column='A316140', blank=True, null=True)  # Field name made lowercase.
    a323410 = models.FloatField(db_column='A323410', blank=True, null=True)  # Field name made lowercase.
    a326030 = models.FloatField(db_column='A326030', blank=True, null=True)  # Field name made lowercase.
    a329180 = models.FloatField(db_column='A329180', blank=True, null=True)  # Field name made lowercase.
    a352820 = models.FloatField(db_column='A352820', blank=True, null=True)  # Field name made lowercase.
    a361610 = models.FloatField(db_column='A361610', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aifunds'