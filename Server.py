from flask import Flask, request, jsonify, send_file
from AppManager import AppManager
from AudioDeviceManager import AudioDeviceManager

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app_manager = AppManager()
        self.audio_device_manager = AudioDeviceManager()

        # Mettre à jour les applications au démarrage
        self.app_manager.update_applications()

        # Définition des routes API
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/applications', methods=['GET'])
        def get_applications():
            self.app_manager.update_applications()
            applications = self.app_manager.get_applications()
            return jsonify({'applications': applications})

        @self.app.route('/applications/<process_name>/volume', methods=['GET', 'POST'])
        def manage_volume(process_name):
            controller = self.app_manager.get_controller(process_name)
            if not controller:
                return jsonify({'error': 'Application not found'}), 404

            if request.method == 'GET':
                volume = controller.get_process_volume()
                if volume is not None:
                    return jsonify({'volume': volume * 100})
                else:
                    return jsonify({'error': 'Unable to get volume'}), 500

            elif request.method == 'POST':
                data = request.get_json()
                volume_percentage = data.get('volume')
                if volume_percentage is not None:
                    controller.set_volume(volume_percentage)
                    return jsonify({'message': 'Volume set', 'volume': volume_percentage})
                else:
                    return jsonify({'error': 'Invalid volume data'}), 400

        @self.app.route('/applications/<process_name>/mute', methods=['POST'])
        def mute_application(process_name):
            controller = self.app_manager.get_controller(process_name)
            if not controller:
                return jsonify({'error': 'Application not found'}), 404

            data = request.get_json()
            action = data.get('action')
            if action == 'mute':
                controller.mute()
                return jsonify({'message': f'{process_name} muted'})
            elif action == 'unmute':
                controller.unmute()
                return jsonify({'message': f'{process_name} unmuted'})
            else:
                return jsonify({'error': 'Invalid action'}), 400
            
        @self.app.route('/applications/<process_name>/mute_status', methods=['GET'])
        def get_mute_status(process_name):
            controller = self.app_manager.get_controller(process_name)
            if not controller:
                return jsonify({'error': 'Application not found'}), 404

            is_muted = controller.is_muted()
            return jsonify({'muted': is_muted}), 200

        @self.app.route('/devices', methods=['GET'])
        def get_devices():
            devices = self.audio_device_manager.get_audio_devices()
            return jsonify({'devices': devices})

        @self.app.route('/devices/default', methods=['GET'])
        def get_default_device():
            device = self.audio_device_manager.get_default_audio_device()
            return jsonify({'default_device': device})

        @self.app.route('/devices/default', methods=['POST'])
        def set_default_device():
            data = request.get_json()
            device_id = data.get('device_id')
            if device_id:
                self.audio_device_manager.set_default_audio_device(device_id)
                return jsonify({'message': 'Default device set', 'device_id': device_id})
            else:
                return jsonify({'error': 'Invalid device data'}), 400
        
        @self.app.route('/applications/<process_name>/icon', methods=['GET'])
        def get_app_icon(process_name):
            controller = self.app_manager.get_controller(process_name)
            if not controller:
                return jsonify({'error': 'Application not found'}), 404

            icon = controller.extract_icon()
            if icon:
                return send_file(icon, mimetype='image/png')
            else:
                return jsonify({'error': 'Icon not found'}), 404

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)
