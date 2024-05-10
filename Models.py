from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class books(db.Model): ## Esto indica que es una clase de tipo modelo
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    year = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer)

##Aca coloco un constructor con el metodo __init__

    def __init__(self, title, year, score):
        super().__init__()
        self.title=title
        self.year=year
        self.score=score

        

    def __str__(self):
        return "\nId: {}. Title: {}. Year: {}. Score: {}.\n".format(
            self.id,
            self.title,
            self.year,
            self.score
        )

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "score": self.score
        }
