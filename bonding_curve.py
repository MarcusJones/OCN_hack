import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


import webbrowser
#%%
class LoggerCritical:
    def __enter__(self):
        my_logger = logging.getLogger()
        my_logger.setLevel("CRITICAL")
    def __exit__(self, type, value, traceback):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")


import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#%% 


#%%


n_points = 1000
token_range = supply * 1.5
if token_range == 0:
    token_range = 100
token_range = np.arange(0.0, token_range,token_range/n_points)

fig1, ax = plt.subplots()
ax.set_xlabel('Supply [Drop tokens]')
ax.set_ylabel('Price [Ocean tokens]')
ax.grid(True)
ax.plot(token_range,this_curve.curve(token_range))

# Plot the current position in curve
ax.plot([supply], [this_curve.get_price(supply)], marker='*', markersize=10, color="red")

# Plot the area under the curve
ix = np.linspace(0, supply)
iy = this_curve.curve(ix)
verts = [(0, 0)] + list(zip(ix, iy)) + [(supply, 0)]
patch_color = (153/255, 229/255, 181/255)
poly = mpl.patches.Polygon(verts, facecolor=patch_color, edgecolor='0.')
ax.add_patch(poly)

# Plot the current position coordinates
coordinate_label = "{:0.0f} Drops \n{:0.0f} Ocean".format(supply,curr_price)
#print(coordinate_label)
ax.text(supply*0.95,curr_price*1.05,coordinate_label,horizontalalignment='right')
ax.plot([0, supply], [curr_price, curr_price], linestyle='--',color='grey',)
ax.plot([supply, supply], [curr_price, 0], linestyle='--',color='grey',)




#%% Bonding curve families
token_range = 1000
supply = 400
class PowerCurve():
    #self.curve = curve_function
    def __init__(self,exponent):
        
        self.exponent = exponent
        self.tag = "power-{}".format(self.exponent)
        self.name = "Exponential bonding curve family, {}".format(self.tag)
        
    def curve(self,tokens):
        return tokens ** self.exponent
    
    def get_price(self,supply):
        return self.curve(supply)
        #plt.plot([x], [y], marker='o', markersize=3, color="red")

    def plot_curve(self, ax):
        #curr_price =  self.get_price(supply)

        n_points = 1000
        token_range = supply * 1.5
        if token_range == 0:
            token_range = 100
        token_range = np.arange(0.0, token_range,token_range/n_points)
        
        #fig1, ax1 = plt.subplots()
        ax.set_xlabel('Supply [Drop tokens]')
        ax.set_ylabel('Price [Ocean tokens]')
        ax.set_title(self.name)
        ax.grid(True)
        ax.plot(token_range,self.curve(token_range))
        if 0:
            # Plot the current position in curve
            ax.plot([supply], [curr_price], marker='*', markersize=10, color="red")
    
            # Plot the area under the curve
            ix = np.linspace(0, supply)
            iy = self.curve(ix)
            verts = [(0, 0)] + list(zip(ix, iy)) + [(supply, 0)]
            patch_color = (153/255, 229/255, 181/255)
            poly = mpl.patches.Polygon(verts, facecolor=patch_color, edgecolor='0.')
            ax.add_patch(poly)
            
            # Plot the current position coordinates
            coordinate_label = "{:0.0f} Drops \n{:0.0f} Ocean".format(supply,curr_price)
            #print(coordinate_label)
            ax.text(supply*0.95,curr_price*1.05,coordinate_label,horizontalalignment='right')
            ax.plot([0, supply], [curr_price, curr_price], linestyle='--',color='grey',)
            ax.plot([supply, supply], [curr_price, 0], linestyle='--',color='grey',)
        
        return ax
        #ax1.axhline(y=curr_price, xmin=0, xmax=0.2, color='grey', linestyle='--')
        #ax1.hlines(y=0.6, xmin=0.0, xmax=1.0, color='b')

    def plot_market_point(self,ax, supply=0):
        curr_price =  self.get_price(supply)
        # Plot the current position in curve
        ax.plot([supply], [curr_price], marker='*', markersize=10, color="red")

        # Plot the area under the curve
        ix = np.linspace(0, supply)
        iy = self.curve(ix)
        verts = [(0, 0)] + list(zip(ix, iy)) + [(supply, 0)]
        patch_color = (153/255, 229/255, 181/255)
        poly = mpl.patches.Polygon(verts, facecolor=patch_color, edgecolor='0.')
        ax.add_patch(poly)
        
        # Plot the current position coordinates
        coordinate_label = "{:0.0f} Drops \n{:0.0f} Ocean".format(supply,curr_price)
        ax.text(supply*0.95,curr_price*1.05,coordinate_label,horizontalalignment='right')
        ax.plot([0, supply], [curr_price, curr_price], linestyle='--',color='grey',)
        ax.plot([supply, supply], [curr_price, 0], linestyle='--',color='grey',)
        
        return ax

    def plot_move(self, ax, supply0,supply1):
        delta = self.change(supply0,supply1)
        # Plot the area under the curve
        
        ix = np.linspace(supply0, supply1)
        iy = self.curve(ix)
        
        #verts = [(supply0, self.curve(supply0))] + list(zip(ix, iy)) + [(supply1, supply0)]
        
        verts = [(supply0, self.curve(supply0))] + list(zip(ix, iy)) + [(supply1, supply0)]
        patch_color = (200/255, 200/255, 200/255)
        poly = mpl.patches.Polygon(verts, facecolor=patch_color, edgecolor='0.')
        ax.add_patch(poly)        
        
    def change(self,supply0,supply1):
        """Calculate the Riemann sum between two bonding curve points. 
        
        The drops are always positive integers
        
        """
        assert isinstance(supply0, int) 
        assert isinstance(supply1, int)
        assert supply0>=0
        assert supply1>=0
        
        if supply0 < supply1:
            log_str = "Buying {} drops".format(supply1-supply0)
            drop_steps = np.arange(supply0,supply1+1,1)
        elif supply0 > supply1:
            log_str = "Selling {} drops".format(supply1-supply0)
            drop_steps = np.arange(supply0,supply1-1,-1)
        else: raise
        
        # TODO: Watch for precision on price and rounding errors!!!
        price = 0
        # TODO: This is still awkward, hardcode +/- 1? 
        for start_supply, stop_supply in zip(drop_steps, drop_steps[1:]):
            #print(start_supply, stop_supply)
            price_delta = self.get_price(stop_supply) - self.get_price(start_supply)
            price += price_delta
            #print("{} - {} @ {}, running total: {}".format(start_supply,stop_supply,price_delta,price))
        
        # TODO: Can do this better without negating? 
        logging.debug("{} costs {} Ocean".format(log_str,price))
        return -price
    
    def plot_market_move(self):
        pass
