# rFactor2 Vehicle File Assistant

Easy and automated creation of .veh(icle) files from a provided template by using short lists.

Useful when creating skin packs for addon content or leagues

## Features 

* automatically creates all files from easily editable lists
* automatically assigns start numbers and supports offsets for different classes
* also allows to assign numbers manually (either for all cars or just for some)
* unlimited amount of classes, teams and cars per class
* user defined in-game filters

## Usage

If you use the default file names as in the `example/` directory, you can run the script from command line by typing:

`python VehicleFileAssistant.py`

You can also specify one or all file names and directories yourself:

`python VehicleFileAssistant.py teamList.txt classList.txt in/ out/`

For more details, simply run with the *-h* argument.

### File structure 

The whole concept is fairly easy. First off all you create a `classList.txt` file like this:

	Name=GTE
	Cars=Ferrari, Aston, BMW, Corvette, Porsche, Dodge
	NumberOffset=100
	CategoryPath=VWEC, GTE
	Classes=VWEC, VWEC_GTE

	Name=LMP1
	Cars=Lola
	NumberOffset=0
	CategoryPath=VWEC, GTE
	Classes=VWEC, VWEC_GTE

Then you need to place the .veh files of the cars you want to use in your templates directory.
Name these files like the cars in your class list (e.g. *Ferrari.veh*)

Now you can add as many teams as you like in your `teamList.txt`, using this structure:

	Class=GTE
	Car=Ferrari
	Team=Team Name 1
	Livery=Filename1.dds
	 
	Class=LMP1
	Car=Lola
	Team=Team Name Three
	Livery=Filename3.dds
	
	[...]
	
To add a number for a certain car, just add the line *Number=* after the *Livery=* line:

	Class=LMP1
	Car=Lola
	Team=Car with a number
	Livery=Filename4.dds
	Number=77

## Prerequisites

* Python 3.3 or newer