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
            "name" : fake.name,
            "country" : fake.country,
            "street_address" : fake.street_address,
            "full_address" :fake.address,
            "city" : fake.city,
            "state": fake.state,
            "postcode" : fake.postcode,
            "latitude" : fake.latitude,
            "longitude" : fake.longitude,
            "credit_card_no" : fake.credit_card_number,
            "color" : fake.color,
            "company_email" : fake.company_email,
            "email1" : fake.email,
            "month_name" : fake.month_name,
            "weekday" : fake.day_of_week,
            "year" : fake.year,
            "time" : fake.time,
            "date" : fake.date,
            "aadhaar_id" : fake.aadhaar_id,
            "company" : fake.company,
            "job_title" : fake.job,
            "phone_num" : self.phone_num,
            "email" : self.email,
            "license_plate" : self.license_plate,
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
       
        