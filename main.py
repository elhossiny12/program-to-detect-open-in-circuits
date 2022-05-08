# This program used to detect open in circuits, i.e. floating nets in subcircuits.
# How to run it? please add your netlist text file in the same code path, you can name the file "netlist" to avoid change the name in programe.

# How the code work? the code designed in 3 steps.
# 1) First part in the code is define the sub_circuit that contains main nets, instances, and internal nets.
# 2) Second part in the code is read the file and make a process on it to determine all sub_circuits, external nets , instances, and internal nets.
# 3) Third part is search and find the floating nets.
################################## First part define the sub_circuit, nets, insatnces, and internal nets #################################
class sub_circuit:
    def __init__(self, nets, instances):
        self.nets = nets
        self.instances = instances


# subckt.append(sub_circuit([],[[]]))     #define new sub_circuits
# subckt[0].nets.append("x")              #sub_circuits add external nets
# subckt[0].instances[0].append("A")      #instance no.0  add internal nets
# subckt[0].instances.append([])          #define instance no. 1
# subckt[0].instances[1].append("M")      #instance no.1 add internal nets


################################# Second part read the file and determine sub_circuits #################################


def white_speace_position(line):  # function to find white spaces in any line
    counter = 0
    space_position = []

    for i in line:
        if i == " ":
            space_position.append(counter)
        counter += 1
    space_position.append(len(line) - 1)

    for i in range(0, len(space_position) - 2):  # this for loop to remove any reduandnce spaces
        if int(space_position[i]) + 1 == int(space_position[i + 1]):
            space_position.pop(i)

    return space_position


def search(list, my_net):  # this function to search for nets

    for i in range(len(list)):
        if list[i] == my_net:
            return True
    return False


subckt = []
flag = 0
subckt_num = 0
inctance_num = 0

netlist2 = open("netlist", "r")
saved_file = netlist2.readlines()  # use this list to have access to the next line or any line in file.
saved_file.append("..")
netlist2.close()

j = 0
netlist = open("netlist", "r")
for line in netlist:  # read file line by line
    j += 1
    next_line = saved_file[j]  # next line access
                                                                  # skip line that contains comment, .end , or include.
    if line.find(".include") != -1 or line.find(".ends") != -1 or line.find("*") != -1 or line.isspace():
        continue
    if j >= 2:                                                        # skip line that contains instance paramater only
        if line.find("+") != -1 and line.find("=") != -1 and saved_file[j - 2].find("=") != -1:
            continue                                               # example: M0 A B C D W11=2 L11=3 ..
                                                    # + W33=122 L33=22 >>>>this line not cotains any nets, so skip it

    if line.find(".subckt") != -1:  # search for sub_circuits
        flag = 1
        subckt_num += 1
        inctance_num = 0
        subckt.append(sub_circuit([], [[]]))  # define new sub_cicuits
        x = white_speace_position(line)
        x.pop(0)
        for i in range(0, len(x) - 1):  # save sub_circuits nets
            subckt_net = line[x[i] + 1:x[i + 1]]
            subckt[subckt_num - 1].nets.append(subckt_net)
    elif line[0] == "+" and flag == 1:  # if the new line begin with + ,so add this nets
        x = white_speace_position(line)
        for i in range(0, len(x) - 1):
            subckt_net = line[x[i] + 1:x[i + 1]]
            subckt[subckt_num - 1].nets.append(subckt_net)

    else:  # fill instances                                     # now fill the instances and its nets
        flag = 0
        if line[0] == "c" or line[0] == "r":  # fill caps, and resistors
            inctance_num += 1
            x = white_speace_position(line)
            if inctance_num > 1:
                subckt[subckt_num - 1].instances.append([])
            for i in range(0, 2):
                subckt_instance_net = line[x[i] + 1:x[i + 1]]
                subckt[subckt_num - 1].instances[inctance_num - 1].append(subckt_instance_net)




        elif line[0] == "+" and flag == 0:        # if the new line begin with + ,so add this nets
            if line.find("=") != -1:               # this line contains "=" , so neglect parameters and add nets only
                new_line = line[0:line.find("=")]
                x = white_speace_position(new_line)
                x.pop(-1)
                x.pop(-1)

                for i in range(0, len(x) - 1):
                    subckt_instance_net = new_line[x[i] + 1:x[i + 1]]
                    subckt[subckt_num - 1].instances[inctance_num - 1].append(subckt_instance_net)


            else:
                x = white_speace_position(line)
                if line[0] == "+" and next_line[0] != "+":
                    x.pop(-1)

                for i in range(0, len(x) - 1):
                    subckt_instance_net = line[x[i] + 1:x[i + 1]]
                    subckt[subckt_num - 1].instances[inctance_num - 1].append(subckt_instance_net)



        else:
            if line.find("=") != -1:
                inctance_num += 1
                new_line = line[0:line.find("=")]
                x = white_speace_position(new_line)
                x.pop(-1)
                x.pop(-1)  # dont add instance type: I1 IN OUT INV,  nets here IN and OUT only
                if inctance_num > 1:
                    subckt[subckt_num - 1].instances.append([])  # instance no. 2
                for i in range(0, len(x) - 1):
                    subckt_instance_net = new_line[x[i] + 1:x[i + 1]]
                    subckt[subckt_num - 1].instances[inctance_num - 1].append(subckt_instance_net)


            else:
                x = white_speace_position(line)
                if line[0] == "+" and next_line[0] != "+":
                    x.pop(-1)

                inctance_num += 1
                if inctance_num > 1:
                    subckt[subckt_num - 1].instances.append([])  # instance no. 2
                for i in range(0, len(x) - 1):
                    subckt_instance_net = line[x[i] + 1:x[i + 1]]
                    subckt[subckt_num - 1].instances[inctance_num - 1].append(subckt_instance_net)

netlist.close()

################################# Third part search and find the floating net #################################
clear = 1
for i in range(0, len(subckt)):
    for M in range(0, len(subckt[i].instances)):  # for any net in instance search if it connected to another one

        for N in range(0, len(subckt[i].instances[M])):  # or net in instance connected to subcircuit net

            net = subckt[i].instances[M][N]

            for O in range(0, len(subckt[i].instances)):

                if O == M:                                  # dont compare net in instance with its self
                    if O == len(subckt[i].instances) - 1:
                        clear = 0
                        print("The folating element in subckt: " + str(i + 1) + " net name: " + net)  # this is last iteration? so this net is floating
                    continue

                line1 = subckt[i].instances[O]
                line2 = subckt[i].nets

                if search(line1, net) or search(line2,  net):  # if you found net connected, so break and search for the next one
                    break

                if O == len(subckt[i].instances) - 1:
                    clear = 0
                    print("The folating element in subckt: " + str(i + 1) + " net name: " + net)    # this is last iteration? so net is floating

if clear: print ("circuit is clear")
# print(saved_file)
# print(subckt_num)
# print(inctance_num)
# print(subckt[0].nets)
# print(subckt[0].instances)
# print(subckt[1].nets)
# print(subckt[1].instances)
