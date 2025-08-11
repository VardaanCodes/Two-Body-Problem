# What?
This is a code to simulate gravitational attraction between two bodies of various masses, and radii.\
We took this challenge up because of a competition hosted by ILM AI for doing the same. It recommended using JavaScript, but since none of know JS, and it was only a reccommendation, we decided to go ahead with python(with which we were more comfortable with)

# Who?

People working on this project
Jawaharbabu 


# The PS

## 🧿 Overview

Simulate the orbital interaction between two bodies under Newtonian gravity. The simulation should be **interactive**, **visual**, and **numerically accurate**.

## 🎯 Objective

Participants must build a 2D simulation that allows users to:

- Set initial **positions, velocities, and masses** for two bodies
- Visualize dynamic **orbital paths**
- Interact with the system in real-time (modify parameters, pause/reset)
- Optionally include: collision detection, escape conditions, or a center-of-mass reference frame

## 💬 Modeling & Numerical Integration

Participants must model gravitational interactions and implement a numerical solver (e.g., **Verlet, Runge-Kutta**, or similar) to update the system state over time. Precision and stability are key.

> **No physics equations are given** — teams are expected to derive and implement appropriate force models and solvers.

## 📊 Simulation Requirements

- Real-time visualization of body positions and orbit trails
- Parameter controls: mass, position, velocity
- Smooth animations and user feedback
- Optional enhancements: elastic collisions, escape paths, center-of-mass tracking

## 🏅 Scoring (100 Points Total)

| Criteria                                              | Points |
|-------------------------------------------------------|--------|
| Accurate physics modeling (gravitational dynamics)     | 40     |
| Numerical integration (stability, accuracy)            | 20     |
| UI interactivity (controls, reset, etc.)               | 15     |
| Visualization quality (orbits, trails)                 | 10     |
| Code clarity & responsiveness                         | 10     |
| Optional enhancements (collisions, etc.)               | 5 to 15    |

---


## 1. UIUX
### Entry screen
A basic background,\
entry fields m1m2,v1v2, x1x2
Button to start
### Simulation screen
#### Data box
Live data casting m1m2,v1v2, x1x2, images of the planets corresponding to the data.
#### Simulation window
images of the planets, along with velocity vector. Show the full trail with the transparency function defined in the algo part
#### Control Box
Pause/Resume and Reset as seperate buttons\
##### Modify live parameters after pausing, 
changes gets applied after pushing a modify button
1. A modify button, entry fields are not shown
2. When it is pressed, program pauses, and entry fields apper with the current parameters, and input boxes, m1m2,v1v2, x1x2, along with an apply button while the modify button remains highlighted.
3. You enter the data, and press the apply button.
4. After that, the parameters are updated, and the simulation resumes. Entry field and the apply button disappear again. The modify button becomes unhighlighted

##### On pressing reset
The simulation stops abruptly, previous data is deleted, screen state changes back to entry screen.


## 2. Algo
### Inputs
1. Position of two bodies
2. initial velocities of two bodies
3. masses


### Outputs
1. $x(t)$ for both bodies
2. $x'(t)$ for both bodies
3. Trail of the com.
    1. Transperency function as T(t)
Extras
4. Real time modifications of position velocity mass
5. ISR Pause or reset


### Processing
1. derive the differential equation
2. solve it numerically
3. Choose a numerical method
    1. Verlet
    2. Runge-Kutta
    3. Implement sophisticated methods like adaptive step size, etc.