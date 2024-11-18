import time
from initialization1 import *
from crossover import *
from mytest import *


st = time.time()

generations = 210
gnc = 1
while generations!=0:
    generations -= 1
    # Will make new child population 
    childrenpop = []
    childFit_value = []

    temppop = pop.copy()
    while temppop!=[]:
        childrens = uniformCrossover(temppop)
        if childrens!=[]:
            o1,o2 = childrens[0],childrens[1]
            childrenpop.append(o1)
            childFit_value.append(fitnessFunction(o1))
            childrenpop.append(o2)
            childFit_value.append(fitnessFunction(o2))


    pop += childrenpop
    Fit_values += childFit_value
    spop = [val for (_, val) in sorted(zip(Fit_values, pop), key=lambda x: x[0],reverse=True)]
    pop = spop.copy()
    pop = pop[:popz]
    Fit_values.clear()
    for i in pop:
        Fit_values.append(fitnessFunction(i))
    

    print("Generation ",gnc)
    gnc+=1
    # import os, psutil; print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)


def separateChromosome(chromosome):
    sem2 = {}
    sem4 = {}
    sem6 = {}
    sem8 = {}
    dayMap = {1:"Mon", 2:"Tue" , 3:"Wed" , 4:"Thurs" , 5:"Fri"}
    for i in range(len(chromosome)):
        
        sem2[dayMap[i+1]] = []
        sem4[dayMap[i+1]] = []
        sem6[dayMap[i+1]] = []
        sem8[dayMap[i+1]] = []
        for  slot in chromosome[i]:
            sem2[dayMap[i+1]].append(slot[0])
            sem4[dayMap[i+1]].append(slot[1])
            sem6[dayMap[i+1]].append(slot[2])
            sem8[dayMap[i+1]].append(slot[3])
    return sem2,sem4,sem6,sem8
                 
    

et = time.time()
print("time : ",et-st)
print("Max fitness achived : ",max(Fit_values))

y1 , y2 , y3 , y4 = separateChromosome(pop[0])
print("\n\n\n\nFirst year\n")
for k , v in y1.items():
    print(k,v)
print("\nSecond year\n")
for k , v in y2.items():
    print(k,v)
print("\nthird year\n")
for k , v in y3.items():
    print(k,v)
print("\nfourth year\n")
for k , v in y4.items():
    print(k,v)
# print(fitnessFunction(pop[0])) #chnaged by me
print("lmao")

# with open("templates/timetable.html", "w") as f:
#     f.write("<html><head><title>Schedule Output</title></head><body>")
#     f.write("<h1>Timetable</h1>")

#     # Add the fitness value
#     f.write(f"<p>Max fitness achieved: {max(Fit_values)}</p>")

#     # Function to format schedule with slot names
#     def format_schedule(sem_dict, year_name):
#         f.write(f"<h2>{year_name}</h2>")
#         f.write("<table border='1'>")
       
#         # Assuming a maximum of 6 slots per day. Adjust if necessary.
#         f.write("<tr><th>Day</th><th>Slot1</th><th>Slot2</th><th>Slot3</th><th>Slot4</th><th>Slot5</th><th>Slot6</th></tr>")
       
#         for day, slots in sem_dict.items():
#             f.write(f"<tr><td>{day}</td>")
#             for slot in slots:
#                 f.write(f"<td>{slot}</td>")
#             # Fill remaining slots if there are fewer than the max number
#             for _ in range(len(slots), 6):
#                 f.write("<td></td>")
#             f.write("</tr>")
#         f.write("</table>")

#     # Assuming separateChromosome() is defined elsewhere and returns the data in the format expected
#     y1, y2, y3, y4 = separateChromosome(pop[0])

#     f.write("<h3>First Year</h3>")
#     format_schedule(y1, "First Year")

#     f.write("<h3>Second Year</h3>")
#     format_schedule(y2, "Second Year")

#     f.write("<h3>Third Year</h3>")
#     format_schedule(y3, "Third Year")

#     f.write("<h3>Fourth Year</h3>")
#     format_schedule(y4, "Fourth Year")

#     f.write("</body></html>")


