# to run, cd C:/PATH/TO/SCRIPT/LOCATION
# python jackboxRandomizer.pyw

import os, sys, subprocess, random
from appJar import gui

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

steamPath = r"C:\Program Files (x86)\Steam\Steam.exe"

steamIDs = [
	{
		"pack": 1,
		"id": 331670
	},
	{
		"pack": 2,
		"id": 397460
	},
	{
		"pack": 3,
		"id": 434170
	},
	{
		"pack": 4,
		"id": 610180
	},
	{
		"pack": 5,
		"id": 774461
	},
	{
		"pack": 6,
		"id": 1005300
	},
	{
		"pack": 7,
		"id": 1211630
	}
]

# define weights to increase/decrease likelyhood of rolling a gamemode
lowest = range(1)
low = range(2)
medium = range(3)
high = range(4)
highest = range(5)

jackboxGames = [
	[
		{
			"pack": 1,
			"game": "You Don't Know Jack",
			"priority": medium
		},
		{
			"pack": 1,
			"game": "Drawful",
			"priority": high
		},
		{
			"pack": 1,
			"game": "Word Spud",
			"priority": medium
		},
		{
			"pack": 1,
			"game": "Lie Swatter",
			"priority": medium
		},
		{
			"pack": 1,
			"game": "Fibbage XL",
			"priority": medium
		}
	],
	[
		{
			"pack": 2,
			"game": "Quiplash XL",
			"priority": highest
		},
		{
			"pack": 2,
			"game": "Bidiots",
			"priority": medium
		},
		{
			"pack": 2,
			"game": "Fibbage 2",
			"priority": medium
		},
		{
			"pack": 2,
			"game": "Earwax",
			"priority": medium
		},
		{
			"pack": 2,
			"game": "Bomb Corp",
			"priority": medium
		}
	],
	[
		{
			"pack": 3,
			"game": "Guesspionage",
			"priority": medium
		},
		{
			"pack": 3,
			"game": "Fakin It",
			"priority": medium
		},
		{
			"pack": 3,
			"game": "Tee K.O.",
			"priority": high
		},
		{
			"pack": 3,
			"game": "Trivia Murder Party",
			"priority": medium
		},
		{
			"pack": 3,
			"game": "Quiplash 2",
			"priority": highest
		}
	],
	[
		{
			"pack": 4,
			"game": "Fibbage 3",
			"priority": medium
		},
		{
			"pack": 4,
			"game": "Monster Seeking Monster",
			"priority": lowest
		},
		{
			"pack": 4,
			"game": "Survive the Internet",
			"priority": medium
		},
		{
			"pack": 4,
			"game": "Bracketeering",
			"priority": medium
		},
		{
			"pack": 4,
			"game": "Civic Doodle",
			"priority": highest
		}
	],
	[
		{
			"pack": 5,
			"game": "You Don't Know Jack",
			"priority": medium
		},
		{
			"pack": 5,
			"game": "Mad Verse City",
			"priority": high
		},
		{
			"pack": 5,
			"game": "Split the Room",
			"priority": medium
		},
		{
			"pack": 5,
			"game": "Patently Stupid",
			"priority": highest
		},
		{
			"pack": 5,
			"game": "Zeeple Dome",
			"priority": lowest
		}
	],
	[
		{
			"pack": 6,
			"game": "Trivia Murder Party 2",
			"priority": medium
		},
		{
			"pack": 6,
			"game": "Dictionarium",
			"priority": medium
		},
		{
			"pack": 6,
			"game": "Joke Boat",
			"priority": highest
		},
		{
			"pack": 6,
			"game": "Push the Button",
			"priority": low
		},
		{
			"pack": 6,
			"game": "Role Models",
			"priority": medium
		}
	],
	[
		{
			"pack": 7,
			"game": "Talking Points",
			"priority": medium
		},
		{
			"pack": 7,
			"game": "Blather Round",
			"priority": medium
		},
		{
			"pack": 7,
			"game": "Quiplash 3",
			"priority": high
		},
		{
			"pack": 7,
			"game": "Champ'd Up",
			"priority": highest
		},
		{
			"pack": 7,
			"game": "Devils in the Details",
			"priority": medium
		}
	]
]

