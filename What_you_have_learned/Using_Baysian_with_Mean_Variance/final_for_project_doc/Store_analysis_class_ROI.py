class statistical_analysis:
    def __init__(self):
        self.num_of_pixels = 0
        self.mean_value_R = 0
        self.mean_value_G = 0
        self.mean_value_B = 0
        self.std_value_R = 0
        self.std_value_G = 0
        self.std_value_B = 0
        self.Bayesian_plus_value_R = 0
        self.Bayesian_plus_value_G = 0
        self.Bayesian_plus_value_B = 0
        self.Bayesian_times_value_R = 0
        self.Bayesian_times_value_G = 0
        self.Bayesian_times_value_B = 0
    def update_num_of_pixels(self, num_pixels):
        self.num_of_pixels = num_pixels
    def update_mean_RGB(self, mean_value):
        self.mean_value_R,self.mean_value_G,self.mean_value_B = mean_value[0],mean_value[1],mean_value[2]
    def update_std_RGB(self, std_value):
        self.std_value_R,self.std_value_G,self.std_value_B = std_value[0],std_value[1],std_value[2]
    def update_plus_Bayesian(self, Baye_plus_value):
        self.Bayesian_plus_value_R,self.Bayesian_plus_value_G,self.Bayesian_plus_value_B = Baye_plus_value[0],Baye_plus_value[1],Baye_plus_value[2]
    def update_times_Bayesian(self, Baye_times_value):
        self.Bayesian_times_value_R,self.Bayesian_times_value_G,self.Bayesian_times_value_B = Baye_times_value[0],Baye_times_value[1],Baye_times_value[2]
    def get_num_of_pixels(self):
        return self.num_of_pixels
    def get_mean_value(self):
        return self.mean_value_R,self.mean_value_G,self.mean_value_B
    def get_std_value(self):
        return self.std_value_R,self.std_value_G,self.std_value_B
    def get_plus_Bayesian_value(self):
        return self.Bayesian_plus_value_R,self.Bayesian_plus_value_G,self.Bayesian_plus_value_B
    def get_times_Bayesian_value(self):
        return self.Bayesian_times_value_R,self.Bayesian_times_value_G,self.Bayesian_times_value_B