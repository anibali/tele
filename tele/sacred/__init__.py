import tele

Sink = tele.Sink


class Conf(tele.Conf):
    def __init__(self, run):
        """Create an output configuration for Sacred.

        Args:
            run (sacred.run.Run): A Sacred Run object.
        """
        super().__init__()
        self.run = run

    def build(self, view_list):
        cell_list = [view.build(self.run) for view in view_list]
        return Sink(cell_list)
