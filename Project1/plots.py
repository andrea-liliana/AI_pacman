import numpy as np
import matplotlib.pyplot as plt

barWidth = 0.25

# Scores Easy layout
hminimax2 = [533, 534, 534]
hminimax1 = [-530, 530, 530]
hminimax0 = [532, 526,528]
#hminimax0 = [-530, 530, 530]
 
r1 = np.arange(len(hminimax2))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

bar1 = plt.bar(r1, hminimax2, color='skyblue', width=barWidth, edgecolor='white', label='Hminimax2')
bar2 = plt.bar(r2, hminimax1, color='lightgreen', width=barWidth, edgecolor='white', label='Hminimax1')
bar3 = plt.bar(r3, hminimax0, color='lightcoral', width=barWidth, edgecolor='white', label='Hminimax0')

plt.xlabel('Scores Normal Layout', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hminimax2))], ['Dumby', 'Greedy', 'Smarty'])

plt.bar_label(bar1, padding=3)
plt.bar_label(bar2, padding=3)
plt.bar_label(bar3, padding=3)

plt.legend()
plt.show()

# Scores Nomal layout
hminimax2 = [545, 546, 546]
hminimax1 = [535, 548, 548]
hminimax0 = [-509, -508, -508]
#hminimax0 = [535, 548, 548]

r1 = np.arange(len(hminimax2))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

bar1 = plt.bar(r1, hminimax2, color='skyblue', width=barWidth, edgecolor='white', label='Hminimax2')
bar2 = plt.bar(r2, hminimax1, color='lightgreen', width=barWidth, edgecolor='white', label='Hminimax1')
bar3 = plt.bar(r3, hminimax0, color='lightcoral', width=barWidth, edgecolor='white', label='Hminimax0')
 
plt.xlabel('Scores Hard Layout', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hminimax2))], ['Dumby', 'Greedy', 'Smarty'])

plt.bar_label(bar1, padding=3)
plt.bar_label(bar2, padding=3)
plt.bar_label(bar3, padding=3)
 
plt.legend()
plt.show()


# Time Performances Easy Layout

hminimax2 = [0.12005329132080078, 0.15901494026184082, 0.24899768829345703 ]
hminimax1 = [3.807037115097046,3.1781246662139893, 3.041027069091797 ] 
hminimax0 = [12.556926727294922, 8.915049314498901, 10.693758726119995 ]
#hminimax0 = [3.807037115097046,3.1781246662139893, 3.041027069091797 ] 
 
r1 = np.arange(len(hminimax2))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

bar1 = plt.bar(r1, hminimax2, color='skyblue', width=barWidth, edgecolor='white', label='Hminimax2')
bar2 = plt.bar(r2, hminimax1, color='lightgreen', width=barWidth, edgecolor='white', label='Hminimax1')
bar3 = plt.bar(r3, hminimax0, color='lightcoral', width=barWidth, edgecolor='white', label='Hminimax0')
 
plt.xlabel('Time Performance (seg) Normal Layout', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hminimax2))], ['Dumby', 'Greedy', 'Smarty'])

plt.bar_label(bar1, padding=3)
plt.bar_label(bar2, padding=3)
plt.bar_label(bar3, padding=3)
 
plt.legend()
plt.show()

# Time Performances Hard Layout

hminimax2 = [0.11391925811767578, 0.12401819229125977, 0.1901254653930664 ]
hminimax1 = [5.3580639362335205,2.5630714893341064,2.399111747741699 ]
hminimax0 = [4.982050895690918,4.201996564865112,4.273043870925903 ]
#hminimax0 = [5.3580639362335205,2.5630714893341064,2.399111747741699 ]
 
r1 = np.arange(len(hminimax2))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

bar1 = plt.bar(r1, hminimax2, color='skyblue', width=barWidth, edgecolor='white', label='Hminimax2')
bar2 = plt.bar(r2, hminimax1, color='lightgreen', width=barWidth, edgecolor='white', label='Hminimax1')
bar3 = plt.bar(r3, hminimax0, color='lightcoral', width=barWidth, edgecolor='white', label='Hminimax0')
 
plt.xlabel('Time Performance (seg) Hard Layout', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hminimax2))], ['Dumby', 'Greedy', 'Smarty'])

plt.bar_label(bar1, padding=3)
plt.bar_label(bar2, padding=3)
plt.bar_label(bar3, padding=3)
 
plt.legend()
plt.show()

# Number of expanded Nodes Easy Layout 

hminimax2 = [184, 274, 274]
hminimax1 = [7753, 6475, 6475]
hminimax0 = [33108, 24120, 23534]
#hminimax0 = [7753, 6475, 6475]
 
r1 = np.arange(len(hminimax2))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

bar1 = plt.bar(r1, hminimax2, color='skyblue', width=barWidth, edgecolor='white', label='Hminimax2')
bar2 = plt.bar(r2, hminimax1, color='lightgreen', width=barWidth, edgecolor='white', label='Hminimax1')
bar3 = plt.bar(r3, hminimax0, color='lightcoral', width=barWidth, edgecolor='white', label='Hminimax0')
 
plt.xlabel('Number of Expanded Nodes Normal Layout', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hminimax2))], ['Dumby', 'Greedy', 'Smarty'])

plt.bar_label(bar1, padding=3)
plt.bar_label(bar2, padding=3)
plt.bar_label(bar3, padding=3)
 
plt.legend()
plt.show()


# Number of Expanded Nodes Nomal layout
hminimax2 = [188, 236, 237]
hminimax1 = [10811, 5219, 5113]
hminimax0 = [13028,10759, 10759]
#hminimax0 = [10811, 5219, 5113]
 
r1 = np.arange(len(hminimax2))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

bar1 = plt.bar(r1, hminimax2, color='skyblue', width=barWidth, edgecolor='white', label='Hminimax2')
bar2 = plt.bar(r2, hminimax1, color='lightgreen', width=barWidth, edgecolor='white', label='Hminimax1')
bar3 = plt.bar(r3, hminimax0, color='lightcoral', width=barWidth, edgecolor='white', label='Hminimax0')
 
plt.xlabel('Number of Expanded Nodes Hard Layout', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(hminimax2))], ['Dumby', 'Greedy', 'Smarty'])

plt.bar_label(bar1, padding=3)
plt.bar_label(bar2, padding=3)
plt.bar_label(bar3, padding=3)
 
plt.legend()
plt.show()
