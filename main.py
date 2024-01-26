from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from get_movie import search_movie
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass
db =  SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
# CREATE TABLE
class Movie(db.Model):
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    year : Mapped[str] = mapped_column(String(250), nullable=False)
    description : Mapped[str] = mapped_column(String(250),nullable=False)
    rating : Mapped[float] = mapped_column(Float,nullable=False)
    ranking : Mapped[int] = mapped_column(Integer,nullable=False)
    review : Mapped[str] = mapped_column(String(250),nullable=False)
    img_url : Mapped[str] = mapped_column(String(250),nullable=False)

with app.app_context():
    db.create_all()

#FORM
class UpdateForm(FlaskForm):
    out_rating = StringField("Your Rating Out of 10 e.g 7.5",validators=[DataRequired()])
    out_review = StringField("Review",validators=[DataRequired()])
    submit = SubmitField('submit')

class FindMovie(FlaskForm):
    title = StringField("Movie Title",validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()
    print(all_movies)
    #Compare movies
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
        print(all_movies[i].title,'-',all_movies[i].ranking)
    return render_template("index.html",movies = all_movies)

@app.route('/edit', methods = ['GET','POST'])
def edit():
    update_form =  UpdateForm()
    movie_id = request.args.get('id')
    movie_to_update = db.get_or_404(Movie,movie_id)
    if request.method == "POST":
        movie_to_update.rating = update_form.out_rating.data
        movie_to_update.review = update_form.out_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',form= update_form)

@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    print(movie_id)
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home')) 

@app.route('/add', methods=['GET','POST'])
def add():
    add_movie = FindMovie()
    if request.method == "POST":
        print(add_movie.title.data)
        results = search_movie(add_movie.title.data)
        if results:
            #Add check points if movie exists or not
            return render_template('select.html',results = results)
        
    return render_template('add.html',form=add_movie)

@app.route('/add_db',methods = ['GET','POST'])
def add_db():
    new_movie = Movie(
    id = request.args.get('id'),
    title=request.args.get('title'),
    year=request.args.get('year'),
    description=request.args.get('description'),
    rating=request.args.get('rating'),
    ranking=4,
    review="No rewviews yet",
    img_url=request.args.get('img_url'))
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit',id=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
