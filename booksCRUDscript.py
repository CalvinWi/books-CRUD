import json
from bson import json_util
from pymongo import MongoClient
import datetime
import pprint

#This script was created to show my skills with algorithms and data structures. The script contains a function for each CRUD operation.
#The user can use the script to make it easier to manage the books collection no matter what local database it was imported to.
#The script only works with the books.json file which can be found in my eportfolio.

connection = MongoClient('localhost', 27017)

#The user can import the books json into any local database and still use the CRUD functions with the books collection.
print("Import books.json to desired database before using CRUD functions.")
userDatabase = input("Enter Name of Database books.json was Imported Into:")
db = connection[userDatabase]
collection = db['books']



#CREATE function for inserting new document
def insert_document(document):
	try:
		collection.insert_one(document)
	except TypeError as te:
		result = "False"
		return result
	else:
		result = "True"
		return result

#READ function for searching for document
def find_document(document):
	try:
		result = collection.find(document)
	except TypeError as te:
		print("Type Error: " + str(te))
		return result
	else:
		return result

#UPDATE function for updating document
def update_document(searchQuery, document):
	try:
		#The user can only update one document at a time
		collection.update_one(searchQuery, {"$set" : document})
		result = collection.find(searchQuery)
	except TypeError as te:
		print("Type Error: " + str(te))
		return result
	except Exception as we:
		print("Write Error " + str(we))
		return result
	else:
		return result

#DELETE function for deleting document
def delete_document(document):
	try:
		result = collection.find(document)
	except TypeError as te:
		print("Type Error: " + str(te))
		result = "False"
	else:
		if result.count() > 0:
			print("Document found")

			for document in result:
				pprint.pprint(document)

			result = "True"
		else:
			result = "False"
	finally:
		collection.delete_one(document)

	return result

#Main Method
def main():
	#The user is given a list of choices of CRUD operations
	print("Available CRUD Functions:\nCreate\nRead\nUpdate\nDelete") 
	userChoice = input("Enter choice as displayed:")

	#Code for Create choice
	if userChoice == "Create":
		title = input("Enter Title Value: ")
		author = input("Enter Author Value: ")
		yearPub = int(input("Enter Year of Publication Value: "))
		fictionNon = input("Enter Fiction/NonFiction Value: ")
		genre = input("Enter Genre Value: ")
		pages = int(input("Enter # of Pages Value: "))
		purchased = input("Enter Purchased? Value: ")
		myDocument = {
			"Title" : title,
			"Author" : author,
			"Year of Publication" : yearPub,
			"Fiction/NonFiction" : fictionNon,
			"Genre" : genre,
			"# of Pages" : pages,
			"Purchased" : purchased
		}

		try:
			print(insert_document(myDocument))
		except NameError as ne:
			print("False")

	#Code for Read choice		
	elif userChoice == "Read":
		#The user can perform a simple query to search a single key for a specific value
		print("Search Keys Are:\nTitle\nAuthor\nYear of Publication\nFiction/NonFiction\nGenre\n# of Pages\nPurchased?")
		queryKey = input("Enter key to be searched as displayed: ")

		#Checks if user selects key that holds integer value type and converts user's input to integer if true
		if queryKey == "Year of Publication" or queryKey == "# of Pages":
			queryValue = int(input("Enter value to be searched for: "))
		else:
			queryValue = input("Enter value to be searched for: ")

		completeQuery = {queryKey : queryValue}

		try:
			cursor = find_document(completeQuery)

			if cursor.count() > 0:
				for document in cursor:
					pprint.pprint(document)
			else:
				print("No documents found")
		except NameError as ne:
			print("Name Error: " + str(ne))

	#Code for Update choice
	elif userChoice == "Update":
		#The user must use the 'Title' key to find the document to be updated and can only update one key/value pair at a time
		print("You must use the 'Title' key to find the document you wish to update.")
		searchValue = input("Enter the value for the 'Title' key of the document you wish to update: ")
		searchComplete = {"Title" : searchValue}

		print("You can update a document one key/value pair at a time.")
		updateKey = input("Enter the key to be updated: ")

		#Checks if user selects key that holds integer value type and converts user's input to integer if true
		if updateKey == "Year of Publication" or updateKey == "# of Pages":
			updateValue = int(input("Enter the value to be updated: "))
		else:
			updateValue = input("Enter the value to be updated: ")

		completeUpdate = {updateKey : updateValue}

		try:
			cursor = update_document(searchComplete, completeUpdate)

			if cursor.count() > 0 or cursor == None:
				for document in cursor:
					pprint.pprint(document)
			else:
				print("No documents found")
		except NameError as ne:
			print("Name Error: " + str(ne))

	#Code for Delete choice
	elif userChoice == "Delete":
		#The user must use the Title key to find the document to be deleted because the values should be unique.
		print("You must use the 'Title' key to find the document you wish to delete.")
		deleteValue = input("Enter the value for the 'Title' key of the document you wish to delete: ")

		deleteComplete = {"Title" : deleteValue}

		try:
			cursor = delete_document(deleteComplete)

			if cursor == "False":
				print("No documents found")
		except TypeError as te:
			print("Type Error: " + str(te))

	else:
		print("Error: You must enter one of the four values as displayed. Please relaunch the script.")

main()