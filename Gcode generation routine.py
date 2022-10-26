from math import ceil               # Ceil is used to calculate the number of line per scan
# definition of the geometrical parameters. All dimentions are expressed in mm
Number_Slides = 1                  # number of slides to coat at once
Center_area = (100,125)             # Coordonates of the center of the sample
Tool_offset=(0,50,0)
Orientation_Slide = 0              # direction of the slide's major dimention. 0 for X, 1 for Y
Dimention_Slide = (75.5,25.5)       # dimention of one slide, major dimention first
Positioning_uncertainty = 2         # imprecision on the slides positioning

# definition of the spraying parameter geometry
Spray_diameter = 23                 # diameter of the spray
Hatch = 12                         # distance between two spraying lines
Spray_height = 100 + Tool_offset[2]  # distance between the sample and the spray head
Offest_Purging = 25             # distance from the coating area to begin spaying
Number_layers = 40                 # Number of layers (ie scans)
Temperature_stage = 100            # hotplate temperature in degree
Feedrate = 4800                     # feedrate, displacement speed during spraying
Time_delay = 20                     # Delay between two layers to let the water evaporate

# definition of the file name and file
File_name = "Spray_scan.gcode"      
file_Path = "C:/Users/Remi/Desktop/"
# Create and/or open and overwright the Gcode file
File_handler = open(f'{file_Path}{File_name}',"w")
File_handler.write("(This Gcode is automaticaly generated to control the movement of a spray coater)\n\n")

# Declaration of variables
Spray_height = Spray_height + Tool_offset[2]
Scan_direction = 1-Orientation_Slide    # direction of the scan 0 for X, 1 for Y. The first scan takes place in the samples small direction

# Calculate the distance between the border of the spraying zone and the first line of spray  
Offset_first_line = Hatch-Spray_diameter/2

# Calculate the dimentions of the area to be caoted
if(Orientation_Slide == 0):
    Coating_zone_dimention = (Dimention_Slide[0]+2*Positioning_uncertainty, Number_Slides*Dimention_Slide[1]+2*Positioning_uncertainty)
else:
    Coating_zone_dimention = (Number_Slides*Dimention_Slide[1]+2*Positioning_uncertainty, Dimention_Slide[0]+2*Positioning_uncertainty)

# Calculate the coordonates of the minimum and maximum corners of the area to coat
Min_Coating_coord = (Center_area[0]-Tool_offset[0]-Coating_zone_dimention[0]/2,Center_area[1]-Tool_offset[1]-Coating_zone_dimention[1]/2)
Max_Coating_coord = (Center_area[0]-Tool_offset[0]+Coating_zone_dimention[0]/2,Center_area[1]-Tool_offset[1]+Coating_zone_dimention[1]/2)

# Calculate the number of line of a scan in X and Y directions
Number_line = [0,0]
Number_line [0] = ceil(((Coating_zone_dimention[1]-Offset_first_line)/Hatch)-Offset_first_line/Hatch)+1
Number_line [1] = ceil(((Coating_zone_dimention[0]-Offset_first_line)/Hatch)-Offset_first_line/Hatch)+1
# Remove the space between the border and the first line, divide the rest by hatch, remove the margin on top, rounds to the sup and adds one

# Definition of the line wrighting functions
def print_G1_line (X,Y,Z=-1,E=-1,F=Feedrate):                   # write a movement line
    if(Z==-1 & E==-1):
        File_handler.write(f'G1 X{X} Y{Y}\n')
    elif(Z==-1):
        File_handler.write(f'G1 X{X} Y{Y} E{E}\n')
    elif(E==-1):
        File_handler.write(f'G1 X{X} Y{Y} Z{Z}\n')
    else:
        File_handler.write(f'G1 X{X} Y{Y} Z{Z} E{E} F{F}\n')    # The feedrate is only explicitely overwritten when all aprameters are filled at the beginig of the file
def Spray_ON ():
    File_handler.write("M106 S255\n")                           # Turn ON the cooling fan (spray)
def Set_Z_Max_F ():
    File_handler.write("M203 Z800\n")
def Set_Acc ():
    File_handler.write("M201 X40000 Y40000\nM203 X5000\nM203 Y5000\n")
def Spray_OFF ():
    File_handler.write("M106 S0\n")                             # Turns OFF the cooling fan (spray)
def Delay (Time):
    File_handler.write(f'G4 P{Time*1000}\n')                    # Delay the execution of folowing code for {Time} seconds
def Home ():
    File_handler.write("G28\n")
def HomeXY ():
    File_handler.write("G28 X0 Y0\n")
def Show(str):
    File_handler.write(f'M117 [{str}]\n')
