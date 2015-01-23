import sfml as sf


# fonts

font_8bit = sf.Font.from_file("content/fonts/8bit.ttf")
font_farmville = sf.Font.from_file("content/fonts/farmville.ttf")

# images

textures = {}
textures["koa"] = sf.Texture.from_file("content/textures/koa.png")
textures["iliahi"] = sf.Texture.from_file("content/textures/pine.png")
textures["button"] = sf.Texture.from_file("content/gui/button.png")
textures["textbox"] = sf.Texture.from_file("content/gui/textbox.png")
