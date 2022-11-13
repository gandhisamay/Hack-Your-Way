DICT_GENDER = {0: "MALE", 1: "FEMALE", 2: "OTHER"}

class Citizen:
    def __init__(self, name, father_name,husband_name, other_name, 
                 age, gender, house, voter_id) -> None:
        self.AGE          = age if age else 0
        self.HOUSE        = house if house else 0
        self.VOTER_ID     = voter_id if voter_id else 0
        self.GENDER       = DICT_GENDER[gender] if gender else DICT_GENDER[0]
        self.NAME         = name if name else 0
        self.OTHER_NAME   = other_name if other_name else 0
        self.FATHER_NAME  = father_name if father_name else 0
        self.HUSBAND_NAME = husband_name if husband_name else 0