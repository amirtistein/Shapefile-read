import struct
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

File_name = input('input your file:')  


def ReadShapeFile(File_name):
    File = open(File_name, "rb")
    return File

File = ReadShapeFile(File_name)

File_binary = File.read(28)              
File_non_binary = struct.unpack('>iiiiiii',File_binary)
#File Length
Length = File_non_binary[6] * 2


File_binary = File.read(72)            
File_non_binary_2 = struct.unpack('<iidddddddd',File_binary)

Version = File_non_binary_2[0]
Shape_type = File_non_binary_2[1]

#Bounding Box
X_min = File_non_binary_2[2]
Y_min = File_non_binary_2[3]    
X_max = File_non_binary_2[4]
Y_max = File_non_binary_2[5]
Z_min = File_non_binary_2[6]
Z_max = File_non_binary_2[7]    
M_min = File_non_binary_2[8]
M_max = File_non_binary_2[9]



#----------------------------------------------------------
#Null
if(Shape_type==0):
        
    #Headers
    record_header = File.read(8)
    non_record_header = struct.unpack('>ii', record_header)

    Record_Number = non_record_header[0]        
    Countent_Length = non_record_header[1]

    #Null Contents
    record_contents = File.read(0)
    non_record_contents = struct.unpack('<i', record_contents)
    
    shape_type_record = non_record_contents[0]    
        
    print('shapefile is Null')
      
#----------------------------------------------------------    
#point
elif Shape_type == 1:                 
    
    point_number = (Length - 100 ) / 28  
    
    X = []
    Y = []


    for i in range(int(point_number)): 
        File.seek(100+i*28+12)                     
        File_binary = File.read(16)             
        x,y = struct.unpack('<dd',File_binary) 
        X.append(x)
        Y.append(y)
    coordinates = [X ,Y]
    print(coordinates)


#----------------------------------------------------------
#polyline 
elif Shape_type == 3:

       
    counter = 100     
                                   
    Index = []
    Points = [] 
    X_coordinates = []
    Y_coordinates = []        


    while counter != Length:
        File_binary = File.read(12)     
        counter += 12


        File_binary = File.read(32)
        counter += 32
                         
        File_binary = File.read(8)
        Number = struct.unpack('<ii',File_binary)
        counter += 8
    
    
        temp = []           
        for i in range(Number[0]):       
            File_binary = File.read(4)                        
            temp.append(struct.unpack('<i',File_binary)[0])
            counter += 4
            
        Index.append(temp)               


        temp=[]
        x_in_each_part = []
        y_in_each_part = []
        for i in range(Number[1]):
            File_binary = File.read(16)
            temp.append(struct.unpack('<dd',File_binary))
            x_in_each_part.append(struct.unpack('<dd',File_binary)[0])
            y_in_each_part.append(struct.unpack('<dd',File_binary)[1])
            counter += 16
            
            
        Points.append(temp)  
        X_coordinates.append(x_in_each_part) 
        Y_coordinates.append(y_in_each_part)
        
#----------------------------------------------------------
#polygon
elif Shape_type == 5:

      
    counter = 100     
                                   
    Index = []
    Points = [] 
    X_coordinates = []
    Y_coordinates = []        


    while counter != Length:
        File_binary = File.read(12)     
        counter += 12


        File_binary = File.read(32)
        counter += 32
                         
        File_binary = File.read(8)
        Number = struct.unpack('<ii',File_binary)
        counter += 8
    
    
        temp = []           
        for i in range(Number[0]):       
            File_binary = File.read(4)                        
            temp.append(struct.unpack('<i',File_binary)[0])
            counter += 4
            
        Index.append(temp)               


        temp=[]
        x_in_each_part = []
        y_in_each_part = []
        for i in range(Number[1]):
            File_binary = File.read(16)
            temp.append(struct.unpack('<dd',File_binary))
            x_in_each_part.append(struct.unpack('<dd',File_binary)[0])
            y_in_each_part.append(struct.unpack('<dd',File_binary)[1])
            counter += 16
            
            
        Points.append(temp)  
        X_coordinates.append(x_in_each_part) 
        Y_coordinates.append(y_in_each_part)          

