from flask import render_template, request, redirect, url_for
from models import db, Expense
from datetime import datetime

def init_routes(app):

    @app.route('/')
    def index():
        expenses = Expense.query.order_by(Expense.date.desc()).all()
        # Monthly summary
        summary = {}
        categories = {}
        for exp in expenses:
            month = exp.date.strftime("%Y-%m")
            summary[month] = summary.get(month, 0) + exp.amount
            categories[exp.category] = categories.get(exp.category, 0) + exp.amount
        return render_template('index.html', expenses=expenses, summary=summary, categories=categories)

    @app.route('/add', methods=['GET', 'POST'])
    def add_expense():
        if request.method == 'POST':
            amount = float(request.form['amount'])
            category = request.form['category']
            description = request.form['description']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            new_expense = Expense(amount=amount, category=category, description=description, date=date)
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_expense.html')

    @app.route('/delete/<int:id>')
    def delete_expense(id):
        exp = Expense.query.get_or_404(id)
        db.session.delete(exp)
        db.session.commit()
        return redirect(url_for('index'))

