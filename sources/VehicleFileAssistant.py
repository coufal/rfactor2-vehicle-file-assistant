"""rFactor2 Vehicle File Assistant by Dennis Coufal <dennis.coufal@gmail.com>

creates rFactor2 .veh files from predefined lists of teams and classes
this is useful for creating skinpacks/leagues

run with argument -h to see options
"""

import re
import os.path
import sys

"""Provides functions to parse and create certain files
"""
class FileHandler():
	def __init__(self, sign_up_list, class_list, template_dir, output_dir):		
		self.sign_up_list=sign_up_list
		self.class_list=class_list
		self.output_dir=output_dir
		self.template_dir=template_dir
		self.checkIfFilesExist()		
			
	def checkIfFilesExist(self):
		list=[self.sign_up_list, self.class_list, self.template_dir]
		for item in list:
			if not os.path.exists(item):
				raise Exception("File not found: {}".format(item))
		if not os.path.exists(self.output_dir):
			os.makedirs(self.output_dir)
	
	def create_veh_file(self,team):		
		lines = [line.strip() for line in open(self.template_dir+team.getCar()+".veh")]
		linesNew = []
		
		for x in range(0,len(lines)):
			linesNew.append("\n")
		for x in range(0,len(lines)):
			if(lines[x].startswith("Number=")):
				linesNew[x]="Number={}".format(team.getNumber())
			elif(lines[x].startswith("DefaultLivery=")):
				linesNew[x]="DefaultLivery=\"{}\"".format(team.getLivery())
			elif(lines[x].startswith("PitGroup=")):
				linesNew[x]="PitGroup=\"Group{}\"".format(team.getNumber())
			elif(lines[x].startswith("Driver=")):
				linesNew[x]="Driver=\"Jon Doe\""
			elif(lines[x].startswith("Description=")):
				linesNew[x]="Description=\"{} #{}\"".format(team.get_name(), team.getNumber())
			elif(lines[x].startswith("FullTeamName=")):
				linesNew[x]="FullTeamName=\"\"".format(team.get_name())
			elif(lines[x].startswith("Team=")):
				linesNew[x]="Team=\"{}\"".format(team.get_name())
			elif(lines[x].startswith("Classes=")):
				linesNew[x]="Classes=\"VWEC, VWEC_{}\"".format(team.getVehClass().get_filtername_classes())
			elif(lines[x].startswith("Category=")):
				linesNew[x]="Category=\"{}\"".format(team.getVehClass().get_category_path())
			else:
				linesNew[x]=lines[x]
		self.list_to_file(linesNew, "{}_{}.veh".format(team.getVehClass().get_name(), team.getNumber()))
		print("Crated: {} {} '{}' #{}".format(team.getVehClass().get_name(), team.getCar(), team.get_name(), team.getNumber()))
		
	def list_to_file(self,content, fname):
		f = open(self.output_dir+fname,'w')
		for x in range(0,len(content)):
			f.write(content[x]+"\n")	
		f.close()

	def parse_signup_list(self, allowed_classes):
		lines = [line.strip() for line in open(self.sign_up_list)]
		teams=[]
		
		for x in range(0,len(lines)):		
			if(lines[x].startswith("Class=")):
				veh_class=allowed_classes.findClassByName(lines[x].replace("Class=",""))					
					
			if(lines[x].startswith("Car=")):
				car_name=lines[x].replace("Car=","")
				if(not allowed_classes.car_nameIsAllowed(car_name, veh_class)):
					raise Exception("unknown CarName: "+lines[x])
					
				#validate if corresponding veh file exist
				if(not os.path.isfile("{}.veh".format(self.template_dir+car_name))):
					raise Exception(("{}.veh template does not exist".format(self.template_dir+car_name)))	
			
			if(lines[x].startswith("Team=")):
				teamName=lines[x].replace("Team=","")
				
			if(lines[x].startswith("Livery=")):
				livery=lines[x].replace("Livery=","")
				
				#start number
				if(len(lines) > x+1 and lines[x+1].startswith("Number=")):
					number=int(lines[x+1].replace("Number=",""))
				else:
					number=veh_class.get_number_counter()+veh_class.get_number_offset()
					veh_class.inc_number_counter()
					
				teams.append(Entry(teamName, veh_class, car_name, livery, number))					
			
		return teams
	
	def parse_class_list(self):
		lines = [line.strip() for line in open(self.class_list)] 
		ret=[]
		for x in range(0,len(lines)):
			if(lines[x].startswith("Name=")):
				name=lines[x].replace("Name=","").strip()
				cars=[x.strip() for x in lines[x+1].replace("Cars=","").split(',')]						
				numberOffset=int(lines[x+2].replace("NumberOffset=","").strip())
				categoryPath=lines[x+3].replace("CategoryPath=","").strip()
				classes=lines[x+4].replace("Classes=","").strip()
				ret.append( VehClass(name, cars, numberOffset, categoryPath, classes) )
		return ret