#----------------------------------------------------------
#multi_point
elif Shape_type == 8 :         
    counter = 100                               
    coordinates_of_vertices = []        
    Number_of_Points =[]                
    X_coordinates = []
    Y_coordinates = []

    while counter != Length:
        File_binary = File.read(12)     
        counter += 12


        File_binary = File.read(32)
        counter += 32

        File_binary = File.read(4)                        
        Num = struct.unpack('<i',File_binary)
        Number_of_Points.append(Num[0])
        counter += 4


        temp = []                        
        x_in_each_part = []
        y_in_each_part = []
        for i in range(Num[0]) :
            File_binary = File.read(16)
            temp.append(struct.unpack('<dd',File_binary))
            x_in_each_part.append(struct.unpack('<dd',File_binary)[0])
            y_in_each_part.append(struct.unpack('<dd',File_binary)[1])
            counter += 16
            
        coordinates_of_vertices.append(temp)
        X_coordinates.append(x_in_each_part)
        Y_coordinates.append(y_in_each_part)
    
    
#----------------------------------------------------------
#pointZ 
elif Shape_type == 11:             
    point_number = (Length - 100 ) / 44  
    X = []
    Y = []
    Z = []
    M = []

    for i in range(int(point_number)):                           
        File_binary = File.read(32)             
        x,y,z,m = struct.unpack('<dddd',File_binary) 
        X.append(x)
        Y.append(y)
        Z.append(z)
        M.append(m)

    coordinates = [X, Y, Z, M]
    print(coordinates)

#----------------------------------------------------------
# polygonZ and polylineZ
elif Shape_type == 13 or Shape_type == 15:       
    counter = 100                                       
    Index_to_First_Point_in_Part = []            
    coordinates_of_vertices = []                 
    X_coordinates_of_vertices = []
    Y_coordinates_of_vertices = []
    Z_coordinates_of_vertices = []
    Measure_of_vertices = []
  
    while counter != Length:
        File_binary = File.read(12)     
        counter += 12


        File_binary = File.read(32)
        counter += 32

        File_binary = File.read[counter:(counter + 4)]                            
        Number_of_Parts = struct.unpack('<i',File_binary)
        counter += 4

        File_binary = File.read[counter:(counter + 4)]                            
        Total_Number_of_Points = struct.unpack('<i',File_binary)
        counter += 4

        index_in_each_part=[]           
        for i in range(Number_of_Parts[0]):       
            File_binary = File.read(4)                        
            index_in_each_part.append(struct.unpack('<i',File_binary)[0])
            counter += 4
        Index_to_First_Point_in_Part.append(index_in_each_part)               


        coor_in_each_part=[]                          
        x_in_each_part = []
        y_in_each_part = []
        for i in range(Total_Number_of_Points[0]):
            File_binary = File.read(16)
            coor_in_each_part.append(struct.unpack('<dd',File_binary))
            x_in_each_part.append(struct.unpack('<dd',File_binary)[0])
            y_in_each_part.append(struct.unpack('<dd',File_binary)[1])
            counter += 16
        coordinates_of_vertices.append(coor_in_each_part)  
        X_coordinates_of_vertices.append(x_in_each_part)
        Y_coordinates_of_vertices.append(y_in_each_part)

        File_binary = File.read(16)         
        counter += 16

        z_in_each_part=[]                           
        for i in range(Total_Number_of_Points[0]) :
            File_binary = File.read[counter:(counter + 8)] 
            z_in_each_part.append(struct.unpack('<d',File_binary)[0])
            counter += 8
        Z_coordinates_of_vertices.append(z_in_each_part)

        File_binary = File.read[counter:(counter + 16)]         
        counter += 16

        m_in_each_part=[]                           
        for i in range(Total_Number_of_Points[0]) :
            File_binary = File.read[counter:(counter + 8)] 
            m_in_each_part.append(struct.unpack('<d',File_binary)[0])
            counter += 8
        Measure_of_vertices.append(m_in_each_part)

    print(Index_to_First_Point_in_Part, coordinates_of_vertices, Z_coordinates_of_vertices, Measure_of_vertices)       

