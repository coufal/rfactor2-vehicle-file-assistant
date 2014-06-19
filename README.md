# rFactor2 Vehicle File Assistant

Automatically creates new .veh files from a provided list of teams and template .veh files.

Useful to create skin packs for leagues or standalone mods

## Features 

* automatically creates all files from easily editable lists
* automatically assigns start numbers and supports offsets for different classes
* unlimited amount of classes, teams and cars per class
* user defined in-game filters

## Usage

If you use the default file names as in the `example/` directory, you can run the script from command line by typing:

`python VehicleFileAssistant.py`

You can also specify one or all file names and directories yourself:

`python VehicleFileAssistant.py teamList.txt classList.txt in/ out/`

For more details, simply run with the *-h* argument.

### File structure 

The whole concept is fairly easy. First off all you create a class list file like this:

> Name=GTE
> Cars=Ferrari, Aston, BMW, Corvette, Porsche, Dodge
> NumberOffset=100
> CategoryPath=VWEC, GTE
> Classes=VWEC, VWEC_GTE
> 
> Name=LMP1
> Cars=Lola
> NumberOffset=0
> CategoryPath=VWEC, GTE
> Classes=VWEC, VWEC_GTE

Then you need to place the .veh files of the cars you want to use in your templates directory.
Name these files like the cars in your class list (e.g. *Ferrari.veh*)

Now you can add as many teams as you like in your team list, using this structure:

> Class=GTE
> Car=Ferrari
> Team=Team Name 1
> Livery=Filename1.dds
> 
> Class=LMP1
> Car=Lola
> Team=Team Name Three
> Livery=Filename3.dds
>
> [...]

## Prerequisites

* Python 3.3 (other versions should work as well)