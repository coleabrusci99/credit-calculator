import math
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--type', help='indicates the type of payment')
parser.add_argument('--payment', help='amount paid each month (do not use with --type=diff', type=float)
parser.add_argument('--principal', help='credit principal', type=float)
parser.add_argument('--periods', help='amount of monthly payments', type=int)
parser.add_argument('--interest', help='yearly interest percentage (must be included, do not use % symbol)', type=float)
args = parser.parse_args()
arg_values = [args.payment, args.principal, args.periods, args.interest]


def calc_periods_annuity(principal, payment, interest):
    p = principal
    a = payment
    i = interest / (100 * 12)
    n = int(math.ceil(math.log((a / (a - i * p)), (1 + i))))
    total_payment = a * n

    if n == 1:
        string = 'You need 1 month to repay this credit!'
    elif 1 < n < 12:
        string = 'You need {} months to repay this credit!'.format(n)
    elif n == 12:
        string = 'You need 1 year to repay this credit!'
    elif n // 12 == 1 and n % 12 != 0:
        string = 'You need 1 year and {} months to repay this credit!'.format(n % 12)
    elif n // 12 > 1 and n % 12 == 0:
        string = 'You need {} years to repay this credit!'.format(n // 12)
    else:
        string = 'You need {} years and {} months to repay this credit!'.format(n // 12, n % 12)

    print(string)
    print('Overpayment = {}'.format(int(total_payment - p)))


def calc_payment_annuity(principal, periods, interest):
    p = principal
    n = periods
    i = interest / (100 * 12)
    a = math.ceil(p * ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)))
    total_payment = a * n
    print('Your annuity payment = {}!'.format(a))
    print('Overpayment = {}'.format(int(total_payment - p)))


def calc_principal_annuity(payment, periods, interest):
    a = payment
    n = periods
    i = interest / (100 * 12)
    p = math.floor(a / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)))
    total_payment = a * n
    print('Your credit principal = {}!'.format(p))
    print('Overpayment = {}'.format(int(total_payment - p)))


def calc_differential_payment(principal, interest, periods):
    p = principal
    i = interest / (100 * 12)
    n = periods
    total_payment = 0
    for m in range(n):
        d = math.ceil((p / n) + (i * (p - ((p * m) / n))))
        total_payment += d
        print('Month {}: paid out {}'.format(m + 1, d))
    print('\nOverpayment = {}'.format(int(total_payment - p)))


def check_negative(iterable):
    for x in iterable:
        if x is None:
            continue
        elif x < 0:
            return True
    return False


error = 'Incorrect parameters.'
if len(sys.argv) == 5:
    if check_negative(arg_values):
        print(error)
    elif args.interest is None:
        print(error)
    elif args.type == 'diff':
        if args.payment is not None:
            print(error)
        else:
            calc_differential_payment(args.principal, args.interest, args.periods)
    elif args.type == 'annuity':
        if args.principal is None:
            calc_principal_annuity(args.payment, args.periods, args.interest)
        elif args.payment is None:
            calc_payment_annuity(args.principal, args.periods, args.interest)
        elif args.periods is None:
            calc_periods_annuity(args.principal, args.payment, args.interest)
    else:
        print(error)
else:
    print(error)
