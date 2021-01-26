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
    
    
        
       
        