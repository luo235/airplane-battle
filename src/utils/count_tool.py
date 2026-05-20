class Count_tool:
    def __init__(self):
        self.all_name={
        "enemy_count" : 0 ,
        "enemy_death" : 0 ,
        "shoot_count" : 0 ,
        }
    def increase(self,key):
        self.all_name[key]+=1
    