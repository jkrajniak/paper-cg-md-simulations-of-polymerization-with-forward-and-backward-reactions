def my_diff(y,t,k):
    f  = np.zeros(4)
    f[0] = - k[0]*y[0] - k[1]*y[0] - k[2]*y[0]**2
    f[1]= k[0]*y[0]
    f[2] = k[1]*y[0]
    f[3] = k[2]*y[0]**2
    return f

# solve the ODE
sol = integrate.odeint(my_diff,y,t,(k,))
# update initial conditions and solve again
y = [ sol.T[0][-1] + new_pulse,
      sol.T[1][-1] , sol.T[2][-1] , sol.T[3][-1]]