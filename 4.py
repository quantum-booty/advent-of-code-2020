import re

# Parse by line, append to dictionary, if \n append to new dictionary in a
# list, check if cid is not present and if all others and present.

with open('inputs/4.txt', 'r') as file:
    input = file.read()

valid = 0
passport = ""
for line in input.splitlines():
    if line != "":
        if passport == "":
            passport = line
        else:
            passport = passport + ' ' + line
    else:
        d = dict(pair.split(':') for pair in passport.split(" "))
        fields = set(d.keys())
        print(d)
        print(fields)

        try:
            assert 1920 <= int(d['byr']) <= 2002

            assert 2010 <= int(d['iyr']) <= 2020

            assert 2020 <= int(d['eyr']) <= 2030

            assert d['hgt'][-2:] in {'in', 'cm'}
            if d['hgt'][-2:] == 'in':
                assert 59 <= int(d['hgt'][:-2]) <= 76
            elif d['hgt'][-2:] == 'cm':
                assert 150 <= int(d['hgt'][:-2]) <= 193

            assert d['hcl'][0] == '#'
            assert len(d['hcl']) == 7
            assert len(re.findall('[a-f0-9]', d['hcl'])) == 6

            assert d['ecl'] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

            assert len(d['pid']) == 9
            assert len(re.findall('[0-9]', d['pid'])) == 9

            # n = len(fields)
            # assert n == 7 and 'cid' not in fields or n == 8

        except Exception:
            print('invalid')
            pass
        else:
            valid += 1

        passport = ""

print(valid)

# %%

from typing import Dict, List
import re

RAW = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

Passport = Dict[str, str]


def make_passport(raw: str) -> Passport:
    lines = raw.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    passport = {}

    for line in lines:
        for chunk in line.split(" "):
            key, value = chunk.split(":")
            passport[key] = value

    return passport


def make_passports(raw: str) -> List[Passport]:
    chunks = raw.split("\n\n")
    return [make_passport(chunk) for chunk in chunks if chunk.strip()]


PASSPORTS = make_passports(RAW)

DEFAULT_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def is_valid(passport: Passport, required_fields: List[str] = DEFAULT_FIELDS) -> bool:
    return all(field in passport for field in required_fields)


assert sum(is_valid(passport) for passport in PASSPORTS) == 2


def is_valid2(passport: Passport) -> bool:
    checks = [
        1920 <= int(passport.get('byr', -1)) <= 2002, 2010 <= int(passport.get('iyr', -1)) <= 2020,
        2020 <= int(passport.get('eyr', -1)) <= 2030,
        is_valid_height(passport.get('hgt', '')),
        re.match(r"^#[0-9a-f]{6}$", passport.get('hcl', '')),
        passport.get('ecl') in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
        re.match(r"^[0-9]{9}$", passport.get('pid', ''))
    ]

    return all(checks)


def is_valid_height(hgt: str) -> bool:
    if hgt.endswith('cm'):
        hgt = hgt.replace('cm', '')
        try:
            return 150 <= int(hgt) <= 193
        except:
            return False
    elif hgt.endswith("in"):
        hgt = hgt.replace("in", "")
        try:
            return 59 <= int(hgt) <= 76
        except:
            return False

    return False


INVALID = make_passports("""eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""")

VALID = make_passports("""pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""")

assert all(is_valid2(passport) for passport in VALID)
assert not any(is_valid2(passport) for passport in INVALID)

with open('inputs/4.txt') as f:
    passports = make_passports(f.read())

    print(sum(is_valid(passport) for passport in passports))
    print(sum(is_valid2(passport) for passport in passports))
