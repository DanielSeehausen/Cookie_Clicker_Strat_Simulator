"""
Cookie Clicker Simulator
"""


import math

# Used to increase the timeout, if necessary


#This class will need to be created, as it is not
#implemented here nor provided in repository
#import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._curr_cookies = 0.0
        self._curr_time = 0.0
        self._curr_cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)] 
        
    def __str__(self):
        """
        Return human readable state
        """
        print_me = ""
        print_me += "Total Cookies: " + str(self._total_cookies) + "\n"
        print_me += "Curr Cookies : " + str(self._curr_cookies) + "\n"
        print_me += "Curr Time    : " + str(self._curr_time) + "\n"
        print_me += "Curr CPS     : " + str(self._curr_cps)
        return print_me
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        """
        return float(self._curr_cookies)
    
    def get_cps(self):
        """
        Get current CPS
        """
        return float(self._curr_cps)
    
    def get_time(self):
        """
        Get current time
        """
        return float(self._curr_time)
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history_list)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._curr_cookies >= cookies: 
            return 0.0
        
        req_cookies = cookies - self._curr_cookies
        return math.ceil(float(req_cookies)/float(self._curr_cps))
        
    def wait(self, time):
        """
        Wait for given amount of time and update state
        """
        if time <= 0.0: 
            return
        
        self._curr_cookies += self._curr_cps * time
        self._total_cookies += self._curr_cps * time
        self._curr_time += time
        return
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        """
        if self._curr_cookies < cost: 
            return
        
        self._curr_cookies -= cost
        self._curr_cps += additional_cps
        self._history_list.append((self._curr_time, item_name, cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    curr_build_info = build_info.clone()
    click_state = ClickerState()
    
    while (True):
        next_item = strategy(click_state.get_cookies(), click_state.get_cps(), click_state.get_history(), duration - click_state.get_time(), curr_build_info)  
        
        if next_item == None: 
            break
        
        req_time = click_state.time_until(curr_build_info.get_cost(next_item))
        if req_time + click_state.get_time() > duration:
            break
        
        click_state.wait(req_time)
        #print next_item + ": ", curr_build_info.get_cost(next_item)
        click_state.buy_item(next_item, curr_build_info.get_cost(next_item), curr_build_info.get_cps(next_item))
        curr_build_info.update_item(next_item)
        
    click_state.wait(duration - click_state.get_time())
    
    return click_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cheapest_item = None
    lowest_cost = float("inf")
    max_prod = cookies + (cps * time_left)
    for item in build_info.build_items():
        temp_price = build_info.get_cost(item)
        if temp_price <= max_prod and temp_price <= lowest_cost:
            lowest_cost = temp_price
            cheapest_item = item
            
            
    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    priciest_item = None
    highest_cost = float("-inf")
    max_prod = cookies + (cps * time_left)
    for item in build_info.build_items():
        temp_price = build_info.get_cost(item)
        if highest_cost < temp_price <= max_prod:
            highest_cost = temp_price
            priciest_item = item
    return priciest_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    roi_item_name = None
    lowest_roi_found = float("inf")
    rem_prod = cookies + (cps * time_left)
    
    for item in build_info.build_items():
        temp_cost = build_info.get_cost(item) 
        temp_roi = temp_cost/build_info.get_cps(item)
        if temp_cost <= rem_prod and temp_roi < lowest_roi_found:
            lowest_roi_found = temp_roi
            roi_item_name = item
    
    return roi_item_name
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    # Plot total cookies over time

    #a new simple plot module will need to be used here if desired
    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()

#tester = ClickerState()
    
