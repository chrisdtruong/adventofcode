from __future__ import annotations
from typing import Union, List
from input import INPUT_PART_ONE, INPUT_PART_TWO


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.parent_directory: Directory = None
        self.content = []

    def add_item(self, item):
        self.content.append(item)

    def set_parent(self, directory):
        self.parent_directory = directory

    def __repr__(self):
        return f"Directory[{self.name}]"

class File:
    def __init__(self, name: str, size: int, location: Directory):
        self.name = name
        self.size = size
        self.location = location


class FileSystem:
    def __init__(self, starting_directory: Directory):
        self.current_location: Directory = starting_directory

    def cd(self, move_target: str):
        if move_target == '..':
            # move up a directory
            if not self.current_location.parent_directory:
                raise ValueError("No Parent to move to... :(")
            self.current_location = self.current_location.parent_directory
        elif move_target == '/':
            # move to the top directory
            while self.current_location.parent_directory is not None:
                self.current_location = self.current_location.parent_directory
        else:
            self.current_location = self.get_local_directory(move_target)
        return

    def mkdir(self, directory_name: str):
        directory = Directory(name=directory_name)
        directory.set_parent(directory=self.current_location)
        self.current_location.add_item(directory)

    def touch(self, file_name: str, file_size: int):
        file = File(name=file_name, size=file_size, location=self.current_location)
        self.current_location.add_item(file)

    def get_local_directory(self, name: str) -> Directory:
        for item in self.current_location.content:
            if isinstance(item, Directory) and item.name == name:
                return item

        raise FileNotFoundError("oopsies")

    def calculate_total_size(self, directory: Union[Directory, None] = None) -> int:
        size: str = 0
        target_directory = directory if directory else self.current_location

        for item in target_directory.content:
            if isinstance(item, Directory):
                size += self.calculate_total_size(directory=item)
            else:
                size += item.size

        return size

    def gather_all_directories(self, current_directory: Union[Directory, None] = None) -> List[Directory]:
        directories = [current_directory]
        for item in current_directory.content:
            if isinstance(item, Directory):
                directories += self.gather_all_directories(current_directory=item)
        
        return directories


def terminal_output_ingester(filesystem: FileSystem, terminal_output: List[str]):
    for line in terminal_output:
        if line.startswith("$"):
            command_parts = line.split(" ")
            command = command_parts[1]
            if command == "cd":
                target = command_parts[2]
                filesystem.cd(move_target=target)
            if command == "ls":
                continue
        else:
            if line.startswith("dir"):
                _, dir_name = line.split(" ")
                filesystem.mkdir(directory_name=dir_name)
            else:
                size, file_name = line.split(" ")
                filesystem.touch(file_name=file_name, file_size=int(size))

    return filesystem


def collect_directories_sizes_within_threshold(filesystem: FileSystem, threshold: int, greater: bool) -> List[Directory]:
    inscope_directories = []

    for directory in filesystem.gather_all_directories(filesystem.current_location):
        if greater:
            if filesystem.calculate_total_size(directory=directory) >= threshold:
                inscope_directories.append(directory)
        else:
            if filesystem.calculate_total_size(directory=directory) < threshold:
                inscope_directories.append(directory)

    return inscope_directories


def solve_part_one():
    size_threshold = 100000

    root_directory = Directory(name="root")
    filesystem = FileSystem(starting_directory=root_directory)
    filesystem = terminal_output_ingester(filesystem=filesystem, terminal_output=INPUT_PART_ONE)
    filesystem.cd(move_target="/")

    # Part One
    inscope_directories = collect_directories_sizes_within_threshold(filesystem, size_threshold, False)
    total_size = 0
    for directory in inscope_directories:
        total_size += filesystem.calculate_total_size(directory=directory)
    print(f"Part 1 [Total Size]:  {total_size}")


def solve_part_two():
    total_disk_size_available = 70000000
    minimum_required_disk_space = 30000000

    root_directory = Directory(name="root")
    filesystem = FileSystem(starting_directory=root_directory)
    filesystem = terminal_output_ingester(filesystem=filesystem, terminal_output=INPUT_PART_TWO)
    filesystem.cd(move_target="/")

    current_used_disk_space = filesystem.calculate_total_size()
    current_disk_size_available = total_disk_size_available - current_used_disk_space
    space_needed_to_be_deleted = minimum_required_disk_space - current_disk_size_available
    inscope_directories = collect_directories_sizes_within_threshold(filesystem, space_needed_to_be_deleted, True)
    best_fit_directory_size = None
    best_fit_directory_excess_deleted_space = None
    for directory in inscope_directories:
        directory_size = filesystem.calculate_total_size(directory=directory)
        excess_deleted_space = directory_size - minimum_required_disk_space
        if best_fit_directory_size is None or excess_deleted_space < best_fit_directory_excess_deleted_space:
            best_fit_directory_size = directory_size
            best_fit_directory_excess_deleted_space = excess_deleted_space

    print(f"Part 2 [Best Fit Size]:     {best_fit_directory_size}")


def main():
    solve_part_one()
    solve_part_two()
    # Part Two
    


if __name__ == "__main__":
    main()