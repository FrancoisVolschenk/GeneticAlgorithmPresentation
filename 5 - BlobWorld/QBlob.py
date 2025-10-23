from Blob import Blob


class QBlob(Blob):
    """This class represents the blobs that will make use of a Q table to decide their behaviours"""
    ### W.I.P.
    def __init__(self):
        super().__init__()
        self.colour = (0, 0, 255)

    def decide_move(self, food_items):
        print("Q blob uses policy")