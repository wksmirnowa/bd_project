from flask import Blueprint, render_template, redirect

from services.musician_service import MusicianService
from web_forms.musician_form import MusicianForm

musician_urls = Blueprint("", __name__)


@musician_urls.route('/musicians')
def musicians():
    musicians = MusicianService().find()
    return render_template('musicians.html', musicians=musicians)


@musician_urls.route('/musician', methods=['GET', 'POST'])
def musician():
    form = MusicianForm()
    if form.validate_on_submit():
        MusicianService().save(form)
        return redirect('/musicians')
    return render_template('musician.html', form=form)


@musician_urls.route('/musician/<id>')
def musician_id(id):
    musician_for_html = MusicianService().find(id=id)
    if len(musician_for_html) == 1:
        musician_for_html = musician_for_html[0]
    else:
        return 'Oops'
    form = MusicianForm()
    form.specialization.data = musician_for_html['specialization']
    form.surname.data = musician_for_html['surname']
    form.firstname.data = musician_for_html['firstname']
    if form.validate_on_submit():
        MusicianService().save(form, id=id)
        return redirect('/musicians')
    return render_template('musician.html', form=form)