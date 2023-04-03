from host.host_interface import HostInterface

def main():
    episodes = 100
    steps = 10000
    hostInterface = HostInterface()
    for i in range(episodes):
        state = hostInterface.NewEpisode()
        for j in range(steps):
            reward, nextState = hostInterface.StepByAction(1)
            print(f'episode: {i}, step: {j}, state: {state}, reward: {reward}, nextState: {nextState}')
            state = nextState

if __name__ == "__main__":
    main()