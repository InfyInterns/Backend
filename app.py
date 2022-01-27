from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password123@localhost/knowledge_portal'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key = True)
    topic_title = db. Column(db.String(100), nullable = False)
    topic_description = db.Column(db.String(500), nullable = False)
    posts = db.relationship('Post', backref='topic', lazy='dynamic')


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    post_title = db. Column(db.String(100), nullable = False)
    post_description = db.Column(db.String(500), nullable = False)

@app.route('/topics', methods = ['GET'])
def gettopics():
    all_topics = []
    topics = Topic.query.all()
    for topic in topics:
          results = {
                    "topic_id":topic.id,
                    "topic_title":topic.topic_title,
                    "topic_description":topic.topic_description, }
          all_topics.append(results)
     
    
    return jsonify(
            {
                "success": True,
                "topics": all_topics,
            }
        )

@app.route('/post', methods = ['POST'])
def create_post():
    post_data = request.json

    topic_id= db.session.query(Topic).filter_by(topic_title=post_data['topic_title']).first().id

    post_title = post_data['post_title']
    post_description = post_data['post_description']

    post = Post(topic_id=topic_id,post_title =post_title ,post_description =post_description )

    db.session.add(post)
    db.session.commit()
    

    return jsonify({"success": True,"response":"Post added"})

@app.route('/topics/<int:topic_id>', methods = ['GET'])
def getposts_under_specific_topic(topic_id):
    all_posts = []
    posts = db.session.query(Post).filter_by(topic_id=topic_id).all()
    for post in posts:
          results = {
                    "post_id":post.id,
                    "post_title":post.post_title,
                    "post_description":post.post_description, }
          all_posts.append(results)
     
    
    return jsonify(
            {
                "success": True,
                "posts": all_posts,
            }
        )

@app.route('/topics/<int:topic_id>/<int:post_id>', methods = ['PUT'])
def updatepost_under_specific_topic(topic_id,post_id):
    posts = db.session.query(Post).filter_by(topic_id=topic_id).all()
    for post in posts:
       if post.id==post_id:
           post_to_be_update=post
    
    post_title = request.json['post_title']
    post_description = request.json['post_description']

    post_to_be_update.post_title = post_title
    post_to_be_update.post_description = post_description
    db.session.add(post_to_be_update)
    db.session.commit()
     
    
    return jsonify({"success": True,"response":"Post Updated"})

@app.route('/topics/<int:topic_id>/<int:post_id>', methods = ['DELETE'])
def deletepost_under_specific_topic(topic_id,post_id):
    posts = db.session.query(Post).filter_by(topic_id=topic_id).all()
    for post in posts:
       if post.id==post_id:
           post_to_be_delete=post
  
    db.session.delete(post_to_be_delete)
    db.session.commit()
     
    
    return jsonify({"success": True,"response":"Post Deleted"})


if __name__=='__main__':
    app.run(debug=True)
   