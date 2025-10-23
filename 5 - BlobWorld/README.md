# Blob world
This is a simple experiment to compare two types of genetically evolved AI against each other in a simulated world.

# Blobs
These are the agents that live in the world. Each blob has energy, speed, and bearing. As they move, their energy depletes until they are completely exhausted, or find food to eat. Higher speed depletes energy faster.

## Neural blobs
These blobs have a tiny neural network controlling their decisions. The networks will not be trained through supervised learning, but rather through neuro-evolution.
These blobs are represented by green squares.
The neural networks accept [speed, energy, distance to nearest food, sin angle component to nearest food, cos angle component to nearest food]
The neural net outputs two values [angle_delta, action], Action dictates -> speed up, slow down, eat

## QBlob
W.I.P
