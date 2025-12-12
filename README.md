# Solving the N-Body Problem Numerically Using a Lagrangian Approach

This repository contains my submission for Ohio State University's Physics 5300 final project.

Start with the `FinalProject.ipynb` file.

<br/>

## Project Organization

The `ProjectInstructions.pdf` document contains directions provided by the class.

The `FinalProject.ipynb` file or the `FinalProject.pdf` export of that notebook present a self-contained lesson on how the N-Body problem was solved. The notebook matches the structure of the *ProjectInstructions* file.

The `src` directory contains python scripts that can be used to solve the N-Body problem for several known cases and to create animations of the results.
- The `ProjectSolution.py` file contains the numerical integrator used to solve the problem.
- The `*Animation.py` files use the integrator to create animations. 

The `media` directory contains resources made for the project.
- The `videos` directory contains the animations made by the provided scripts.
- The `presentations` directory contains the presentation slides used on *12-9-25*. 
  - The animations were removed from the slides to reduce file size.

<br/>

## Usage Instrustions

Start the Jupyter notebook and run the cells in order to understand how the problem was solved and how the numerical integrator works.

To create animations, run either of provided `src/*Animation.py` scripts.
- ex) `python ./src/3BodyAnimation.py`

To use the numerical integrator in other projects, include the `src/ProjectSolution` script.
- ex) `from ProjectSolution import NBodyOrbit`