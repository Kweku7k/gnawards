# from _typeshed import NoneType
from email.policy import default
from json.tool import main
from unicodedata import category
from flask import Flask,redirect,url_for,render_template,request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import *
# from werkzeug.utils import secure_filename
# from werkzeug.utils import 
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_uploads import configure_uploads, IMAGES, UploadSet
from PIL import Image
import os
from flask_migrate import Migrate
import urllib.request, urllib.parse
import urllib
import secrets
import os
import psycopg2

app=Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# UPLOAD_FOLDER = 'static/img/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SECRET_KEY'] = 'll91628bb0b13ce0c676d32e2vsba245'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://eaozkuagjcyspm:4b1d05b75a1d0e956977ccab32d3c6542ad6f433d65ef2ea7cd9d0e3be069e77@ec2-3-217-251-77.compute-1.amazonaws.com:5432/d3nljg5tlb58ot'
# Takes the name of the file and the extensions
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class Posts(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String)
    image_file = db.Column(db.String(2000), default='default.png')
    
    def __repr__(self):
        return f"Posts('{self.id}', '{self.title}')"

class Candidates(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    subcategory = db.Column(db.String)
    description = db.Column(db.String)
    number = db.Column(db.String(), default=0)
    age = db.Column(db.String)
    institution = db.Column(db.String())    
    votes = db.Column(db.Integer, default = 0)
    image_file = db.Column(db.String(2000), default='default.png')
    picture = db.Column(db.String(2000), default='default.png')
    updatedVotes = db.Column(db.Integer, default = 0)
    testField = db.Column(db.String(2000), default="Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing. You'll see the number of characters and words increase or decrease as you type, delete, and edit them. You can also copy and paste text from another program over into the online editor above. The Auto-Save feature will make sure you won't lose any changes while editing, even if you leave the site and come back later. Tip: Bookmark this page now.Knowing the word count of a text can be important. For example, if an author has to write a minimum or maximum amount of words for an article, essay, report, story, book, paper, you name it. WordCounter will help to make sure its word count reaches a specific requirement or stays within a certain limit.In addition, WordCounter shows you the top 10 keywords and keyword density of the article you're writing. This allows you to know which keywords you use how often and at what percentages. This can prevent you from over-using certain words or word combinations and check for best distribution of keywords in your writing.In the Details overview you can see the average speaking and reading time for your text, while Reading Level is an indicator of the education level a person would need in order to understand the words you’re using.Disclaimer: We strive to make our tools as accurate as possible but we cannot guarantee it will always be so.")
    
    # approved = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Candidates('{self.id}', '{self.name}')"


class Issue(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String)
    
    def __repr__(self):
        return f"Issue('{self.id}', '{self.title}')"

class Feedback(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Feedback('{self.id}', '{self.phone}')"

class Votes(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    candidateId = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    amount = db.Column(db.String)
    ref = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Vote Ghc('{self.amount}', ' - {self.candidateId}')"

class Category(db.Model):
    tablename = ['Cateogy']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Category ('{self.title}')"


class SubCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.String)
    title = db.Column(db.String)
    mainCategory = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"SubCategory ('{self.title}' = '{self.parent}' )"


class Gallery(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # link = db.Column(db.String)
    image = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Gallery Ghc('{self.id}', ' - {self.title}')"

# functions
# 1856913067:AAF6ZpmhgQ8BcTZASwlyaeELB0V5CaXVZZs

def sendtelegram(params):
    url = "https://api.telegram.org/bot1856913067:AAF6ZpmhgQ8BcTZASwlyaeELB0V5CaXVZZs/sendMessage?chat_id=-594997151&text=" + urllib.parse.quote(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    return content


# @app.route('/',methods=['GET','POST'])
# def home():
#     candidates = Candidates.query.all()
#     limitpost = Posts.query.order_by(Posts.id.desc()).limit(3).all()
#     print("The Posts" + str(limitpost)) 
#     return render_template('index.html', candidates=candidates, limitpost=limitpost)

@app.route('/faceofcu',methods=['GET','POST'])
def faceofcu():
    candidates = Candidates.query.all()
    return render_template('faceofcu.html', candidates=candidates)
# Default Config
@app.route('/',methods=['GET','POST'])
def home():
    limitpost = Posts.query.order_by(Posts.id.desc()).limit(3).all()
    categories = SubCategory.query.order_by(SubCategory.id.desc()).all()
    print("The Posts" + str(limitpost)) 
    return render_template('index.html', categories=categories,limitpost=limitpost)

@app.route("/post/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    print(post)
    return render_template('post.html', post=post)

@app.route("/addcontestant", methods=['POST','GET'])    
def addcontestant():
    form = AddContestant()
    print("in form function")
    categories = Category.query.all()
    subcategories = SubCategory.query.all()
    if form.validate_on_submit():
        print("validated successful")
        newForm = Candidates(name=form.name.data, age="21", category=form.category.data, description=form.description.data, institution=form.institution.data, image_file="form.picture.data", votes=form.votes.data, number=form.number.data, testField = form.picture.data)
        db.session.add(newForm)
        db.session.commit()
        flash(f' ' + form.name.data + ' has been nominated for review', 'success')
        # sendtelegram(form.name.data + " has been nominated. Call on:" + form.number.data) 
        newNominationMessage="New Nomination:" +"\n" + form.name.data + " : " + form.number.data + "\n" + form.description.data + "\n" + "Category : " + form.category.data  + "\n" + "Instituition : " + form.institution.data  + "\n" + form.picture.data
        sendtelegram(newNominationMessage) 
        # return redirect(url_for('adminCandidates'))
        return redirect(url_for('home'))
    # else:
    #     return redirect(url_for('home'))
        # flash(f'There has been a problem, please try again later', 'danger')
        
    return render_template('addcontestant.html', form=form, subcategories=subcategories, categories=categories)

@app.route("/addcategory", methods=['POST','GET'])    
def addCategory():
    form = AddCategory()
    categories = Category.query.order_by(Category.id.desc()).all()
    if form.validate_on_submit():
        newCategory = Category(title=form.title.data)
        db.session.add(newCategory)
        db.session.commit()
        flash(f' ' + form.title.data + ' category has been created', 'success')
        # sendtelegram(form.name.data + " has been nominated. Call on:" + form.number.data) 
        # newNominationMessage="New Nomination:" + form.name.data + " : " + form.number.data + "\n" + form.description.data
        # sendtelegram(newNominationMessage) 
        # return redirect(url_for('adminCandidates'))
        return redirect(url_for('addCategory'))
    return render_template('addcategory.html', categories=categories, form=form)

@app.route("/addsubcategory", methods=['POST','GET'])    
def addSubCategory():
    # form = AddCategory()
    mainCategory = "asdf"
    print(mainCategory)
    categories = Category.query.order_by(Category.id.desc()).all()
    subcategories = SubCategory.query.all()
    if request.method == 'POST':
        mainCategory = request.form.get('category')
        newSubcategory = SubCategory(parent=mainCategory, title=request.form.get('subcategory'))
        db.session.add(newSubcategory)
        db.session.commit()
        flash(f' ' + mainCategory + ' subcategory has been created', 'success')
        # sendtelegram(form.name.data + " has been nominated. Call on:" + form.number.data) 
        # newNominationMessage="New Nomination:" + form.name.data + " : " + form.number.data + "\n" + form.description.data
        # sendtelegram(newNominationMessage) 
        # return redirect(url_for('adminCandidates'))
        return redirect(url_for('addSubCategory'))
    return render_template('addsubcategory.html', categories=categories, subcategories=subcategories )

@app.route("/category/<string:category>")
def showCategory(category):
    print(category)
    # session['username'] = 'admin'
    candidates = Candidates.query.filter_by(category = category).all()
    print(candidates)
    return render_template('allCandidates.html', category=category, candidates=candidates)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted','danger')
    print(post)
    return redirect(url_for('adminPosts'))

@app.route("/deletecandidate/<int:candidate_id>")
def deleteCandidate(candidate_id):
    candidate = Candidates.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    flash(f'Your post has been deleted','danger')
    print(candidate)
    return redirect(url_for('adminCandidates'))


@app.route("/edit/<int:post_id>", methods=['GET','POST'])
def edit(post_id):
    form = AddPostForm()
    post = Posts.query.get_or_404(post_id)
    print(post.id)
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.author.data = post.author
    elif request.method == 'POST':
        print("Post ")
        if form.validate_on_submit(): 
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash(f'Your post has been editted succesfully','success')
            return redirect(url_for('adminPosts'))
            print(post)
    return render_template('editpost.html', form=form, title=post.id, post=post)

# Candidate Edit
@app.route("/editCandidate/<int:candidate_id>", methods=['GET','POST'])
def editCandidate(candidate_id):
    form = AddContestant()
    candidate = Candidates.query.get_or_404(candidate_id)
    print(candidate_id)
    if request.method == 'GET':
        form.name.data = candidate.name
        form.description.data = candidate.description
        form.age.data = candidate.age
        form.votes.data = candidate.votes
    elif request.method == 'POST':
        print("Post ")
        if form.validate_on_submit(): 
            candidate.name = form.name.data
            candidate.description = form.description.data
            candidate.votes = form.votes.data
            db.session.commit()
            flash(f'Your post has been editted succesfully','success')
            return redirect(url_for('adminCandidates'))
    return render_template('editcandidate.html', form=form, candidate=candidate, post=post)

@app.route('/updates')
def updates(): 
    posts = Posts.query.all()
    return render_template('updates.html', posts=posts)


@app.route('/gallery')
def gallery():  
    pictures = Gallery.query.all()
    return render_template('gallery.html', gallery=pictures)


@app.route("/uploadGallery", methods=['POST','GET'])
def uploadGallery():
    form = AddGallery()
    if form.validate_on_submit():
        newImage = Gallery(title=form.title.data, image=form.image.data )
        db.session.add(newImage)
        db.session.commit()
        return redirect(url_for('gallery'))

    return render_template('uploadgallery.html', form=form)

# @app.route("/faceofcu")
# def faceofcu():
#     return render_template('faceOfCu.html')

@app.route("/fpreview/<int:id>")
def fpreview(id):
    candidate = Candidates.query.get_or_404(id)
    return render_template('faceofcupreview.html', candidate=candidate)


@app.route("/payment")
def payment():
    return render_template('payment.html')

@app.route("/votes")
def votes():
    return render_template('votes.html')
    
@app.route("/thanks/<int:id>/<int:amount>/<string:ref>")
def thanks(id, amount, ref):
    user = Candidates.query.get_or_404(id)
    print(user.votes)
    print("amount-" + str(amount))
    amount = amount / 100
    print(ref)
    print("amount-" + str(amount))
    candidate = Candidates.query.get_or_404(id)
    print(str(amount) + " votes have been added to " + str(candidate.updatedVotes) + "For " + str(candidate.name))
    # user.votes = user.votes + amount
    newVote = Votes(candidateId = id, amount=amount, ref=ref, name=candidate.name)
    # candidate.updatedVotes = candidate.updatedVotes + amount
    # print("Total of" + str(candidate.updatedVotes) )
    db.session.add(newVote)
    db.session.commit()

    
    print("User Votes = " + str(user.votes))
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0545977791, 0544588320" #SMS recepient"s phone number
    message = str(amount) + ' votes(s) have been cast for ' + user.name
    sender_id = "PrestoSl" #11 Characters maximum
    # send_sms(api_key,phone,message,sender_id)
    amount = round(amount / 0.5)

    # sendtelegram(message)
    flash(f'' + str(amount) + ' votes(s) have been cast for ' + user.name,'success')
    return redirect(url_for('home'))
    # return render_template('thankyou.html')
       
@app.route("/nothanks/<int:id>/<int:amount>")
def nothanks(id, amount):
    user = Candidates.query.get_or_404(id) 
    print(user.votes)
    print("User Votes = " + str(user.votes))
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0545977791" #SMS recepient"s phone number
    message = str(amount) + ' votes(s) was being attempted to cast for ' + user.name
    sender_id = "PrestoSl" #11 Characters maximum
    # send_sms(api_key,phone,message,sender_id)
    flash(f'' + str(amount) + ' votes(s) was being attempted to cast for ' + user.name,'danger')
    return redirect(url_for('home'))
    # return render_template('thankyou.html')
    
     
def send_sms(api_key,phone,message,sender_id):
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":sender_id}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print (content)
    print (url)
# @app.route('/msgtry', methods=['POST','GET'])
def next():
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0545977791" #SMS recepient"s phone number
    message = "Your payment was successful?"
    sender_id = "PrestoSl" #11 Characters maximum
    send_sms(api_key,phone,message,sender_id)
    return render_template('menu.html')


@app.route('/admin')
def admin():    
    return render_template('admin.html')


@app.route("/profile/<int:id>")
def profile(id):
    return render_template('profile.html')

@app.route("/update/<int:id>")
def update(id):
    return render_template('update.html')

@app.route("/feedback",methods=['GET','POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        print("Done")
        newFeedback = Feedback(phone=form.phone.data, feedback=form.feedback.data)
        db.session.add(newFeedback)
        db.session.commit()
        sendtelegram(form.feedback.data)
        flash(f'Your feedback has been submitted successfully','success')
        return redirect(url_for('home'))
    return render_template('feedback.html', form=form)

@app.route("/admin/posts")
def adminPosts():
    posts = Posts.query.order_by(Posts.id.desc()).all()
    return render_template('posts.html', posts=posts)

@app.route("/admin/candidates")
def adminCandidates():
    candidates = Candidates.query.all()
    return render_template('candidates.html', candidates=candidates)

@app.route("/admin/votes/logs")
def adminvoteslogs():
    votes = Votes.query.order_by(Votes.id.desc()).all()
    return render_template('adminvoteslogs.html', votes=votes)
 

@app.route("/admin/votes")
def adminvotes():
    candidates = Candidates.query.order_by(Candidates.votes.desc()).all()
    votes = Votes.query.all()
    totalamount = 0
    totaloldvotes = 0

    # Calculate the votes in db before logs
    for old_vote in candidates:
        totaloldvotes = totaloldvotes + old_vote.votes
    print("Total votes " + str(totaloldvotes))
    # Calculate votes from logs 
    # for vote in votes:
    #     totalamount = totalamount + float(vote.amount)
    # totalamount = totaloldvotes + totalamount

    # print("Total Amount is " + str( totalamount))

    # for loop to assign votes to candidates
    # for candidate in candidates:

    #     print(candidate)
    #     candidateVotes = Votes.query.filter_by(candidateId = str(candidate.id)).all()
    #     candidateTotalVotes = 0

    #     for vote in candidateVotes:
    #         candidateTotalVotes = candidateTotalVotes + float(vote.amount)
        

    #     print("Total Votes for "  + candidate.name + " " + str(candidateTotalVotes))
    #     candidate.updatedVotes = candidate.votes + candidateTotalVotes
    #     db.session.commit()
    #     print("------")

        # print("All The Votes are" + str(votes))
    print("Total amount of money recieved is " + str(totalamount))
    return render_template('adminvotes.html', candidates=candidates, totalamount=totalamount)


@app.route("/public/votes")
def publicvotes():
    candidates = Candidates.query.all()
    return render_template('publicvotes.html', candidates=candidates)


@app.route("/addpost", methods=['GET','POST'])
def addpost():
    form = AddPostForm()
    if form.validate_on_submit():
        # print(form.picture.data)
        filename = 'IneruuTrade.png'
        if form.picture.data:
            pass
            # filename = images.save(form.picture.data)
        else:
            filename = 'IneruuTrade.png'
        # print(filename)
        newPost = Posts(title=form.title.data, content=form.content.data, author=form.author.data, image_file = filename)
        db.session.add(newPost)
        db.session.commit()
        print("Form has been submitted successfully")
        flash(f'Your post has been uploaded successfully', 'success')

        return redirect(url_for('admin'))
    return render_template('addpost.html', form=form)


@app.route("/raiseissue", methods=['GET','POST'])
def raiseissue():
    form = RaiseIssue()
    if form.validate_on_submit():
        newIssue = Issue(title=form.title.data, content=form.content.data, author=form.author.data, image_file=form.picture.data)
        db.session.add(newIssue)
        db.session.commit()
        print("Form has been submitted successfully")
        flash(f'Your post has been uploaded successfully', 'success')

        return redirect(url_for('admin'))
    return render_template('addpost.html', form=form)

@app.route("/team")
def team():
    return render_template('team.html')
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True  )