from PIL import Image, ImageDraw

def create_gradient(width, height, start_color, end_color):
    base = Image.new('RGBA', (width, height), start_color)
    top = Image.new('RGBA', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (x / width)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Configuration
LOGO_PATH = 'xibalba-solutions-site/XibalbaSolutionsLogo.png'
BANNER_SIZE = (1584, 396)
PROFILE_SIZE = (400, 400)
COLOR_START = hex_to_rgb('#0f172a') # Slate 900
COLOR_END = hex_to_rgb('#334155')   # Slate 700

# Load Logo
logo = Image.open(LOGO_PATH)

# --- Create Banner ---
banner = create_gradient(BANNER_SIZE[0], BANNER_SIZE[1], COLOR_START, COLOR_END)

# Resize logo for banner (fit within height with padding)
banner_logo_height = int(BANNER_SIZE[1] * 0.6) # 60% of banner height
aspect_ratio = logo.width / logo.height
banner_logo_width = int(banner_logo_height * aspect_ratio)
logo_resized_banner = logo.resize((banner_logo_width, banner_logo_height), Image.Resampling.LANCZOS)

# Center logo on banner
banner_x = (BANNER_SIZE[0] - banner_logo_width) // 2
banner_y = (BANNER_SIZE[1] - banner_logo_height) // 2
banner.paste(logo_resized_banner, (banner_x, banner_y), logo_resized_banner)

banner.save('linkedin_banner.png')
print("Created linkedin_banner.png")

# --- Create Profile Photo ---
profile = create_gradient(PROFILE_SIZE[0], PROFILE_SIZE[1], COLOR_START, COLOR_END)

# Resize logo for profile (fit within width with padding)
profile_logo_width = int(PROFILE_SIZE[0] * 0.8) # 80% of profile width
profile_logo_height = int(profile_logo_width / aspect_ratio)
logo_resized_profile = logo.resize((profile_logo_width, profile_logo_height), Image.Resampling.LANCZOS)

# Center logo on profile
profile_x = (PROFILE_SIZE[0] - profile_logo_width) // 2
profile_y = (PROFILE_SIZE[1] - profile_logo_height) // 2
profile.paste(logo_resized_profile, (profile_x, profile_y), logo_resized_profile)

profile.save('linkedin_profile.png')
print("Created linkedin_profile.png")
