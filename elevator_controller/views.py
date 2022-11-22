from django.shortcuts import render
from django.http import HttpResponse
from .elevator import Elevator
from .interface import Interface

from threading import Thread
from multiprocessing.pool import ThreadPool
import csv 
import pandas as pd
import random 
import time

def home(request):
     return render(request, "index.html")

def controller(request):
    return HttpResponse(Controller(5,floors=15))

def test_string(request):
    #create testcases
   return HttpResponse("Click next Input_Create_TestCases button to Go to console for passing input args {}")

def test(request):
    return HttpResponse("Click next button Run Elevator System to start simulation {}".format(Test()))




    
class Controller():
    """Manages/controls one or more elevators that work together, assuming they both can access the same floors"""

    def __init__(self, elevators=0, floors=0, use_gui=True):
        
        self.elevators = list()
        
        elevators = int(input("Enter number of elevators you need for the system"))
        floors= int(input("Enter the maximum number of floors in the building"))
        self.floors = floors
        for x in range(elevators):
            self.elevators.append(Elevator(self.floors, name="Elevator " + str(x+1)))
        self.called = dict()  # {1: {"up": False, "down": False}, 2: {"up": False, "down": False}}
        for x in range(floors):
            self.called[x+1] = {"up": False, "down": False}
        if use_gui:
            self.interface = Interface(self)
        else:
            self.interface = None
        self.simulate_system()
            

    def assign_elevator(self,user,floor):
        floor_s = floor[0]
        floor_d = floor[1]
        elevators = sorted(self.elevators, key=lambda e: abs(e.current_floor - floor_s))
        
        for elevator in elevators:
            
            if elevator.busy:
                if  elevator.going_up and (elevator.current_floor < floor_s): 
                    if elevator.go_to_drop[floor_d] == False:
                        elevator.go_to_drop[floor_d] = []   
                    if elevator.go_to[floor_s]==False:
                        elevator.go_to[floor_s] = []
                    elevator.go_to[floor_s].append(user)
                    elevator.go_to_drop[floor_d].append(user)
                    elevator.going_up = True
                    self.called[floor_s]["up"] = False
                    return elevator
            
                # called to go down and elevator going down from higher floor
                elif not elevator.going_up and (elevator.current_floor > floor_s):
                    if elevator.go_to_drop[floor_d] == False:
                        elevator.go_to_drop[floor_d] = []   
                    if elevator.go_to[floor_s]==False:
                        elevator.go_to[floor_s] = []
                    elevator.go_to[floor_s].append(user)
                    elevator.go_to_drop[floor_d].append(user)
                    elevator.going_up = False
                    self.called[floor_s]["down"] = False
                    return elevator
                    
            else:
            
                elevator.busy = True
                if elevator.go_to_drop[floor_d] == False:
                    elevator.go_to_drop[floor_d] = []   
                if elevator.go_to[floor_s]==False:
                    elevator.go_to[floor_s] = []
                elevator.go_to[floor_s].append(user)
                elevator.go_to_drop[floor_d].append(user)
                direction  =None
                if elevator.current_floor<floor_s:
                    elevator.going_up = True
                    direction = "up"
                else:
                    elevator.going_up = False
                    direction = "down"
                self.called[floor_s][direction] = False
                print("Elevator {} assigned to user {}".format(elevator.name,user) )
                return elevator


    def call_elevator(self, floor, direction):
        self.called[floor][direction] = True

    def simulate_system(self):

        st_time = 0
        prev_time = time.time()
        next_time = time.time()
        df = pd.read_csv('testcases.csv')
        while(1):
          
            for index,row in df.iterrows():
                
                curr_time = st_time + (next_time-prev_time)
                st_time = curr_time
                prev_time = next_time
                while curr_time<row["arrival_time"]:
                    curr_time = st_time+(time.time()-prev_time)
                    continue

                if row["arrival_floor"]==row["destination_floor"]:
                    print("Invalid request")
                    continue

                if curr_time>=row["arrival_time"]:
                    
                    
                    floor_input = (int(row["arrival_floor"]),int(row["destination_floor"]))
                    elevator = None

                    elevator = self.assign_elevator(row["id"],floor_input)
        
                    if elevator is None:
                        print("Invalid request.")
                        continue
                    Thread(target=elevator.run).start()
                    elevator.running_status = True
                next_time = time.time()
                       

            print("Data has been fed into the system. Generating UI")
          
            self.interface.run()
            self.interface.window.mainloop()
            
            
class Test():
    def __init__(self):
        header = ['id', 'arrival_time', 'arrival_floor', 'destination_floor']
        print("Creating testcases_")
        
        n = int(input("Please enter total number of passengers using elevators in a day"))
        floors = int(input("Please enter maximum number of floors in the building"))
        with open('testcases.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            start_time = time.time()
            ini_time = 0
            for i in range(0,n):
                floor_a = random.randint(1,floors)
                floor_d = random.randint(1,floors)
                end_time = time.time()
                time_ = ini_time+end_time-start_time
                ini_time = time_
                start_time = end_time
                data = [i,time_,floor_a,floor_d]
                writer.writerow(data)
                time.sleep(2)       
            print("test-cases are created. Please run api to start elevator_on_server")             
                
#app.main_loop()