#%%

this_curve = PowerCurve(0.5)
this_curve.change(400,410)
this_curve.change(400,395)


#%% Plot a market point
# Execute this all at once!
fig1, ax = plt.subplots()
ax = this_curve.plot_curve(ax)
ax = this_curve.plot_market_point(ax,400)
#ax = this_curve.plot_move(ax,400,410)
plt.show(ax)

#
#this_curve.plot(400)


#%%
class Track():
    def __init__(self,title,URL,sell_bonding_curve,buy_bonding_curve):
        self.title = title
        self.URL = URL
        self.sell_bonding_curve = sell_bonding_curve
        self.buy_bonding_curve = buy_bonding_curve
        self.supply = 0 
        logging.debug("New asset {} with Sell: {} and Buy: {}".format(
                self.title,
                self.sell_bonding_curve.tag,
                self.buy_bonding_curve.tag,))
    
    def calculate_price(drops):
        pass
    
    def buy_stake(drops):
        
        pass
        # Backend connection to on-chain smart contract
    
    def plot_stake(self):
        self.sell_bonding_curve.plot()

tracks = list()

t1 = Track("Barrets Privateers",
           "https://open.spotify.com/track/4NEPQ4lRsO2JF5ZMqw63nC",
           PowerCurve(1.4),PowerCurve(1.4))
tracks.append(t1)

t2 = Track("Whale song",
           "https://open.spotify.com/track/6lsXCbHZ7BpssdVtG2hQZM",
           PowerCurve(0.8),PowerCurve(1.4))
tracks.append(t2)

t3 = Track("The Ocean",
           "https://open.spotify.com/track/2CPqh63wRVscbceKcPxwvv",
           PowerCurve(0.5),PowerCurve(1.4))
tracks.append(t3)

#%%

t3.plot_stake()

#%%

#webbrowser.open(t1.URL)
#webbrowser.open(t2.URL)
#%%


#%%
def power(_baseN,_baseD,_expN,_expD):
    lnBaseTimesExp = math.log(_baseN, _baseD) * (_expN / _expD);
    

#%%
value = 37
bitstring = "{:b}".format(value)
format(value,'b').zfill(256)
format(value,'x').zfill(256)

power(value,1,2,1)


print(bitstring)
hexstring = "{:x}".format(value)
print(hexstring)

value.zfill(n) 
hex(37)


#%%

def