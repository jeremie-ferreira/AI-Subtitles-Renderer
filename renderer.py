import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from dotmap import DotMap
import styles

# Calculate a point on a cubic Bezier curve
def bezier(t, points):
    return (1 - t)**3 * np.array(points[0]) + 3 * (1 - t)**2 * t * np.array(points[1]) + 3 * (1 - t) * t**2 * np.array(points[2]) + t**3 * np.array(points[3])

# Pop-up animation effect using a Bezier curve
def pop_effect(time_elapsed, duration):
    points = [(0, .75), (.4, 1.1), (.6, 1), (1, 1)]
    return 1 if time_elapsed > duration else bezier(time_elapsed / duration, points)[1]

class Renderer:
    def __init__(self, style_name, position):
        self.__subs_position = position
        self.__style = styles.get_style(style_name)
    
    def draw_subtitle(self, frame, sentence, words, current_time):
        # Convert OpenCV image to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
        overlay = Image.new("RGBA", pil_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        if self.__style.caps:
            sentence = sentence.upper()

        # Calculate the total size of the sentence
        bbox = draw.textbbox((0, 0), sentence + " ", font=self.__style.font)
        text_width = bbox[2] - bbox[0]
        text_height = self.__style.font_height
        x, y = self.__subs_position
        text_x = x - text_width // 2
        text_y = y - text_height // 2

        # Identify the current word and its position
        word_positions = self.__compute_word_positions(current_time, words)

        # draw background rectangle
        if self.__style.bg_rect:
            self.__draw_bg_rectangle(draw, text_x, text_y, bbox)

        # Draw each word with appropriate color and effects
        current_x = text_x
        for word, is_active, start, end in word_positions:
            
            if self.__style.active_bg_rect and is_active:
                self.__draw_active_bg_rectangle(current_time, draw, text_y, current_x, word, start)

            self.__draw_word(draw, current_x, text_y, word, is_active)

            # Prepare next word position
            word_bbox = draw.textbbox((0, 0), word, font=self.__style.font)
            word_width = word_bbox[2] - word_bbox[0]
            current_x += word_width
        combined = Image.alpha_composite(pil_image, overlay)

        # Convert PIL Image back to OpenCV
        return cv2.cvtColor(np.array(combined), cv2.COLOR_RGB2BGR)

    def __draw_word(self, draw, x, y, word, is_active):
        color = self.__style.active_color if is_active else self.__style.color
        if self.__style.text_shadow:
            draw.text((x + self.__style.text_shadow.x, y + self.__style.text_shadow.y), word, font=self.__style.font, fill="black", stroke_width=self.__style.stroke_width, stroke_fill="black")
        draw.text((x, y), word, font=self.__style.font, fill=color, stroke_width=self.__style.stroke_width, stroke_fill=self.__style.stroke_color)
    
    def __draw_bg_rectangle(self, draw, text_x, text_y, bbox):
        rect_style = self.__style.bg_rect
        rect_width = bbox[2] - bbox[0] + 2 * rect_style.padding
        rect_height = self.__style.font_height + 2 * rect_style.padding
        rect_x = text_x + bbox[0] - rect_style.padding
        rect_y = text_y - rect_style.padding
        draw.rounded_rectangle([rect_x, rect_y, rect_x + rect_width, rect_y + rect_height], radius=rect_style.radius, fill=rect_style.fill)

    def __draw_active_bg_rectangle(self, current_time, draw, text_y, current_x, word, start):
        t = current_time - start
        scale = pop_effect(time_elapsed=t, duration=.2)
        word_bbox = draw.textbbox((current_x, text_y), word + " ", font=self.__style.font)
        rect_style = self.__style.active_bg_rect

        rect_width = (word_bbox[2] - word_bbox[0])
        rect_height = self.__style.font_height + 2 * rect_style.padding
        rect_x = word_bbox[0]
        rect_y = text_y - rect_style.padding

        # Apply scaling animation effect
        if rect_style.animated:
            center_x = rect_x + rect_width // 2
            center_y = rect_y + rect_height // 2
            rect = [center_x - rect_width * scale // 2,
                            center_y - rect_height * scale // 2,
                            center_x + rect_width * scale // 2,
                            center_y + rect_height * scale // 2]
                    
            draw.rounded_rectangle(rect, radius=rect_style.radius, fill=rect_style.fill)
        else:
            draw.rounded_rectangle([rect_x, rect_y, rect_x + rect_width, rect_y + rect_height], radius=rect_style.radius, fill=rect_style.fill)

    def __compute_word_positions(self, current_time, words):
        word_positions = []
        for word in words:
            word_start, word_end = word["start"], word["end"]
            word_text = word["word"]
            if self.__style.caps:
                word_text = word_text.upper()

            if word_start <= current_time <= word_end:
                word_positions.append((word_text, True, word_start, word_end))
            else:
                word_positions.append((word_text, False, word_start, word_end))
        return word_positions