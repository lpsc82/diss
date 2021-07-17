import DatabaseInterface as di

database = di.DataInterface()

with open("../dataset/infobox_names.txt", "r") as file:
	for line in file:
		database.shared.c.execute("Insert into Infobox(info_name)Values(%s)", (line.replace("\n",""),))
		database.shared.conn.commit()

