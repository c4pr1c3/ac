import hashlib
import hmac
from flask import Blueprint, render_template, flash, redirect, request
from models import File
from common import *
from flask import current_app as app
from datetime import date, datetime, timedelta

import random
import datetime

def random_within_7_days():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=7)
    if (now - delta) < last_generated_date:
        return last_generated_number
    else:
        last_generated_date = now
        last_generated_number = random.randint(0, 100)
        return last_generated_number

def within_7_days(date):
    return (datetime.now() - date) < timedelta(days=7)


def hamc_encrypt(filename, key):

    result = hmac.new(key.encode(), filename.encode(), hashlib.md5).hexdigest()

    print(result)


if __name__ == "__main__":
   filename = request.args.get('filename')
   key = random_within_7_days()
   hamc_encrypt(filename, key)
