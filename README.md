# Servidor de mail de pruba para Redes y Transmición de Datos UNPSJB

Como parte del trabajo práctico 1 del materia se hacen pruebas con telnet para enviar y recibir mails.

Para iniciar el servidor utilizar el Makefile. Revisar con make help, es necesario instalar docker.

El contenedor tiene 2 servicios:

1. El Servidor SMTP acepta cualquier mail @localhost y lo guarda en `/tmp/mail`.
2. El servior POP3 acepta como nombre de usuario destinatarios que hayan sido enviados por 1.


El código tanto del servidor POP como SMTP son tomados de los ejemplos del libro "Twisted Network Programming Essentials" de [Jessica McKellar](https://github.com/jesstess)

![Twisted Network Programming Essentials](https://images-na.ssl-images-amazon.com/images/I/518wm5u3TjL._SX377_BO1,204,203,200_.jpg)
