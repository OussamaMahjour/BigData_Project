from datetime import datetime

class Date :

    def build(self,year=2024,day=21,month=21,hour=0,minute=0,seconde=0):
        return datetime(self.year, self.month, self.day, self.hour, self.minute, second)
    
    def toUnixTimestamp(self):
        return self.build().timestamp() * 1000



