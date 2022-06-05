#!/bin/python3

import sys

#system call of sys.argv[0] will accept an argument that will be used as filename

try:
	filename = sys.argv[1]
	#check to see if the files are entered in the write order
	split_filename = filename.split(".")
	if split_filename[-1] == "html" or split_filename[-1] == "HTML":
		print("A HTML file was entered as an input. Enter a text file to convert it to HTML. Exiting...")
		sys.exit()
	new_filename = sys.argv[2]
	split_new_filename = new_filename.split(".")
	if split_new_filename != "html":
		print("A non-html file was entered as output. Please enter the name of the new HTML document as the second argument with the file name ending in '.html'")
		sys.exit()
except:
	print("This script must be run with 2 arguments.\n1: the filename of the system to be read from.\n2: the name of the file that the resulting html will be placed in.")
	sys.exit()

unread_contents = open(filename, "r")

contents = unread_contents.read()

contents_list = []

newline_character = '\n'

#for unix
try:
	contents_list = contents.split('\n')
#for windows
except:
	contents_list = contents.split('\r\n')
	newline_character = '\r\n'

# to print contents of file
#print(contents.read())

print(contents_list)

#open file to write to

new_file_writer = open(new_filename, "w")
#new_file_writer.write()

#preliminaries
new_file_writer.write("<!DOCTYPE html>" + newline_character)
new_file_writer.write("<html>" + newline_character)

# head info
new_file_writer.write('\t' + "<head>" + newline_character)
new_file_writer.write('\t\t' + "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">" + newline_character)

# find first line of text and make it the page title
i = 0
while i < len(contents_list):
	if contents_list[i] == "":
		i += 1
		continue
	else:
		new_file_writer.write('\t\t' + "<title>" + contents_list[i] + "</title>" + newline_character)
		break

#if you want to add a stylesheet. Replace articles.css with stylesheet name
new_file_writer.write('\t\t' + "<link rel=\"stylesheet\" href=\"articles.css\">" + newline_character)

new_file_writer.write('\t' + "</head>" + newline_character)


# body info/ the actual HTML being changed
new_file_writer.write('\t' + "<body>" + newline_character)

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
	if j == 1:
		new_file_writer.write("\t\t<h1>" + contents_list[i] + "</h1>" )
		new_file_writer.write(newline_character)
		i += 1
		j += 1
	else:
		new_file_writer.write("\t\t<p>" + contents_list[i] + "</p>")
		new_file_writer.write(newline_character)
		i += 1
		j += 1


# close preliminaries
new_file_writer.write('\t' + "</body>" + newline_character)
new_file_writer.write("</html>" + newline_character)

# close file writer
new_file_writer.close()
