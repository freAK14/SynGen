#importing required libraries
import os
import random
from random import randint, choice
import pandas as pd

class syngen:
    def __init__(self, seed = None):
        """
        Initiates the class and creates a Faker() object for later data generation by other methods
        seed: User can set a seed parameter to generate deterministic, non-random output
        """
        from faker import Faker
        
        self.faker = Faker
        self.fake = Faker('en_IN')
        self.seed = seed
        self.randnum = randint(1, 9)
        
        #initializing license-plate state list
        self.state_initials = self._initialize_state_initials()
        #initializing email domain list
        self.domain_list =  self._initialize_email_domains()
            
        
    def _initialize_state_initials(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = dir_path + os.sep + "state_initials.txt"
        
        state_initials = []
        with open(path) as f:
            state_initials = [str(line).strip() for line in f.readlines()]
            
        return state_initials
     
        
    def _initialize_email_domains(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = dir_path + os.sep + "email_domains.txt"
        
        email_domains = []
        with open(path) as f:
            email_domains = [str(line).strip() for line in f.readlines()]
            
        return email_domains
    
    
    def phone_num(self, seed = None):
        """
        Generates 10 digit Indian phone number in xxxxx-xxxxx format
        seed: Currently not used. Uses seed from the syngen class if chosen by user
        """
        random.seed(self.seed)
        
        phone_format = "{p1}-{p2}"
        
        p1 = str(randint(70000, 99999))
        p2 = str(randint(0, 99999)).rjust(5, "0")
        
        return phone_format.format(p1 = p1, p2 = p2)
    
    
    def license_plate(self, seed = None):
        """
        Generates vehicle license plate in the format MH-31-VS-9999
        seed: Currently not used. Uses seed from the syngen class if chosen by user
        """
        random.seed(self.seed)
        
        license_plate_format = "{p1}{p2}{p3}{p4}{p5}{p6}{p7}"    #try without placeholders for '-'
        state_in = choice(self.state_initials)
        
        p1 = str(state_in)
        p2 = "-"
        p3 = "".join([str(randint(0, 9)) for i in range(2)])
        p4 = "-"
        p5 = "".join([chr(randint(65, 90)) for _ in range(2)])
        p6 = "-"
        p7 = "".join([str(randint(0, 9)) for _ in range(4)])
        
        return license_plate_format.format(p1 = p1, p2 = p2, p3 = p3, p4 = p4, p5 = p5, p6 = p6, p7 = p7)
        
    
    def college_regno(self, seed = None):
        """
        Generates a 15-character college registration number in the format 2018ACSC1101085
        seed: Currently not used. Uses seed from the syngen class if chosen by user
        """
        random.seed(self.seed)
        
        reg_no_format = "{p1}{p2}{p3}"
        dept_list = ["ACSC", "ACIV", "AIFT", "AETX", "AETC"]
        dept = choice(dept_list)
        
        p1 = str(randint(2010, 2022))
        p2 = "".join([str(dept)])
        p3 = "".join([str(randint(0, 9)) for _ in range (7)]) 
        
        return reg_no_format.format(p1 =p1, p2 = p2, p3 = p3)
    
    def email(self, name, seed = None):
        """
        Generates realistic email from first and last name and a random domain address
        seed: Currently not used. Uses seed from the syngen class if chosen by user
        """
        random.seed(self.seed)
        
        name = str(name)
        f_name = name.split()[0]
        l_name = name.split()[-1]
        
        choice_int = choice(range(10))
        
        domain = choice(self.email_domains)
        
        name_formats = [
            "{first}{last}",
            "{first}.{last}",
            "{first}_{last}",
            "{last}.{first}",
            "{last}_{first}",
            "{f}{last}",
            "{first}.{l}",
            "{first}_{l}"
            ]
        name_fmt_choice = choice(name_formats)
        name_combo = name_fmt_choice.format(f = f_name[0], l = l_name[0], first = f_name, last = l_name)
        
        if choice_int < 7:
            email = name_combo + "@" + str(domain)
        else:
            email = name_combo + str(randint(1, 99)) + "@" + str(domain)
            
        return email
    
    def gen_data_series(self, num = 10, data_type = "name", seed = None):
        #description needs edit
        """
        Returns a pandas series object with the desired number of entries and data type
        Data types available:
        - name, country, city(indian), state(indian), zipcode, latitude, longitude
        - month, weekday, year, time, date
        - personal email, Aadhaar No.
        - company, Job title, phone number, license plate
        Phone number can be two types:
        'phone_num' generates 10 digit Indian number in xxxxx-xxxxx format
        'phone_number_full' may generate an international number with different format
        seed: Currently not used. Uses seed from the syngen class if chosen by user
        """
        if type(data_type) != str:
            raise ValueError(
                "Data type must be of type str, found " + str(type(data_type))
                )
        try:
            num = int(num)
        except:
            raise ValueError(
                "Number of samples must be a positive integer, found " + num
                )
            
        if num <= 0:
            raise ValueError(
                "Number of samples must be a positive integer, found " + num
                )
        num = int(num)
        fake = self.fake
        self.faker.seed(self.seed)
        
        func_lookup = {
            #-----Address-----#
            "address" : fake.address,
            "building_number" : fake.building_number,
            "city" : fake.city,
            "country" : fake.country,
            "country_code" : fake.country_code,
            "postcode" : fake.postcode,
            "street_address" : fake.street_address,
            "state" : fake.state,
            
            #-----Automotive-----#
            "license_plate" : self.license_plate,
            
            #-----Barcode-----#
            "ean" : fake.ean,
            
            #-----Color-----#
            "color" : fake.color,
            "color_name" : fake.color_name,
            "rgb_color" : fake.rgb_color,
            
            #-----Company-----#
            "company" : fake.company,
            
            #-----Credit Card-----#
            
            
            #-----Date-Time-----#
            "century" : fake.century,
            "date" : fake.date,
            "date_between" : fake.date_between,        #between today and last 30 years
            "date_this_century" : fake.date_this_century,
            "date_this_decade" : fake.date_this_decade,
            "date_this_year" : fake.date_this_year,
            "date_this_month" : fake.date_this_month,
            "date_time" : fake.date_time,
            "day_of_month" : fake.day_of_month,
            "day_of_week" : fake.day_of_week,
            "future_date" : fake.future_date,        #between today and next 30 days
            "month" : fake.month,
            "month_name" : fake.month_name,
            "time" : fake.time,
            "year" : fake.year,
            
            #-----Geographic-----#
            "coordinate" : fake.coordinate,
            "latitude" : fake.latitude,
            "longitude" : fake.longitude,
            
            #-----Internet-----#
            "company_email" : fake.company_email,
            "ipv4" : fake.ipv4,
            "ipv4_private" : fake.ipv4_private,
            "ipv6" : fake.ipv6,
            "mac_address" : fake.mac_address,
            "port_number" : fake.port_number,
            "url" : fake.url,
            
            #-----Book ISBN-----#
            "isbn10" : fake.isbn10,
            "isbn13" : fake.isbn13,
            
            #-----Job-----#
            "job" : fake.job,
            
            #-----Text-----#
            "paragraph" : fake.paragraph,
            "sentence" : fake.sentence,
            "text" : fake.text,
            "word" : fake.word,
            
            #-----Miscellaneous-----#
            "boolean" : fake.boolean,
            "json" : fake.json,
            "md5" : fake.md5,        #hexadecimal MD5 hash
            "password" : fake.password,
            
            #-----Person-----#
            "first_name" : fake.first_name,
            "first_name_female" : fake.first_name_female,
            "first_name_male" : fake.first_name_male,
            "last_name" : fake.last_name,
            "name" : fake.name,
            "name_female" : fake.name_female,
            "name_male" : fake.name_male,
            "aadhaar_id" : fake.aadhaar_id,
            "prefix" : fake.prefix,
            "language_name" : fake.language_name,
            
            "phone_num" : self.phone_num,
            "email" : self.email,
            "college_regno" : self.college_regno
            }
        
        if data_type not in func_lookup:
            raise ValueError(
                "Data type must be one of " + str(list(func_lookup.keys()))
                )
        
        datagen_func = func_lookup[data_type]

        return pd.Series((datagen_func() for _ in range(num)))
    

    def _validate_args(self, num, fields):
        try:
            num = int(num)
        except:
            raise ValueError(
                "Number must be a positive integer, found " + num
                )
            
        if num <= 0:
            raise ValueError(
                "Number must be a positive integer, found " + num
                )
        
        num_cols = len(fields)
        if num_cols < 0:
            raise ValueError(
                "Please provide at least one type of data field to be generated"
                )
    
        