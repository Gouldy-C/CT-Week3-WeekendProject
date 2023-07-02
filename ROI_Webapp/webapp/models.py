from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    rental_income = db.Column(db.Float)
    laundry = db.Column(db.Float, default= 0.0)
    storage = db.Column(db.Float, default= 0.0)
    misc = db.Column(db.Float, default= 0.0)
    mortgage = db.Column(db.Float)
    tax = db.Column(db.Float, default= 0.0)
    insurance = db.Column(db.Float, default= 0.0)
    utilities = db.Column(db.Float, default= 0.0)
    hoa = db.Column(db.Float, default= 0.0)
    lawn_snow = db.Column(db.Float, default= 0.0)
    vacancy = db.Column(db.Float, default= 0.0)
    repairs = db.Column(db.Float, default= 0.0)
    cap_ex = db.Column(db.Float, default= 0.0)
    prop_man = db.Column(db.Float, default= 0.0)
    down_payment = db.Column(db.Float)
    closing_costs = db.Column(db.Float, default= 0.0)
    remodel_budget = db.Column(db.Float, default= 0.0)
    misc_invest = db.Column(db.Float, default= 0.0)
    monthly_cash_flow = db.Column(db.Float, default= 0.0)
    annual_roi = db.Column(db.Float, default= 0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def calc_annual_roi(self):
        monthly_income = sum([self.rental_income,
                                self.laundry,
                                self.storage,
                                self.misc])

        monthly_expenses = sum([self.mortgage,
                                self.tax,
                                self.insurance,
                                self.utilities,
                                self.hoa,
                                self.lawn_snow,
                                self.vacancy,
                                self.repairs,
                                self.cap_ex,
                                self.prop_man])
        
        investment = sum([self.down_payment,
                            self.closing_costs,
                            self.remodel_budget,
                            self.misc_invest])
        
        self.monthly_cash_flow = round(monthly_income - monthly_expenses, 2)
        self.annual_roi = round(((self.monthly_cash_flow * 12)
                                 / investment) * 100, 2)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(150))
    properties = db.relationship('Property')
    