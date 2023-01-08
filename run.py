from foodapp import create_app

app=create_app()
if __name__ == "__main__":
    app.run(port=7500,debug=True)
    
### Uncomment this out to find out how to create the database  
# from foodapp.models import db
# from foodapp import create_app
# app=create_app()
# app.app_context().push()
# db.create_all()