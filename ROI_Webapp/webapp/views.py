from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Property
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def roi():
    if request.method == 'POST':
        name = request.form.get('name')
        rental_income = (request.form.get('rental_income'))
        laundry = request.form.get('laundry')
        storage = request.form.get('storage')
        misc = request.form.get('misc')
        mortgage = request.form.get('mortgage')
        tax = request.form.get('tax')
        insurance = request.form.get('insurance')
        utilities = request.form.get('utilities')
        hoa = request.form.get('hoa')
        lawn_snow = request.form.get('lawn_snow')
        vacancy = request.form.get('vacancy')
        repairs = request.form.get('repairs')
        cap_ex = request.form.get('cap_ex')
        prop_man = request.form.get('prop_man')
        down_payment = request.form.get('down_payment')
        closing_costs = request.form.get('closing_costs')
        remodel_budget = request.form.get('remodel_budget')
        misc_invest = request.form.get('misc_invest')
        
        values_0 = [laundry,storage,misc,tax,insurance,utilities,hoa,lawn_snow,vacancy,repairs,cap_ex,prop_man,down_payment,closing_costs]
        
        values_1 = [rental_income,mortgage,down_payment,closing_costs]
        
        if name == '' or name == None:
            flash('Name can not be empty', category='error')
            return redirect(url_for('views.roi'))
        
        for value in values_1:
            if value == '' or value == None:
                flash('Rental income, mortgage, down payment, closing_costs all require greater then 0.00 input.', category='error')
                return redirect(url_for('views.roi'))
        
        for value in values_0:
            if value == '' or value == None:
                flash('All fields are required. Input 0.00 for non applicable fields.', category='error')
                return redirect(url_for('views.roi'))
        
        
        property = Property.query.filter_by(name=name).first()
        if property:
            flash('This property name is already used, please change it and try again.', category='error')
            return redirect(url_for('views.roi'))
        else:
            new_property = Property(name=name,
                        rental_income=round(float(rental_income), 2),
                        laundry=round(float(laundry), 2),
                        storage=round(float(storage), 2),
                        misc=round(float(misc), 2),
                        mortgage=round(float(mortgage), 2),
                        tax=round(float(tax), 2),
                        insurance=round(float(insurance), 2),
                        utilities=round(float(utilities), 2),
                        hoa=round(float(hoa), 2),
                        lawn_snow=round(float(lawn_snow), 2),
                        vacancy=round(float(vacancy), 2),
                        repairs=round(float(repairs), 2),
                        cap_ex=round(float(cap_ex), 2),
                        prop_man=round(float(prop_man), 2),
                        down_payment=round(float(down_payment), 2),
                        closing_costs=round(float(closing_costs), 2),
                        remodel_budget=round(float(remodel_budget), 2),
                        misc_invest=round(float(misc_invest), 2),
                        monthly_cash_flow = 0.00,
                        annual_roi = 0.00,
                        user_id=current_user.id)
            new_property.calc_annual_roi()
            db.session.add(new_property)
            db.session.commit()
            
            flash('Property added to your properties.', category='success')
            return redirect(url_for('views.properties'))
    return render_template('ROI.html', user=current_user)


@views.route('/update_property', methods=['POST'])
@login_required
def update_property():
    prop_id = request.form.get('prop_id')
    name = request.form.get('name')
    rental_income = (request.form.get('rental_income'))
    laundry = request.form.get('laundry')
    storage = request.form.get('storage')
    misc = request.form.get('misc')
    mortgage = request.form.get('mortgage')
    tax = request.form.get('tax')
    insurance = request.form.get('insurance')
    utilities = request.form.get('utilities')
    hoa = request.form.get('hoa')
    lawn_snow = request.form.get('lawn_snow')
    vacancy = request.form.get('vacancy')
    repairs = request.form.get('repairs')
    cap_ex = request.form.get('cap_ex')
    prop_man = request.form.get('prop_man')
    down_payment = request.form.get('down_payment')
    closing_costs = request.form.get('closing_costs')
    remodel_budget = request.form.get('remodel_budget')
    misc_invest = request.form.get('misc_invest')
    
    
    
    values_0 = [laundry,storage,misc,tax,insurance,utilities,hoa,lawn_snow,vacancy,repairs,cap_ex,prop_man,down_payment,closing_costs]
        
    values_1 = [rental_income,mortgage,down_payment,closing_costs]
        
    if name == '' or name == None:
        flash('Name can not be empty', category='error')
        return redirect(url_for('views.properties'))
    
    for value in values_1:
        if value == '' or value == None:
            flash('Rental income, mortgage, down payment, closing_costs all require greater then 0.00 input.', category='error')
            return redirect(url_for('views.properties'))
    
    for value in values_0:
        if value == '' or value == None:
            flash('All fields are required. Input 0.00 for non applicable fields.', category='error')
            return redirect(url_for('views.properties'))

    property = Property.query.filter_by(id=prop_id).first()
    
    property.name = name
    property.rental_income = round(float(rental_income), 2)
    property.storage = round(float(storage), 2)
    property.laundry = round(float(laundry), 2)
    property.misc = round(float(misc), 2)
    property.mortgage = round(float(mortgage), 2)
    property.tax = round(float(tax), 2)
    property.insurance = round(float(insurance), 2)
    property.utilities = round(float(utilities), 2)
    property.hoa = round(float(hoa), 2)
    property.lawn_snow = round(float(lawn_snow), 2)
    property.vacancy = round(float(vacancy), 2)
    property.repairs = round(float(repairs), 2)
    property.cap_ex = round(float(cap_ex), 2)
    property.prop_man = round(float(prop_man), 2)
    property.down_payment = round(float(down_payment), 2)
    property.closing_costs = round(float(closing_costs), 2)
    property.remodel_budget = round(float(remodel_budget), 2)
    property.misc_invest = round(float(misc_invest), 2)
    
    property.calc_annual_roi()
    
    db.session.commit()
        
    flash('Property Updated.',category='success')
    return redirect(url_for('views.properties'))




@views.route('/properties')
@login_required
def properties():
    return render_template('properties.html', user=current_user)


@views.route('/remove_property', methods=['POST'])
@login_required
def remove_property():
    prop_id = request.form.get('prop_id')

    # Remove element from the database
    property = Property.query.filter_by(id=prop_id).first()
    if property:
        db.session.delete(property)
        db.session.commit()
        flash('Property deleted.', category='success')
    else:
        flash('Property no longer exists.', category='error')
    return redirect(url_for('views.properties'))


