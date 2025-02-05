from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_cors import CORS  # Importa CORS
import os
from dotenv import load_dotenv

def crear_app():
    load_dotenv()  # Carga las variables de entorno desde .env

    app = Flask(__name__)
    CORS(app)  # Habilita CORS para todos los endpoints

    @app.route('/')
    def home():
        return render_template('Index.html')

    @app.route('/Nosotros')
    def nosotros():
        return render_template('nosotros.html')

    @app.route('/Servicios')
    def servicios():
        return render_template('servicios.html')

    # Configuración de Flask-Mail con variables de entorno
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    mail = Mail(app)

    @app.route('/send-email', methods=['POST'])
    def send_email():
        name = request.form.get('name')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        message = request.form.get('message')

        if not all([name, email, telefono, message]):
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        try:
            msg = Message(
                subject=f"Nuevo mensaje de {name}",
                recipients=['abtrujilloyasociados@gmail.com'],
                body=f"Nombre: {name}\nTeléfono: {telefono}\nCorreo: {email}\nMensaje:\n{message}"
            )
            mail.send(msg)
            print("Correo enviado exitosamente")  # Depuración
            return jsonify({'success': 'Correo enviado exitosamente'})
        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")  # Depuración
            return jsonify({'error': str(e)}), 500
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(host="0.0.0.0", port=5000, debug=True)