def generateWeightedList():
	weightedList = []
	for i in range(len(jackboxGames)):
		boxName = 'Jackbox Party Pack {}'.format(i+1)
		if window.getCheckBox(boxName):
			pack = jackboxGames[i]
			weightedList = appendToList(pack, weightedList)
	return weightedList

def appendToList(pack, weightedList):
	for game in pack:
			for i in game["priority"]:
				weightedList.append(game)
	return weightedList

def formatOutput(game):
	return "Jackbox Party Pack {} - {}".format(game["pack"], game["game"])

def launchApp(pack):
	appId = next((app["id"] for app in steamIDs if app["pack"] == pack), None)
	if appId:
		cmd = f"{steamPath} -applaunch {appId}"
		subprocess.call(cmd)

def updateAlert(output):
	window.openFrame('ALERT')
	if output.split(' ')[0] == 'Failed':
		window.setBg('red')
	else:
		window.setBg('green')
	window.setLabel('alert', output)
	window.stopFrame()

def selectGame():
	try:
		global game
		weightedList = generateWeightedList()
		game = weightedList[random.randrange(len(weightedList))]
		return 'Selected: {}'.format(formatOutput(game))
	except:
		return 'Failed to select game, select at least 1 party pack.'

def launchGame():
	try:
		launchApp(game["pack"])
		return 'Launched: {}'.format(formatOutput(game))
	except:
		return 'Failed to launch game, make sure to select a game first.'

def press(button):
	if button == 'selectGame':
		window.threadCallback(selectGame, updateAlert)
	elif button == 'launchGame':
		window.threadCallback(launchGame, updateAlert)

# Build & display GUI
window = gui('Jackbox Randomizer')
window.setSize(800, 280)
window.setResizable(canResize=False)
window.setLocation('CENTER')
window.setIcon(resource_path(r'_reqs\jackbox.ico'))

# Start top frame
window.startFrame('TOP', row=0, column=0)
window.setBg('#38688c')

jackboxLogo = resource_path(r'_reqs\jackbox.gif')

window.setStretch('none')
window.addImage('jackbox_l', jackboxLogo, 0, 0)

window.setStretch('column')
window.addLabel('title', 'Jackbox Randomizer', 0, 1)
window.getLabelWidget('title').config(font=('Sans Serif', '36', 'bold'))
window.setLabelFg('title', 'white')
window.setLabelAlign('title', 'center')

window.setStretch('none')
window.addImage('jackbox_r', jackboxLogo, 0, 2)

window.stopFrame()
# End top frame

# Start mid frame
window.startFrame('MID', row=1, column=0)

## Start pack selection
window.startLabelFrame('Select Available Packs', 2, 0)
window.setSticky('nswe')
window.setStretch('column')

### Add pack checkboxes
for i in range(len(jackboxGames)):
	boxName = 'Jackbox Party Pack {}'.format(i+1)
	window.addCheckBox(boxName, i//4, i%4)
	window.setCheckBox(boxName, ticked=True, callFunction=False)

window.stopLabelFrame()
## End pack selection

window.stopFrame()
# End mid frame

# Start button frame
window.startFrame('BUTTON', row=2, column=0)
window.setStretch('column')

## Add select button
window.addNamedButton('Select a Random Game', 'selectGame', press)
window.getButtonWidget('selectGame').config(font=('Sans Serif', '16', 'bold'))
window.setButtonBg('selectGame', '#38688c')
window.setButtonFg('selectGame', 'white')

## Add launch button
window.addNamedButton('Launch Selected Party Pack', 'launchGame', press)
window.getButtonWidget('launchGame').config(font=('Sans Serif', '16', 'bold'))
window.setButtonBg('launchGame', '#38688c')
window.setButtonFg('launchGame', 'white')

window.stopFrame()
# Stop button frame

# Start alert frame
window.startFrame('ALERT', row=3, column=0)
window.setBg('red')

## Add alert label
window.addLabel('alert', 'Select your Jackbox Party Packs, then press the button!', 0, 0)
window.getLabelWidget('alert').config(font=('Sans Serif', '18', 'bold'))
window.setLabelFg('alert', 'white')

window.stopFrame()
# End alert frame

window.setFastStop(True)

window.go()