#----------------------------------------------------------
#Multi_pointZ
elif Shape_type == 18 :        
    counter = 100                              
    coordinates_of_vertices = []        
    Number_of_Points =[]                
    X_coordinates_of_vertices = []
    Y_coordinates_of_vertices = []
    Z_coordinates_of_vertices = []
    Measure_of_vertices = []

    while counter != Length:
        File_binary = File.read(12)     
        counter += 12


        File_binary = File.read(32)
        counter += 32

        File_binary = File.read(4)                   
        N_o_P = struct.unpack('<i',File_binary)
        Number_of_Points.append(N_o_P[0])
        counter += 4


        coor_in_each_part=[]                       
        x_in_each_part = []
        y_in_each_part = []
        for i in range(N_o_P[0]) :
            File_binary = File.read(16)
            coor_in_each_part.append(struct.unpack('<dd',File_binary))
            x_in_each_part.append(struct.unpack('<dd',File_binary)[0])
            y_in_each_part.append(struct.unpack('<dd',File_binary)[1])
            counter += 16
        coordinates_of_vertices.append(coor_in_each_part)
        X_coordinates_of_vertices.append(x_in_each_part)
        Y_coordinates_of_vertices.append(y_in_each_part)

        File_binary = File.read(16)        
        counter += 16

        z_in_each_part=[]                           
        for i in range(N_o_P[0]) :
            File_binary = File.read(8)
            z_in_each_part.append(struct.unpack('<d',File_binary)[0])
            counter += 8
        Z_coordinates_of_vertices.append(z_in_each_part)



        File_binary = File.read(16)        
        counter += 16

        m_in_each_part=[]                          
        for i in range(N_o_P[0]) :
            File_binary = File.read(8)
            m_in_each_part.append(struct.unpack('<d',File_binary)[0])
            counter += 8
        Measure_of_vertices.append(m_in_each_part)


    print(Number_of_Points, coordinates_of_vertices, Z_coordinates_of_vertices, Measure_of_vertices)      
    
#----------------------------------------------------------
#pointM  
elif Shape_type == 21:             
    numbers_of_point = (Length - 100 ) / 36  
    X = []
    Y = []
    M = []

    for i in range(int(numbers_of_point)):           
        File_binary = File.read(24)
        x,y,m = struct.unpack('<ddd',File_binary) 
        X.append(x)
        Y.append(y)
        M.append(m)

    coordinates = [X, Y ,M]
    print(coordinates)


#----------------------------------------------------------
#polygonM and polylineM
elif Shape_type == 23 or Shape_type == 25:       
    Index_to_First_Point_in_Part = []            
    coordinates_of_vertices = []                 
    X_coordinates_of_vertices = []
    Y_coordinates_of_vertices = []
    Measure_of_vertices = []

    while counter != Length:
        File_binary = File.read(12)     
        counter += 12


        File_binary = File.read(32)
        counter += 32

        File_binary = File.read(4)                            
        counter += 4

        File_binary = File.read[counter:(counter + 4)]                           
        Total_Number_of_Points = struct.unpack('<i',File_binary)
        counter += 4

        index_in_each_part=[]           
        for i in range(Number_of_Parts[0]):      
            File_binary = File.read(4)                        
            index_in_each_part.append(struct.unpack('<i',File_binary)[0])
            counter += 4
        Index_to_First_Point_in_Part.append(index_in_each_part)               


        coor_in_each_part=[]                          
        x_in_each_part = []
        y_in_each_part = []
        for i in range(Total_Number_of_Points[0]):
            File_binary = File.read(16)
            coor_in_each_part.append(struct.unpack('<dd',File_binary))
            x_in_each_part.append(struct.unpack('<dd',File_binary)[0])
            y_in_each_part.append(struct.unpack('<dd',File_binary)[1])
            counter += 16
        coordinates_of_vertices.append(coor_in_each_part)  
        X_coordinates_of_vertices.append(x_in_each_part)
        Y_coordinates_of_vertices.append(y_in_each_part)

        File_binary = File.read(16)         
        counter += 16

        m_in_each_part=[]                          
        for i in range(Total_Number_of_Points[0]) :
            File_binary = File.read(8)
            m_in_each_part.append(struct.unpack('<d',File_binary)[0])
            counter += 8
        Measure_of_vertices.append(m_in_each_part)

    print(Index_to_First_Point_in_Part, coordinates_of_vertices,Measure_of_vertices)             
     

