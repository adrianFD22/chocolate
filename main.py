#!/usr/bin/python

########################
#       Functions
########################

import os
# Calcular recursivamente con bottom-up backtracking el nim
# value de la tableta de chocolate

# Cada tableta es un fichero. La primera línea tiene el NIM
# value y la segunda el movimiento que la transforma en 0 (en
# caso de existir)

# Las tabletas se identifican con un string conteniendo las
# alturas de las columnas separadas por comas y cuyo primer
# número es el número de columnas.

# Las tabletas se almacenan a lo largo (lado más largo es
# el horizontal).

# Generar tabletas iterativamente:
#def next_tablet(tablet):
    #new_tablet = tablet.copy()
#
    #flag_changed = False
    #for i in range(len(tablet)-1, 0, -1):
        #if new_tablet[i] < new_tablet[i-1]:
            #new_tablet[i] = new_tablet[i] + 1
            #flag_changed = True
            #break
#
    #if not flag_changed:
        #new_tablet = [ len(tablet) ]
        #for _ in range(len(tablet)):
            #new_tablet.append(1)
#
    #return new_tablet

def tablet_to_str(tablet):
    tablet_str = ""
    for i in range(len(tablet)-1):
        tablet_str += str(tablet[i]) + ","
    tablet_str += str(tablet[len(tablet)-1])
    return tablet_str

# Given a tablet and the coordinates (row,col) of a square,
# return the tablet after playing at (row,col)
def play_tablet(tablet, sel_row, sel_col):
    new_tablet = tablet.copy()
    #print("DB. play_tablet: ", tablet)
    #print("DB. play_tablet", "sel_row =", sel_row, ", sel_col =", sel_col)
    for col in range(sel_col, len(tablet)):
        #print("\tDB. col =", col)
        new_tablet[col] = min(sel_row, new_tablet[col])

    if sel_row == 0:
        new_tablet = new_tablet[:sel_col]

    #print("DB. new_tablet =", new_tablet)
    return new_tablet

# Rotate tablet if necessary
def rotate_if_needed(tablet):
    max_col = tablet[0]

    #print("DB. rotate_if_needed")
    #print("\tDB. max_col", max_col)
    if max_col >= len(tablet):
        # Compute rotated tablet
        new_tablet = []
        for _ in range(max_col):
            new_tablet.append(0)

        for col in range(len(tablet)):
            for row in range(tablet[col]):
                new_tablet[row] += 1

        # Check if rotation is needed
        for col in range(len(tablet)):
            if tablet[col] > new_tablet[col]:
                #print("DB. rotate")
                return new_tablet

            if tablet[col] < new_tablet[col]:
                return tablet

        return tablet

    else:
        return tablet


# Obtain nim value from already known nim values. Tablet
# is a list of column heights.
def nim_value(tablet):
    # Check base case
    if len(tablet) == 1 and tablet[0] == 1:
        return 0

    # Rotate tablet is necessary
    tablet = rotate_if_needed(tablet)

    # If nim is already computed
    tablet_name = "db/" + tablet_to_str(tablet)
    if os.path.isfile(tablet_name):
        file = open(tablet_name, "r")
        value = int(file.readline()[:-1])
        file.close()

    else:
        #print("DB. nim_value")
        #print("\tDB. tablet =", tablet)
        # Compute nim value of subtablets
        list_subnim_values = []
        list_zero_plays = []
        for col in range(len(tablet)):
            for row in range(tablet[col]):
                if col == 0 and row == 0:   # Junk: cannot eat poison square
                    continue

                #print("DB. Compute nim_value")
                #print("\tDB. col =", col, " row =", row)
                new_tablet = play_tablet(tablet, row, col)
                curr_play_value = nim_value(new_tablet)

                if curr_play_value == 0:
                    list_zero_plays.append(str(row+1) +  "," + str(col+1))

                list_subnim_values.append(curr_play_value)

        # Compute mex (minimum excluded value)
        value = 0
        #print("DB. mex=", list_subnim_values)
        while True:
            if not value in list_subnim_values:
                break
            value += 1

        # Save value
        file = open(tablet_name, "w")
        file.write(str(value) + "\n")       # Save nim value
        for curr_play in list_zero_plays:   # Save zero plays
            file.write(str(curr_play) + "\n")
        file.close()
        if value == 0:
            os.system("cp " + tablet_name + " db_zero/" + tablet_name[3:])

    return value


########################
#         Main
########################

# DB: Reset db
#os.system("rm -f db/*")

square_size = 11
tablet = [square_size] * square_size
print(tablet)

value = nim_value(tablet)

#print("Tablet: " + str(tablet))
#print("rotated:", rotate_if_needed(tablet))
#print("Value: " + str(value))

