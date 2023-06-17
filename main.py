import os.path
from concurrent.futures import ThreadPoolExecutor
from Core.Logger import Logger
from Core.Talabat import TalabatClient
from datetime import date


logger = Logger(debug=True)
valid = 0


def generate():
    global valid
    if valid > accounts_count:
        return
    talabat = TalabatClient(logger=logger, proxy=proxy)
    if talabat.register() and talabat.addVoucherCode(voucher_code):
        valid += 1
        emails_writer.write(f"{talabat.email}:{talabat.password}:{voucher_code}\n")
        emails_writer.flush()
        return
    return generate()


if __name__ == "__main__":
    print(r"""
     _______  _______  ___      _______  _______  _______  _______ 
    |       ||   _   ||   |    |   _   ||  _    ||   _   ||       |
    |_     _||  |_|  ||   |    |  |_|  || |_|   ||  |_|  ||_     _|
      |   |  |       ||   |    |       ||       ||       |  |   |  
      |   |  |       ||   |___ |       ||  _   | |       |  |   |  
      |   |  |   _   ||       ||   _   || |_|   ||   _   |  |   |  
      |___|  |__| |__||_______||__| |__||_______||__| |__|  |___|  

      DEV: TPCT
      FACEBOOK: https://www.facebook.com/taylor.ackerley.9
      MOBILE: +201094950765
    """)

    accounts_count = int(input("Please enter accounts count to generate: ") or 10)
    voucher_code = input("Please enter voucher code to claim: ")
    proxy = None
    emails_writer = open(f"{voucher_code}-{date.today().isoformat()}.txt", 'w+')

    if os.path.isfile("proxy.txt"):
        with open("proxy.txt", "r+") as proxy_reader:
            proxy = proxy_reader.read().strip()

    with ThreadPoolExecutor(5) as e:
        for i in range(accounts_count):
            e.submit(generate)



