from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from pokecard_inventory.forms import CardForm
from pokecard_inventory.models import Poke_Card, db
# from pokecard_inventory.helpers import poke_image_generator

site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    cardform = CardForm()

    try:
        if request.method == 'POST' and cardform.validate_on_submit():
            name = cardform.name.data
            type = cardform.type.data
            series = cardform.series.data
            year = cardform.year.data
            collector_card_number = cardform.collector_card_number.data
            is_graded = cardform.is_graded.data
            grade = cardform.grade.data
            description = cardform.description.data
            for_sale = cardform.for_sale.data
            # add image generator here
            user_token = current_user.token

            card = Poke_Card(name, type, series, year, collector_card_number, is_graded, grade, description, for_sale, user_token)

            db.session.add(card)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Pokemon card not created, please review form and try again.')
    
    user_token = current_user.token
    cards = Poke_Card.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=cardform, cards=cards)