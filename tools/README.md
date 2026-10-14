# Generadores de las animaciones del perfil

| Script | Genera | Qué es |
| --- | --- | --- |
| `make_header.py` | `assets/header.svg` | Tarjeta con la constelación de edgar-ontiveros.com, el logo EO·, el nombre y la línea |
| `make_typing.py` | `assets/typing-dark.svg`, `assets/typing-light.svg` | Línea de terminal `>_` con las frases del sitio |

Los ajustes van al inicio de cada script: tamaño y espaciado del nombre (`SIZE`, `TRACK`), número de nodos (`N`), duración del ciclo (`T`), colores, frases (`LINES`) y tiempos de escritura.

## Requisitos

```bash
pip install fonttools brotli
```

Las fuentes (licencia OFL) vienen del repo del sitio, `edgar-ontiveros.com`, después de `npm install`:

- Space Grotesk: `node_modules/@fontsource-variable/space-grotesk/files/space-grotesk-latin-wght-normal.woff2`
- JetBrains Mono: `node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2`

## Regenerar

Desde la raíz de este repo, con `SITE` apuntando al repo del sitio:

```bash
SITE=../edgar-ontiveros.com/node_modules/@fontsource-variable
python tools/make_header.py "$SITE/space-grotesk/files/space-grotesk-latin-wght-normal.woff2" assets/header.svg
python tools/make_typing.py "$SITE/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2" assets
```

Después de publicar, conviene revisar que cada imagen de la portada responda 200.
