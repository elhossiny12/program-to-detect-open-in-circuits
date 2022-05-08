 This program used to detect open in circuits, i.e. floating nets in subcircuits.
 How to run it? please add your netlist text file in the same code path, you can name the file "netlist" to avoid change the name in programe.

 How the code work? the code designed in 3 steps.
 1) First part in the code is define the sub_circuit that contains main nets, instances, and internal nets.
 2) Second part in the code is read the file and make a process on it to determine all sub_circuits, external nets , instances, and internal nets.
 3) Third part is search and find the floating nets.
