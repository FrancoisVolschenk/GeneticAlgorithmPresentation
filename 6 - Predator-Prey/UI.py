import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import Trainer
import os
from scrollFrame import ScrollableFrame
import threading


class GUI:
    """This class represents the User Interface for setting up training and for viewing the agent in action"""

    def __init__(self):
        # set up the basic window
        self.window = tk.Tk()
        self.window.title("AI setup menu")
        self.lstAgentButtons = []

        # create the widgets that make up the interface
        self.lstWidgets = []
        self.frSize = tk.Frame()
        self.lstWidgets.append(self.frSize)

        # Components to determine world size
        self.lblHeading = ttk.Label(
            master=self.frSize, text="Setup the size of the world"
        )
        self.lblHeading.grid(row=0, column=0, columnspan=2)
        self.lblRows = ttk.Label(master=self.frSize, text="Number of rows:", width=18)
        self.lblRows.grid(row=1, column=0, pady=5, padx=5)
        self.sbRows = ttk.Spinbox(master=self.frSize, from_=10, to=50, wrap=True)
        self.sbRows.set(20)
        self.sbRows.grid(row=1, column=1, pady=5, padx=5)

        self.lblCols = ttk.Label(
            master=self.frSize, text="Number of columns:", width=18
        )
        self.lblCols.grid(row=2, column=0, pady=5, padx=5)
        self.sbCols = ttk.Spinbox(master=self.frSize, from_=10, to=50, wrap=True)
        self.sbCols.set(20)
        self.sbCols.grid(row=2, column=1, pady=5, padx=5)

        # Components for setting up tarining parameters
        self.frTraining = tk.Frame()
        self.lblTrainHeading = ttk.Label(
            master=self.frTraining, text="Enter the parameters for the training"
        )
        self.lblTrainHeading.grid(row=0, column=0, columnspan=2)

        self.lblNumAgents = ttk.Label(
            master=self.frTraining, text="Number of Agents Per Generation: "
        )
        self.lblNumAgents.grid(row=1, column=0)

        self.sbNumAgents = ttk.Spinbox(master=self.frTraining, from_=1, to=1000)
        self.sbNumAgents.set(1)
        self.sbNumAgents.grid(row=1, column=1)

        self.numSurvivors = ttk.Label(
            master=self.frTraining, text="Number of Survivors Per Generation: "
        )
        self.numSurvivors.grid(row=2, column=0)

        self.sbNumSurvivors = ttk.Spinbox(master=self.frTraining, from_=1, to=1000)
        self.sbNumSurvivors.set(1)
        self.sbNumSurvivors.grid(row=2, column=1)

        self.lblGensHint = ttk.Label(
            master=self.frTraining,
            text="Set this value to -1 to run training until the threshold is met",
        )
        self.lblGensHint.grid(row=3, column=0, columnspan=2)

        self.lblNumGenerations = ttk.Label(
            master=self.frTraining, text="Number of Generations to Train: "
        )
        self.lblNumGenerations.grid(row=4, column=0)

        self.sbNumGenerations = ttk.Spinbox(master=self.frTraining, from_=-1, to=1000)
        self.sbNumGenerations.set(1)
        self.sbNumGenerations.grid(row=4, column=1)

        self.lblThreshold = ttk.Label(
            master=self.frTraining, text="Goal for number of food items: "
        )
        self.lblThreshold.grid(row=5, column=0)

        self.sbThreshold = ttk.Spinbox(master=self.frTraining, from_=1, to=1000)
        self.sbThreshold.set(1)
        self.sbThreshold.grid(row=5, column=1)

        self.lblMutationRate = ttk.Label(master=self.frTraining, text="Mutation Rate: ")
        self.lblMutationRate.grid(row=6, column=0)

        self.sbMutationRate = ttk.Spinbox(
            master=self.frTraining, from_=0.0, to=1.0, increment=0.1
        )
        self.sbMutationRate.set(0.5)
        self.sbMutationRate.grid(row=6, column=1)

        self.Visualize = tk.StringVar()
        self.cbVisualize = ttk.Checkbutton(
            master=self.frTraining, text="Visualize training", variable=self.Visualize
        )  # , onvalue = "True", offvalue = "False"
        self.cbVisualize.grid(row=7, column=0, columnspan=2)

        self.lblSate = ttk.Label(master=self.frTraining, text="")
        self.lblSate.grid(row=0, column=2)

        self.txtProgress = scrolledtext.ScrolledText(
            master=self.frTraining, width=45, height=20
        )
        self.txtProgress.grid(row=1, column=2, rowspan=7)

        # Components for pre-trained agent selection
        self.frAgentSelect = ScrollableFrame(self.window)
        self.lstWidgets.append(self.frAgentSelect)

        self.lblAgentHeading = ttk.Label(
            master=self.frAgentSelect.scrollable_frame, text="Select an agent to run"
        )
        self.lblAgentHeading.pack(fill=tk.X)

        self.selectedAgent = tk.StringVar()
        self.loadAgentFiles()

        self.mode = 1

        # Components for navigating the interface
        self.frActions = tk.Frame()
        self.lstWidgets.append(self.frActions)

        self.btnGo = ttk.Button(
            master=self.frActions, text="Go", width=20, command=self.go
        )
        self.btnGo.grid(row=0, column=0)

        self.btnTrain = ttk.Button(
            master=self.frActions,
            text="Train from scratch",
            width=20,
            command=self.displayTraining,
        )
        self.btnTrain.grid(row=0, column=1)

        self.btnAgentSelect = ttk.Button(
            master=self.frActions,
            text="Select Agent to Simulate",
            state="disabled",
            command=self.displayAgentSelect,
        )
        self.btnAgentSelect.grid(row=0, column=2)

        # Place all of the widgets on the interface
        for widget in self.lstWidgets:
            widget.pack(fill=tk.X)

        # Begin main loop to stop the program from closing once all the code has been run
        self.window.mainloop()

    def loadAgentFiles(self):
        # Find all of the ai files in the current directory and present them to the user
        files = os.listdir("Agents")

        # clear the list that is currently displayed
        for btn in self.lstAgentButtons:
            btn.pack_forget()
            btn.destroy()

        # Display a new list of selectable agents
        for f in files:
            if f.endswith(".ai"):
                self.lstAgentButtons.append(
                    tk.Radiobutton(
                        master=self.frAgentSelect.scrollable_frame,
                        text=f,
                        indicator=0,
                        value=f,
                        variable=self.selectedAgent,
                        background="light blue",
                    )
                )
                self.lstAgentButtons[len(self.lstAgentButtons) - 1].pack(
                    fill=tk.X, pady=2, padx=5
                )

    def displayTraining(self):
        # Display the controls for setting up training
        self.mode = 2
        self.frAgentSelect.pack_forget()
        self.frActions.pack_forget()
        self.btnTrain.configure(state="disabled")
        self.btnAgentSelect.configure(state="enabled")
        self.frTraining.pack()
        self.frActions.pack()

    def displayAgentSelect(self):
        # Display the controls for selecting and running an agent
        self.mode = 1
        self.frTraining.pack_forget()
        self.frActions.pack_forget()
        self.btnAgentSelect.configure(state="disabled")
        self.btnTrain.configure(state="enabled")
        self.loadAgentFiles()
        self.frAgentSelect.pack()
        self.frActions.pack()

    def go(self):
        # Begin training, or start agent simulation
        width = int(self.sbCols.get())
        height = int(self.sbRows.get())
        if self.mode == 1:  # Simulate agent
            if self.selectedAgent.get() == "":
                tk.messagebox.showerror(
                    title="Error", message="Please select an agent to simulate"
                )
            else:
                Trainer.simulate(width, height, self.selectedAgent.get())
        if self.mode == 2:  # Begin training
            self.lblSate.configure(text="")
            # gather the set parameters for training
            numPerGen = int(self.sbNumAgents.get())
            numKeepers = int(self.sbNumSurvivors.get())
            numGens = int(self.sbNumGenerations.get())
            if numGens == 0:
                numGens = -1

            threshold = int(self.sbThreshold.get())
            mutationRate = float(self.sbMutationRate.get())
            show = self.Visualize.get() == "1"

            self.txtProgress.delete(1.0, tk.END)

            # begin training
            # Use threading to allow the Trainer class to print updates to the UI as the generations progress
            self.lblSate.configure(text="Training in progress...")
            # tTraining = threading.Thread(target = Trainer.TrainFromScratch, args=(width, height, numPerGen, numKeepers, numGens, threshold, mutationRate, show, self.txtProgress))
            # tTraining.start()

            Trainer.TrainFromScratch(
                width,
                height,
                numPerGen,
                numKeepers,
                numGens,
                threshold,
                mutationRate,
                show,
                self.txtProgress,
            )


if __name__ == "__main__":
    # if this file is run on its own, start the UI
    GUI()
