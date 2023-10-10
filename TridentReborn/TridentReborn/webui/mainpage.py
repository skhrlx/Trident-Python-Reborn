from flask import Flask, render_template, request
import configparser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data and update settings.cfg file
        bhop = 'bhop' in request.form
        rcs = 'rcs' in request.form
        rcs_aim = 'rcs_aim' in request.form
        triggerbot = 'triggerbot' in request.form
        minecraft = 'minecraft' in request.form
        aimbot = 'aimbot' in request.form
        fortnite = 'fortnite' in request.form
        hitbox = float(request.form.get('hitbox', 0.15))
        fov = float(request.form.get('fov', 0.25))
        screen_height = int(request.form.get('screen_height', 768))
        screen_width = int(request.form.get('screen_width', 1024))
        color = request.form.get('color', 'purple')

        # Update settings.cfg file
        config = configparser.ConfigParser()
        config.read('settings.cfg')

        if not config.has_section('Settings'):
            config.add_section('Settings')

        config.set('Settings', 'FOV', str(fov))
        config.set('Settings', 'COLOR', color)
        config.set('Settings', 'HITBOX', str(hitbox))

        if not config.has_section('Features'):
            config.add_section('Features')

        config.set('Features', 'BHOP', str(bhop))
        config.set('Features', 'RCS', str(rcs))
        config.set('Features', 'RCS_AIM', str(rcs_aim))
        config.set('Features', 'TRIGGERBOT', str(triggerbot))
        config.set('Features', 'MINECRAFT', str(minecraft))
        config.set('Features', 'AIMBOT', str(aimbot))
        config.set('Features', 'FORTNITE', str(fortnite))

        if not config.has_section('Screen Resolution'):
            config.add_section('Screen Resolution')

        config.set('Screen Resolution', 'S_HEIGHT', str(screen_height))
        config.set('Screen Resolution', 'S_WIDTH', str(screen_width))

        with open('settings.cfg', 'w') as config_file:
            config.write(config_file)

    # Read values from settings.cfg file
    config = configparser.ConfigParser()
    config.read('settings.cfg')

    fov = config.getfloat('Settings', 'FOV')
    color = config.get('Settings', 'COLOR')
    hitbox = config.getfloat('Settings', 'HITBOX')

    bhop = config.getboolean('Features', 'BHOP')
    rcs = config.getboolean('Features', 'RCS')
    rcs_aim = config.getboolean('Features', 'RCS_AIM')
    triggerbot = config.getboolean('Features', 'TRIGGERBOT')
    minecraft = config.getboolean('Features', 'MINECRAFT')
    aimbot = config.getboolean('Features', 'AIMBOT')
    fortnite = config.getboolean('Features', 'FORTNITE')

    screen_height = config.getint('Screen Resolution', 'S_HEIGHT')
    screen_width = config.getint('Screen Resolution', 'S_WIDTH')

    return render_template('index.html', fov=fov, color=color, hitbox=hitbox,
                           bhop=bhop, rcs=rcs, rcs_aim=rcs_aim, triggerbot=triggerbot,
                           minecraft=minecraft, aimbot=aimbot, fortnite=fortnite,
                           screen_height=screen_height, screen_width=screen_width)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')