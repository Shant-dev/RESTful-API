import falcon
import mysql.connector
import subprocess

class UsersResource:
  def on_get(self, req, resp):
    try:
      connection = mysql.connector.connect( #Connect to DB with the user we created in the mysql ( in the ubuntu terminal)
        host='localhost',
        database='cmp210DB',
        user='neshant',
        password='CT1234ct!')
      cursor = connection.cursor() # make the DB Connection
      cursor.execute("SELECT * FROM users") # Run the query
      rows = cursor.fetchall() # Fetch all the rows from the sql query

      result = [] # Create an empty array
      for row in rows:
        result.append({"id": row[0], "email": row[1], "password": row[2], "name": row[3]}) #add the data to the array with json format

      resp.media = result #The respone back to the browser
      resp.status = falcon.HTTP_200

    except Error as e: # If error in the DB show  the error
      resp.status = falcon.HTTP_500
      resp.media = {'error': str(e)}

    finally:
      if (connection.is_connected()):
        cursor.close()
        connection.close()

class login:
  def on_get(self, req, resp, email, password):
    try:
      connection = mysql.connector.connect( #Connect to DB with the user we created in the mysql ( in the ubuntu terminal)
        host='localhost',
        database='cmp210DB',
        user='neshant',
        password='CT1234ct!')
      cursor = connection.cursor() # make the DB Connection
      cursor.execute("SELECT * FROM users WHERE email = %s and password = %s",(email,password)) # Run the query the email and the password go as vaiables and get the data from the vars in the parenthesis
      rows = cursor.fetchall() # Fetch all the rows from the sql query

      result = [] # Create an empty array
      for row in rows:
        result.append({"id": row[0], "email": row[1], "password": row[2], "name": row[3]}) #add the data to the array with json format

      resp.media = result #The respone back to the browser
      resp.status = falcon.HTTP_200

    except Error as e: # If error in the DB show  the error
      resp.status = falcon.HTTP_500
      resp.media = {'error': str(e)}

    finally:
      if (connection.is_connected()):
        cursor.close()
        connection.close()

class HelloWorld:
	def on_get(self,req,resp):
		resp.media = {'message':'Hello World'} #Shows Hello World ( for debugging purposes))

class registerResources:
  def on_post(self, req, resp, email, password, name):
    try:
      connection = mysql.connector.connect(
        host='localhost',
        database='cmp210DB',
        user='neshant',
        password='CT1234ct!')
      cursor = connection.cursor()
      cursor.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (email, password, name))
      #rows = cursor.fetchall()
      connection.commit()  # Commit changes to the database

     
      resp.media = email #The respone back to the browser
      resp.status = falcon.HTTP_200

    except Error as e: # If error in the DB show  the error
      resp.status = falcon.HTTP_500
      resp.media = {'error': str(e)}


    finally:
      if (connection.is_connected()):
        cursor.close()
        connection.close() 

class Server:

  def on_get(self,req,resp):

    resp.media = {'message':subprocess.getoutput("sh system_information.sh")} #Executes the system_information.sh bash which shows memory usage, network, cpu processes





class Analisys:

  def on_get(self,req,resp):

    resp.media = {'message':subprocess.getoutput("python3 pd13.py")}#Executes pd13.py which uses panda library and matplotlib library


class OpenImageResource:
    def on_get(self, req, resp):
        # Path to the PNG file
        file_path = '/home/neshant/python/pd13_result.png'
        
        try:
            # Using xvfb-run with eog (Eye of GNOME) to open the image
            subprocess.run(['xvfb-run', '-a', 'eog', file_path], check=True)
            resp.status = falcon.HTTP_200
            resp.media = {'message': 'Image opened successfully'}
        except subprocess.CalledProcessError as e:
            resp.status = falcon.HTTP_500
            resp.media = {'error': f'Failed to open {file_path}: {e}'}

class updateResources:
    def on_put(self, req, resp, email, password=None, name=None):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='cmp210DB',
                user='neshant',
                password='CT1234ct!'
            )
            cursor = connection.cursor()

            # Prepare the SQL update statement
            update_fields = []
            update_values = []

            if password:
                update_fields.append("password = %s")
                update_values.append(password)
            
            if name:
                update_fields.append("name = %s")
                update_values.append(name)
            
            if not update_fields:
                resp.status = falcon.HTTP_400
                resp.media = {'error': 'No fields to update'}
                return

            update_values.append(email)
            sql_update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE email = %s"

            cursor.execute(sql_update_query, tuple(update_values))
            connection.commit()  # Commit changes to the database

            if cursor.rowcount == 0:
                resp.status = falcon.HTTP_404
                resp.media = {'error': 'User not found'}
            else:
                resp.status = falcon.HTTP_200
                resp.media = {'message': 'User updated successfully'}

        except Error as e:  # If error in the DB, show the error
            resp.status = falcon.HTTP_500
            resp.media = {'error': str(e)}

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class deleteResources:
    def on_delete(self, req, resp, email):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='cmp210DB',
                user='neshant',
                password='CT1234ct!'
            )
            cursor = connection.cursor()

            # Prepare the SQL delete statement
            sql_delete_query = "DELETE FROM users WHERE email = %s"
            cursor.execute(sql_delete_query, (email,))
            connection.commit()  # Commit changes to the database

            if cursor.rowcount == 0:
                resp.status = falcon.HTTP_404
                resp.media = {'error': 'User not found'}
            else:
                resp.status = falcon.HTTP_200
                resp.media = {'message': 'User deleted successfully'}

        except Error as e:  # If error in the DB, show the error
            resp.status = falcon.HTTP_500
            resp.media = {'error': str(e)}

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

app = falcon.App() # Create the urls
app.add_route('/',HelloWorld()) #When we go to the main url it will show the HelloWorld class from above 
app.add_route('/users',UsersResource()) #When we go to the main url /users it will show the UsersResource class from above
app.add_route('/login/{email}/{password}', login())
app.add_route('/register/{email}/{password}/{name}', registerResources())
app.add_route('/server', Server())
app.add_route('/update', updateResources())
app.add_route('/delete/{email}', deleteResources())
app.add_route('/analytics', Analisys())
app.add_route('/img', OpenImageResource())