# with open("templates/timetable.html", "w") as f:
#     f.write("<html><head><title>Schedule Output</title>")
#     f.write("<style>")
#     f.write("body { font-family: Arial, sans-serif; }")
#     f.write("h1, h2, h3 { color: #333; }")
#     f.write("table { border-collapse: collapse; width: 100%; }")
#     f.write("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
#     f.write("th { background-color: #f0f0f0; }")
#     f.write("</style>")
#     f.write("</head><body>")
#     f.write("<h1>Timetable</h1>")

#     # # Add the fitness value
#     # f.write(f"<p>Max fitness achieved: {max(Fit_values)}</p>")

#     # Function to format schedule with slot names
#     def format_schedule(sem_dict, year_name):
#         # f.write(f"<h2>{year_name}</h2>")
#         f.write("<table border='1'>")
       
#         # Assuming a maximum of 6 slots per day. Adjust if necessary.
#         f.write("<tr><th>Day</th><th>Slot1</th><th>Slot2</th><th>Slot3</th><th>Slot4</th><th>Slot5</th><th>Slot6</th></tr>")
       
#         for day, slots in sem_dict.items():
#             f.write(f"<tr><td>{day}</td>")
#             for slot in slots:
#                 f.write(f"<td>{slot}</td>")
#             # Fill remaining slots if there are fewer than the max number
#             for _ in range(len(slots), 6):
#                 f.write("<td></td>")
#             f.write("</tr>")
#         f.write("</table>")

#     # Assuming separateChromosome() is defined elsewhere and returns the data in the format expected
#     y1, y2, y3, y4 = separateChromosome(pop[0])

#     f.write("<h3>First Year</h3>")
#     format_schedule(y1, "First Year")

#     f.write("<h3>Second Year</h3>")
#     format_schedule(y2, "Second Year")

#     f.write("<h3>Third Year</h3>")
#     format_schedule(y3, "Third Year")

#     f.write("<h3>Fourth Year</h3>")
#     format_schedule(y4, "Fourth Year")

#     f.write("</body></html>")


with open("templates/timetable.html", "w") as f:
    f.write("<html><head><title>Schedule Output</title>")
    f.write("<style>")
    f.write("body { font-family: Arial, sans-serif; background-color: #f4f4f4; }")
    f.write("h1, h2, h3 { color: #333; margin-bottom: 10px; }")
    f.write("table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }")
    f.write("th, td { border: 3px solid #ddd; padding: 8px; text-align: left; }")
    f.write("th { background-color: #f0f0f0; font-weight: bold; }")
    f.write("tr:nth-child(even) { background-color: #f2f2f2; }")
    f.write("</style>")
    f.write("</head><body>")
    f.write("<h1 style='text-align: center;'>Timetable</h1>")

    # # Add the fitness value
    # f.write(f"<p style='text-align: center;'>Max fitness achieved: {max(Fit_values)}</p>")

    # Function to format schedule with slot names
    def format_schedule(sem_dict, year_name):
        # f.write(f"<h3>{year_name}</h3>")
        f.write("<table border='1'>")
       
        # Assuming a maximum of 6 slots per day. Adjust if necessary.
        f.write("<tr><th>Day</th><th>Slot1</th><th>Slot2</th><th>Slot3</th><th>Slot4</th><th>Slot5</th><th>Slot6</th></tr>")
       
        for day, slots in sem_dict.items():
            f.write(f"<tr><td>{day}</td>")
            for slot in slots:
                f.write(f"<td>{slot}</td>")
            # Fill remaining slots if there are fewer than the max number
            for _ in range(len(slots), 6):
                f.write("<td></td>")
            f.write("</tr>")
        f.write("</table>")

    # Assuming separateChromosome() is defined elsewhere and returns the data in the format expected
    y1, y2, y3, y4 = separateChromosome(pop[0])

    f.write("<h3>First Year</h3>")
    format_schedule(y1, "First Year")

    f.write("<h3>Second Year</h3>")
    format_schedule(y2, "Second Year")

    f.write("<h3>Third Year</h3>")
    format_schedule(y3, "Third Year")

    f.write("<h3>Fourth Year</h3>")
    format_schedule(y4, "Fourth Year")

    f.write("</body></html>")