"""each car class defined in the class list is stored as a VehClass()
"""
class VehClass:	
	def __init__(self, name, allowed_cars, number_offset, category_path, filtername_classes):
		self.name=name
		self.allowed_cars=allowed_cars
		self.number_offset=number_offset
		self.category_path=category_path
		self.filtername_classes=filtername_classes
		self.number_counter=1 #the number to assign to cars automatically
		
	def inc_number_counter(self):
		self.number_counter+=1
		
	def get_number_counter(self):
		return self.number_counter
		
	def get_category_path(self):
		return self.category_path
		
	def get_filtername_classes(self):
		return self.filtername_classes
		
	def get_allowed_cars(self):
		return self.allowed_cars
		
	def get_name(self):
		return self.name
		
	def get_number_offset(self):
		return self.number_offset

"""each team from the sign-up list is stored as an Entry()
"""
class Entry:	
	def __init__(self, name, veh_class, car, livery, number):
		self.name=name
		self.veh_class=veh_class
		self.car=car
		self.livery=livery
		self.number=number		
		
	def getVehClass(self):
		return self.veh_class
		
	def get_name(self):
		return self.name

	def getCar(self):
		return self.car
		
	def getLivery(self):
		return self.livery
		
	def getNumber(self):
		return self.number

"""Stores all vehicle classes in a list and provides functions to access them easily
"""
class VehClassHandler:
	def __init__(self, allowed_classes):
		self.allowed_classes=allowed_classes

	def add(self, veh_class):
		self.allowed_classes.append(veh_class)
		
	def getAllClasses():
		return self.allowed_classes
		
	def findClassByName(self, veh_class_name):
		for x in range(0,len(self.allowed_classes)):
			if(self.allowed_classes[x].get_name() == veh_class_name):
				return self.allowed_classes[x]
		raise Exception("vehicle class not found: "+veh_class_name)
	
	def car_nameIsAllowed(self, car_name, veh_class):		
		if(car_name in self.findClassByName(veh_class.get_name()).get_allowed_cars()):
			return 1
		return 0

"""Open and parse sign-up list and class list and then create .veh file for each team 
"""
class VehFileCreator:
	def __init__(self, sign_up_list, class_list, template_dir, output_dir):
		self.print_startup_msg()
		
		fh=FileHandler(sign_up_list, class_list, template_dir, output_dir)
		teams=fh.parse_signup_list(VehClassHandler(fh.parse_class_list()))

		for x in range(0,len(teams)):
			fh.create_veh_file(teams[x])
		print("\nFinished successfully.")
		
	def print_startup_msg(self):
		version = 1.0
		print("rFactor2 Vehicle File Assistant v{}".format(version))
		print()
		

def main():
	sign_up_list=sys.argv[1] if (len(sys.argv) >1) else "teamList.txt"
	class_list=sys.argv[2] if (len(sys.argv) >2) else "classList.txt"
	template_dir=sys.argv[3] if (len(sys.argv) >3) else "templates/"
	output_dir=sys.argv[4] if (len(sys.argv) >4) else "out/"
	
	if "-h" in sys.argv or "--help" in sys.argv:
		print("Usage:")
		print(">>>{} teamList.txt classList.txt templates/ out/".format(os.path.basename(sys.argv[0])))
		print("\nTo run with default settings, just use:")
		print(">>>{} ".format(os.path.basename(sys.argv[0])))
		print("\nIf you provide fewer arguments, default values will be used for undefined values")		
		sys.exit()
	
	VehFileCreator(sign_up_list, class_list, template_dir, output_dir)
if  __name__ =='__main__':main()
	