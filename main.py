from simulation import Simulation
import config

def main():
    sim = Simulation()

    sim.load_coordinates()

    sim.add_worker("worker A", start_pos = config.START_POSITION)
    # sim.add_worker("worker B", start_pos = config.START_POSITION)

    sim.run()

if __name__ == "__main__":
    main()