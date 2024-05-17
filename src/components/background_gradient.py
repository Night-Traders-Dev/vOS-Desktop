import random
from time import time
from math import sin, pi, cos

from textual import on, events
from textual.app import ComposeResult, RenderResult
from textual.screen import Screen
from textual.containers import Container
from textual.color import Gradient
from textual.renderables.gradient import LinearGradient
from textual.widgets import Static

def lerp(a, b, t):
    return a + (b - a) * t

def cubic_hermite(a, b, t):
    return a + (b - a) * smoothstep(t)

def bezier(p0, p1, p2, p3, t):
    return (
        (1 - t) ** 3 * p0 +
        3 * (1 - t) ** 2 * t * p1 +
        3 * (1 - t) * t ** 2 * p2 +
        t ** 3 * p3
    )

def cubic_bezier(a, b, c, d, t):
    return (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d

def catmull_rom(p0, p1, p2, p3, t):
    return 0.5 * (
        (2 * p1) +
        (-p0 + p2) * t +
        (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 +
        (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3
    )

def smoothstep(t):
    return t * t * (3 - 2 * t)

def cos_interpolate(t):
    return (1 - cos(t * pi)) / 2

def interpolate_color(color1, color2, factor):
    # Convert hex colors to RGB tuples
    c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))

    # Choose interpolation function based on the factor
    if factor < 0.125:
        smoothed_factor = smoothstep(factor * 8)
        r = int(c1[0] * (1 - smoothed_factor) + c2[0] * smoothed_factor)
        g = int(c1[1] * (1 - smoothed_factor) + c2[1] * smoothed_factor)
        b = int(c1[2] * (1 - smoothed_factor) + c2[2] * smoothed_factor)
    elif factor < 0.25:
        r = lerp(c1[0], c2[0], factor * 8 - 1)
        g = lerp(c1[1], c2[1], factor * 8 - 1)
        b = lerp(c1[2], c2[2], factor * 8 - 1)
    elif factor < 0.375:
        r = cubic_hermite(c1[0], c2[0], factor * 8 - 2)
        g = cubic_hermite(c1[1], c2[1], factor * 8 - 2)
        b = cubic_hermite(c1[2], c2[2], factor * 8 - 2)
    elif factor < 0.5:
        r = cubic_bezier(c1[0], c2[0], c1[0], c2[0], factor * 8 - 3)
        g = cubic_bezier(c1[1], c2[1], c1[1], c2[1], factor * 8 - 3)
        b = cubic_bezier(c1[2], c2[2], c1[2], c2[2], factor * 8 - 3)
    elif factor < 0.625:
        r = catmull_rom(c1[0], c2[0], c1[0], c2[0], factor * 8 - 4)
        g = catmull_rom(c1[1], c2[1], c1[1], c2[1], factor * 8 - 4)
        b = catmull_rom(c1[2], c2[2], c1[2], c2[2], factor * 8 - 4)
    elif factor < 0.75:
        r = cos_interpolate(c1[0], c2[0], factor * 8 - 5)
        g = cos_interpolate(c1[1], c2[1], factor * 8 - 5)
        b = cos_interpolate(c1[2], c2[2], factor * 8 - 5)
    elif factor < 0.875:
        r = bezier(c1[0], c2[0], c1[0], c2[0], factor * 8 - 6)
        g = bezier(c1[1], c2[1], c1[1], c2[1], factor * 8 - 6)
        b = bezier(c1[2], c2[2], c1[2], c2[2], factor * 8 - 6)
    else:
        r = smoothstep(c1[0], c2[0], factor * 8 - 7)
        g = smoothstep(c1[1], c2[1], factor * 8 - 7)
        b = smoothstep(c1[2], c2[2], factor * 8 - 7)

    # Convert back to hex color
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_random_colors(n):
    return [random_color() for _ in range(n)]


class Splash(Container):

    # Initialize colors in the class definition
    colors = generate_random_colors(2)

    def on_mount(self) -> None:
        self.auto_refresh = 10  # Refresh rate
        self.last_update_time = time()
        self.gradient_stops_cache = []  # Cache for gradient stops
        self.cache_size = 2048  # Size of the cache

    def compute_gradient_stops(self):
        gradient_stops = []
        for i, color in enumerate(self.colors):
            stop = (i / (len(self.colors) - 1), color)
            gradient_stops.append(stop)
        return gradient_stops

    def fill_gradient_stops_cache(self):
        # Clear the cache
        self.gradient_stops_cache = []

        # Compute and store gradient stops for each iteration
        for _ in range(self.cache_size):
            self.gradient_stops_cache.append(self.compute_gradient_stops())

    def get_gradient_stops(self):
        # If cache is empty, fill it
        if not self.gradient_stops_cache:
            self.fill_gradient_stops_cache()

        # Get and remove the first iteration from the cache
        stops = self.gradient_stops_cache.pop(0)

        # Compute and append new stops to the cache
        self.gradient_stops_cache.append(self.compute_gradient_stops())

        return stops

    def render(self) -> RenderResult:
        current_time = time()
        elapsed_time = current_time - self.last_update_time

        # If one second has passed, rotate the colors and refill cache
        if elapsed_time >= 1:
            i = random.randint(0, len(self.colors) - 1)
            self.colors.pop(i)
            self.colors.append(random_color())
            self.fill_gradient_stops_cache()  # Refill cache
            self.last_update_time = current_time
            elapsed_time = 0

        # Calculate the interpolation factor
        factor = (elapsed_time % 1) / 1

        # Get gradient stops from cache
        stops = self.get_gradient_stops()

        # Calculate rotation angle for the gradient
        amplitude = 0.0005  # Adjust amplitude between 0 and 1
        frequency = 0.0002  # Adjust frequency based on desired speed
        rotation = sin(current_time * frequency) * pi * amplitude


        return LinearGradient(rotation, stops)


    @on(events.MouseEvent)
    def return_to_desktop(self):
        self.app.push_screen("DesktopBase")

class ScreenSaver(Screen):

    def compose(self) -> ComposeResult:
        yield Splash()


