This project can be started from various files

For the GUI version, run 
python UI.py

- This will launch the setup program from where you can select a pre-trained agent to simulate
	or start a new training session with some customized parameters
- If any pre-trained agents exist, they will be populated onto the interface to be selected.
	- Once you have selected an agent and set the world size, you can click "Go" to see the simulation
- To start a new training session, click on "Train From Scratch"
	- You will be presented with a list of parameters you can change to alter the course of training
	-> Number of agents per generation determines the population size
		(Larger population size means more variety in every generation and may discover a good agent faster, but will take longer to train)
	-> Number of survivors per generation determines how many of the best performers from each generation will be carried over to the next
		(Allowing more agents to survive lowers the rate of exploration)
	-> Number of generations to train sets a limit on the number of training cycles. If this value is set to -1, the training will run until the threshold is reached
	-> Goal for food items is the threshold for success. If an agent manages to eat at least this many food items, the training will end
	-> Mutation rate determines the probability of mutations occuring when a new generation is created.
		(Higher mutation rate means greater difference in behaviour from generation to generation)
	- You have the option to visualize the training. This allows you to see the agent becoming better (or sometimes worse) at finding food and staying alive
	- Once the parameters have been set up, you may click "Go" to begin training
		- The text area to the right will display information about the performance of each generation and will display a message if training ended early


For the command line version, run
python Trainer.py

- You will be prompted to enter the training parameters via the command line, however you will still have the option to have the training visualised