def Temperature (Temperature, Offset=10):
    File_handler.write(f'M140 S{Temperature}\n')                # Set the bed target temperature
    File_handler.write(f'M190 S{Temperature - Offset}\n')       # Wait for the temparature to reach within {Offset} of the target temperature


Curent_position=[0,0]                                           # Stores the curent position
Next_position=[0,0]                                             # Stores the next positon
Line_direction = 1                                              # Indicates the direction of the next line (+ or -1) wether it folows the axes or goes against

# Begining of the file
Set_Z_Max_F()
Set_Acc ()
File_handler.write(f'M140 S{Temperature}\n')
Home()
print_G1_line (0,0,Z=Spray_height,E=1,F=Feedrate)               # move the bed to the designed height and set the feedrate 
Show("Waiting for the bed temperature to stabilize")
Temperature(Temperature_stage)

#print_G1_line (X=Center_area[0],Y=Center_area[1],E=1,Z=Spray_height,F=Feedrate)       # moves to the center of the csample 
#print_G1_line (X=Min_Coating_coord[0],Y=Min_Coating_coord[1],E=1,Z=Spray_height,F=Feedrate)       # moves to one corner of the sample 
#print_G1_line (X=Max_Coating_coord[0],Y=Max_Coating_coord[1],E=1,Z=Spray_height,F=Feedrate)       # moves to the second corner


# Test if the path includes point outside the printer bondaries and stop program execution in that case
if (Min_Coating_coord[0]+Offset_first_line <0 or Min_Coating_coord[1]-Offest_Purging <0 or Min_Coating_coord[1]+Offset_first_line <0 or Min_Coating_coord[0]-Offest_Purging <0 or Min_Coating_coord[0]+Offset_first_line >200 or Min_Coating_coord[1]-Offest_Purging >200 or Min_Coating_coord[1]+Offset_first_line >200 or Min_Coating_coord[0]-Offest_Purging >200):
    print("Curent parameters creates a path outside the machine boundaries")
    exit()


for i in range(Number_layers):                                  # iterate over the number of layers
    Show(f'layer {i} ongoing')
    if (Scan_direction == 1):
        Next_position[0]=Min_Coating_coord[0]+Offset_first_line
        Next_position[1]=Min_Coating_coord[1]-Offest_Purging
    else:
        Next_position[1]=Min_Coating_coord[1]+Offset_first_line
        Next_position[0]=Min_Coating_coord[0]-Offest_Purging
    #Next_position=[Min_Coating_coord[Scan_direction]+Offset_first_line,Min_Coating_coord[1-Scan_direction]-Offest_at_begining]
    
    print_G1_line (X=Next_position[0],Y=Next_position[1])       #goes to the initial point of the scan depending on the scan direction
    
    Curent_position[Scan_direction]=Next_position[Scan_direction]+Offest_Purging-Spray_diameter/2    # Trick current position to enlarge the first line
    Curent_position[1-Scan_direction]=Next_position[1-Scan_direction]  

    ### Implement suplementary movement 
    Spray_ON()
    for j in range(Number_line[Scan_direction]):            # iterate over the number of lines per scan
        Next_position[Scan_direction]=Curent_position[Scan_direction]+Line_direction*(Spray_diameter+Coating_zone_dimention[Scan_direction])
        print_G1_line (X=Next_position[0],Y=Next_position[1],E=10000,Z=Spray_height,F=Feedrate)
        Curent_position=Next_position
        if (j<Number_line[Scan_direction]-1):               # Check if the line is the last of the scan to minimize useless movement and save ink
            Next_position[1-Scan_direction]=Curent_position[1-Scan_direction]+Hatch
            Spray_OFF ()
            # Delay (0.2)
            print_G1_line (X=Next_position[0],Y=Next_position[1],E=10000,Z=Spray_height,F=Feedrate/2)  # Devide feedrate by two for non spraying movments
            Spray_ON ()
            Curent_position=Next_position

        Line_direction=-Line_direction                          # invert the direction of the next line
    Line_direction = 1                                          # Reset the line direction at 1 for the begining of the next scan
    Spray_OFF()                                                 # Stop the spray
    Show("waiting for the ink to dry")
    HomeXY()                                                      # Home X and Y axes to compensate for potential step losses
    Delay(Time_delay)                                           # wait after each layer for the ink to dry
    Scan_direction=1-Scan_direction                             # inverts the scan direction of the next scan
HomeXY()                                                          # Goes back to home position at the end of the spraying
#print (Coating_zone_dimention)                                 # Debug command to print the 
Show("Code finished executing")
print ("Code finished executing")                               # Shows the execution completion of all the code
