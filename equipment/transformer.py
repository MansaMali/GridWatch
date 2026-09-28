import random
from datetime import datetime

class Transformer:
    def __init__(self, asset_id):
        self.asset_id = asset_id

        self.voltage = 7200

        self.current = 120

        self.temperature = 65

        self.load_percent = 50

        self.simulation_mode = "NORMAL"

        self.scenario_cycles = 0



    def update(self):

        self.scenario_cycles += 1

        print(
            f"{self.asset_id} | "
            f"Mode: {self.simulation_mode} | "
            f"Cycles: {self.scenario_cycles}  "
        )

        if self.simulation_mode == "NORMAL":
        
        
            self.voltage += random.randint(-15,15)

            self.current += random.randint(-3,3)

            self.temperature += random.randint(-5, 5)

            self.load_percent += random.randint(-5, 5)


        elif self.simulation_mode == "OVERLOAD":
                
            self.voltage += random.randint(-15,15)
        
            self.current += random.randint(2,8)
            
            self.temperature += random.randint(2, 6)
            
            self.load_percent += random.randint(3, 8)

            if self.temperature > 105:
                self.temperature = 102

            if self.load_percent > 110:
                self.load_percent = 105

            if self.scenario_cycles >= 20:

                self.simulation_mode = "RECOVERY"

                self.scenario_cycles = 0

                print(f"{self.asset_id} entering RECOVERY mode")

        elif self.simulation_mode == "RECOVERY":  
                
            self.voltage += random.randint(-15,15)
    
            self.current += random.randint(-5,2)
        
            self.temperature += random.randint(-5, -1)
        
            self.load_percent += random.randint(-5, -1)

            if self.scenario_cycles >20:

                self.simulation_mode = "NORMAL"

                self.scenario_cycles = 0

                print(f"{self.asset_id} returning to NORMAL mode")



    def get_telemetry(self):
            return {
                "asset_id": self.asset_id,
                "voltage": self.voltage,
                "current": self.current,
                "temperature": self.temperature,
                "load_percent": self.load_percent,
                "timestamp": datetime.now()
    
            }