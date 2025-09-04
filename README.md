# Tic-Tac-Toe (Tres en Ralla)

Un juego clásico de Tres en Ralla implementado en Python usando Pygame, con una IA que tiene múltiples niveles de dificultad.

## Características

- 🎮 Interfaz gráfica intuitiva
- 🤖 IA con 4 niveles de dificultad:
  - Fácil (70% aleatorio, 30% perfecto)
  - Normal (40% aleatorio, 60% perfecto)
  - Difícil (10% aleatorio, 90% perfecto)
  - Imposible (100% perfecto usando algoritmo **minimax**)
- 📊 Sistema de conteo de victorias
- 🎨 Efectos visuales para victorias y derrotas
- 🔄 Reinicio rápido del juego

## Posibles mejoras futuras
- Añadir modo para dos jugadores
- Mejorar la interfaz gráfica
- Añadir sonidos

## Requisitos

- Python 3.x
- Pygame
- NumPy

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/ComfyPenguin/Tic-Tac-Toe.git
```

2. Instala las dependencias:
```bash
pip install pygame numpy
```

## Cómo Jugar

1. Ejecuta el juego:
```bash
python game.py
```

2. Selecciona la dificultad usando las teclas 1-4:
   - 1: Fácil
   - 2: Normal
   - 3: Difícil
   - 4: Imposible

3. Controles:
   - Click izquierdo: Colocar ficha
   - R: Reiniciar partida
   - ESC: Cambiar dificultad
   - Cierra la ventana para salir
