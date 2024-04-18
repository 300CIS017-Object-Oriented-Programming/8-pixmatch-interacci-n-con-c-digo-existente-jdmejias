## Requisitos Funcionales y Criterios de Aceptación

### 1. Seleccionar dificultad y colocar nombre
- **Requisito:** El sistema debe permitir a los jugadores seleccionar el nivel de dificultad antes de comenzar el juego.
  - **Criterios de Aceptación:**
    - Opciones de dificultad fácil, medio y difícil disponibles para selección.
    - La configuración de dificultad debe influir en la mecánica del juego, como la frecuencia de regeneración de imágenes y la puntuación.
    - Tiempos de regeneración específicos:
      - Fácil: cada 8 segundos.
      - Medio: cada 6 segundos.
      - Difícil: cada 5 segundos.
- **Requisito:** El sistema debe permitir a los jugadores colocar un nombre y país para empezar a jugar.
  - **Criterios de Aceptación:**
    - Debe existir un campo de texto para que los jugadores ingresen su nombre y país.
    - Es posible que los campos de nombre y país estén vacíos, pero en ese caso no se muestra el _Leaderboard_.
    - La información del jugador debe persistir durante la sesión de juego.
### 2. Inicialización del Tablero
- **Requisito:** Al comenzar un juego, el sistema debe inicializar el tablero con un conjunto aleatorio de imágenes basado en la dificultad seleccionada.
  - **Criterios de Aceptación:**
    - El tablero debe ser llenado con imágenes de emojis que corresponden a la dificultad elegida.
    - La imagen objetivo debe ser seleccionada aleatoriamente y mostrada en la barra lateral.

### 3. Gestión del Juego
- **Requisito:** El sistema debe ser capaz de iniciar un nuevo juego.
  - **Criterios de Aceptación:**
    - El sistema debe ser capaz de mostrar las instrucciones y reglas del juego.
    - El sistema debe mostrar la puntuación actual del juego en tiempo real.
    - El sistema debe permitir al jugador volver a la página principal, mientras juega.

### 4. Funcionalidades del Juego
- **Requisito:** El sistema debe permitir al jugador seleccionar una imagen en el tablero para intentar emparejarla con la imagen objetivo.
  - **Criterios de Aceptación:**
    - El sistema debe comparar la selección del jugador con la imagen objetivo y actualizar la puntuación en consecuencia.
    - El sistema debe generar dinámicamente nuevas imágenes en el board después de un intervalo de tiempo.
    - El sistema debe penalizar al jugador con la disminución de la puntuación si no logra emparejar la imagen en el tiempo asignado.
    - El sistema debe evitar que el jugador seleccione una imagen que ya ha sido seleccionada anteriormente.
    - El sistema debe finalizar el juego cuando el jugador ha emparejado todas las imágenes en el tablero.

### 5. Marcador y Clasificación
- **Requisito:** El sistema debe mantener un registro de los puntajes más altos de los jugadores.
  - **Criterios de Aceptación:**
    - El sistema debe mostrar los 3 puntajes más altos de los jugadores en una tabla de clasificación al final del juego.