#----------------------------------------------------------
#Multi_pointM
elif Shape_type == 28 :         
    counter = 100                               
    coordinates_of_vertices = []        
    Number_of_Points =[]                
    X_coordinates_of_vertices = []
    Y_coordinates_of_vertices = []
    Measure_of_vertices = []


    while counter != Length:
        File_binary = File.read(12)     
        counter += 12


        File_binary = File.read(32)
        counter += 32

        File_binary = File.read(4)                   
        N_o_P = struct.unpack('<i',File_binary)
        Number_of_Points.append(N_o_P[0])
        counter += 4


        coor_in_each_part=[]                        
        x_in_each_part = []
        y_in_each_part = []
        for i in range(N_o_P[0]) :
            File_binary = File.read(16)
            coor_in_each_part.append(struct.unpack('<dd',File_binary))
            x_in_each_part.append(struct.unpack('<dd',File_binary)[0])
            y_in_each_part.append(struct.unpack('<dd',File_binary)[1])
            counter += 16
        coordinates_of_vertices.append(coor_in_each_part)
        X_coordinates_of_vertices.append(x_in_each_part)
        Y_coordinates_of_vertices.append(y_in_each_part)

        File_binary = File.read(16)         
        counter += 16

        m_in_each_part=[]                           
        for i in range(N_o_P[0]) :
            File_binary = File.read(8)
            m_in_each_part.append(struct.unpack('<d',File_binary)[0])
            counter += 8
        Measure_of_vertices.append(m_in_each_part)


    print(Number_of_Points, coordinates_of_vertices ,Measure_of_vertices)      

#----------------------------------------------------------
else :
    print('we can not open this type')

#show----------------------------------------------------------

if Shape_type == 0:
    print('shapefile is Null')
    
elif Shape_type == 1:
    fig = plt.figure(2)
    plt.title('Points')
    plt.scatter(X, Y, marker='.',color='black')
    plt.xlim(X_min-100,X_max+100)
    plt.ylim(Y_min-100,Y_max+100)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
    
elif Shape_type == 3:            
    fig = plt.figure(3)
    plt.title('Polyline')
    for i in range(len(Index)):
        X = X_coordinates[i]
        Y = Y_coordinates[i]
        plt.plot(X, Y,color='black', linewidth=0.5)
        plt.xlim(X_min-100,X_max+100)
        plt.ylim(Y_min-100,Y_max+100)
        plt.xlabel('X')
        plt.ylabel('Y')
    plt.show() 
    
elif Shape_type == 5:   
    axes = plt.gca()
    for i in Points:
        poly = []
        for j in range(len(i)):
            if j == 0:
                poly.append(Path.MOVETO)
            elif j == len(i)-1 :
                poly.append(Path.CLOSEPOLY)
            else:
                poly.append(Path.LINETO)
        path = Path(i,poly)
        patch = PathPatch(path)
        axes.set_xlim(X_min-100,X_max+100)
        axes.set_ylim(Y_min-100,Y_max+100)
        axes.add_patch(patch)
    plt.show()
    
elif Shape_type == 8:  
    fig = plt.figure(5)
    plt.title('Multi point')
    for i in range(len(Number_of_Points)):
        X = X_coordinates[i]
        Y = Y_coordinates[i]
        plt.scatter(X, Y , marker='+')
        plt.xlim(X_min-100,X_max+100)
        plt.ylim(Y_min-100,Y_max+100)
        plt.xlabel('X')
        plt.ylabel('Y')
    plt.show()
    
