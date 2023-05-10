# Transformation and Simulator Abstraction Language (TSAL) Interpreter

This is a python package for parsing Transformation and Simulator Abstraction Language (TSAL) domain and problem files
into python objects. TSAL is similar (and largely inspired) from the class of Planning Definition Domain Languages
(PDDL). 

This library is required for the [noveltygen](https://github.com/Parallax-Advanced-Research/noveltygen) library.

## Papers

If you use this library, please cite [our paper](https://arxiv.org/abs/2305.04315) that describes the TSAL language:

```text
@misc{molineaux2023framework,
      title={A Framework for Characterizing Novel Environment Transformations in General Environments}, 
      author={Matthew Molineaux and Dustin Dannenhauer and Eric Kildebeck},
      year={2023},
      eprint={2305.04315},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```


***

## Installation
No packages should need to be installed to use this tsal interpreter.

```commandline
# get the code
git clone git@github.com:Parallax-Advanced-Research/tsal.git
cd tsal

# optional: create a virtual environment
python3 -m venv venv

# optional: activate the virtual environment
source venv/bin/activate

# install the package
pip install -e .
```

## Usage
To use the TSAL Interpreter, include the package tsal-interpreter within your project. Creating an Interpreter object requires passing the constructor a domain file and/or a problem_file as a string.

Problem file is optional.

```python
from tsal.interpreter import Interpreter
interpreter = Interpreter(domain_file="examples/blocksworld/domain.tsal", problem_file="examples/blocksworld/problem.tsal")
```

Then you can interact with the domain object, like:

```python
for op in interpreter.domain.operators:
    print(op)
```

## Constructs and Syntax in TSAL

TSAL contains the following constructs:

| TSAL Construct         | Description                                                                                                                      | Originating PDDL Version              |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| Types                  | Enables a type hierarchy of objects                                                                                              | PDDL (McDermott, et al., 1998)        |
| Predicates             | Enables symbolic relationships between objects                                                                                   | PDDL (McDermott, et al., 1998)        |
| Continuous Fluents     | Models continuous state variables                                                                                                | PDDL (McDermott, et al., 1998)        |
| Object Fluents         | Models state variables that contain objects of custom types                                                                      | PDDL 3.1 (Kovacs, 2011)               |
| Instantaneous Actions  | Enables actions that occur instantly, and effects become true  instantly                                                         | PDDL (McDermott, et al., 1998)        |
| Durative Actions       | Enables actions that occur between a start and end time, rather  than being instantaneous                                        | PDDL 2.1 (Fox & Long, 2003)           |
| Events                 | Enables external events to trigger changes to the environment  outside of the actions of an agent                                | PDDL+ (Fox & Long, 2002)              |
| Processes              | Enables processes for updated fluent values via an equation                                                                      | PDDL+ (Fox & Long, 2002)              |
| Negative Preconditions | Enables negated preconditions and effects of actions                                                                             | PDDL (McDermott, et al., 1998)        |
| Timed Initial Literals | Enables initial literals to become true at a specific moment in time                                                             | PDDL 2.2 ( Edelkamp  & Hoffman, 2004) |
| Probabilistic Effects  | Effects of actions and events can occur with some probability                                                                    | PPDDL (Younes & Littman, 2004)        |
| Derived Predicates     | Predicates that are defined in terms of one or more existing  predicates. These predicates serve as higher levels of abstraction | PDDL 2.2 ( Edelkamp  & Hoffman, 2004) |
| Frequency Distribution | Enables a description of events that may occur with some  probability distribution over  a period of time                        | Not in any version of PDDL            |   
Each construct requires its own section in a .tsal file, even if that section is empty.

### TSAL Domain Files

A TSAL Domain file must contain the following constructs inside the domain definition in this order:

    - types definition
    - constants definition
    - fluents definition
    - predicates definition
    - derived predicates definition
    - processes definition
    - actions definition
    - events definition

Within the fluents definitions, there must be a fluent named (self) that is of type "agent". This is used for defining
the expected actor during planning time.
See `domains/carla.tsal` and `domains/monopoly.tsal` for examples.

### TSAL Problem Files
A TSAL problem file must contain the following constructs in this order:

    - problem definition
    - domain definition (the name here should match the domain file '(:domain ...)' clause)
    - objects definition
    - init definition
    - timed-init definition
    - goal
 
##### Important Notes:
- The init definition have a ```(self)``` fluent instantiated with an agent. For example, a fact of ```(= (self) ag1)``` where
```ag1``` is of type agent. 
- The structure of the goal statement within the problem file has some constraints. 
    - We view goals in terms of the agents trying to achieve them. 
    - Goals consist of an *or* statement, where each value within the top-level *or* is directed at a specific agent.
    - Specifying an agent's goal is accomplished using the ```(self)``` fluent. Therefore each subset of the *or* in the goals needs to include
a ```(self)``` fluent attached to the agent. 
    - To perform novelty generation with respect to a particular agent (i.e. the agent being tested) we specify that agent's goals using ```(= (self) agent)``` and for non-self agents we use ```(!= (self) agent)```. 

 
The following goal example describes the goals for 3 agents in a capture-the-flag game where there is a blue team and red team, and the goal for the blue team is to capture the flag while the goal for the opposing team is to remove all agents from the blue team. ```ag1``` is the agent *under test* who is considered the single, non-external agent. All other agents are considered external agents.



    (:goal
        (or
            (and
                (is-blue ag1)
                (= (self) ag1)
                (holds-flag ag1)
            )
            (and
                (!= (self) ag2)
                (not (is-blue ag2))
                (all-blue-dead)
            )
            (and
                (!= (self) ag3)
                (not (is-blue ag3))
                (all-blue-dead)
            )
        )
    )

## Converting PDDL to TSAL

There are a few differences from PDDL and TSAL.

1.  Remove the requirements line.
2.  Check that there exists the following construct sections, in the following order (they can be empty):
    
    - types definition
    - constants definition
    - fluents definition
    - predicates definition
    - derived predicates definition
    - processes definition
    - actions definition
    - events definition

    
## Acknowledgment
This material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Contract No. HR001121C0236. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Defense Advanced Research Projects Agency (DARPA).


## Contributors

- [Dustin Dannenhauer](https://github.com/dtdannen)
  - dustin.dannenhauer@parallaxresearch.org
- [Noah Reifsnyder](https://github.com/NoahDReifsnyder) 
  - noah.reifnsyder@parallaxresearch.org
- AJ Regester
- Matthew Molineaux

## License
tsal is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tsal is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

tsal extends pypddl-parser (https://github.com/thiagopbueno/pypddl-parser)

You should have received a copy of the GNU General Public License
along with tsal.  If not, see <http://www.gnu.org/licenses/>.


