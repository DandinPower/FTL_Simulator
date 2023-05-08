from dotenv import load_dotenv
import os
load_dotenv()

def WriteReport(path, length, gcCount, rewardSum, coldCount, hotCount):
    report = f'Simulation Report\n'
    report += '-' * 35 + '\n'
    report += '{:35s} {:20d}\n'.format('Simulate Length:', length)
    report += '{:35s} {:20d}\n'.format('Total Gc Times:', gcCount)
    report += '{:35s} {:20.2f}\n'.format('Total Reward:', rewardSum)
    report += '{:35s} {:20d}\n'.format('Cold Action Count:', coldCount)
    report += '{:35s} {:20d}\n'.format('Hot Action Count:', hotCount)
    report += '{:35s} {:20.2f}\n'.format('Cold Action Ratio:', (coldCount / length))
    report += '{:35s} {:20.2f}\n'.format('Hot Action Ratio:', (hotCount / length))
    with open(path, 'w') as file:
        file.write(report)