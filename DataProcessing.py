import sys
import numpy as np
import os
from graphs.GraphIO import *

class DataPreprocessing:
    def __init__(self):
        pass

    def getExperimentsFromCfgFile(self, cfg):
        res = np.matrix([], [])
        ls = []
        try:
            br = open(cfg, "r")
            for line in br:
                if line.startsWith("//") or line.startsWith("#") or len(line) == 0:
                    continue
                ls.add(line.split())
            res = np.matrix([np.size(ls)], [])
            idx = 0
            for l in ls:
                res[++idx] = l
            br.close()
        except ValueError:
            print("error")
            res = [0][1]
        return res

    def executeCommand(self, command, inFile, outDir, outFile):
        if command[0] == "Preprocessing":
            folder = os.path.join("Users\Dylan\Documents\Independent Study\independent_study", outDir)
            if not os.path.exists(folder):
                os.mkdir(folder)
            if command[1] == "convertMatrixToEdgeList":
                print("\n\t[Operation]: cover matrix to edge list")
                m = convertAdjacentMatrixToEdgeList(GraphIO.getAdjacencyMatrixFromFile(inFile))
                outFile = outDir + "/" + inFile[inFile.rindex('1') + 1:inFile.rindex("_adj")] + "EdgeList.txt"
                outputMatrix(outFile, m)
            elif command[1] == "ID2Integer":
                isEgo = False
                if len(command) > 2 and command[2] == "ego":
                    isEgo = True
                convertStrIDToIntInFile(inFile, isEgo)

    def main(self, args):
        if len(args) < 2:
            print("need two configuration files as input:\n\t1. configfile for data file paths\n\t2. experiments to execute")
            return

        dataFile = args[0]
        expCfg = args[1]
        files = getDataFileNamesFromFileList(dataFileCfg)
        intMtr = np.matrix([], [])
        commands = getExperimentsFromCfgFile(expCfg)

        if len(commands[0]) < 2 or len(commands[1]) < 2 or commands[0][0] != "expName" or commands[1][0] != "outDir":
            print("experiment configuration file format error:",
                  "\n\tThe first line should be in the format: expName experiment_name",
                  "\n\tThe second line should be in the format: outDir output_folder_for_result")
            return

        expName = commands[0][1]
        outDir = commands[1][1]

        for i in range(len(files)):
            print("Process file[", i, "]: ", files[i])
            for j in range(2, len(commands)):
                executeCommand(commands[j], files[i], outDir + "/" + expName, None)

main_var = DataPreprocessing()
if __name__ == "__main__":
    main_var.main(sys.argv[1:])
