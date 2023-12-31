#!/usr/bin/env python
# coding: utf-8

# In[162]:


'''Monte Carlo simulation of release-and-recapture experiments in optical tweezers to 
                 determine the temperature of trapped ytterbium atoms '''


import numpy as np
import matplotlib.pyplot as plt

# Define trapping frequencies (in Hz)
omega_x = (2*np.pi * 135 )* 1000
omega_y = (2*np.pi * 135 )* 1000
omega_z = (2*np.pi * 30 )* 1000
    
def monte_carlo_simulation(num_particles):
    positions = np.zeros((num_particles, 3))
    velocities = np.zeros((num_particles, 3))
    for i in range(num_particles):
        # Generate x, y, and z components of velocity
        vx, vy, vz = np.random.normal(0, 1, 3) * np.sqrt(kb*T / m) 
        # Generate x, y, and z components of position
        x= np.random.normal(0, 1) * np.sqrt(kb*T / (m * omega_x**2))
        y= np.random.normal(0, 1) * np.sqrt(kb*T / (m * omega_y**2))
        z= np.random.normal(0, 1) * np.sqrt(kb*T / (m * omega_z**2))
        positions[i] = [x, y, z]
        velocities[i] = [vx, vy, vz]
    return positions, velocities


# In[184]:


# Parameters
kb =  1.380649e-23  #unit: m2 kg s-2 K-1
T = 31e-6 # temperature in K
m = 173.04* 1.66e-27   # mass in kg
g = 9.8  # m s-2

# Run simulation
num_particles = 1000
positions, velocities = monte_carlo_simulation(num_particles)
#velocities



# In[185]:


x=np.zeros(num_particles)
y=np.zeros(num_particles)
z=np.zeros(num_particles)

vx = np.zeros(num_particles)
vy = np.zeros(num_particles)
vz = np.zeros(num_particles)

for i in range(len(velocities)):
    x[i] = positions[i][0]
    y[i] = positions[i][1]
    z[i] = positions[i][2]
    vx[i] = velocities[i][0]
    vy[i] = velocities[i][1]
    vz[i] = velocities[i][2]
len(x)    


# In[186]:


#Initializing arrays to store new position and velocity after time evolution
x_n = []
y_n = []
z_n = []
vx_n = []
vy_n = []
vz_n = []

time_int = np.linspace(1e-6,20e-6,50)
num_steps = len(time_int)

#Time evolution
for time in time_int:
    new_x = x + vx*time
    new_y = y + vy*time
    new_z = z + vz*time - (g* time**2)/2
    
    new_vx = vx
    new_vy = vy
    new_vz = vz - g * time
        
    x_n.append(new_x)
    y_n.append(new_y)
    z_n.append(new_z)
    vx_n.append(new_vx)
    vy_n.append(new_vy)
    vz_n.append(new_vz)

kinetic_e = m * (np.square(vx_n) + np.square(vy_n) + np.square(vz_n))/2  #kinetic energy


# In[187]:


#Comparing with trap depth
k = 2*np.pi/(532*10**-9) # 2pi/532nm in this case since the trapping light is generated by a 532nm laser.

# Define trapping frequencies (in Hz)
omega_x = (2*np.pi * 135 )* 1000
omega_y = (2*np.pi * 135 )* 1000
omega_z = (2*np.pi * 30 )* 1000  

#hbar = 1.05457182e-34 # m2 kg / s

# Gaussian factor 
def gauss_factor(x,sd):
    prob_density =  np.exp(-2*(x**2/sd**2))
    return prob_density

#Get local trapping potentials
def get_localVx(x):
    V= np.zeros(len(x))
    for i in range(len(x)):
        V[i] = omega_x**2 * mass/ (2 * k**2 ) * gauss_factor(x[i],5e-7) 
    return V                       

def get_localVy(x):
    V= np.zeros(len(x))
    for i in range(len(x)):
        V[i] = omega_y**2 * mass/ (2 * k**2 ) * gauss_factor(x[i],5e-7) 
    return V 

def get_localVz(x):
    V= np.zeros(len(x))
    for i in range(len(x)):
        V[i] = omega_z**2 * mass/ (2 * k**2 ) * gauss_factor(x[i],5e-7) 
    return V 


# In[188]:


#Since ħω_x,y,z = sqrt(2ħ^2 |V_x,y,z|k^2 / m) 

V_x = []
V_y = []
V_z = []

for i in range(len(x_n)):
        V_x.append(get_localVx(x_n[i]))
        V_y.append(get_localVy(y_n[i]))
        V_z.append(get_localVz(z_n[i]))

#standard dev of 1.2um and mean 0. Tweezer waist is on the order of 500nm    


# In[189]:


trap_depth = []

for i in range(len(V_x)):
    trap_depth.append(V_x[i] + V_y[i] + V_z[i])
    
#trap_depth


# In[190]:


# Compare trap depth with kinetic energy and create num_recapture array
num_recapture = np.where(trap_depth > kinetic_e, 1, 0)
num_recapture


# In[191]:


counts = []
for i in range(len(num_recapture)):
    counts.append(sum(num_recapture[i]))
    
prob = np.array(counts)/num_particles


# In[192]:


prob


# In[193]:


plt.plot(time_int*1e+6,prob, 'bo')
plt.xlabel("Time in microsecs")
plt.ylabel("Recapture probability")
plt.show()


# In[ ]:





# In[ ]:




