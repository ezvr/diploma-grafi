def ingestTemporalLine(filename):
    # This function returns a cleaned up array from the FLIR temporal csv export
    measurements = []
    with open(filename) as file:
        for index, line in enumerate(file):
            # First we prepare the array of items
            for index, line in enumerate(file):
                if index == 0:
                    # We remove the header row
                    continue
                # Split at comma
                line = line.split(",")
                # Transform temperature to float
                line[2] = float(line[2])
                line[3] = float(line[3])
                measurements.append(line[2:4])
    return measurements

def ingestGradLine(filename):
    # This function returns a cleaned up array from the FLIR profile csv export
    measurements = []
    with open(filename) as file:
        for index, line in enumerate(file):
            # First we prepare the array of items
            for index, line in enumerate(file):
                if index == 0:
                    # We remove the header row
                    continue
                # Split at comma
                line = line.split(",")
                # Transform temperature to float
                line[0] = float(line[0])
                line[1] = float(line[1])
                measurements.append(line[0:2])
    return measurements


def returnDiplRoot():
    import sys
    return sys.path[0]

def testPyPlot(data):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    x = list(map(lambda x: x[0], data))
    y = list(map(lambda x: x[1], data))
    ax.plot(x, y)
    plt.savefig('foo.png')

def crawlFolders(root):
    import os
    flatFolderList = []

    # get root subdirs
    rootSubDirs = [f for f in os.scandir(root) if f.is_dir()]

    # crawl all root subdirs
    for dir in rootSubDirs:
        flatFolderList += [f for f in os.scandir(dir) if f.is_dir()]

    # return a flat list of all the directories
    return flatFolderList

def processDir(dir, dataMap):
    import os
    csvFiles = []
    # This function will scan the directory, and find all relevant csv files

    # List all the CSV files to the csvFiles list
    with os.scandir(dir) as currentDir:
        for entry in currentDir:
            ext = os.path.splitext(entry)[-1].lower()
            if ext == ".csv":
                csvFiles.append(entry)

    # For each CSV file, determine the type, and process it
    markerlist = [f for f in csvFiles if f.name[0] == 'm']
    profilelist = [f for f in csvFiles if f.name[0] == 'p']
    ogrevanje = [f for f in csvFiles if f.name == 'ogrevanje.csv']

    # Create new output dir
    pyroot = returnDiplRoot()
    # Get the relative path, from meritve root to the current meritev dir
    dirrelpath = os.path.relpath(dir, dataMap.dataMap['meritveRoot'])
    # Prepare the output directory
    outputpath = os.path.join(pyroot, 'output', dirrelpath)
    os.makedirs(outputpath, exist_ok=True)

    # Create the plots
    makeMarkerPlot(markerlist, outputpath)
    makeGradTimePlot(profilelist, outputpath)
    makeHeatingTimePlot(ogrevanje, outputpath)

def makeMarkerPlot(data,dir):
    import matplotlib.pyplot as plt
    import os
    # This function will create a plot with stacked temporal lines

    # If there is no data, stop the work
    if len(data) == 0:
        print('\033[93m No data for Marker plot in dir: \033[0m' + dir)
        return
    # Process the data via an ingestion function
    print('Making Marker Plot in dir: ' + dir)
    processeddata = [ingestTemporalLine(f) for f in data]

    # Create a plot
    fig, ax = plt.subplots()

    # Add each of the csv datasets to the plot
    for dataset in processeddata:
        x = list(map(lambda x: x[0], dataset))
        y = list(map(lambda x: x[1], dataset))
        ax.plot(x, y)

    # Save the plot
    outputpath = os.path.join(dir, 'markerplot.png')
    plt.savefig(outputpath)
    plt.close(fig)

def makeGradTimePlot(data,dir):
    import matplotlib.pyplot as plt
    import os
    # This function will create a plot with stacked profile lines

    # If there is no data, stop the work
    if len(data) == 0:
        print('\033[93mNo data for Grad Time plot in dir: \033[0m' + dir)
        return

    # Process the data via an ingestion function
    print('Making Grad Time Plot in dir: ' + dir)
    processeddata = [ingestGradLine(f) for f in data]

    # Create a plot
    fig, ax = plt.subplots()

    # Add each of the csv datasets to the plot
    for dataset in processeddata:
        x = list(map(lambda x: x[0], dataset))
        y = list(map(lambda x: x[1], dataset))
        ax.plot(x, y)

    # Save the plot
    outputpath = os.path.join(dir, 'gradplot.png')
    plt.savefig(outputpath)
    plt.close(fig)

def makeHeatingTimePlot(data,dir):
    import matplotlib.pyplot as plt
    import os
    # This function will create a plot with stacked profile lines

    # If there is no data, stop the work
    if len(data) == 0:
        print('\033[93mNo data for Heating Time plot in dir: \033[0m' + dir)
        return

    # Process the data via an ingestion function
    print('Making Heating Time Plot in dir: ' + dir)
    processeddata = [ingestTemporalLine(f) for f in data]

    # Create a plot
    fig, ax = plt.subplots()

    # Add each of the csv datasets to the plot
    for dataset in processeddata:
        x = list(map(lambda x: x[0], dataset))
        y = list(map(lambda x: x[1], dataset))
        ax.plot(x, y)

    # Save the plot
    outputpath = os.path.join(dir, 'heatingplot.png')
    plt.savefig(outputpath)
    plt.close(fig)

if __name__ == '__main__':
    import dataMap
    #filename = returnDiplRoot() + '\\meritve\\tc\\tc3,0.2w\\ogrevanje.csv'
    #data = ingestTemporalLine(filename)
    #testPyPlot(data)

    for dir in crawlFolders(dataMap.dataMap['meritveRoot']):
        processDir(dir, dataMap)
