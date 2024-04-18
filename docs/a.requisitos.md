## Requisitos Funcionales y Criterios de Aceptación
**Requisito:** 
### 1. Seleccionar dificultad y colocar nombre
- El sistema debe permitir a los jugadores seleccionar el nivel de dificultad antes de comenzar el juego.
- El sistema debe permitir a los jugadores colocar un nombre y país para empezar a jugar .
### 2. Gestión del Juego
- El sistema debe ser capaz de iniciar un nuevo juego.
- El sistema debe ser capaz de mostrar las instrucciones y reglas del juego.
- El sistema debe mostrar la puntuación actual del juego en tiempo real.
- El sistema debe permitir al jugador volver a la página principal, mientras juega.

### 3. Interfaz de Usuario
- El sistema debe mostrar una barra lateral con una imagen objetivo.
- El sistema debe mostrar un board de imágenes aleatoreas para que el jugador las empareje con la imagen objetivo.

### 4. Funcionalidades del Juego
- El sistema debe permitir al jugador seleccionar una imagen en el tablero para intentar emparejarla con la imagen objetivo.
- El sistema debe comparar la selección del jugador con la imagen objetivo y actualizar la puntuación en consecuencia.
- El sistema debe generar dinámicamente nuevas imágenes en el board después de un intervalo de tiempo.
- El sistema debe penalizar al jugador con la disminución de la puntuación si no logra emparejar la imagen en el tiempo asignado.
- El sistema debe evitar que el jugador seleccione una imagen que ya ha sido seleccionada anteriormente.
- El sistema debe finalizar el juego cuando el jugador ha emparejado todas las imágenes en el tablero.

### 5. Marcador y Clasificación
- El sistema debe mantener un registro de los puntajes más altos de los jugadores.
- El sistema debe mostrar los 3 puntajes más altos de los jugadores en una tabla de clasificación al final del juego.


**Criterios de Aceptación:**
- Opciones de dificultad fácil, medio y difícil disponibles para selección.
- La configuración de dificultad debe influir en la mecánica del juego, como la frecuencia de regeneración de imágenes y la puntuación.
- Tiempos de regeneración específicos:
  - Fácil: cada 8 segundos.
  - Medio: cada 6 segundos.
  - Difícil: cada 5 segundos.

  