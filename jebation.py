from typing import List
from PIL import Image, ImageSequence
from math import cos, radians
from traceback import print_exc

import sys
import numpy as np


def rainbow_angle(number: float) -> float:
    """Sinusoidal function."""
    return abs(cos(radians(number)))


def rainbow_list(image: Image.Image) -> List[Image.Image]:
    """Make List of rainbow image."""
    frames = ImageSequence.all_frames(image)
    if len(frames) > 1:
        np_frames = []
        for frame in frames:
            np_frame = np.array(frame.convert("RGBA"))
            np_frames.append((np_frame, frame.info))
    else:
        np_image = np.array(image.convert("RGBA"))
        np_frames = [(np.copy(np_image), image.info) for _ in range(30)]

    colored_frames = []
    for i, (np_frame, info) in enumerate(np_frames):
        change_color = i * 180 / len(np_frames)
        np_frame[..., 0] = np_frame[..., 0] * rainbow_angle(change_color + 45)
        np_frame[..., 1] = np_frame[..., 1] * rainbow_angle(change_color + 90)
        np_frame[..., 2] = np_frame[..., 2] * rainbow_angle(change_color)
        np_frame[..., 3] = (np_frame[..., 3] > 130) * 255
        img = Image.fromarray(np_frame)
        img.info = info
        colored_frames.append(img)
    return colored_frames


def rainbow(path: str, dest: str) -> None:
    """Make rainbow image of image at `path`."""
    image = Image.open(path)
    frames = rainbow_list(image)
    frames[0].save(
        dest,
        background=frames[0].info.get("background", 255),
        fromat='GIF',
        version="GIF89a",
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=[frame.info.get("duration", 40) for frame in frames],
        loop=image.info.get("loop", 0),
        transparency=255,
        palette=Image.WEB,
        disposal=[frame.info.get("disposal", 1) for frame in frames],
        comment="Made by Dashstrom"
    )


if __name__ == "__main__":
    path_number = len(sys.argv) - 1
    for progress, path in enumerate(sys.argv[1:], start=1):
        print(f"\rConvert {path} ({progress}/{path_number})")
        try:
            rainbow(path, path + ".rainbow.gif")
        except Exception:
            print_exc()
