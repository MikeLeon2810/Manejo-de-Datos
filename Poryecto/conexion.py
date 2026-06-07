import mysql.connector


# Create a connection to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkuniverse_08",
    database="sistema_paqueteria",
    port=3306
)

cursor = conn.cursor()



# cursor.execute("SELECT * FROM socio")
# result = cursor.fetchall()

# for row in result:
#     print(row)

# # Close the cursor and connection
# cursor.close()
# conn.close()