elif Shape_type == 11:
    fig = plt.figure(6)
    ax = fig.add_subplot(projection='3d')
    plt.title('pointZ')
    X = X_coordinates
    Y = Y_coordinates
    Z = Z_coordinates_of_vertices
    ax.scatter(X, Y, Z)
    plt.xlim(X_min-100,X_max+100)
    plt.ylim(Y_min-100,Y_max+100)
    plt.zlim(Z_min-100,Z_max+100)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.zlabel('Z')
    plt.show() 

    
elif Shape_type == 13:      
    fig = plt.figure(7)
    ax = fig.add_subplot(projection='3d')
    plt.title('PolylineZ')
    for i in range(len(Index)):
        X = X_coordinates[i]
        Y = Y_coordinates[i]
        Z = 1
        ax.scatter(X, Y, Z)
        plt.xlim(X_min-100,X_max+100)
        plt.ylim(Y_min-100,Y_max+100)
        plt.zlim(Z_min-100,Z_max+100)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.zlabel('Z')
    plt.show() 
    

elif Shape_type == 15:
    axes = plt.gca()
    for i in Points:
        poly = []
        for j in range(len(i)):
            if j == 0:
                poly.append(Path.MOVETO)
            elif j == len(i)-1 :
                 poly.append(Path.CLOSEPOLY)
            else:
                poly.append(Path.LINETO)
        path = Path(i,poly)
        patch = PathPatch(path)
        axes.set_xlim(X_min-100,X_max+100)
        axes.set_ylim(Y_min-100,Y_max+100)
        axes.add_patch(patch)
    plt.show() 
    
elif Shape_type == 18:
    fig = plt.figure(9)
    ax = fig.add_subplot(projection='3d')
    plt.title('Multi_pointZ')
    for i in range(len(Number_of_Points)):
        X = X_coordinates[i]
        Y = Y_coordinates[i]
        Z = Z_coordinates_of_vertices[i]
        plt.scatter(X, Y , marker='+')
        plt.xlim(X_min-100,X_max+100)
        plt.ylim(Y_min-100,Y_max+100)
        plt.zlim(Z_min-100,Z_max+100)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.zlabel('Z')
    plt.show()
    
elif Shape_type == 21:
    fig = plt.figure(10)
    plt.title('PointM')
    plt.scatter(X, Y, marker='.',color='black')
    plt.xlim(X_min-100,X_max+100)
    plt.ylim(Y_min-100,Y_max+100)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
    
elif Shape_type == 23:       
    fig = plt.figure(11)
    plt.title('PolylineM')
    for i in range(len(Index)):
           X = X_coordinates[i]
           Y = Y_coordinates[i]
           plt.plot(X, Y,color='black', linewidth=0.5)
           plt.xlim(X_min-100,X_max+100)
           plt.ylim(Y_min-100,Y_max+100)
           plt.xlabel('X')
           plt.ylabel('Y')
    plt.show()
    
elif Shape_type == 25:
    axes = plt.gca()
    for i in coordinates:
        p2 = []
        for j in range(len(i)):
            if j == 0:
                p2.append(Path.MOVETO)
            elif j == len(i)-1 :
                p2.append(Path.CLOSEPOLY)
            else:
                p2.append(Path.LINETO)
        path = Path(i,p2)
        patch = PathPatch(path)
        axes.set_xlim(X_min-100,X_max+100)
        axes.set_ylim(Y_min-100,Y_max+100)
        axes.add_patch(patch)
    plt.show()
                                
elif Shape_type == 28:
    fig = plt.figure(13)
    plt.title('Multi_pointM')
    for i in range(len(Number_of_Points)):
        X = X_coordinates[i]
        Y = Y_coordinates[i]
        plt.scatter(X, Y , marker='+')
        plt.xlim(X_min-100,X_max+100)
        plt.ylim(Y_min-100,Y_max+100)
        plt.xlabel('X')
        plt.ylabel('Y')
    plt.show()