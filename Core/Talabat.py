import random
from uuid import uuid4
from Core.Logger import Logger
from string import ascii_letters, digits
from cfscrape import create_scraper
from faker import Faker


class TalabatClient:
    LOGIN_URL = "https://api.talabat.com/apiAndroid/v1/AuthToken"
    LOYALTY_URL = "https://loyalty.talabat.com/api/v3/me/promo-codes/redeem"

    def __init__(self, **kwargs):
        self._faker = Faker()
        self._logger = kwargs.get("logger", Logger(debug=True))
        self._proxy = kwargs.get("proxy", None)
        self._country_id = kwargs.get("country_id", 9)
        self._email = self._faker.name().lower().split(" ")[0] + ''.join(random.choices(digits, k=4)) + "@gmail.com"
        self._password = ''.join(random.choices(ascii_letters, k=10))
        self._auth_token = ""

        self._session = create_scraper()
        self._session.proxies.update({
            'http': self._proxy,
            'https': self._proxy,
        })

    def register(self):
        try:
            self._logger.log(f"Trying to register {self._email}")
            headers = {
                "accept-encoding": "gzip",
                "accept-language": "en-US",
                "appbrand": "1",
                "brandtype": "1",
                "connection": "Keep-Alive",
                "content-type": "application/x-www-form-urlencoded",
                "isreg": "true",
                "user-agent": "Dalvik/2.1.0 (Linux; U; Android 11; Galaxy Note 10+ Build/RQ1A.210105.003)",
                "x-device-source": "6",
                "x-device-version": "9.95"
            }

            response = self._session.post(self.LOGIN_URL, data={
                "UserName": self._email,
                "Email": self._email,
                "mobileCountryCode": "0",
                "FirstName": self._faker.name().split(" ")[0],
                "mobileNumber": "",
                "AdjustId": f"{uuid4().hex}",
                "otp": "",
                "AdvertisingId": f"{uuid4()}",
                "UDID": self._session.headers.get('x-device-id'),
                "countryId": self._country_id,
                "ConfirmPassword": self._password,
                "IsSubscribeNews": "true",
                "grant_type": "password",
                "registrationType": "0",
                "IsSubscribeSMS": "true",
                "Region": "0",
                "LastName": self._faker.name().split(" ")[0],
                "IsMale": "true",
                "Password": self._password,
                "BirthDate": "",
            }, headers=headers)

            if response.status_code == 200:
                self._auth_token = f"Bearer {response.json()['access_token']}"
                self._logger.log(f"{self._email} logged in successfully")
                return True
            else:
                self._logger.error("Invalid username or password")
        except Exception as e:
            self._logger.error(f"An error occurred while trying to login {self._email}, error: {e}")
        return False

    def addVoucherCode(self, voucher_code):
        try:
            self._logger.log(f"Trying to voucher {self._email}, voucher code: {voucher_code}")

            headers = {
                "accept-encoding": "gzip",
                "accept-language": "en-US",
                "appbrand": "1",
                "authorization": self._auth_token,
                "brandtype": "1",
                "connection": "Keep-Alive",
                "user-agent": "okhttp/4.9.3",
                "x-device-id": f"{uuid4().hex[:len('acf38984b35ae882')]}",
                "x-device-source": "6",
                "x-device-version": "9.95",
                'x-talabat-android-installation-path': ''.join(random.choices(ascii_letters, k=len('L2RhdGEvdXNlci8wL2NvbS50YWxhYmF0'))),
                "x-talabat-android-package-name": "com.talabat"
            }

            response = self._session.post(self.LOYALTY_URL, json={
                "country": self._country_id,
                "promoCode": voucher_code
            }, headers=headers)

            if response.status_code == 200:
                self._logger.log("Voucher has been claimed successfully")
                return True
            self._logger.error("Voucher has failed to be claimed")
        except Exception as e:
            self._logger.error(f"An error occurred while trying to claiming {self._email} {voucher_code}, error: {e}")
        return False

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password