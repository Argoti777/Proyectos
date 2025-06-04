# Tesis_apuestas_deportivas
Plataforma web de apuestas deportivas con IA para actualizar marcadores en tiempo real.

# 🎓 Tesis: Plataforma de Apuestas Deportivas con IA

Este proyecto corresponde a la tesis de Alejandro y Alexis. Consiste en una **plataforma web de apuestas deportivas locales**, que actualiza **estadísticas y marcadores en tiempo real** utilizando un modelo de **inteligencia artificial** para predecir resultados.

## 📌 Objetivos
- Crear una interfaz web atractiva para realizar apuestas.
- Programar un backend que gestione usuarios, apuestas y resultados.
- Conectar con una base de datos para almacenar toda la información.
- Entrenar un modelo de IA que realice predicciones deportivas.
- Integrar todo en un sistema funcional, moderno y fácil de usar.

---
## 📁 Estructura del proyecto

tesis-apuestas-deportivas/
│
├── backend/                  # Lógica del servidor y procesamiento
│   ├── api/                  # Endpoints de la API
│   ├── modelos/              # Modelos de datos y lógica de negocio
│   └── ia/                   # Código del modelo de inteligencia artificial
│
├── frontend/                 # Interfaz de usuario
│   ├── public/               # Archivos públicos (favicon, index.html, etc.)
│   └── src/                  # Código fuente de React/Vue/JS
│       └── componentes/      # Componentes reutilizables (Navbar, Footer, etc.)
│
├── docs/                     # Documentación, cronograma, capturas, presentaciones
├── README.md                 # Descripción general del proyecto
└── .gitignore                # Archivos que Git debe ignorar

---

## 👥 División de Trabajo

| Área | Alejandro | Alexis |
|------|-----------|-----------|
| Frontend (interfaz) | ✅ Principal | 🔁 Apoyo |
| Backend (API) | 🔁 Apoyo | ✅ Principal |
| Base de datos | 🔁 Apoyo | ✅ Principal |
| Inteligencia Artificial | ✅ Principal | 🔁 Apoyo |
| Testing / Documentación | ✅ | ✅ |

---

## 🗓️ Cronograma

| Semana | Objetivo |
|--------|----------|
| 15-21 abril | Estructura del repositorio + planificación |
| 22-28 abril | Frontend inicial + backend de usuarios |
| 29 abr - 5 may | Dashboard + lógica de apuestas |
| 6 - 12 mayo | IA (predicción + conexión con backend) |
| 13 - 19 mayo | Testing, corrección de errores, presentación |
| 20 - 25 mayo | Demo final y entrega del proyecto |

---

## 🚀 Tecnologías

- **Frontend:** HTML, CSS, JavaScript, React (opcional)
- **Backend:** Node.js / Python / .NET (según elección)
- **Base de datos:** MySQL / PostgreSQL / SQLite
- **IA:** TensorFlow / Keras
- **Control de versiones:** Git + GitHub

---

## ✅ Estado del proyecto

📍 En planificación y construcción inicial (abril 2025)

---

## ✅ Primeras tareas realizadas

Planificacion: difinir 
               -nombre de la plataforma
               -el estilo de las interfaces
               -decidir la organizacion 

---

## ✅ Primeras decisiones tomadas

NOMBRE DE LA PLATAFORMA:
- ECUAFUT
NOMBRE DE LA CASA DE APUESTAS:
- CHULLAGOL

COLORES A UTILIZAR:
- VERDE OSCURO
- BLANCO
---


## ✅ RECOLECCION DE DATOS

¿Que funcionalidades debe tener nuestra plataforma?

-REGISTRAR CON DOS TIPOS DE USUARIOS ADMINISTRADOR Y USUARIO
-INICIO DE SESION
-VIZUALISACION DE ESTADISTICAS
-VIZUALISACION DE CRONOGRAMAS DE PARTIDOS 

estructura del proyecto

TESIS_PROYECTO/
│── backend/
│   ├── api/
│   │   └── auth.js       # Controlador para login y registro
│   │   └── bets.js       # Controlador para apuestas
│   │   └── matches.js    # Controlador para partidos
│   │
│   ├── modelos/
│   │   └── User.js       # Modelo de usuario
│   │   └── Bet.js        # Modelo de apuesta
│   │   └── Match.js      # Modelo de partido
│   │
│   ├── config/
│   │   └── db.js         # Configuración de la base de datos
│   │   └── server.js     # Configuración del servidor
│   │
│   ├── middlewares/
│   │   └── authMiddleware.js  # Verificación de autenticación
│   │
│   ├── utils/
│   │   └── token.js      # Funciones para manejo de tokens JWT
│   │
│   └── server.js         # Punto de entrada del backend
│
│── frontend/
│   ├── componentes/
│   │   └── Login.jsx     # Componente de inicio de sesión
│   │   └── Register.jsx  # Componente de registro
│   │   └── Navbar.jsx    # Barra de navegación
│   │   └── Dashboard.jsx # Componente principal del usuario
│   │
│   ├── context/
│   │   └── AuthContext.js # Contexto para manejo de autenticación
│   │
│   ├── pages/
│   │   └── Home.jsx      # Página de inicio
│   │   └── Profile.jsx   # Página del perfil del usuario
│   │   └── Bets.jsx      # Página de apuestas
│   │
│   ├── styles/
│   │   └── main.css      # Estilos globales
│   │
│   └── App.jsx           # Punto de entrada del frontend
│
│── docs/
│   └── README.md         # Documentación general del proyecto
│   └── api_docs.md       # Documentación de los endpoints
│   └── db_design.png     # Diagrama ERD de la base de datos
│
│── .env                  # Variables de entorno (credenciales DB, JWT secret)
│── package.json          # Dependencias del proyecto
│── .gitignore            # Archivos a ignorar por Git


## ✅ Primeras decisiones tomadas

Vistas: 
- Inicio sesion: Alexis
- Registrarse: Alexis
- Home: Argoti


