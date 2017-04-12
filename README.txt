# Servidor de mail de pruba para Redes y Transmición de Datos UNPSJB

Como parte del trabajo práctico 1 del materia se hacen pruebas con telnet para enviar y recibir mails.

Para iniciar el servidor utilizar el Makefile. Revisar con make help, es necesario instalar docker.

El contenedor tiene 2 servicios:

1. El Servidor SMTP acepta cualquier mail @localhost y lo guarda en `/tmp/mail`.
2. El servior POP3 acepta como nombre de usuario destinatarios que hayan sido enviados por 1.
