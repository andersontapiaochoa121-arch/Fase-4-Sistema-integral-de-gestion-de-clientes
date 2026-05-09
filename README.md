# Sistema de Gestión de Reservas y Servicios Empresariales

## 🧾 Descripción
Este proyecto implementa un sistema en Python para la gestión integral de clientes, servicios y reservas en un entorno empresarial.  

El sistema está desarrollado bajo el paradigma de Programación Orientada a Objetos (POO), incorporando buenas prácticas como encapsulamiento, abstracción y manejo robusto de errores mediante registros en archivos log.

No utiliza bases de datos; toda la información se gestiona en memoria y mediante archivos.

---

## 🎯 Objetivo
Diseñar e implementar un sistema modular y robusto que permita:
- Administrar clientes
- Gestionar servicios
- Controlar reservas
- Registrar errores sin interrumpir la ejecución

---

## ⚙️ Funcionalidades
- Registro y validación de clientes
- Gestión de servicios empresariales
- Creación de reservas
- Registro automático de errores en `error_log.txt`
- Limpieza automática del log al iniciar
- Salida en consola estructurada

---

## 🧩 Estructura del Proyecto
📁 proyecto/
│
├── sistema_reservas.py
├── error_log.txt
└── README.md

---

## 📊 Diagrama de Clases

Cliente
 - _nombre
 - _correo

Servicio (ABC)
 - método abstracto

Servicios derivados
 - Implementaciones concretas

Reserva
 - cliente
 - servicio
 - fecha

---

## 📌 Explicación

Cliente: Maneja datos del usuario con validaciones.  
Servicio: Clase abstracta base.  
Servicios derivados: Aplican polimorfismo.  
Reserva: Relaciona cliente, servicio y fecha.

---

## 🚀 Ejecución
python sistema_reservas.py

---

## ⚠️ Manejo de Errores
Los errores se registran en error_log.txt con fecha, contexto y descripción.

---

## 👥 Integrantes
Anderson David Tapia Ochoa  
Heidy Carolina Oviedo Villar                                                                                                              Adriana Melissa Araujo Pabon

---

## 🎓 Información Académica
Ingeniería de Sistemas  
Curso: Programación  
Fase 4 – Prácticas simuladas  
UNAD  

---

## 📌 Conclusión
Sistema desarrollado aplicando POO, manejo de errores y estructura modular sin base de datos.
