class File():
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)

    def get_size(self):
        return self.size


class Folder():
    def __init__(self, parentFolder, name):
        self.parentFolder = parentFolder
        self.name = name
        self.contents = []
        self.childrenFolders = []

    def get_size(self):
        return sum([currFile.get_size() for currFile in self.contents]) + sum([currFolder.get_size() for currFolder in self.childrenFolders])

    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parentFolder

    def get_child_folder(self, name):
        for currFolder in self.childrenFolders:
            if currFolder.get_name() == name:
                return currFolder
        else:
            raise Exception(f"Folder {self.name} does not have a child folder called {name}")

    def add_file(self, file):
        self.contents.append(file)

    def add_folder(self, folder):
        self.childrenFolders.append(folder)

#Reading the puzzle input 
with open("./input_07.txt", "r") as file:
    terminal_hist = file.read()

# Getting all the commands 
terminal_hist = terminal_hist.split('$ ')
terminal_hist = [temp.splitlines() for temp in terminal_hist]

# Initializing the directory tree
allFolders = []
rootFolder = Folder(None, "/")
activeFolder = rootFolder

# Removing the first two commands  since they are already processed  
terminal_hist.pop(0)
terminal_hist.pop(0)

for terminal_entry in terminal_hist:
    command = terminal_entry[0]
    command_output = terminal_entry[1:]

    command_exec = command.split(" ")[0]
    command_args = command.split(" ")[1:]

    if command_exec == "ls":
        for output_line in command_output:
            output_line_content = output_line.split(" ")
            if output_line_content[0] == "dir":
                newFolder = Folder(activeFolder, output_line_content[1])
                allFolders.append(newFolder)
                activeFolder.add_folder(newFolder)
            elif output_line_content[0].isdigit():
                newFile = File(output_line_content[1], output_line_content[0])
                activeFolder.add_file(newFile)
            else:
                raise Exception(f"ls output gave something unexpected which was {output_line_content}")

    elif command_exec == "cd":
        assert len(command_args) == 1, f"cd command should have 1 argument only but here it is {command}"
        
        cd_arg = command_args[0]
        if cd_arg == "..":
            activeFolder = activeFolder.get_parent()
        else:
            activeFolder = activeFolder.get_child_folder(cd_arg)

    else:
        raise Exception(f"This command is not recognized: {command_exec}")


# Part 2
totalSpace = 70000000
requiredSpace = 30000000
usedSpace = rootFolder.get_size()
emptySpace = totalSpace - usedSpace

assert emptySpace < requiredSpace, f"You already have enough space since {emptySpace=} and {requiredSpace=}"

allSizes = [currFolder.get_size() for currFolder in allFolders]

deletionSpace = requiredSpace - emptySpace
finalResult = min(currSize for currSize in allSizes if currSize > deletionSpace)

print(f"Final result for part 2 is {finalResult}")

