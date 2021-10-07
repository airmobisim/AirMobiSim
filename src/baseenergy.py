class Baseenergy():
    def __init__(self):
        pass

    def getcurrentEnergy(self, speed, passedTime):
        distance = speed * passedTime
        energy = 0.032*9.81*distance
        return (distance, energy)



    