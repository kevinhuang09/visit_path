from simulation import Simulation
from visualizer import draw_paths
import config

def main():
    sim = Simulation()

    sim.load_coordinates()

    sim.add_worker("worker A", start_pos = config.START_POSITION)
    sim.add_worker("worker B", start_pos = config.START_POSITION)

    sim.run()

    draw_paths(sim.workers, "result/picture/two_workers.png")

if __name__ == "__main__":
    main()