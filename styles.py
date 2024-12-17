from PIL import ImageFont
from dotmap import DotMap
import os

FONT_ROBOTO = "Roboto-Black.ttf"

def get_style(style_name):
    if style_name == 'spectre':
        return get_spectre_style()
    elif style_name == 'vibe':
        return get_vibe_style()
    elif style_name == 'spark':
        return get_spark_style()
    elif style_name == 'cozy':
        return get_cozy_style()
    elif style_name == 'pure':
        return get_pure_style()

def get_font_properties(font_name, font_size):
    font_path = f"{os.environ['LOCALAPPDATA']}/Microsoft/Windows/Fonts/{font_name}"
    font = ImageFont.truetype(font_path, font_size)
    ascent, descent = font.getmetrics()
    return DotMap({"font": font, "font_height": ascent + descent})

def get_spectre_style():
    font_size = 80
    font_props = get_font_properties(FONT_ROBOTO, font_size)

    return DotMap({
        "caps": False,
        "font": font_props.font,
        "color": "white",
        "font_height": font_props.font_height,
        "stroke_color": "black",
        "stroke_width": 4,
        "active_color": "white",
        "active_animation": False,
        "active_bg_rect": DotMap({
            "padding": 10,
            "radius": 20,
            "fill": (100, 100, 255, 220),
            "animated": True
        })
    })

def get_vibe_style():
    font_size = 80
    font_props = get_font_properties(FONT_ROBOTO, font_size)

    return DotMap({
        "caps": True,
        "font": font_props.font,
        "color": "white",
        "font_height": font_props.font_height,
        "stroke_color": "black",
        "stroke_width": 6,
        "active_color": "yellow",
        "active_animation": False,
        "active_bg_rect": False,
        "text_shadow": DotMap({"x": 10, "y": 10})
    })

def get_spark_style():
    font_size = 80
    font_props = get_font_properties("KOMIKAX.ttf", font_size)

    return DotMap({
        "caps": True,
        "font": font_props.font,
        "color": "white",
        "font_height": font_props.font_height,
        "stroke_color": "black",
        "stroke_width": 6,
        "active_color": (99, 117, 255),
        "active_animation": False,
        "active_bg_rect": False,
        "text_shadow": DotMap({"x": 10, "y": 10})
    })

def get_cozy_style():
    font_size = 80
    font_props = get_font_properties(FONT_ROBOTO, font_size)

    return DotMap({
        "caps": True,
        "font": font_props.font,
        "color": "white",
        "font_height": font_props.font_height,
        "stroke_color": "black",
        "stroke_width": 6,
        "active_color": (255, 29, 141),
        "active_animation": False,
        "active_bg_rect": False,
        "text_shadow": False,
        "bg_rect": DotMap({
            "padding": 10,
            "radius": 20,
            "fill": (0, 0, 0, 255),
            "animated": False
        }) 
    })

def get_pure_style():
    font_size = 80
    font_props = get_font_properties(FONT_ROBOTO, font_size)

    return DotMap({
        "caps": True,
        "font": font_props.font,
        "color": "black",
        "font_height": font_props.font_height,
        "stroke_color": "black",
        "stroke_width": 0,
        "active_color": (99, 117, 255),
        "active_animation": False,
        "active_bg_rect": False,
        "text_shadow": False,
        "bg_rect": DotMap({
            "padding": 10,
            "radius": 20,
            "fill": "white",
            "animated": False
        }) 
    })