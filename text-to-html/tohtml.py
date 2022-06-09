#!/bin/python3

import sys
import platform

##################### Checking entered filenames #######################################

try:
	filename = sys.argv[1]
	#check to see if the files are entered in the write order
	split_filename = filename.split(".")
	if split_filename[-1] == "html" or split_filename[-1] == "HTML":
		print("A HTML file was entered as an input. Enter a text file to convert it to HTML. Exiting...")
		sys.exit()
	new_filename = sys.argv[2]
	split_new_filename = new_filename.split(".")
	if split_new_filename[-1] != "html":
		print("A non-html file was entered as output. Please enter the name of the new HTML document as the second argument with the file name ending in '.html'")
		sys.exit()
except:
	print("This script must be run with 2 arguments.\n1: the filename of the system to be read from.\n2: the name of the file that the resulting html will be placed in.")
	sys.exit()

try:
	unread_contents = open(filename, "r")
except:
	print(filename + " was not found. Exiting...")
	sys.exit()


######################## End of checking filenames ####################################
######################## Start of reading first file ##################################

contents = unread_contents.read()

contents_list = []

newline_character = '\n'

if platform.system() == "Linux" or platform.system() == "Darwin":
	contents_list = contents.split('\n')
elif platform.system() == "Windows":
	contents_list = contents.split('\r\n')
	newline_character = '\r\n'
else:
	print("Could not identify OS. Exiting...")
	sys.exit()

######################### End of reading first file ###################################
######################## Start of selecting options of HTML format ####################

successful_input = False
options = {
	"title": 0,
	"subtitle": 0,
	"author": 0,
	"php": 0
}

while successful_input == False:
	option_input = input("Select the option you would like:" + newline_character + "1) default (Only title on top line is stylized). Create full page." + newline_character + "2) Assumes there is a php header and footer. Otherwise mirrors option 1." + newline_character + "3) custom" + newline_character)

	if option_input == str(1):
		options = {
			"title": 1,
			"subtitle": 0,
			"author": 0,
			"php": 0
		}
		successful_input = True
	elif option_input == str(2):
		options = {
			"title": 1,
			"subtitle": 0,
			"author": 0,
			"php": 1
		}
		successful_input = True
	elif option_input == str(3):
		# TODO create checks to make sure numbers entered are not the same
		try:
			options["title"] = int(input("Enter what number paragraph of the document contains the title. Enter 0 to skip this option."))
			options["subtitle"] = int(input("Enter what number paragraph of the document contains the subtitle. Enter 0 to skip this option."))
			options["author"] = int(input("Enter what number paragraph of the document contains the author name. Enter 0 to skip this option."))
			options["php"] = int(input("Is this a static HTML page or will it be used with PHP headers and footers? 0 for static page, 1 for PHP."))
			successful_input = True
		except:
			print("Paragraph number must be entered as a number" + newline_character)
	else:
		print("Please enter the number of the option you would like")

######################## End of selecting options of HTML format ######################
######################### Start of writing HTML to second file ########################

#open file to write to
new_file_writer = open(new_filename, "w")


############# Start of header if that html needs to be included / no PHP ##############

if options["php"] == 0:

	#preliminaries
	new_file_writer.write("<!DOCTYPE html>" + newline_character)
	new_file_writer.write("<html lang=en>" + newline_character)

	# head info
	new_file_writer.write('\t' + "<head>" + newline_character)
	new_file_writer.write('\t\t' + "<meta charset=\"utf-8\">" + newline_character)
	new_file_writer.write('\t\t' + "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">" + newline_character)

	# find title and make it the page title
	i = 0
	j = 1
	while i < len(contents_list):
		if contents_list[i] == "":
			i += 1
			continue
		elif j == options["title"]:
			new_file_writer.write('\t\t' + "<title>" + contents_list[i] + "</title>" + newline_character)
			break
		else:
			i += 1
			j += 1

	#if you want to add a stylesheet. Replace articles.css with stylesheet name
	#new_file_writer.write('\t\t' + "<link rel=\"stylesheet\" href=\"articles.css\">" + newline_character)

	new_file_writer.write('\t' + "</head>" + newline_character)


	# body info/ the actual HTML being changed
	new_file_writer.write('\t' + "<body>" + newline_character)

########### End of header if that html needs to be included / no PHP ##################

# is the line of the file being read in
i = 0
# j represents what line that has actual text in it will the current line be in the html
# for example the title will be the first line / where j == 1
j = 1
while i < len(contents_list):
	# get rid of trailing extra line
	if contents_list[i] == "" and i == len(contents_list):
		i += 1
		continue
	if contents_list[i] == "":
		#use the below line if extra lines should be converted into breaks instead of removed
		#new_file_writer.write("\t\t<br>")
		i += 1
		continue
	# creates header/ title. Consider wrapping in a <header> tag
	if j == options["title"]:
		new_file_writer.write("\t\t<h1>" + contents_list[i] + "</h1>" )
		new_file_writer.write(newline_character)
		i += 1
		j += 1
	elif j == options["subtitle"]:
		new_file_writer.write("\t\t<h2>" + contents_list[i] + "</h2>" )
		new_file_writer.write(newline_character)
		i += 1
		j += 1
	elif j == options["author"]:
		new_file_writer.write("\t\t<h5>" + contents_list[i] + "</h5>" )
		new_file_writer.write(newline_character)
		i += 1
		j += 1
	else:
		new_file_writer.write("\t\t<p>" + contents_list[i] + "</p>")
		new_file_writer.write(newline_character)
		i += 1
		j += 1


############################ No PHP/ add footer starts ########################################
if options["php"] == 0:
	# close preliminaries
	new_file_writer.write('\t' + "</body>" + newline_character)
	new_file_writer.write("</html>" + newline_character)
############################ No PHP/ add footer ends ##########################################

# close file writer
new_file_writer.close()

############################ End of writting HTML to second file #############################
