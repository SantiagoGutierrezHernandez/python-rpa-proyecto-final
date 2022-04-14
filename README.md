# Proyecto final - Python RPA

Este proyecto cumple la función de cargar automáticamente las facturas indicadas en un excel para, luego de cargarlas a una aplicación que simula procesar facturas, eliminarlas. También se encarga de comprar los productos cargados a un excel determinado a través de una página de simuñación de e-commerce.  
Adicionalmente, me encargué de agregarle la funcionalidad de separar los logs según fecha mediante un wrapper, y la de en lugar de simplemente eliminar archivos con datos potencialmente sensibles, esperar hasta que expire el tiempo indicado desde el último acceso al archivo para borrarlo, en caso de que se desee recuperar.

## Dependencias

Para ejecutar el proyecto, además de requerir Python (En el desarrollo fue utilizada la version 3.7.9 de 64 bits), se requiere descargar las siguientes librerías:

- pyautogui
- python-decouple
- selenium
- openpyxl

Además, por limitaciones de almacenamiento, se debe descargar por separado el archivo [Calyx.Invoices](https://drive.google.com/file/d/1jiuVr-h-H0Zh6OVUC4fV6t6PHexY30_t/view?usp=sharing) y, ubicarlo en la carpeta facturas (O bien en cualquier ruta relativa, actualizando `INVOICES_APP_PATH` en el archivo "setting.ini").

## Justificaciones

*¿Por qué openpyxl?*
Frente a pandas, lo consideré una mejor alternativa ya que en este trabajo en concreto solo se utilizaron archivos excel, y esta primera librería es más robusta para ese caso.  

*¿Por qué utilicé el logger de raíz?*
Si utilizaba varios loggers, cabía la posibilidad de que en algún punto me confunda y acceda a la librería base para loguear. Si utilizo el de raíz, una vez lo configuro puedo confundirme de librería y obtener aún así prácticamente el mismo resultado.  

*¿Por qué agregué un directorio de archivos temporales?*
A la hora de desarrollar el proyecto, no solo me di cuenta que si fuese un caso real estaría perdiendo información relevante de forma permanente, sino que también resultaba muy tedioso eliminar archivos a la hora de testear y tener que volver a descargarlos para continuar.  