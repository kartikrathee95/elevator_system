import time

class Elevator(object):
    def __init__(self, floors, name=""):
        """Initialize the state of the elevator"""
        if name != "":
            self.name = name
        else:
            self.name = "Elevator"
        self.current_floor = 1
        self.top_floor = floors
        self.busy = False  
        self.door_open = False 
        self.going_up = True 
        self.go_to_drop = dict()
        self.go_to = dict()
        self.no_of_users = 0
        self.running_status = False
        for x in range(floors):
            self.go_to[x + 1] = False
            self.go_to_drop[x + 1] = False
        self.user_id = None
    def __str__(self):
        return self.name

    def do(self, seconds, action):
        """Waits for a period of seconds to simulate an action being carried out"""
        print("                     ")
        print("Elevator {} _machinery_action".format(self.name))
        print("%s (%d seconds)" % (action, seconds))
        print("                     ")
        print(self.get_status())
        print("                     ")
        time.sleep(seconds)

    def get_status(self):
        go_to = list()
        for x in self.go_to.keys():
            if self.go_to[x]:
                go_to.append(x)
        return "%(name)s (floor: %(floor)02d, door: %(door)s, direction: %(direction)s, go to: %(go_to)s)" % {
            "name": self.name,
            "floor": self.current_floor,
            "door": "open" if self.door_open else "closed",
            "direction": "up" if self.going_up else "down",
            "go_to": repr(go_to)
        }

    def open_door(self):
        if not self.door_open:
            self.do(2, "Opening door")
            self.door_open = True

    def close_door(self):
        if self.door_open:
            self.do(2, "Closing door")
            self.door_open = False

    def go_to_floor(self, target_floor,state,users):
        """Moves the elevator from its current floor to target_floor"""
        print("the state is {}".format(state))
        if self.door_open:  
            self.close_door()
        original_floor = self.current_floor

        while (self.current_floor != target_floor):

            # Going up!
            if (self.current_floor < target_floor):

                self.going_up = True
                if (self.current_floor == original_floor):
                    self.do(1, "Starting elevator {} at floor ={} ".format(self.name,self.current_floor))

                self.do(2, "Elevator {} Moving from floor {} to {}".format(self.name,self.current_floor, self.current_floor + 1))
                self.current_floor += 1

                if (self.current_floor == target_floor):
                    self.do(3, "Stopping elevator {} at floor = {}".format(self.name,self.current_floor))
                    if state=="drop":
                        for usid in users:
                            print("                                   ")
                            print("Elevator {} dropping passenger {} at floor = {}".format(self.name,usid,target_floor))
                            print("                                   ")
                            print("Passenger {} is being dropped at floor = {} by elevator = {}".format(usid,target_floor,self.name))
                    else:
                        for usid in users:
                            print("                                   ")
                            print("Elevator {} picking up passenger {} at floor = {}".format(self.name,usid,target_floor))
                            print("                                   ")
                            print("Passenger {} is picked from at floor = {} by elevator = {}".format(usid,target_floor,self.name))
                else:
                    target_floor,users = self.next_floor_up()

            # Going down!
            elif (self.current_floor > target_floor):

                self.going_up = False
                if (self.current_floor == original_floor):
                    self.do(1, "Starting elevator {} at floor = {}".format(self.name,self.current_floor))

                self.do(2, "Elevator {} Moving from floor {} to {}".format(self.name,self.current_floor, self.current_floor - 1))
                self.current_floor -= 1

                if (self.current_floor == target_floor):
                    self.do(3, "Stopping elevator {} at floor = {}".format(self.name,self.current_floor))

                    if state=="drop":
                        for usid in users:
                            print("                                   ")
                            print("Elevator {} dropping passenger {} at floor = {}".format(self.name,usid,target_floor))
                            print("                                   ")
                            print("Passenger {} is being dropped at floor = {} by elevator = {}".format(usid,target_floor,self.name))
                    else:
                        for usid in users:
                            print("                                   ")
                            print("Elevator {} picking up passenger {} at floor = {}".format(self.name,usid,target_floor))
                            print("                                   ")
                            print("Passenger {} is picked from at floor = {} by elevator = {}".format(usid,target_floor,self.name))

                else:
                    target_floor,users = self.next_floor_down()

        self.go_to[target_floor] = False

    def next_floor_up(self):
        for f in range(self.current_floor, self.top_floor + 1):
            if self.go_to[f] != False:
                return f,self.go_to[f]
        return None,None

    def next_floor_down(self):
        for f in range(self.current_floor - 1, 0, -1):
            if self.go_to[f] != False:
                return f,self.go_to[f]
        return None,None

    def run(self,state = "pick"):
        if self.running_status==False:
            self.running_status = True
            while True:
           
                if self.going_up:
                    next_floor,users = self.next_floor_up()
                else:
                    next_floor,users = self.next_floor_down()

            # Check floors in the opposite direction if no floor was received
                if next_floor is None:
                    if self.going_up:
                        next_floor,users = self.next_floor_down()
                    else:
                        next_floor,users = self.next_floor_up()
                
                if next_floor is None:
                   
                    if  state=="pick":
                        state= "drop"
                        self.go_to = self.go_to_drop
                        continue
                    else:
                        self.running_status = False
                        return
                else:
                    self.busy = True
                    self.go_to_floor(next_floor,state,users)
                    if self.current_floor == self.top_floor:
                        self.going_up = False
                    elif self.current_floor == 1:
                        self.going_up = True
                    self.open_door()
                    print("                               ")
                    self.do(5, "Loading/unloading elevator {} at floor = {}".format(self.name,next_floor))
                    print("                               ")
                    self.close_door()
                
