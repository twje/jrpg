import os
import subprocess
from collections import defaultdict
from pathlib import Path


def run(command):
    os.environ['PYTHONUNBUFFERED'] = "1"

    # run command
    proc = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = [output.decode("utf-8").strip()
                      for output in proc.communicate()]

    # parse result
    if proc.returncode != 0:
        default = "Unable to execute command"
        error = next(_ for _ in (stderr, stdout, default) if _ != "")
        raise Exception(error)

    return stdout, stderr, proc.returncode


audio_converter_regsitry = defaultdict(dict)


def registor_converter(source, target):
    def add_to_registry(func):
        audio_converter_regsitry[source][target] = func
        return func
    return add_to_registry


@registor_converter(source=".mp3", target=".ogg")
def mp3_to_ogg(binary, filepath):
    command = f"{binary} -i \"{filepath}\" \"{filepath.with_suffix('.ogg')}\""
    run(command)


@registor_converter(source=".flac", target=".ogg")
def mp3_to_ogg(binary, filepath):
    command = f"{binary} -i \"{filepath}\" \"{filepath.with_suffix('.ogg')}\""
    run(command)


@registor_converter(source=".wav", target=".ogg")
def mp3_to_ogg(binary, filepath):
    command = f"{binary} -i \"{filepath}\" \"{filepath.with_suffix('.ogg')}\""
    run(command)


class AudioConverter:
    def __init__(self, ffmpeg_filepath, search_filepath):
        self.ffmpeg_filepath = Path(ffmpeg_filepath)
        self.search_filepath = Path(search_filepath)
        self.allowed_extentions = [".ogg", ".mp3", ".flac", ".wav"]
        self.target_extention = ".ogg"

    def convert_files(self):
        for filepath, extensions in self.collect_files().items():
            self.convert_file(filepath, extensions)

    # --------------
    # Helper Methods
    # --------------
    def convert_file(self, filepath, extensions):
        if self.target_extention in extensions:
            return

        for extension in extensions:
            converter = audio_converter_regsitry.get(
                extension).get(self.target_extention)
            if converter is not None:
                converter(self.ffmpeg_filepath, Path(filepath + extension))
                return

    def collect_files(self):
        result = defaultdict(list)
        self.collect_files_recursive(result, self.search_filepath)
        return result

    def collect_files_recursive(self, result, directory):
        for p in directory.iterdir():
            if p.is_dir():
                self.collect_files_recursive(result, p)
            if p.is_file():
                if p.suffix in self.allowed_extentions:
                    result[str(p.with_suffix(''))].append(p.suffix)
