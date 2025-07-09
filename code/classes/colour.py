class Colour:
    def __init__(self, colour_details: list[str]) -> None:
        self.colour_id: str = colour_details[0]
        self.colour_name: str = colour_details[1]
        self.colour_code: str = colour_details[2]
        self.protected: bool = colour_details[3].lower() == "true"

        self.luminance: float
        self.rgb_values: list[float]
        self.calculate_relative_luminance()
         
    def calculate_rgb_values(self) -> None:
        colour_code = self.colour_code.replace("#", "")
        r_value = colour_code[0] + colour_code[1]
        g_value = colour_code[2] + colour_code[3]
        b_value = colour_code[4] + colour_code[5]

        r_value = int(r_value, 16) / 255
        g_value = int(g_value, 16) / 255
        b_value = int(b_value, 16) / 255

        self.rgb_values = [r_value, g_value, b_value]

    def calculate_relative_luminance(self) -> None:
        self.calculate_rgb_values()

        r_value = self.calculate_luminance(self.rgb_values[0])
        g_value = self.calculate_luminance(self.rgb_values[1])
        b_value = self.calculate_luminance(self.rgb_values[2])

        r_value = r_value * 0.2126
        g_value = g_value * 0.7152
        b_value = b_value * 0.0722

        self.luminance = r_value + g_value + b_value + 0.05

    def calculate_luminance(self, c_value) -> float:
        if c_value <= 0.03928:
            c_value = c_value / 12.92
        else:
            c_value = ((c_value + 0.055) / 1.055) ** 2.4

        return c_value
